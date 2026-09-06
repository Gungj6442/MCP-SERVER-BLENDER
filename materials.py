"""Инструменты для работы с материалами."""

from typing import Dict, Any, List, Optional
from ..blender_runner import BlenderRunner


class MaterialTools:
    """Инструменты для работы с материалами."""
    
    def __init__(self, runner: BlenderRunner):
        self.runner = runner
    
    def create(self, name: str, color: List[float] = [0.8, 0.2, 0.2],
               roughness: float = 0.5, metallic: float = 0.0) -> Dict[str, Any]:
        """Создать материал."""
        script = f"""
import bpy
import json

# Создаём материал
mat = bpy.data.materials.new(name="{name}")
mat.use_nodes = True

# Настройка нодов
nodes = mat.node_tree.nodes
links = mat.node_tree.links

# Очищаем
nodes.clear()

# Principled BSDF
bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
bsdf.inputs["Base Color"].default_value = ({color[0]}, {color[1]}, {color[2]}, 1.0)
bsdf.inputs["Roughness"].default_value = {roughness}
bsdf.inputs["Metallic"].default_value = {metallic}

# Output
output = nodes.new(type="ShaderNodeOutputMaterial")
links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])

result = {{
    "success": True,
    "name": mat.name,
    "color": {color},
    "roughness": {roughness},
    "metallic": {metallic}
}}
print(json.dumps(result))
"""
        return self.runner.execute_script(script)
    
    def assign(self, object_name: str, material_name: str) -> Dict[str, Any]:
        """Применить материал к объекту."""
        script = f"""
import bpy
import json

obj = bpy.data.objects.get("{object_name}")
if not obj:
    result = {{"success": False, "error": "Объект не найден", "name": "{object_name}"}}
    print(json.dumps(result))
    exit()

mat = bpy.data.materials.get("{material_name}")
if not mat:
    result = {{"success": False, "error": "Материал не найден", "name": "{material_name}"}}
    print(json.dumps(result))
    exit()

# Применяем материал
if obj.data.materials:
    obj.data.materials[0] = mat
else:
    obj.data.materials.append(mat)

result = {{
    "success": True,
    "object": "{object_name}",
    "material": "{material_name}"
}}
print(json.dumps(result))
"""
        return self.runner.execute_script(script)
    
    def list_all(self) -> Dict[str, Any]:
        """Список всех материалов."""
        script = """
import bpy
import json

materials = []
for mat in bpy.data.materials:
    materials.append({
        "name": mat.name,
        "users": mat.users
    })

result = {
    "success": True,
    "count": len(materials),
    "materials": materials
}
print(json.dumps(result))
"""
        return self.runner.execute_script(script)
    
    def delete(self, name: str) -> Dict[str, Any]:
        """Удалить материал."""
        script = f"""
import bpy
import json

mat = bpy.data.materials.get("{name}")
if mat:
    bpy.data.materials.remove(mat)
    result = {{"success": True, "deleted": "{name}"}}
else:
    result = {{"success": False, "error": "Материал не найден", "name": "{name}"}}

print(json.dumps(result))
"""
        return self.runner.execute_script(script)
