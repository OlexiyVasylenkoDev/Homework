import requests
import psutil
import functools
from collections import OrderedDict


def lfu(f, max_limit=2):
    cache = {}

    @functools.wraps(f)
    def deco(*args, **kwargs):
        cache_key = (args, tuple(kwargs.items()))
        if cache_key in cache.keys():
            cache[cache_key] += 1
        else:
            cache.update({cache_key: 1})
        my_func = f(*args, **kwargs)
        result = OrderedDict(sorted(cache.items(), key=lambda x: x[1]))
        while len(result) > max_limit:
            result.popitem(last=False)
        return my_func, result

    return deco


def memory_usage_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        process = psutil.Process()
        memory_before = process.memory_info().rss
        my_func = func(*args, **kwargs)
        print(f'This function takes {process.memory_info().rss - memory_before} bytes')
        return my_func

    return wrapper


@lfu
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
