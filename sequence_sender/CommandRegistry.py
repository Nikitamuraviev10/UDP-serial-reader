class CommandRegistry:
    _commands = {}

    @classmethod
    def register(cls, name: str = None):
        def decorator(func):
            final_name = name or func.__name__
            cls._commands[final_name] = func
            return func
        return decorator

    @classmethod
    def apply_to_model(cls, model):
        model.command_registry.update(cls._commands)