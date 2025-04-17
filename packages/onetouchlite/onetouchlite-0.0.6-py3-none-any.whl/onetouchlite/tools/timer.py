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


def load_progress_lib():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../utils"))
    system = platform.system()

    if system == "Windows":
        libname = "progress.dll"
    elif system == "Linux":
        libname = "libprogress.a"
    else:
        raise RuntimeError(f"Unsupported platform: {system}")

    lib_path = os.path.join(base_dir, libname)
    return ctypes.CDLL(lib_path)


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


lib = load_progress_lib()

# 设置函数参数类型
lib.init_progress.argtypes = [ctypes.c_int]
lib.update_progress.argtypes = [ctypes.c_int]


# 示例用法
if __name__ == "__main__":
    for i in pace(range(10_000_000)):
        pass


