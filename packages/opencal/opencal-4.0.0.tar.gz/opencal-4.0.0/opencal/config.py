import logging
import os
from pathlib import Path
import tomllib

DEFAULT_SYSTEM_CONFIG_PATH: Path = Path("/etc/opencal/opencal.toml")
DEFAULT_USER_CONFIG_PATH: Path = Path.home() / ".opencal.toml"

def get_config(config_path: Path | str | None = None) -> tuple[dict, Path]:
    """
    Get the configuration dictionary and the path to the configuration file.

    Parameters
    ----------
    config_path : Path, optional
        The path to the configuration file.
    
    Returns
    -------
    dict
        The configuration dictionary.
    """
    if config_path is None:
        if 'OPENCAL_CONFIG_PATH' in os.environ:
            config_path = Path(os.environ['OPENCAL_CONFIG_PATH'])
        elif DEFAULT_SYSTEM_CONFIG_PATH.exists():
            config_path = DEFAULT_SYSTEM_CONFIG_PATH
        else:
            config_path = DEFAULT_USER_CONFIG_PATH

    # Expand the user's home directory
    config_path = Path(config_path).expanduser()   # Replace '~' with the user's home directory

    # Make sure the configuration file exists
    if not config_path.exists():
        logging.error(f"The configuration file '{config_path}' does not exist.")

    # Read the TOML file
    with open(config_path, 'rb') as file:
        logging.info(f'Loading OpenCAL configuration: "{config_path}"')
        config_dict = tomllib.load(file)

    return config_dict, config_path