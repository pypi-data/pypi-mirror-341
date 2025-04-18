from liveconfig.core import manager

def liveclass(cls):
    """
    Decorator to track the attributes of a class and register it with the manager.
    This decorator adds methods to the class to track attributes and their values.
    It ensures that the class is still recognised by IDEs and type checkers.
    """
    original_init = cls.__init__
    original_setattr = getattr(cls, '__setattr__', object.__setattr__)

    def __init__(self, *args, **kwargs):
        self._tracked_attrs = set()
        original_init(self, *args, **kwargs)

    def __setattr__(self, name, value):
        original_setattr(self, name, value)
        if name != "_tracked_attrs":
            self._tracked_attrs.add(name)

    def get_tracked_attrs(self):
        return {attr for attr in self._tracked_attrs if attr != "_tracked_attrs"}

    def get_tracked_attrs_values(self):
        return {name: getattr(self, name) for name in self._tracked_attrs if name != "_tracked_attrs"}

    cls.__init__ = __init__
    cls.__setattr__ = __setattr__
    cls.get_tracked_attrs = get_tracked_attrs
    cls.get_tracked_attrs_values = get_tracked_attrs_values

    manager.register_class(cls)
    return cls


def liveinstance(name=None):
    """
    Decorator to track the attributes of a class instance
    """
    def wrapper(obj):
        if not hasattr(obj, "get_tracked_attrs") or not hasattr(obj, "get_tracked_attrs_values"):
            raise TypeError("Instance is not from a @liveclass-decorated class. Use @liveclass on the class first.")
        obj_name = name if name else f"instance_{id(obj)}"
        manager.register_instance(obj_name, obj)
        return obj
    return wrapper
