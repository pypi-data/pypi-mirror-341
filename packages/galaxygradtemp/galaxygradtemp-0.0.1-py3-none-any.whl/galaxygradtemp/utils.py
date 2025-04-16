# Helper scrip to download the models from Huggingface
from huggingface_hub import hf_hub_download

repo_id = "sampsonML/galaxygrad-trained-models"

models_avail = ["hsc32", "hsc64", "ztf32", "ztf64", "roman120", "lsst60"]

def show_available_models(*args):
    """
    Print the available models.
    """
    print("Available models:")
    for model in models_avail:
        print(f"- {model}")

def get_model(model_name: str, local_dir: str = None) -> str, int:
    if model_name not in models_avail:
        raise ValueError(f"Model {model_name} is not available. Available models are: {models_avail}")
    if model_name == "hsc32":
        return hsc32(local_dir)
    elif model_name == "hsc64":
        return hsc64(local_dir)
    elif model_name == "ztf32":
        return ztf32(local_dir)
    elif model_name == "ztf64":
        return ztf64(local_dir)
    elif model_name == "roman120":
        return roman120(local_dir)
    elif model_name == "lsst60":
        return lsst60(local_dir)
    else:
        raise ValueError(f"Model {model_name} is not available. Available models are: {models_avail}")


def hsc32(str: local_dir = None) -> str, int:
    """
    Download the HSC 32x32 ScoreNet model from Hugging Face Hub.
    """
    size = 32
    if local_dir is not None:
        path = hf_hub_download(
            repo_id=repo_id,
            filename="eqx_hsc_ScoreNet32.eqx",
            local_dir=local_dir,
            repo_type="dataset",
        )
    else:
        path = hf_hub_download(
            repo_id=repo_id, filename="eqx_hsc_ScoreNet32.eqx", repo_type="dataset"
        )
    return path, size

def hsc64(str: local_dir = None) -> str, int:
    """
    Download the HSC 64x64 ScoreNet model from Hugging Face Hub.
    """
    size = 64
    if local_dir is not None:
        path = hf_hub_download(
            repo_id=repo_id,
            filename="eqx_hsc_ScoreNet64.eqx",
            local_dir=local_dir,
            repo_type="dataset",
        )
    else:
        path = hf_hub_download(
            repo_id=repo_id, filename="eqx_hsc_ScoreNet64.eqx", repo_type="dataset"
        )
    return path, size


def ztf32(str: local_dir = None) -> str, int:
    """
    Download the ZTF 32x32 ScoreNet model from Hugging Face Hub.
    """
    size = 32
    if local_dir is not None:
        path = hf_hub_download(
            repo_id=repo_id,
            filename="eqx_ZTF_ScoreNet32.eqx",
            local_dir=local_dir,
            repo_type="dataset",
        )
    else:
        path = hf_hub_download(
            repo_id=repo_id, filename="eqx_ZTF_ScoreNet32.eqx", repo_type="dataset"
        )
    return path, size

def ztf64(str: local_dir = None) -> str, int:
    """
    Download the ZTF 64x64 ScoreNet model from Hugging Face Hub.
    """
    size = 64
    if local_dir is not None:
        path = hf_hub_download(
            repo_id=repo_id,
            filename="eqx_ZTF_ScoreNet64.eqx",
            local_dir=local_dir,
            repo_type="dataset",
        )
    else:
        path = hf_hub_download(
            repo_id=repo_id, filename="eqx_ZTF_ScoreNet64.eqx", repo_type="dataset"
        )
    return path, size


def roman120(str: local_dir = None) -> str, int:
    """
    Download the Roman 120x120 ScoreNet model from Hugging Face Hub.
    """
    size = 120
    if local_dir is not None:
        path = hf_hub_download(
            repo_id=repo_id,
            filename="eqx_roman_ScoreNet120.eqx",
            local_dir=local_dir,
            repo_type="dataset",
        )
    else:
        path = hf_hub_download(
            repo_id=repo_id, filename="eqx_roman_ScoreNet120.eqx", repo_type="dataset"
        )
    return path, size

def lsst60(str: local_dir = None) -> str, int:
    """
    Download the LSST 60x60 ScoreNet model from Hugging Face Hub.
    """
    size = 60
    if local_dir is not None:
        path = hf_hub_download(
            repo_id=repo_id,
            filename="eqx_lsst_ScoreNet60.eqx",
            local_dir=local_dir,
            repo_type="dataset",
        )
    else:
        path = hf_hub_download(
            repo_id=repo_id, filename="eqx_lsst_ScoreNet60.eqx", repo_type="dataset"
        )
    return path, size
