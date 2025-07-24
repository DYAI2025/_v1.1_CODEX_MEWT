import json
import yaml
from pathlib import Path

class SchemaLoader:
    """Load analysis schemas in JSON or YAML format."""

    def load(self, path: str | Path) -> dict:
        file_path = Path(path)
        if not file_path.exists():
            raise FileNotFoundError(path)
        if file_path.suffix in {'.yml', '.yaml'}:
            return yaml.safe_load(file_path.read_text())
        elif file_path.suffix == '.json':
            return json.loads(file_path.read_text())
        else:
            raise ValueError(f"Unsupported schema format: {file_path.suffix}")
