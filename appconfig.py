import logging

import yaml

# reads configuration from yml file and loads as an object.
class AppConfig(object):
    def __init__(self, config_file: str):
        with open(config_file, 'r') as config_file_handle:
            properties = yaml.safe_load(config_file_handle)
        if properties is None:
            message = f'Could not to load properties from {config_file}'
            logging.error(message)
            raise Exception(message)
        if 'config' in properties:
            config = properties['config']
            self.bot_token = config['bot_token']
            self.chat_id = config['chat_id']
            self.interval = config['interval']
            self.stock_name = config['stock_name']
            self.is_valid = True
        else:
            logging.error(f'Field \'config\' is missing in {config_file}')
            self.is_valid = False
