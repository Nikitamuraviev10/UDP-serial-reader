import logging
from typing import Dict, Any, Callable
import yaml

from bench.model import BenchModel
from support.constants import Cmd


class SequenceSenderController:
    def __init__(self, bench_model: BenchModel):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug("Initializing ConfigController")
        self.bench_model: BenchModel = bench_model
        self.execution_results: Dict[str, Any] = {}
        self.command_registry: Dict[str, callable] = {}
        self.logger.info("ConfigController initialized")

    def load_config(self, file_path: str):
        self.logger.info("Loading configuration from: %s", file_path)
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
        
        if not isinstance(config, list):
            raise ValueError("YAML config must be a list of sections")

        for item in config:
            if isinstance(item, dict):
                for section_type, content in item.items():
                    if section_type.startswith('Function:'):
                        self._process_function_section(section_type[9:], content)
                    elif section_type == 'Command':
                        self._process_command_section( content)
                    else:
                        raise ValueError(f"Unknown section type: {section_type}")
            else:
                raise ValueError(f"Invalid configuration item: {item}")

        self.logger.info("Configuration loaded successfully")

    def _process_command_section(self, section: dict):
        """Обработка секций с командами"""

        self.logger.debug("Processing command section with %d commands", len(section))

        sequence = []
        for cmd_key, raw_value in section.items():
            try:
                cmd = getattr(Cmd, cmd_key.strip())  # Получаем команду из перечисления Cmd
                self.logger.debug("Resolved command: %s.%s", "Cmd", cmd_key)
            except AttributeError:
                raise ValueError(f"Invalid command: {cmd_key}")

            if raw_value is None:
                error_msg = f"Missing value for command: {cmd_key}"
                self.logger.error(error_msg)
                raise ValueError(f"Missing value for command: {cmd_key}")

            value = self._parse_value(raw_value)
            sequence.append((cmd, value))
            self.logger.debug("Added command to sequence: %s=%s", cmd.name, value)
        
        try:
            self.bench_model.execute_sequence(sequence)
            self.logger.info("Command sequence executed successfully")
        except Exception as e:
            self.logger.error("Failed to execute command sequence: %s", str(e), exc_info=True)
            raise


    def _process_function_section(self, func_name: str, section: dict):
        """Обработка секций с функциями"""

        self.logger.info("Processing function '%s'", func_name)

        if func_name not in self.command_registry:
            raise ValueError(f"Unregistered function: {func_name}")

        kwargs = dict(section)

        try:
            result = self.command_registry[func_name](**kwargs)
        except Exception as e:
            self.logger.error(f"Ошибка выполнения функции {func_name}: {e}", exc_info=True)
            raise RuntimeError(f"Ошибка выполнения функции {func_name}: {e}")

        self.execution_results[func_name] = result


    def _parse_value(self, raw_value):
        """Обработка значений с переменных """
        if isinstance(raw_value, str) and raw_value.startswith('$'):
            var_name = raw_value[1:]
            return self.execution_results.get(var_name)
        return raw_value

    def register(self, name: str = None) -> Callable:
        """
        Декоратор для регистрации пользовательских функций
        
        Пример использования:
        
        1. С явным указанием имени:
        @controller.register("my_command")
        def some_function(): ...
        
        2. С автоматическим именем (используется __name__ функции):
        @controller.register()
        def another_function(): ...
        """
        def decorator(func: Callable) -> Callable:
            nonlocal name
            final_name = name or func.__name__
            
            if final_name in self.command_registry:
                raise ValueError(f"Function {final_name} already registered")
                
            self.command_registry[final_name] = func
            return func
            
        return decorator
    

