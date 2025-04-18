from . import logger
from liveconfig.typechecker import TypeChecker

class LiveManager:
    def __init__(self):
        self.live_classes = {}
        self.live_instances = {}
        self.file_handler = None
    
    def register_class(self, cls):
        """
        Register a class to be tracked
        """
        self.live_classes[cls.__name__] = cls
        return cls
    
    def register_instance(self, name, instance):
        """
        Register an instance of a class to be tracked
        """
        if name in self.live_instances:
            raise ValueError(f"Instance with name {name} already exists.")
        
        # Load value from file if it exists, else use the default value
        if self.file_handler is not None and self.file_handler.loaded_values is not None and "live_instances" in self.file_handler.loaded_values:
            saved_attrs = self.file_handler.loaded_values["live_instances"].get(name, {})
            instance = self.load_values_into_instance(instance, saved_attrs)
        
        self.live_instances[name] = instance
        # Register the instance in its class if it has a _instances attribute
        cls = type(instance)
        if hasattr(cls, "_instances"):
            cls._instances.append(instance)
        else:
            cls._instances = [instance]

    def load_values_into_instance(self, instance, attrs):
        """
        Loads the values from the save file into the instance.
        """
        for attr, value in attrs.items():
            setattr(instance, attr, value)
        return instance
    
    def get_live_classes(self):
        """
        Get all live classes
        """
        return self.live_classes
    
    def get_live_class_by_name(self, class_name):
        """
        Get a live class by name
        """
        return self.live_classes.get(class_name)
    
    def get_live_instances(self, class_name):
        """
        Get all instances of a live class
        """
        cls = self.get_live_class_by_name(class_name)
        if cls:
            return getattr(cls, "_instances", [])
        return None
    
    def get_all_instances(self):
        """
        Get all live instances
        """
        return self.live_instances
    
    def get_live_instance_by_name(self, instance_name):
        """
        Get a live class instance by name
        """
        if instance_name in self.live_instances:
            return self.live_instances[instance_name]
        else:
            logger.warning(f"WARNING: Instance '{instance_name}' does not exist")
            return None
        
    def get_live_instance_attr_by_name(self, instance, attr_name):
        """
        Get an attribute of a live instance by name
        """
        if instance is not None:
            attr = getattr(instance, attr_name, None)
            if not hasattr(instance, attr_name):
                logger.warning(f"WARNING: Attribute '{attr_name}' does not exist on '{instance}'")
            return attr
        
    
    def set_live_instance_attr_by_name(self, instance_name, attr_name, value):
        """
        Set an attribute of a live instance.
        Type is parsed from the input string.
        """
        instance = self.get_live_instance_by_name(instance_name)
        if instance is None: return
        attr = self.get_live_instance_attr_by_name(instance, attr_name)
        if attr is None: return
        value = TypeChecker.handle_type(instance, attr_name, value)
        if value is not None:            
            try:
                setattr(instance, attr_name, value)
            except Exception as e:
                logger.warning(f"WARNING: Failed to update: {e}. Reverting to previous value.")
        return
    