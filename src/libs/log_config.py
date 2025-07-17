import logging
import os

def setup_logging():
    # Get the script file name without the extension
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    script_log_file = f"../../log/{script_name}.log"
    combined_log_file = "../../log/simple_azure_scripts.log"
    
    # Create a custom logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Create handlers
    script_handler = logging.FileHandler(script_log_file)
    combined_handler = logging.FileHandler(combined_log_file)
    
    # Create formatters and add them to the handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    script_handler.setFormatter(formatter)
    combined_handler.setFormatter(formatter)
    
    # Add handlers to the logger
    logger.addHandler(script_handler)
    logger.addHandler(combined_handler)

