import random
import time
from typing import Dict, Any
from src.hardware.interface import DeviceInterface

class MockCamera(DeviceInterface):
    """
    Stateful Mock Camera，支援隨機故障與狀態查詢。
    """
    def __init__(self):
        self.pan = 0.0
        self.tilt = 0.0
        self.zoom_level = 1.0
        self.power_on = True

    def rotate(self, pan: float, tilt: float) -> Dict[str, Any]:
        # 模擬隨機延遲
        time.sleep(random.uniform(0.05, 0.2))
        # 5% 機率執行失敗
        if random.random() < 0.05:
            return {"success": False, "reason": "Motor jammed", "pan": self.pan, "tilt": self.tilt}
        self.pan = pan
        self.tilt = tilt
        return {"success": True, "pan": self.pan, "tilt": self.tilt}

    def zoom(self, level: float) -> Dict[str, Any]:
        time.sleep(random.uniform(0.05, 0.15))
        if random.random() < 0.05:
            return {"success": False, "reason": "Zoom motor error", "zoom": self.zoom_level}
        self.zoom_level = level
        return {"success": True, "zoom": self.zoom_level}

    def get_status(self) -> Dict[str, Any]:
        return {
            "pan": self.pan,
            "tilt": self.tilt,
            "zoom": self.zoom_level,
            "power": self.power_on
        }

    def power(self, on: bool) -> Dict[str, Any]:
        self.power_on = on
        return {"success": True, "power": self.power_on}