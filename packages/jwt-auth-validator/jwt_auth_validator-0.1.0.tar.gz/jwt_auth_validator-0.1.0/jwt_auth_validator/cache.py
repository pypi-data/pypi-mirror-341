public_key_cache = {}

def get_cached_public_key(kid):
    return public_key_cache.get(kid)

def set_cached_public_key(kid, key):
    public_key_cache[kid] = key