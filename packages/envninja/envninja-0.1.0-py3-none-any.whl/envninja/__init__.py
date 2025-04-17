''' envninja - simple and typesafe env manager for your backend needs '''

# from dotenv import load_dotenv
#  import os
#  load_dotenv(override=True)

from .core import load_env, val_env, getenv, generate_env_example

__all__ = ["load_env", "val_env", "getenv", "generate_env_example"]