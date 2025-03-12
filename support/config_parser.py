import configparser
import os
import logging

class ConfigManager:
    def __init__(self, config_file='config.ini'):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)
            self.logger.info(f"Configuration loaded from {self.config_file}")
        else:
            self.create_default_config()
            self.logger.info(f"Default configuration created and saved to {self.config_file}")

    def create_default_config(self):
        self.config['Network'] = {
            'ip': 'localhost',
            'port': '41000'
        }
        self.save_config()
        self.logger.debug("Default configuration created")

    def save_config(self):
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)
        self.logger.debug(f"Configuration saved to {self.config_file}")

    def get(self, section, key, fallback=None):
        value = self.config.get(section, key, fallback=fallback)
        self.logger.debug(f"Get: [{section}] {key} = {value}")
        return value

    def set(self, section, key, value):
        if not self.config.has_section(section):
            self.config.add_section(section)
            self.logger.debug(f"New section created: {section}")
        self.config.set(section, key, str(value))
        self.save_config()
        self.logger.debug(f"Set: [{section}] {key} = {value}")

    def get_int(self, section, key, fallback=None):
        value = self.config.getint(section, key, fallback=fallback)
        self.logger.debug(f"Get int: [{section}] {key} = {value}")
        return value

    def get_float(self, section, key, fallback=None):
        value = self.config.getfloat(section, key, fallback=fallback)
        self.logger.debug(f"Get float: [{section}] {key} = {value}")
        return value

    def get_boolean(self, section, key, fallback=None):
        value = self.config.getboolean(section, key, fallback=fallback)
        self.logger.debug(f"Get boolean: [{section}] {key} = {value}")
        return value
