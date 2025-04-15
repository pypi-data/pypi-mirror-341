from .configuration import Config
from .utils import BASE_DIR, CONFIG_DIR

env = Config(
    path=CONFIG_DIR / "config.json",
    keys=[
        dict(
            name="DATA_DIR",
            key_type="str",
            description="\nConfigure data\n",
            default=str((BASE_DIR.parent / "data").resolve()),
            group="data",
        ),
        dict(
            name="DIGITAL_OCEAN_API_KEY",
            key_type="str",
            description="\nConfigure Digital Ocean\n",
            default=None,
            mask=True,
            group="do",
        ),
        dict(
            name="WHITELISTED_IPS",
            key_type="str",
            description="\nComma separated ips to whitelist\n",
            default=None,
            mask=True,
            group="do",
        ),
        dict(
            name="PYPI_TOKEN",
            key_type="str",
            description="\nConfigure Pypi\n",
            default=None,
            mask=True,
            group="pypi",
        ),
    ],
)
