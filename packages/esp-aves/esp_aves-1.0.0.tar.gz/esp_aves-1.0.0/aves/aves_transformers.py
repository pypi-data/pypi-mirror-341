from huggingface_hub import PyTorchModelHubMixin
from .aves import AVESTorchaudioWrapper


class ESPAves(
    AVESTorchaudioWrapper,
    PyTorchModelHubMixin,
):
    def __init__(self, config_path, model_path, **kwargs):
        super().__init__(config_path=config_path, model_path=model_path, **kwargs)
