import requests
import psutil
import functools
from collections import OrderedDict


def lfu(max_limit=2):
    def internal(f):
        cache = {}
        @functools.wraps(f)
        def deco(*args, **kwargs):
            cache_key = (args, tuple(kwargs.items()))
            if cache_key in cache:
                cache[cache_key]["counter"] += 1
                return cache[cache_key]["result"]
            if len(cache) >= max_limit:
                del cache[min(cache, key=lambda x: cache[x]["counter"])]
            cache[cache_key] = {}
            result = f(*args, **kwargs)
            cache[cache_key]["counter"] = 1
            cache[cache_key]["result"] = result
            print(cache)
            return result
        return deco
    return internal


def memory_usage_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        process = psutil.Process(os.getpid())
        memory_before = process.memory_info()[0]
        my_func = func(*args, **kwargs)
        print(f'This function takes {process.memory_info()[0] - memory_before} bytes')
        return my_func

    return wrapper


@lfu()
@memory_usage_decorator
def fetch_url(url, first_n=100):
    """Fetch a given url"""
    res = requests.get(url)
    return res.content[:first_n] if first_n else res.content


if __name__ == '__main__':
    print(fetch_url('https://stackoverflow.com'))
    print(fetch_url('https://google.com'))
    print(fetch_url('https://google.com'))
    print(fetch_url('https://google.com'))
    print(fetch_url('https://github.com'))
    print(fetch_url('https://github.com'))
    print(fetch_url('https://github.com'))
    print(fetch_url('https://reyestr.court.gov.ua'))
    print(fetch_url('https://reyestr.court.gov.ua'))
    print(fetch_url('https://reyestr.court.gov.ua'))
    print(fetch_url('https://ua.tribuna.com'))
    print(fetch_url('https://ua.tribuna.com'))
    print(fetch_url('https://ua.tribuna.com'))
    print(fetch_url('https://ua.tribuna.com'))
    print(fetch_url('https://ua.tribuna.com'))
    print(fetch_url('https://ithillel.com'))