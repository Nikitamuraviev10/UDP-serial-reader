from functools import partial
import logging
from typing import Any, Callable, Dict, Optional, Tuple


class CommandRegistry:
    _commands: Dict[str, Tuple[Callable, Optional[object]]] = {}

    @classmethod
    def register(cls, name: Optional[str] = None, instance: Any = None):
        def decorator(func: Callable) -> Callable:
            nonlocal name, instance
            final_name = name or func.__name__

            def wrapper(self=None, *args, **kwargs):
                nonlocal instance
                if instance == "self":
                    instance = self
                if instance:
                    return func(instance, *args, **kwargs)
                return func(*args, **kwargs)

            if final_name in cls._commands:
                raise KeyError(f"Command '{final_name}' already registered")

            cls._commands[final_name] = (wrapper, instance)
            logging.debug(f"Command registered: {final_name}")
            return wrapper

        return decorator
    
    @classmethod
    def get_commands(cls) -> Dict[str, Tuple[Callable, Optional[object]]]:
        """
        Возвращает копию словаря зарегистрированных команд
        """
        return cls._commands.copy()
    
    @classmethod
    def clear_registry(cls) -> None:
        """
        Очищает реестр команд
        """
        cls._commands.clear()
        logging.debug("Command registry cleared")

    @classmethod
    def execute(cls, command_name: str, *args: Any, **kwargs: Any) -> Any:
        """
        Выполняет зарегистрированную команду
        """
        if command_name not in cls._commands:
            raise KeyError(f"Command '{command_name}' not found")
        
        func, instance = cls._commands[command_name]
        if instance:
            return func(instance, *args, **kwargs)
        else:
            return func(*args, **kwargs)