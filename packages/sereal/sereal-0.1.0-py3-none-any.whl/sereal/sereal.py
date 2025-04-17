from typing import Dict, Any, Type, List, TypeVar
from abc import ABC, abstractmethod
from types import NoneType
import inspect


class Serializable(ABC):
    @classmethod
    @abstractmethod
    def serialize(cls, obj) -> Dict[str, Any]:
        """Convert the object into a dictionary."""
        pass

    @classmethod
    @abstractmethod
    def deserialize(cls, src: Dict[str, Any]) -> Any:
        """Convert the object into a dictionary."""
        pass


class Adapter(ABC):
    def __init__(self, adaptee: Type) -> None:
        """Initializes the adapter with an adaptee."""
        self.adaptee = adaptee


__registry__: Dict[str, type] = {}
__registry_hash_map__: Dict[type, str] = {}


def register(serializable: Type[Serializable] | Type[Adapter] | Adapter, suffix: str, force=False):
    cls = serializable
    if type(serializable) is Type[Adapter] and issubclass(serializable, Adapter):
        n = serializable.__new__(serializable)
        init_args = inspect.signature(serializable.__init__).parameters
        if len(init_args) == 1:
            n.__init__()
        serializable = n
    if isinstance(serializable, Adapter):
        print(serializable)
        print(serializable.__dict__)
        cls = serializable.adaptee
    if not force and cls in __registry__.keys():
        raise Exception("Serializable for this class already exists.\nYou might be using an Adapter try force=True.")
    __registry_hash_map__[cls] = suffix
    __registry__[cls.__name__ + ":" + suffix] = serializable


base_types: List[Type] = [int, float, bool, str]


def serialize(obj: Any, typed=True):
    t: Type = type(obj)
    if t == NoneType:
        return {"type": t.__name__, "value": "null"} if typed else "null"
    if t in base_types:
        return {"type": t.__name__, "value": ("true" if obj else "false") if t == bool else str(obj)} if typed else (("true" if obj else "false") if t == bool else str(obj))
    elif issubclass(t, dict):
        return {"type": f"dict", "value": {str(serialize(key, typed=False)): serialize(value) for key, value in obj.items()}} if typed else {str(serialize(key, typed=False)): serialize(value) for key, value in obj.items()}
    elif issubclass(t, list) or issubclass(t, set) or issubclass(t, tuple):
        return {"type": str(t.__name__), "value": [serialize(value) for value in obj]} if typed else [serialize(value) for value in obj]
    if t.__name__ + ":" + __registry_hash_map__[t] in __registry__.keys():
        return {"type": f"cls.{t.__name__}:{__registry_hash_map__[t]}", "value": {key: serialize(value) for key, value in __registry__[t.__name__ + ":" + __registry_hash_map__[t]].serialize(obj).items()}} if typed else {key: serialize(value) for key, value in __registry__[t].serialize(obj).items()}
    raise Exception(f"Unable to serialize {obj}:{type(obj)}.")


def get_type(name: str) -> type:
    t: type
    if name == "none":
        t = NoneType
    if name == "int":
        t = int
    elif name == "float":
        t = float
    elif name == "bool":
        t = bool
    elif name == "str":
        t = str
    elif name.startswith("dict"):
        t = dict
    elif name.startswith("list"):
        t = list
    elif name.startswith("tuple"):
        t = tuple
    elif name.startswith("set"):
        t = set
    elif name.startswith("cls."):
        t = __registry__[name.removeprefix("cls.")]
    else:
        raise ValueError(f"Unknown type name: {name}")
    return t


def deserialize(source: Dict[str, Any], typed=True):
    if typed:
        t: type = get_type(source["type"])
        val = source["value"]
        if t == NoneType:
            return None
        if t == int:
            return int(val)
        elif t == float:
            return float(val)
        elif t == str:
            return val
        elif t == bool:
            return True if val == "true" else False
        elif t == dict:
            return {key: deserialize(value) for key, value in val.items()}
        elif t == list:
            return [deserialize(value) for value in val]
        elif t == tuple:
            return (deserialize(value) for value in val)
        elif t == set:
            return {deserialize(value) for value in val}
        if isinstance(t, Serializable):
            return t.deserialize(val)
    else:
        raise Exception("Untyped deserialization is not supported.")
