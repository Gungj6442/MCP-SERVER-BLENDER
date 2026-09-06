"""Мост между MCP и Blender."""

import subprocess
import tempfile
import json
import os


class BlenderBridge:
    def __init__(self, blender_path: str = "blender"):
        self.blender_path = blender_path
    
    async def _run_script(self, script: str) -> dict:
        """Выполнить Python скрипт в Blender."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(script)
            path = f.name
        
        try:
            result = subprocess.run(
                [self.blender_path, '--background', '--python', path],
                capture_output=True, text=True, timeout=30
            )
            
            # Ищем JSON в выводе
            for line in reversed(result.stdout.splitlines()):
                if line.startswith('{'):
                    return json.loads(line)
            
            return {"error": "Нет JSON в выводе", "stdout": result.stdout[:200]}
        finally:
            os.unlink(path)
    
    async def create_object(self, type: str = "cube", location: list = [0, 0, 0], size: float = 1.0):
        script = f"""
import bpy, json
bpy.ops.mesh.primitive_{type}_add(size={size}, location={location})
print(json.dumps({{"status": "ok", "name": bpy.context.object.name}}))
"""
        return await self._run_script(script)
    
    async def render_image(self, resolution_x=1920, resolution_y=1080, output_path="render.png"):
        script = f"""
import bpy, json
scene = bpy.context.scene
scene.render.resolution_x = {resolution_x}
scene.render.resolution_y = {resolution_y}
scene.render.filepath = "{output_path}"
bpy.ops.render.render(write_still=True)
print(json.dumps({{"status": "ok", "output": "{output_path}"}}))
"""
        return await self._run_script(script)
