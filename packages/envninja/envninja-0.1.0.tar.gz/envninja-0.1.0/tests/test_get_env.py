from envninja import getenv, load_env
# from dotenv import load_dotenv
# import os

load_env()

print(getenv("PORT",8000, False))
print(type(getenv("PORT",8000, False)))
print(getenv("DEBUG", False, True))
print(type(getenv("DEBUG", False, True)))
print(getenv("USERNAME", "NOUSERSET!", True))
print(type(getenv("USERNAME", "NOUSERSET!", True)))

