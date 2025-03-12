import configparser
import os

class ConfigManager:
    def __init__(self, config_file='config.ini'):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)
        else:
            self.create_default_config()

    def create_default_config(self):
        self.config['Network'] = {
            'ip': 'localhost',
            'port': '41000'
        }
        self.save_config()

    def save_config(self):
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    def get(self, section, key, fallback=None):
        return self.config.get(section, key, fallback=fallback)

    def set(self, section, key, value):
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, str(value))
        self.save_config()

    def get_int(self, section, key, fallback=None):
        return self.config.getint(section, key, fallback=fallback)

    def get_float(self, section, key, fallback=None):
        return self.config.getfloat(section, key, fallback=fallback)

    def get_boolean(self, section, key, fallback=None):
        return self.config.getboolean(section, key, fallback=fallback)
