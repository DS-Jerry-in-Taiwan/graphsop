from abc import ABC, abstractmethod
from typing import Dict, Any

class DeviceInterface(ABC):
    """
    硬體抽象層介面，規範所有設備控制方法。
    """

    @abstractmethod
    def rotate(self, pan: float, tilt: float) -> Dict[str, Any]:
        """
        旋轉設備到指定 pan/tilt 角度。
        回傳執行結果與狀態。
        """
        pass

    @abstractmethod
    def zoom(self, level: float) -> Dict[str, Any]:
        """
        設定變焦倍率。
        回傳執行結果與狀態。
        """
        pass

    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """
        取得設備當前狀態（pan, tilt, zoom, power 等）。
        """
        pass

    @abstractmethod
    def power(self, on: bool) -> Dict[str, Any]:
        """
        開關設備電源。
        """
        pass