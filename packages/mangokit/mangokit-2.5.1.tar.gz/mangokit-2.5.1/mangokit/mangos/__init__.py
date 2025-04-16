# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2025-02-26 11:46
# @Author : 毛鹏
import os
import platform
import sys
from pathlib import Path

system = platform.system().lower()
if system == "windows":
    runtime_path = os.path.join(os.path.dirname(__file__), "pyarmor_runtime_windows")
elif system == "linux":
    runtime_path = os.path.join(os.path.dirname(__file__), "pyarmor_runtime_linux")
elif system == "Darwin":
    runtime_path = os.path.join(os.path.dirname(__file__), "pyarmor_runtime_linux")
else:
    raise RuntimeError(f"Unsupported platform: {system}")

if runtime_path not in sys.path:
    sys.path.append(runtime_path)
runtime_sub_path = os.path.join(runtime_path, "pyarmor_runtime_000000")
if runtime_sub_path not in sys.path:
    sys.path.append(runtime_sub_path)


def _load_pyarmor():
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    runtime_base = Path(base_path)

    runtime_dir = runtime_base / ('pyarmor_runtime_windows' if sys.platform == 'win32' else 'pyarmor_runtime_linux')

    if not runtime_dir.exists():
        raise RuntimeError(f"PyArmor运行时目录不存在: {runtime_dir}")

    sys.path.insert(0, str(runtime_dir))
    sys.path.insert(0, str(runtime_dir / 'pyarmor_runtime_000000'))


_load_pyarmor()

try:
    from mango import Mango

    mango = Mango()
    mango.v(1)
except ImportError as e:
    raise RuntimeError(f"导入mango模块失败: {str(e)}")
