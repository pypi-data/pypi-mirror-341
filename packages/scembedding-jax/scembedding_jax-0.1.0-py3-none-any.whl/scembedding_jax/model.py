import jax
import jax.numpy as jnp
import equinox as eqx
import optax

# ---------------------
# 模型定义
# ---------------------
class VQEmbedding(eqx.Module):
    embedding: jnp.ndarray
    num_embeddings: int
    embedding_dim: int
    commitment_cost: float

    def __init__(self, num_embeddings, embedding_dim, commitment_cost, *, key):
        self.num_embeddings = num_embeddings
        self.embedding_dim = embedding_dim
        self.commitment_cost = commitment_cost
        self.embedding = jax.random.uniform(
            key,
            (num_embeddings, embedding_dim),
            minval=-1/num_embeddings,
            maxval=1/num_embeddings
        )

    def __call__(self, z):  # z: (B, latent_dim)
        z_sq = jnp.sum(z ** 2, axis=1, keepdims=True)    # (B, 1)
        emb_sq = jnp.sum(self.embedding ** 2, axis=1)     # (E,)
        dot = jnp.dot(z, self.embedding.T)                # (B, E)
        distances = z_sq + emb_sq - 2 * dot

        indices = jnp.argmin(distances, axis=1)           # (B,)
        z_q = self.embedding[indices]                     # (B, latent_dim)

        loss = (
            jnp.mean((jax.lax.stop_gradient(z) - z_q) ** 2)
            + self.commitment_cost * jnp.mean((jax.lax.stop_gradient(z_q) - z) ** 2)
        )

        z_q_st = z + jax.lax.stop_gradient(z_q - z)
        return z_q_st, loss, indices


class VQVAE(eqx.Module):
    encoder: eqx.nn.MLP
    decoder: eqx.nn.MLP
    vq: VQEmbedding

    def __init__(
            self, input_dim, latent_dim, 
            num_embeddings: int = 512,
            commitment_cost: float = 0.25,
            *, 
            key
    ):
        k1, k2, k3 = jax.random.split(key, 3)

        self.encoder = eqx.nn.MLP(
            in_size=input_dim, out_size=latent_dim, width_size=1024, depth=2,
            activation=jax.nn.silu, key=k1
        )
        self.decoder = eqx.nn.MLP(
            in_size=latent_dim, out_size=input_dim, width_size=1024, depth=2,
            activation=jax.nn.silu, key=k2
        )
        self.vq = VQEmbedding(
            num_embeddings=num_embeddings,
            embedding_dim=latent_dim,
            commitment_cost=commitment_cost,
            key=k3
        )

    def __call__(self, x):  # x: (B, input_dim)
        encode = jax.vmap(self.encoder)
        decode = jax.vmap(self.decoder)

        z = encode(x)                     # (B, latent_dim)
        z_q, vq_loss, _ = self.vq(z)     # (B, latent_dim)
        x_hat = jax.nn.softplus(decode(z_q))  # (B, input_dim)
        return (x_hat, vq_loss, z)



# --------------------------
# 时间正则 + 总 loss
# --------------------------
# def compute_time_reg(z, time, sigma=0.5):
#     time = (time - jnp.min(time)) / (jnp.max(time) - jnp.min(time) + 1e-8)
#     time_diff = time[:, None] - time[None, :]
#     exponent = -time_diff**2 / (sigma**2 + 1e-6)
#     exponent = jnp.clip(exponent, -50, 0)
#     w_time = jnp.exp(exponent)

#     z_diff = z[:, None, :] - z[None, :, :]
#     z_dist_sq = jnp.sum(z_diff**2, axis=-1)
#     return jnp.sum(w_time * z_dist_sq) / (z.shape[0]**2)

# @eqx.filter_value_and_grad
# def compute_loss(model, x, time, sigma=0.5, lambda_time=0.1):
#     x_hat, vq_loss, z = model(x)
#     recon_loss = jnp.mean((x - x_hat)**2)
#     time_reg = compute_time_reg(z, time, sigma) if lambda_time>0 else 0.0
#     return recon_loss + vq_loss + lambda_time * time_reg

# @eqx.filter_jit
# def make_step(model, opt_state, x, time, optimizer, sigma=0.5, lambda_time=0.0):
#     loss, grads = compute_loss(model, x, time, sigma, lambda_time)
#     updates, opt_state = optimizer.update(grads, opt_state, params=model)
#     model = eqx.apply_updates(model, updates)
#     return model, opt_state, loss