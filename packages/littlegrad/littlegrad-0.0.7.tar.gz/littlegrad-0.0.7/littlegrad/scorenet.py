import jax.random as jr
import equinox as eqx
from .models_eqx import ScoreNet
import os
import jax.numpy as jnp

# model params
patch_size = 4
hidden_size = 64
mix_patch_size = 512
mix_hidden_size = 512
num_blocks = 4
t1 = 10.0

# noise -- time schedule
int_beta = lambda t: t

# rng numbers
key = jr.PRNGKey(42)
model_key, train_key, loader_key, sample_key = jr.split(key, 4)


def check_file_exists(url):
    exit_code = os.system(f"wget --spider -q {url}")
    if exit_code == 0:
        return 1
    else:
        raise FileNotFoundError(f"File not found at URL: {url}")

# create prior generation function
def get_prior(name, size, url=None):

    # initialise model
    data_shape = (1, size, size)
    model_ = ScoreNet(
        data_shape,
        patch_size,
        hidden_size,
        mix_patch_size,
        mix_hidden_size,
        num_blocks,
        t1,
        key=model_key,
    )

    # check if already in the directory
    cwd = os.getcwd()
    if os.path.exists(os.path.join(cwd, name)):
        # if so, load it
        FN = os.path.join(cwd, name)
    # otherwide download from url
    else:
        if check_file_exists(url) == 1:
            # download the model
            os.system(f"wget {url} -O {name}")
            FN = os.path.join(cwd, name)

    prior_ = eqx.tree_deserialise_leaves(FN, model_)

    def model_wrapper(x, t=0.01):
        sigma = 0.1
        x_ = jnp.log(x + 1) / sigma
        raw_grad = prior_(x_, t)
        transform_grad = raw_grad * (1 / (sigma * (x + 1)))  # analytic derrivitive
        return transform_grad

    score_func = model_wrapper

    # define a local class to store shape attribute
    class ScoreNet_:
        def __init__(self):
            self.shape = (size, size)

        def __call__(self, x, t=0.02):
            return score_func(x, t)

    prior_model = ScoreNet_()
    return prior_model


