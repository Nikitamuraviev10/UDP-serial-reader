import logging
from typing import Any, Callable, Dict, Optional


class CommandRegistry:
    _commands: Dict[str, Callable] = {}

    @classmethod
    def register(cls, name: Optional[str] = None ):
        def decorator(func: Callable) -> Callable:
            nonlocal name
            final_name = name or func.__name__

            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            if final_name in cls._commands:
                raise KeyError(f"Command '{final_name}' already registered")

            cls._commands[final_name] = (wrapper)
            logging.debug(f"Command registered: {final_name}")
            return wrapper

        return decorator
    
    @classmethod
    def get_commands(cls) -> Dict[str,Callable]:
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
