"""
EndoriumUtils - Bibliothèque d'utilitaires réutilisables pour les projets Endorium

Ce module fournit des fonctionnalités communes qui peuvent être utilisées 
dans différents projets, principalement:
- Gestion des logs (configuration, rotation, purge)
- Gestion des versions (lecture, incrémentation)
"""

from EndoriumUtils.log_utils import setup_logger, get_logger, log_function_call, log_performance, purge_old_logs
from EndoriumUtils.version_utils import get_version, increment_version, set_version

__version__ = "1.0.0"
