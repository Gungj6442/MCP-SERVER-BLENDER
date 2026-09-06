"""Набор инструментов MCP для Blender."""

from .objects import ObjectTools
from .materials import MaterialTools
from .animation import AnimationTools
from .scene import SceneTools
from .export import ExportTools

__all__ = [
    'ObjectTools',
    'MaterialTools', 
    'AnimationTools',
    'SceneTools',
    'ExportTools'
]
