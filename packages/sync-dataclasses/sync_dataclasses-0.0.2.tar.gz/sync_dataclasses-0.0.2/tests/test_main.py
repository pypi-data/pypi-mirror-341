import threading
import time
from sync_dataclasses import SyncDataClass

class _TestData(SyncDataClass):
    value1: int = 0
    value2: str = ""
    value3: list[int] = []

def _worker(data: _TestData):
    for _ in range(100):
        data.value1 += 1
        data.value2 += str(1)
        data.value3.append(1)
        time.sleep(0.001)

def test_main():
    test_data = _TestData()
    threads = [threading.Thread(target=_worker, args=[test_data]) for i in range(10)]
    for t in threads: t.start()
    for t in threads: t.join()
    assert test_data.value1 == 1000
    assert test_data.value2 == "1" * 1000
    assert test_data.value3 == [1] * 1000
