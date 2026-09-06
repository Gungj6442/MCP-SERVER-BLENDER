"""Управление запуском Blender."""

import subprocess
import os
import tempfile
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class BlenderRunner:
    """Класс для запуска и управления Blender."""
    
    def __init__(self, blender_path: str = "blender", timeout: int = 30):
        self.blender_path = blender_path
        self.timeout = timeout
        self._temp_files = []
    
    def _cleanup_temp_files(self):
        """Удалить временные файлы."""
        for path in self._temp_files:
            try:
                if os.path.exists(path):
                    os.unlink(path)
            except Exception as e:
                logger.warning(f"Не удалось удалить {path}: {e}")
        self._temp_files.clear()
    
    def _create_temp_script(self, script: str) -> str:
        """Создать временный файл со скриптом."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', 
                                        delete=False, encoding='utf-8') as f:
            f.write(script)
            path = f.name
            self._temp_files.append(path)
            return path
    
    def execute_script(self, script: str) -> Dict[str, Any]:
        """Выполнить скрипт в Blender и вернуть результат."""
        script_path = self._create_temp_script(script)
        
        try:
            # Запускаем Blender в фоновом режиме
            cmd = [
                self.blender_path,
                '--background',  # Без GUI
                '--python', script_path,
                '--python-exit-code', '1'  # Выход с кодом ошибки
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                env={**os.environ, 'PYTHONUNBUFFERED': '1'}
            )
            
            # Парсим вывод
            output = result.stdout
            error = result.stderr
            
            # Ищем JSON в выводе
            for line in reversed(output.splitlines()):
                line = line.strip()
                if line.startswith('{') and line.endswith('}'):
                    try:
                        data = json.loads(line)
                        data['_success'] = True
                        return data
                    except json.JSONDecodeError:
                        continue
            
            # Если JSON не найден
            return {
                'success': False,
                'error': 'JSON не найден в выводе',
                'stdout': output[-1000:],
                'stderr': error[-1000:]
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': f'Таймаут выполнения ({self.timeout}с)'
            }
        except FileNotFoundError:
            return {
                'success': False,
                'error': f'Blender не найден по пути: {self.blender_path}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
        finally:
            self._cleanup_temp_files()
    
    def check_blender(self) -> bool:
        """Проверить, доступен ли Blender."""
        try:
            result = subprocess.run(
                [self.blender_path, '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False
    
    def get_blender_version(self) -> Optional[str]:
        """Получить версию Blender."""
        try:
            result = subprocess.run(
                [self.blender_path, '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
              lines = result.stdout.split('\n')
                if lines:
                    return lines[0].strip()
            return None
        except:
            return None
