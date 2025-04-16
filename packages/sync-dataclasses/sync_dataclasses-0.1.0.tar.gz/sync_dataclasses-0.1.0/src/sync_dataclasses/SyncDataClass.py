from threading import RLock

ATOMIC_DATACLASS_LOCK_NAME = "_lock"
def _is_proxied_attr(name) -> bool:
    """
    Check if the attribute is proxied (i.e., should be got and set via reflect).
    This function is defined independently to avoid recursive attribute read.
    """
    return name == ATOMIC_DATACLASS_LOCK_NAME or (
            name.startswith("__") and name.endswith("__"))

class SyncDataClass:
    def __post_init__(self):
        object.__setattr__(self, ATOMIC_DATACLASS_LOCK_NAME, RLock())

    def __getattribute__(self, name):
        if _is_proxied_attr(name):
             return object.__getattribute__(self, name)

        # directly get attribute while init
        try: lock = object.__getattribute__(self, ATOMIC_DATACLASS_LOCK_NAME)
        except AttributeError: return object.__getattribute__(self, name)

        with lock: return object.__getattribute__(self, name)

    def __setattr__(self, name, value):
        if _is_proxied_attr(name):
            object.__setattr__(self, name, value)
            return

        # directly set attribute while init
        try: lock = object.__getattribute__(self, ATOMIC_DATACLASS_LOCK_NAME)
        except AttributeError: return object.__setattr__(self, name, value)

        with lock: object.__setattr__(self, name, value)
