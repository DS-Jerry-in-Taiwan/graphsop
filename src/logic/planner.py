"""
SOP 路徑規劃器 (SOP Planner) for TwinLex Phase 03
- 根據意圖與圖譜，規劃從當前狀態到目標狀態的 SOP 步驟序列
- 支援最短路徑搜尋與步驟驗證條件生成
"""

from typing import List, Dict, Any

def plan_sop_steps(intent: Dict[str, Any], graph_path: List[str]) -> List[Dict[str, Any]]:
    """
    根據意圖與圖譜路徑，生成 SOP 步驟列表
    :param intent: 使用者意圖 dict
    :param graph_path: 從 current 到 target 的節點名稱序列
    :return: SOP 步驟列表，每步包含 action、params、verify
    """
    steps = []
    step_num = 1
    # 範例規則：根據節點名稱決定 SOP 步驟
    for node in graph_path:
        if node == "MOTOR_LOCK":
            steps.append({
                "step": step_num,
                "action": "UNLOCK_MOTOR",
                "verify": "status == UNLOCKED"
            })
            step_num += 1
        elif node == "ROTATE":
            steps.append({
                "step": step_num,
                "action": "ROTATE",
                "params": intent.get("parameters", {}),
                "verify": f"angle == {intent.get('parameters', {}).get('angle')}"
            })
            step_num += 1
        elif node == "ZOOM":
            steps.append({
                "step": step_num,
                "action": "ZOOM",
                "params": intent.get("parameters", {}),
                "verify": f"zoom_level == {intent.get('parameters', {}).get('zoom_level')}"
            })
            step_num += 1
        # 可擴充更多 SOP 節點
    return steps