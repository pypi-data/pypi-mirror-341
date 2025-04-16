from setuptools import setup, find_packages

VERSION = "0.0.11"
DESCRIPTION = "Diffusion model for galaxy generation"
LONG_DESCRIPTION = "Contains 4 generative diffusion models ScoreNet32 and ScoreNet64 for both the HSC and ZTF surveys. These are used to return the gradients of an arbitrary image with respect to a prior distribution of individual artifact free galaxy models."

# Setting up
setup(
    name="galaxygradtemp",
    version=VERSION,
    author="Matt Sampson",
    author_email="matt.sampson@princeton.edu",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["jax", "equinox", "einops", "huggingface-hub"],
    keywords=["python", "diffusion"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
    ],
)
