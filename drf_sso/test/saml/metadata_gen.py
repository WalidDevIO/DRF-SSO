from pathlib import Path
from samlsp.metadata import write_metadata_to_file
from .providers import SP, OUT_DIR

write_metadata_to_file(SP, OUT_DIR / "sp_meta.xml")