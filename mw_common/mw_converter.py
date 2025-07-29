from typing import Literal
from mw_common import Console

DataCastType = Literal["str", "int", "float", "bool", "list", "set", "tuple", "dict"]

class MwConverter:

    @classmethod
    def dynamic_cast(cls, value, cast_type: DataCastType):
        type_map = {
            "str": str,
            "int": int,
            "float": float,
            "bool": lambda v: str(v).lower() in ['true', '1', 'yes'],
            "list": lambda v: list(v) if isinstance(v, (str, list, set, tuple)) else [v],
            "set": lambda v: set(v) if isinstance(v, (str, list, set, tuple)) else {v},
            "dict": lambda v: eval(v) if isinstance(v, str) and v.strip().startswith("{") else {},
        }

        try:
            cast_func = type_map.get(cast_type.lower())
            if not cast_func:
                raise ValueError(f"Unsupported target type: {cast_type}")
            return cast_func(value)
        except Exception as e:
            Console.log(f"Conversion error: {e}")
            return None

