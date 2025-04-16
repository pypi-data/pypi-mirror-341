import jax.random as jr
import equinox as eqx
from .models_eqx import ScoreNet
from .utils import*
import os
import jax.numpy as jnp

# model params
patch_size = 4
hidden_size = 64
mix_patch_size = 512
mix_hidden_size = 512
num_blocks = 4
t1 = 10.0
int_beta = lambda t: t
key = jr.PRNGKey(42)
model_key, train_key, loader_key, sample_key = jr.split(key, 4)

def print_info(name, size, path):
    if name == 'hsc32' or name == 'hsc64':
        print("HSC prior model")
        print("--------------")
        print(f"This model is trained on Scarlet1 deblends from \nthe HSC survey")
        print(f"Model size: {size}x{size}")
        print(f"Model path: {path}")

    elif name == 'ztf32' or name == 'ztf64':
        print("ZTF prior model")
        print("--------------")
        print(f"This model is trained on simulated ZTF-like galaxies")
        print(f"Model size: {size}x{size}")
        print(f"Model path: {path}")

    elif name == 'roman120':
        print("Roman prior model")
        print("--------------")
        print(f"This model is trained on simulated Roman lensed galaxies")
        print(f"Model size: {size}x{size}")
        print(f"Model path: {path}")

    elif name == 'lsst60':
        print("LSST prior model")
        print("--------------")
        print(f"This model is trained on simulated LSST lensed galaxies")
        print(f"Model size: {size}x{size}")
        print(f"Model path: {path}")

# make a prior class that contains model information 
class Prior: 
    def __init__(self, model, name, size, path):
        self.name = name
        self.size = size
        self.path = path 

    def model(self):
        return self.model 

    def info(self):
        print_info(self.name, self.size, self.path)
        
    def shape(self):
        return (self.size, self.size)

    def path(self):
        return self.path


# create prior generation function
def get_prior(name, local_dir=None):
    """ 
    Get the prior model for the given name.
    Parameters
    ----------
    name : str 
    local_dir : str 

    Returns 
    ------- 
    prior_model : ScoreNet 
    """

    path, size = get_model(name, local_dir=local_dir)
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
    prior_ = eqx.tree_deserialise_leaves(path, model_)

    def model_wrapper(x, t=0.01):
        sigma = 0.1
        x_ = jnp.log(x + 1) / sigma
        raw_grad = prior_(x_, t)
        transform_grad = raw_grad * (1 / (sigma * (x + 1)))  # analytic derrivitive
        return transform_grad

    score_func = model_wrapper

# make a prior class that contains model information 
    class Prior: 
        def __init__(self, model, name, size, path):
            self.name = name
            self.size = size
            self.path = path 

        def model(self):
            return score_func 

        def info(self):
            print_info(self.name, self.size, self.path)
            
        def shape(self):
            return (self.size, self.size)

        def path(self):
            return self.path

        def __call__(self, x, t=0.02):
            return score_func(x, t)

    # define a local class to store shape attribute
    #class ScoreNet_:
    #    def __init__(self):
    #        self.shape = (size, size)

    #    def __call__(self, x, t=0.02):
    #        return score_func(x, t)

    #prior_model = ScoreNet_()

    # instantiate the model class 
    PriorModel = Prior(name, size, path)

    return PriorModel


