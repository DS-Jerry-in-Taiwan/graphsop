from enum import Enum
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class IntentCategory(str, Enum):
    CONTROL = "CONTROL"
    QUERY = "QUERY"
    MAINTENANCE = "MAINTENANCE"

class ActionType(str, Enum):
    ROTATE = "ROTATE"
    ZOOM = "ZOOM"
    RESET = "RESET"
    # 可依 ontology.json 擴充

class ControlParameters(BaseModel):
    angle: Optional[float] = Field(None, description="旋轉角度")
    direction: Optional[str] = Field(None, description="LEFT/RIGHT/UP/DOWN")
    zoom_level: Optional[float] = Field(None, description="變焦倍率")

class ControlIntent(BaseModel):
    category: IntentCategory = Field(default=IntentCategory.CONTROL)
    action: ActionType
    target_id: str = Field(..., description="對應圖譜節點 ID")
    parameters: Optional[ControlParameters] = None

class QueryIntent(BaseModel):
    category: IntentCategory = Field(default=IntentCategory.QUERY)
    query_type: str = Field(..., description="查詢類型")
    target_id: Optional[str] = Field(None, description="對應圖譜節點 ID")
    parameters: Optional[Dict[str, Any]] = None

class MaintenanceIntent(BaseModel):
    category: IntentCategory = Field(default=IntentCategory.MAINTENANCE)
    issue_type: str = Field(..., description="維修問題類型")
    target_id: Optional[str] = Field(None, description="對應圖譜節點 ID")
    description: Optional[str] = None

IntentUnion = ControlIntent | QueryIntent | MaintenanceIntent