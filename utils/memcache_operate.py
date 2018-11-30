
import memcache
from config import MEMCACHE_HOST

cache = memcache.Client([MEMCACHE_HOST],debug=True)

def set(key,value,timeout=60):
    return cache.set(key,value,timeout)

def get(key):
    return cache.get(key)

def delete(key):
    return cache.delete(key)
