# __init__.py

from __future__ import annotations
import os
from cyborgdb_lite.cyborgdb_lite import Client
from cyborgdb_lite.cyborgdb_lite import DBConfig
from cyborgdb_lite.cyborgdb_lite import EncryptedIndex
from cyborgdb_lite.cyborgdb_lite import IndexConfig
from cyborgdb_lite.cyborgdb_lite import IndexIVFFlat
from .cyborgdb_lite import set_working_dir
from . import cyborgdb_lite

# Determine the path to .cyborglicense in the package directory
current_path = os.path.dirname(__file__)

# Set the global license file path in the C++ code
set_working_dir(current_path)

__all__ = ['Client', 'DBConfig', 'EncryptedIndex', 'IndexConfig', 'IndexIVFFlat', 'cyborgdb_lite']
