from enum import Enum
from typing import Literal
from pydantic import BaseModel

class IntentCategory(str, Enum):
    CONTROL = "CONTROL"
    QUERY = "QUERY"
    MAINTENANCE = "MAINTENANCE"

class RouterOutput(BaseModel):
    category: IntentCategory

def classify_intent(user_input: str) -> RouterOutput:
    """
    根據 Phase 02 Prompt，將 user_input 分類為 CONTROL、QUERY 或 MAINTENANCE。
    """
    # 簡易規則範例，可替換為 LLM/向量分類
    control_keywords = ["轉", "開", "關", "調整", "變焦", "重設"]
    query_keywords = ["多少", "規格", "查詢", "手冊", "安全", "狀態", "多重"]
    maintenance_keywords = ["維修", "報修", "異常", "故障", "修理"]

    text = user_input.strip().lower()
    if any(k in text for k in control_keywords):
        return RouterOutput(category=IntentCategory.CONTROL)
    if any(k in text for k in query_keywords):
        return RouterOutput(category=IntentCategory.QUERY)
    if any(k in text for k in maintenance_keywords):
        return RouterOutput(category=IntentCategory.MAINTENANCE)
    # 預設為查詢
    return RouterOutput(category=IntentCategory.QUERY)