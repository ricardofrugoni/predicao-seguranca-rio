"""
📝 LOGGER - Sistema de Logging
===============================

Configuração centralizada de logging para o projeto.
"""

import logging
import sys
from pathlib import Path
from typing import Optional

def setup_logger(
    name: str,
    level: int = logging.INFO,
    log_file: Optional[Path] = None
) -> logging.Logger:
    """
    Configura logger para o projeto
    
    Args:
        name: Nome do logger (geralmente __name__)
        level: Nível de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Caminho para arquivo de log (opcional)
        
    Returns:
        Logger configurado
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove handlers existentes
    logger.handlers.clear()
    
    # Formato do log
    formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler para arquivo (se especificado)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


# Logger padrão do projeto
default_logger = setup_logger(
    'projeto_violencia_rj',
    level=logging.INFO
)

