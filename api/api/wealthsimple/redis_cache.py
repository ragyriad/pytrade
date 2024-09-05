from datetime import datetime, timedelta
from django.core.cache import cache

def set_instance_cache(instance,expiry):
    print(f" expiry {expiry}")
    test_expiry = datetime.now() + timedelta(minutes=5)
    expiry_timestamp = (expiry - datetime.now())
    print(f"test_expiry {test_expiry}   in Seconds {5*60}")
    print(f"expiry_timestamp {expiry} in seconds {expiry_timestamp.total_seconds()}")
    cache.set('ws_instance',instance,timeout=300)
    return True

def get_instance_cache():
    instance = cache.get('ws_instance')
    return instance

def del_instance_cache(key):
    cache.delete(key)
    return True