"""Инструменты для создания и управления 3D объектами."""

from typing import Dict, Any, List, Optional
from ..blender_runner import BlenderRunner


class ObjectTools:
    """Инструменты для работы с объектами."""
    
    def __init__(self, runner: BlenderRunner):
        self.runner = runner
    
    def create(self, obj_type: str, location: List[float] = [0, 0, 0],
               size: float = 1.0, name: str = "") -> Dict[str, Any]:
        """Создать 3D объект."""
        script = f"""
import bpy
import json

# Удаляем стандартный куб если он есть
if "Cube" in bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects["Cube"])

# Создаём объект
bpy.ops.mesh.primitive_{obj_type}_add(
    size={size},
    location={location}
)

obj = bpy.context.object
if "{name}":
    obj.name = "{name}"

# Обновляем сцену
bpy.context.view_layer.update()

result = {{
    "success": True,
    "name": obj.name,
    "type": "{obj_type}",
    "location": list(obj.location),
    "scale": list(obj.scale),
    "rotation": list(obj.rotation_euler)
}}
print(json.dumps(result))
"""
        return self.runner.execute_script(script)
    
    def delete(self, name: str) -> Dict[str, Any]:
        """Удалить объект по имени."""
        script = f"""
import bpy
import json

obj = bpy.data.objects.get("{name}")
if obj:
    bpy.data.objects.remove(obj)
    result = {{"success": True, "deleted": "{name}"}}
else:
    result = {{"success": False, "error": "Объект не найден", "name": "{name}"}}

print(json.dumps(result))
"""
        return self.runner.execute_script(script)
    
    def list_all(self) -> Dict[str, Any]:
        """Получить список всех объектов."""
        script = """
import bpy
import json

objects = []
for obj in bpy.data.objects:
    objects.append({
        "name": obj.name,
        "type": obj.type,
        "location": list(obj.location),
        "scale": list(obj.scale),
        "rotation": list(obj.rotation_euler),
        "parent": obj.parent.name if obj.parent else None
    })

result = {
    "success": True,
    "count": len(objects),
    "objects": objects
}
print(json.dumps(result))
"""
        return self.runner.execute_script(script)
    
    def duplicate(self, name: str, new_name: str = "") -> Dict[str, Any]:
        """Дублировать объект."""
        script = f"""
import bpy
import json

obj = bpy.data.objects.get("{name}")
if not obj:
    result = {{"success": False, "error": "Объект не найден", "name": "{name}"}}
    print(json.dumps(result))
    exit()

# Дублируем
new_obj = obj.copy()
new_obj.data = obj.data.copy()
bpy.context.collection.objects.link(new_obj)

if "{new_name}":
    new_obj.name = "{new_name}"

result = {{
    "success": True,
    "original": "{name}",
    "new_name": new_obj.name
}}
print(json.dumps(result))
"""
        return self.runner.execute_script(script)
    
    def transform(self, name: str, location: Optional[List[float]] = None,
                 rotation: Optional[List[float]] = None,
                 scale: Optional[List[float]] = None) -> Dict[str, Any]:
        """Трансформировать объект."""
        loc_str = str(location) if location else "None"
        rot_str = str(rotation) if rotation else "None"
        scale_str = str(scale) if scale else "None"
        
        script = f"""
import bpy
import json

obj = bpy.data.objects.get("{name}")
if not obj:
    result = {{"success": False, "error": "Объект не найден", "name": "{name}"}}
    print(json.dumps(result))
    exit()

if {loc_str} is not None:
    obj.location = {loc_str}
if {rot_str} is not None:
    obj.rotation_euler = {rot_str}
if {scale_str} is not None:
    obj.scale = {scale_str}

bpy.context.view_layer.update()

result = {{
    "success": True,
    "name": obj.name,
    "location": list(obj.location),
    "rotation": list(obj.rotation_euler),
    "scale": list(obj.scale)
}}
print(json.dumps(result))
"""
        return self.runner.execute_script(script)
