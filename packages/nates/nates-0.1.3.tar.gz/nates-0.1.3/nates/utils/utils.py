import uuid
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.resolve()
CONFIG_DIR = Path.home() / ".cache" / "nates"


def get_device_id():
    """Get a unique ID for this device."""
    device_id_path = CONFIG_DIR / "device_id.txt"
    if not device_id_path.exists():
        device_id = str(uuid.uuid4())
        device_id_path.write_text(device_id)
    else:
        device_id = device_id_path.read_text()
    return device_id


def notabs(text: str) -> str:
    """Remove leading/trailing whitespace on each line."""
    return "\n".join([x.strip() for x in text.split("\n")]).strip()
