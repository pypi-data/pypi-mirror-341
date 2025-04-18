"""
HiveCraft - A tool for creating, testing, and compiling AlgoHive puzzles.

This package provides tools for managing and creating .alghive format files.
"""

from hivecraft.alghive import Alghive
from hivecraft.version import __version__
from hivecraft.ressources import PUZZLES_DIFFICULTY

__all__ = ['Alghive', '__version__', 'PUZZLES_DIFFICULTY']
