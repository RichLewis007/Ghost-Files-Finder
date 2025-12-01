# Filename: __init__.py
# Author: Rich Lewis @RichLewis007
# Description: Worker components package for background tasks. Exports worker classes
#              for filesystem scanning and file deletion operations.

from rfe.workers.delete_worker import DeleteResult, DeleteWorker
from rfe.workers.scan_worker import ScanPayload, ScanStats, ScanWorker

__all__ = [
    "DeleteResult",
    "DeleteWorker",
    "ScanPayload",
    "ScanStats",
    "ScanWorker",
]
