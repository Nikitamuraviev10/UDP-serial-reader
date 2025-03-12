import yaml
import logging
from typing import Dict, Any, Callable, Optional, Type

from PyQt5.QtCore import QEventLoop, QObject, QTimer

from bench.model import BenchModel
from sequence_sender.command_registry import CommandRegistry
from support.constants import Cmd

class SequenceSenderModel(QObject):
    def __init__(self, bench_model: BenchModel, registry: Type[CommandRegistry]):
        super().__init__()
        self.bench_model: BenchModel = bench_model
        self.logger = logging.getLogger(self.__class__.__name__)
        self.execution_results: Dict[str, Any] = {}
        self.command_registry: Dict[str, Callable] = registry.get_commands()

    def load_config(self, file_path: str):
        try:
            with open(file_path, 'r') as file:
                config = yaml.safe_load(file)
            
            if not isinstance(config, list):
                raise ValueError("YAML config must be a list of sections")

            for item in config:
                self._process_config_item(item)

        except Exception as e:
            self.logger.error(str(e))
            raise

    def _process_config_item(self, item):
        if isinstance(item, dict):
            for section_type, content in item.items():
                if section_type.startswith('Function:'):
                    self._process_function_section(section_type[9:], content)
                elif section_type.startswith('Function_Blocking:'):
                    self._process_blocking_function_section(section_type[18:], content)
                elif section_type == 'Command':
                    self._process_command_section(content)
                else:
                    raise ValueError(f"Unknown section type: {section_type}")
        else:
            raise ValueError(f"Invalid configuration item: {item}")

    def _process_command_section(self, section_list: dict):
        """Обработка секций с командами"""

        self.logger.debug(f"Processing command section with {len(section_list)} commands")

        sequence = []
        for section in section_list:
            for cmd_key, raw_value in section.items():
                try:
                    cmd = getattr(Cmd, cmd_key.strip())  # Получаем команду из перечисления Cmd
                    self.logger.debug(f"Resolved command: Cmd.{cmd_key}")
                except AttributeError:
                    raise ValueError(f"Invalid command: {cmd_key}")

                if raw_value is None:
                    error_msg = f"Missing value for command: {cmd_key}"
                    self.logger.error(error_msg)
                    raise ValueError(error_msg)

                value = self._parse_value(raw_value)
                sequence.append((cmd, value))
                self.logger.debug(f"Added command to sequence: {cmd.name}={value}")
            
        try:
            self.bench_model.execute_sequence(sequence)
            self.logger.info("Command sequence executed successfully")
        except Exception as e:
            self.logger.error(f"Failed to execute command sequence: {str(e)}", exc_info=True)
            raise
 
    def _process_function_section(self, func_name: str, section: dict):
        """Обработка секций с функциями"""

        self.logger.info(f"Processing function '{func_name}'")

        if func_name not in self.command_registry:
            raise ValueError(f"Unregistered function: {func_name}")
        
        result_input = {}

        for var, raw_value in section.items():
            result_input[var] = self._parse_value(raw_value)

        try:
            func = self.command_registry[func_name]

            result = func(**result_input)

            self.execution_results[func_name] = result
            self.logger.info(f"Function '{func_name}' executed successfully")
        except Exception as e:
            self.logger.error(f"Function execution failed: {str(e)}")
            raise Exception("Function execution failed") from e

    def _process_blocking_function_section(self, func_name: str, section: dict):

        self.logger.info(f"Processing blocking function '{func_name}'")
        
        loop = QEventLoop()
        timer = QTimer()

        timer.setSingleShot(True)
        timer.timeout.connect(loop.quit)
        timer.timeout.connect(lambda: self.logger.info("Blocking Function Timeout"))
        self.bench_model.handle_done.connect(loop.quit)
        timer.start(1000*200)  

        loop.exec_()

        self._process_function_section(func_name, section)

    def _parse_value(self, raw_value):
        """Обработка значений с переменных """
        if isinstance(raw_value, str) and raw_value.startswith('$'):
            var_name = raw_value[1:]
            return self.execution_results.get(var_name)
        return raw_value
