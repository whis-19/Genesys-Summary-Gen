import tiktoken
import time

def count_tokens(text: str, model: str = "cl100k_base") -> int:
    tokenizer = tiktoken.get_encoding(model)
    return len(tokenizer.encode(text))

def timeit(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Function {func.__name__} took {end - start:.2f} seconds.")
        return result
    return wrapper 