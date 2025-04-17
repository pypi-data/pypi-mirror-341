import logging
import os
from pathlib import Path
import tomllib

DEFAULT_SYSTEM_CONFIG_PATH: Path = Path("/etc/opencal/opencal.toml")
DEFAULT_USER_CONFIG_PATH: Path = Path.home() / ".opencal.toml"

DEFAULT_CONFIG_STR: str = f"""# OpenCAL configuration file
[opencal]
db_path = "/var/lib/opc/opencal.sqlite"
db_assets_path = "/var/lib/opc/assets"
consolidation_professor = "doreen"
acquisition_professor = "arthur"
"""

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
        logging.warning(f"The configuration file '{config_path}' does not exist. Creating a default one.")
        make_default_config_file(config_path)

    # Read the TOML file
    with open(config_path, 'rb') as file:
        logging.info(f'Loading OpenCAL configuration: "{config_path}"')
        config_dict = tomllib.load(file)

    return config_dict, config_path


def make_default_config_file(config_path: Path):
    """
    Make a default configuration file.

    Parameters
    ----------
    config_path : Path
        The path to the configuration file.
    """
    config_path = config_path.expanduser()   # Replace '~' with the user's home directory
    
    if not config_path.exists():
        with open(config_path, 'w') as fd:
            fd.write(DEFAULT_CONFIG_STR)