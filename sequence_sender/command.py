import subprocess
import sys
import logging

from sequence_sender.command_registry import CommandRegistry


logger = logging.getLogger("Command execution")

@CommandRegistry.register()
def sum(a,b):
    return a + b

@CommandRegistry.register()
def run_analysis(file_name):
    try:
        logging.info(f"Run Analysis: {file_name}")
        result = subprocess.run(
            [sys.executable, "scripts/Freq_Phase_response.py", file_name],
            check=True,
            stdout=subprocess.PIPE,  
            stderr=subprocess.PIPE,  
            text=True 
        )
        logging.info("Script output:\n" + result.stdout)
    except subprocess.CalledProcessError as e:
        logging.error(f"Script failed with error:\n{e.stderr}")
        raise 