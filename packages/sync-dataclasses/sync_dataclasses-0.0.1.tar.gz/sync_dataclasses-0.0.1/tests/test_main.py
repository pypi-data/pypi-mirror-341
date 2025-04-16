import threading
import time
from atomic_dataclasses import ADataClass

class AtomicData(ADataClass):
    value1: int = 0
    value2: str = ""

# --- 使用示例 ---
auto_data = AtomicData()

def worker(data_obj):
    for i in range(3):
        current_v1 = data_obj.value1
        current_v2 = data_obj.value2
        print(f"{threading.current_thread().name}: Read v1={current_v1}, v2='{current_v2}'")
        time.sleep(0.01)
        data_obj.value1 += 10
        data_obj.value2 += str(i)
        print(f"{threading.current_thread().name}: Wrote v1={data_obj.value1}, v2='{data_obj.value2}'")
        time.sleep(0.02)

threads = []
for i in range(5):
    t = threading.Thread(target=worker, args=(auto_data,), name=f"Worker-{i}")
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"Final state: value1={auto_data.value1}, value2='{auto_data.value2}'")