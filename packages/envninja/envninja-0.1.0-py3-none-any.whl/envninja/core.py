import os
from dotenv import load_dotenv as dotenv_loader
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

#-----------------------------------------------

@dataclass
class TypedConfig:
    config: Dict[str, Any] = field(default_factory=dict)


    def __post_init__(self):
        for key, value in self.config.items():
            setattr(self, key, value)

    def __repr__(self):
        return f"TypedConfig(config={self.config})"

    def __str__(self):
        return f"TypedConfig(config={self.config})"

#-----------------------------------------------

def auto_cast(v):
    if v.isdigit() :
        return int(v)
    if v.lower() in ['true', 1, 't', 'y', 'yes']:
        return True
    if v.lower() in ['false', 0, 'f', 'n', 'no']:
        return False
    return v

#-----------------------------------------------

def load_env(path : str= ".env", silent: bool=False) -> bool:

    env_path = Path(path)

    if not env_path.exists():
        if not silent:
            raise FileNotFoundError(f".env file not found at : {env_path.resolve()}")
            return False
    
    return dotenv_loader(dotenv_path=env_path, override=True)

#-----------------------------------------------



def getenv(key: str, default=None, required=False, expectedtype: type = None):
    value = os.environ.get(key)

    if value is None:
        if required:
            raise KeyError(f"Missing required environment variable: {key}")
        return default

    if expectedtype is not None:
        try:
            if expectedtype == bool:
                v_lower = value.lower()
                if v_lower in ['true', '1', 't', 'y', 'yes']:
                    return True
                elif v_lower in ['false', '0', 'f', 'n', 'no']:
                    return False
                raise ValueError(f"Invalid boolean value for {key}: {value}")
            return expectedtype(value)
        except ValueError as e:
            raise ValueError(f"Error casting {key} to {expectedtype.__name__}: {str(e)}")


    return auto_cast(value)

#-----------------------------------------------

def val_env(schema :dict) -> TypedConfig:
    results = {}

    for key, options in schema.items():
        default = options.get("default")
        required = options.get("required")
        expectedtype = options.get("expectedType")
    
        value = getenv(
            key=key,
            default=default,
            required=required,
            expectedtype=expectedtype
        )

        results[key] = value
    return TypedConfig(results)
    


#-----------------------------------------------

def generate_env_example(schema: dict, output_path: str = ".env.example") -> None:
    with open(output_path, "w") as file:
        for key, options in schema.items():
            expected_type = options.get("expectedtype", str)
            default = options.get("default")
            required = options.get("required", False)

            comment_parts = [f"Type: {expected_type.__name__}"]
            if key.lower() in ['password', 'pass', 'pw', 'security_key', 'key', 'api_token', 'api token', 'api', 'db_pass', 'database_pass', 'db_key']:
                comment_parts.append("🔒")
            if key.lower() in ['db_link', 'dblink', 'username', 'usr', 'debug']:
                comment_parts.append("⚠️")
            if default is not None:
                comment_parts.append(f"Default: {default}")
            if required:
                comment_parts.append("📌Required")

            file.write(f"# {' | '.join(comment_parts)}\n")
            file.write(f"{key}=\n\n") 
