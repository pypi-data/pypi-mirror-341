from dataclasses import asdict, astuple, fields, replace, dataclass
from sync_dataclasses import SyncDataClass

@dataclass
class _TestData(SyncDataClass):
    value1: int = 1
    value2: str = "1"

def test_asdict():
    data = _TestData()
    assert asdict(data) == {"value1": 1, "value2": "1"}
    data.value1 = 2
    data.value2 = "2"
    assert asdict(data) == {"value1": 2, "value2": "2"}

def test_fields():
    data = _TestData()
    assert [field.name for field in fields(data)] == ["value1", "value2"]
    assert [field.type for field in fields(data)] == [int, str]
    assert [field.default for field in fields(data)] == [1, "1"]
    data.value1 = 2
    data.value2 = "2"
    assert [field.default for field in fields(data)] == [1, "1"]

def test_astuple():
    data = _TestData()
    assert astuple(data) == (1, "1")
    data.value1 = 2
    data.value2 = "2"
    assert astuple(data) == (2, "2")

def test_replace():
    data = _TestData()
    new_data = replace(data, value1=3, value2="3")
    assert new_data.value1 == 3
    assert new_data.value2 == "3"
    assert data.value1 == 1
    assert data.value2 == "1"
    assert new_data != data
