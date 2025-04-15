import json
from pathlib import Path

from hatchling.metadata.plugin.interface import MetadataHookInterface

class CustomMetadataHook(MetadataHookInterface):
    def update(self, metadata):
        metadata_file = Path(self.root) / "metadata.json"
        if not metadata_file.exists():
            raise FileNotFoundError(f"Metadata file not found at: {metadata_file}")

        with metadata_file.open(encoding="utf-8") as f:
            meta = json.load(f)

        required_fields = ["version", "description", "authors"]
        for field in required_fields:
            if field not in meta:
                raise ValueError(f"Missing required field '{field}' in metadata.json")

        metadata["version"] = meta["version"]
        metadata["description"] = meta["description"]
        metadata["authors"] = meta["authors"]
