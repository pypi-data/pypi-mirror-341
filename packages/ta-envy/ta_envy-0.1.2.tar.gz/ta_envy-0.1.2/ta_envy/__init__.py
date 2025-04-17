import os
from pathlib import Path

class Env:
    def __init__(self, required=None, dotenv_path=".env"):
        self.vars = dict(os.environ)  # carrega tudo do ambiente real
        self.required = required or []
        self._load(dotenv_path)       # sobrescreve com o que tiver no .env (se tiver)
        self._validate()

    def _load(self, path):
        path = Path(path)
        if path.is_file():  # Garante que é um arquivo antes de abrir
            with path.open() as f:
                for line in f:
                    if "=" in line and not line.strip().startswith("#"):
                        k, v = line.strip().split("=", 1)
                        self.vars[k] = v.strip().strip('"').strip("'")

    def _validate(self):
        for key in self.required:
            if key not in self.vars:
                raise ValueError(f"Missing required env var: {key}")

    def get(self, key, default=None, type=str):
        value = self.vars.get(key, default)
        if value is None:
            return None
        if type == bool:
            return str(value).lower() in ["1", "true", "yes", "on"]
        if type == list:
            return [v.strip() for v in value.split(",")]
        return type(value)
