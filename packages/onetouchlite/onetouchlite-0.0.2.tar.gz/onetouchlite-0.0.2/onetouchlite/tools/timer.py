import functools
import os
import platform
import time
import ctypes


def timer(func):
    """
    装饰器：记录函数的运行时长
    """
    @functools.wraps(func)  # 保留原函数的元信息
    def wrapper(*args, **kwargs):
        start_time = time.time()  # 记录开始时间
        result = func(*args, **kwargs)  # 调用原函数
        end_time = time.time()  # 记录结束时间
        duration = end_time - start_time  # 计算运行时长
        print(f"Function {func.__name__} took {duration:.6f} seconds to run.")
        return result
    return wrapper


def format_time(seconds):
    return f"{int(seconds // 60):02d}:{int(seconds % 60):02d}"


# 获取 DLL 或 SO 文件的路径
base_dir = os.path.dirname(__file__)
if platform.system() == "Windows":
    # 在 Windows 上加载 .dll 文件
    dll_path = os.path.abspath(os.path.join(base_dir, "../utils/progress.dll"))
elif platform.system() == "Linux":
    # 在 Linux 上加载 .so 文件
    dll_path = os.path.abspath(os.path.join(base_dir, "../utils/progress.a"))
else:
    raise Exception("Unsupported platform")

# 加载动态库
lib = ctypes.CDLL(dll_path)

# 设置函数参数类型
lib.init_progress.argtypes = [ctypes.c_int]
lib.update_progress.argtypes = [ctypes.c_int]

class Progress:
    def __init__(self, total):
        self.obj = lib.create_progress(total)
        self.total = total

    def update(self, value):
        lib.update_progress(self.obj, value)

    def finish(self):
        lib.finish_progress(self.obj)


def pace(it, min_interval=0.05):
    total = len(it)
    lib.init_progress(total)
    last_time = time.perf_counter()

    for idx, val in enumerate(it):
        yield val
        now = time.perf_counter()
        is_last = idx + 1 == total
        if (now - last_time >= min_interval) or is_last:
            lib.update_progress(idx + 1)
            last_time = now


# 示例用法
if __name__ == "__main__":
    for i in pace(range(10_000_000)):
        pass


