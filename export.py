"""Инструменты для экспорта моделей."""

from typing import Dict, Any, List, Optional
from ..blender_runner import BlenderRunner


class ExportTools:
    """Инструменты для экспорта 3D моделей."""
    
    def __init__(self, runner: BlenderRunner):
        self.runner = runner
    
    def export_fbx(self, output_path: str, selected_only: bool = False) -> Dict[str, Any]:
        """Экспорт в FBX."""
        script = f"""
import bpy
import json

# Выбираем объекты
if {str(selected_only).lower()}:
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.context.selected_objects:
        obj.select_set(True)
else:
    bpy.ops.object.select_all(action='SELECT')

# Экспорт
bpy.ops.export_scene.fbx(
    filepath="{output_path}",
    use_selection={str(selected_only).lower()}
)

result = {{
    "success": True,
    "output": "{output_path}",
    "selected_only": {str(selected_only).lower()}
}}
print(json.dumps(result))
"""
        return self.runner.execute_script(script)
    
    def export_gltf(self, output_path: str, selected_only: bool = False) -> Dict[str, Any]:
        """Экспорт в GLTF."""
        script = f"""
import bpy
import json

# Выбираем объекты
if {str(selected_only).lower()}:
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.context.selected_objects:
        obj.select_set(True)
else:
    bpy.ops.object.select_all(action='SELECT')

# Экспорт
bpy.ops.export_scene.gltf(
    filepath="{output_path}",
    use_selection={str(selected_only).lower()}
)

result = {{
    "success": True,
    "output": "{output_path}",
    "selected_only": {str(selected_only).lower()}
}}
print(json.dumps(result))
"""
        return self.runner.execute_script(script)
    
    def export_stl(self, output_path: str, selected_only: bool = False) -> Dict[str, Any]:
        """Экспорт в STL."""
        script = f"""
import bpy
import json

# Выбираем объекты
if {str(selected_only).lower()}:
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.context.selected_objects:
        obj.select_set(True)
else:
    bpy.ops.object.select_all(action='SELECT')

# Экспорт
bpy.ops.export_mesh.stl(
    filepath="{output_path}",
    use_selection={str(selected_only).lower()}
)

result = {{
    "success": True,
    "output": "{output_path}",
    "selected_only": {str(selected_only).lower()}
}}
print(json.dumps(result))
"""
        return self.runner.execute_script(script)
    
    def export_obj(self, output_path: str, selected_only: bool = False) -> Dict[str, Any]:
        """Экспорт в OBJ."""
        script = f"""
import bpy
import json

# Выбираем объекты
if {str(selected_only).lower()}:
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.context.selected_objects:
        obj.select_set(True)
else:
    bpy.ops.object.select_all(action='SELECT')

# Экспорт
bpy.ops.export_scene.obj(
    filepath="{output_path}",
    use_selection={str(selected_only).lower()}
)

result = {{
    "success": True,
    "output": "{output_path}",
    "selected_only": {str(selected_only).lower()}
}}
print(json.dumps(result))
"""
        return self.runner.execute_script(script)
