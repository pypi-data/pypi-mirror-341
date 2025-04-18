__maintainer__ = "Fabia Miorelli, Eugenio Salavador Arellano Ruiz"
__license__ = "BSD-3-Clause"

from pathlib import Path

import yaml


def read_metadata_config():
    """
    Funtion to load  the needed config for metadata generation.

    Args:
        base_path (Path): _description_

    Returns:
        metadata_config (dict): Dictionary with opened yaml config files
    """
    config_name = "metadata_default"
    config_path = Path((__file__)).parent.parent / "config"
    file_path = (config_path / config_name).with_suffix(".yaml")
    with open(file_path, encoding="utf-8") as ipf:
        metadata_config = yaml.load(ipf, Loader=yaml.SafeLoader)
    return metadata_config


def write_out_metadata(metadata_yaml, file_name):
    with open(file_name, "w", encoding="utf-8") as f:
        yaml.Dumper.ignore_aliases = lambda *args: True
        yaml.dump(metadata_yaml, f, sort_keys=False, allow_unicode=True)
