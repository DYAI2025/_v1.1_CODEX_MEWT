import logging
import os
from datetime import datetime

def setup_logger(name: str = "chat_chunker") -> logging.Logger:
    """
    Erstellt und konfiguriert einen Logger für das Projekt.
    
    Args:
        name: Name des Loggers
        
    Returns:
        Konfigurierter Logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Logs-Verzeichnis erstellen, falls nicht vorhanden
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    # File Handler
    file_handler = logging.FileHandler(
        f"logs/{name}_{datetime.now().strftime('%Y%m%d')}.log"
    )
    file_handler.setLevel(logging.DEBUG)
    
    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Handler hinzufügen
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger 