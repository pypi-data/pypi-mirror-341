# Auto-generated __init__.py

# Version of the pyfunc2 package
import sys
sys.path.append('../')
from ._version import __version__

# Import necessary modules and functions here
from Serialization import Serialization
from find_class_name import find_class_name
from find_words import find_words
from find_words import test
from generate_pattern import generate_pattern

# Public API of the package
__all__ = [Serialization, find_words, test, generate_pattern]