import os
from envninja import load_env
from dotenv import load_dotenv

load_env()

def test_env_vars():
    assert os.environ.get("PORT") == "8080"
    assert os.environ.get("DEBUG") == "True"
    assert os.environ.get("USERNAME") == "aswin"
    print("all test passed~")

if __name__ == "__main__":
    test_env_vars()