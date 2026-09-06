"""Инструменты для анимации."""

from typing import Dict, Any, List, Optional
from ..blender_runner import BlenderRunner


class AnimationTools:
    """Инструменты для работы с анимацией."""
    
    def __init__(self, runner: BlenderRunner):
        self.runner = runner
    
    def add_keyframe(self, object_name: str, property: str, 
                     frame: int, value: List[float]) -> Dict[str, Any]:
        """Добавить ключевой кадр."""
        script = f"""
import bpy
import json

obj = bpy.data.objects.get("{object_name}")
if not obj:
    result = {{"success": False, "error": "Объект не найден", "name": "{object_name}"}}
    print(json.dumps(result))
    exit()

# Устанавливаем значение
if "{property}" == "location":
    obj.location = {value}
elif "{property}" == "rotation":
    obj.rotation_euler = {value}
elif "{property}" == "scale":
    obj.scale = {value}
else:
    result = {{"success": False, "error": "Неизвестное свойство", "property": "{property}"}}
    print(json.dumps(result))
    exit()

# Добавляем ключ
obj.keyframe_insert(data_path="{property}", frame={frame})

result = {{
    "success": True,
    "object": "{object_name}",
    "property": "{property}",
    "frame": {frame},
    "value": {value}
}}
print(json.dumps(result))
"""
        return self.runner.execute_script(script)
    
    def set_frame(self, frame: int) -> Dict[str, Any]:
        """Установить текущий кадр."""
        script = f"""
import bpy
import json

bpy.context.scene.frame_set({frame})

result = {{
    "success": True,
    "frame": {frame}
}}
print(json.dumps(result))
"""
        return self.runner.execute_script(script)
    
    def play(self, start_frame: int = 1, end_frame: int = 100) -> Dict[str, Any]:
        """Установить диапазон анимации."""
        script = f"""
import bpy
import json

scene = bpy.context.scene
scene.frame_start = {start_frame}
scene.frame_end = {end_frame}

result = {{
    "success": True,
    "start": {start_frame},
    "end": {end_frame}
}}
print(json.dumps(result))
"""
        return self.runner.execute_script(script)
    
    def clear_animation(self, object_name: str) -> Dict[str, Any]:
        """Очистить анимацию объекта."""
        script = f"""
import bpy
import json

obj = bpy.data.objects.get("{object_name}")
if not obj:
    result = {{"success": False, "error": "Объект не найден", "name": "{object_name}"}}
    print(json.dumps(result))
    exit()

# Удаляем анимацию
if obj.animation_data:
    obj.animation_data_clear()

result = {{
    "success": True,
    "object": "{object_name}",
    "message": "Анимация удалена"
}}
print(json.dumps(result))
"""
        return self.runner.execute_script(script)
