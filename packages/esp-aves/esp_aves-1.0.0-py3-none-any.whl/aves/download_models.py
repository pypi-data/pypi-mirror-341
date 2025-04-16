"""Download pre-trained models for the aves package."""

import os
import logging
from gcsfs import GCSFileSystem

logger = logging.getLogger("aves")


model_registry = {
    "aves-core": "gs://esp-public-files/ported_aves/aves-base-core.torchaudio.pt",
    "aves-bio": "gs://esp-public-files/ported_aves/aves-base-bio.torchaudio.pt",
    "aves-nonbio": "gs://esp-public-files/ported_aves/aves-base-nonbio.torchaudio.pt",
    "aves-all": "gs://esp-public-files/ported_aves/aves-base-all.torchaudio.pt",
    "birdaves-biox-base": "gs://esp-public-files/birdaves/birdaves-biox-base.torchaudio.pt",
    "birdaves-biox-large": "gs://esp-public-files/birdaves/birdaves-biox-large.torchaudio.pt",
    "birdaves-bioxn-large": "gs://esp-public-files/birdaves/birdaves-bioxn-large.torchaudio.pt",
}

config_registry = {
    "aves-core": "gs://esp-public-files/ported_aves/aves-base-core.torchaudio.model_config.json",
    "aves-bio": "gs://esp-public-files/ported_aves/aves-base-bio.torchaudio.model_config.json",
    "aves-nonbio": "gs://esp-public-files/ported_aves/aves-base-nonbio.torchaudio.model_config.json",
    "aves-all": "gs://esp-public-files/ported_aves/aves-base-all.torchaudio.model_config.json",
    "birdaves-biox-base": "gs://esp-public-files/birdaves/birdaves-biox-base.torchaudio.model_config.json",
    "birdaves-biox-large": "gs://esp-public-files/birdaves/birdaves-biox-large.torchaudio.model_config.json",
    "birdaves-bioxn-large": "gs://esp-public-files/birdaves/birdaves-bioxn-large.torchaudio.model_config.json",
}


def download_model(model_name: str, output_dir: str = "../models") -> None:
    """Download a pre-trained model for the aves package.

    Arguments
    ---------
    model_name: str
        The name of the model to download.
    output_dir: str
        The directory to save the downloaded model and config files to

    Examples
    --------
    >>> download_model("aves-all")
    Downloading model aves-all to ../models/aves-base-all.torchaudio.pt
    """
    if model_name not in model_registry:
        raise ValueError(f"Model {model_name} not found in the registry")

    model_url = model_registry[model_name]
    config_url = config_registry[model_name]

    model_path = os.path.join(output_dir, os.path.basename(model_url))
    config_path = os.path.join(output_dir, os.path.basename(config_url))

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    try:
        fs = GCSFileSystem(token="anon")

        logger.info(f"Downloading model {model_name} to {model_path}")
        fs.get(model_url, model_path)
        logger.info(f"Downloading model config to {config_path}")
        fs.get(config_url, config_path)

        logger.info("Download complete! ✅")
    except Exception as e:
        logger.error(f"Failed to download model with exception {e}")
