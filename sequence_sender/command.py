
from sequence_sender.command_registry import CommandRegistry


@CommandRegistry.register()
def sum(a,b):
    return a + b