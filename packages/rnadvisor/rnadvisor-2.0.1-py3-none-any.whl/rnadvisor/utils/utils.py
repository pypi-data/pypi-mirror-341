import time
from typing import Tuple, Any, List
from tqdm import tqdm


def time_it(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        time_result = {list(result.keys())[0]: execution_time}
        return result, time_result

    return wrapper

def fn_time(func, *args, **kwargs) -> Tuple[Any, float]:
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    execution_time = end_time - start_time
    return result, execution_time


def read_txt_file(in_path: str) -> List[str]:
    """
    Read a txt file and return a list of lines
    :param in_path: path to a .txt file
    :return: list of the lines
    """
    with open(in_path, "r") as f:
        lines = f.readlines()
    return [line.strip() for line in lines]

def write_to_txt_file(out_path: str, lines: List[str]) -> None:
    """
    Write a list of lines to a txt file
    :param out_path: path to a .txt file
    :param lines: list of the lines
    """
    with open(out_path, "w") as f:
        for line in lines:
            f.write(line + "\n")

class TqdmCompatibleHandler:
    def write(self, message):
        tqdm.write(message.strip())
    def flush(self):
        pass