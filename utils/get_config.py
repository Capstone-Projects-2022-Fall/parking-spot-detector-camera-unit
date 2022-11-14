import yaml

config_dict = None

def get_config():
    global config_dict

    if(config_dict == None):
        with open("config.yml", "r") as stream:
            try:
                config_dict = yaml.safe_load(stream)
                print(config_dict)
            except yaml.YAMLError as exc:
                print(exc)

    return config_dict

get_config()
