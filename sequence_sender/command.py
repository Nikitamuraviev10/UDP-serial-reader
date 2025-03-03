
from sequence_sender.command_registry import CommandRegistry


@CommandRegistry.register()
def sum(a,b):
    return a + b

@CommandRegistry.register()
def run_analysis(file_name):
    print("Run Analisys:", file_name)