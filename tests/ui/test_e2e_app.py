import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.hardware.mock_camera import MockCamera
from src.logic.verifier import verify_execution, VerificationError

@pytest.fixture
def camera():
    return MockCamera()

def test_successful_rotate(camera):
    # 成功案例：旋轉到 30 度
    result = camera.rotate(30, 0)
    assert result["success"]
    status = camera.get_status()
    verify_execution({"pan": 30}, status)

def test_violation_rotate(camera):
    # 違規案例：旋轉到 400 度（假設驗證器只允許 <= 180）
    camera.rotate(400, 0)
    status = camera.get_status()
    with pytest.raises(VerificationError):
        verify_execution({"pan": 180}, status)  # 預期值超過，應報錯

def test_hardware_failure(camera, monkeypatch):
    # 故障案例：強制 rotate 回傳失敗
    def fail_rotate(pan, tilt):
        return {"success": False, "reason": "Motor jammed", "pan": camera.pan, "tilt": camera.tilt}
    monkeypatch.setattr(camera, "rotate", fail_rotate)
    result = camera.rotate(30, 0)
    assert not result["success"]
    # 驗證失敗訊息可由 UI 顯示