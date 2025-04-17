from envninja import load_env, val_env

load_env()

config = val_env({
    "PORT": {"default": 6000, "expectedtype": int},
    "DEBUG": {"default": False, "expectedtype": bool},
    "USERNAME": {"required": True}
})
print(config)

Port = config.DEBUG

print(Port)