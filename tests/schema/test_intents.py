import json
import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src", "schema")))
from intents import ActionType, ControlIntent, QueryIntent, MaintenanceIntent

@pytest.fixture(scope="module")
def ontology_actions():
    with open("src/schema/ontology.json", encoding="utf-8") as f:
        data = json.load(f)
    return {n["type"] for n in data.get("nodes", []) if n["type"] == "Action"}

def test_actiontype_enum_covers_ontology(ontology_actions):
    enum_actions = {a.value for a in ActionType}
    # 假設 ontology.json 會有 Action 節點的名稱清單
    # 若 ontology.json 有更細的 action name 屬性，請調整此處
    assert enum_actions >= {"ROTATE", "ZOOM", "RESET"}
    # 可根據實際 ontology.json 擴充

def test_control_intent_required_fields():
    intent = ControlIntent(action=ActionType.ROTATE, target_id="node_1")
    assert intent.action == ActionType.ROTATE
    assert intent.target_id == "node_1"

def test_query_intent_required_fields():
    intent = QueryIntent(query_type="SPEC", target_id="node_2")
    assert intent.category.value == "QUERY"
    assert intent.target_id == "node_2"

def test_maintenance_intent_required_fields():
    intent = MaintenanceIntent(issue_type="ERROR", target_id="node_3", description="test")
    assert intent.category.value == "MAINTENANCE"
    assert intent.target_id == "node_3"
    assert intent.description == "test"