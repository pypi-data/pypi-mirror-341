from envninja import generate_env_example

schema = {
    "PORT": {"default": 6000, "expectedtype": int},
    "DEBUG": {"default": False, "expectedtype": bool},
    "USERNAME": {"required": True}
}

generate_env_example(schema)
