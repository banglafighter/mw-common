import dataclasses
import json
from collections import OrderedDict
from enum import Enum
import re
from typing import get_origin, get_args


class PropsModType(Enum):
    CAMEL_TO_SNAKE = "CAMEL_TO_SNAKE"
    SNAKE_TO_CAMEL = "SNAKE_TO_CAMEL"


class SDLize(object):
    _exclude_props_mod: dict = {}
    _props_mod_type: PropsModType = None
    _camel_to_snake_regex = re.compile(r"(?<!^)(?=[A-Z])")
    _include_null: bool = False

    def convert_snake_to_camel_case(self, text: str) -> str:
        camel_cased = "".join(x.capitalize() for x in text.lower().split("_"))
        if camel_cased:
            return camel_cased[0].lower() + camel_cased[1:]
        else:
            return camel_cased

    def convert_camel_to_snake_case(self, text: str) -> str:
        return self._camel_to_snake_regex.sub("_", text).lower()

    def _get_property_modifier(self):
        if not self._props_mod_type:
            return None
        elif self._props_mod_type == PropsModType.CAMEL_TO_SNAKE:
            return self.convert_camel_to_snake_case
        elif self._props_mod_type == PropsModType.SNAKE_TO_CAMEL:
            return self.convert_snake_to_camel_case
        return None

    def _load_data_class(cls, data: dict):
        if not dataclasses.is_dataclass(cls):
            raise ValueError(f"{cls.__name__} must be a dataclass")
        if not isinstance(data, dict):
            raise ValueError(f"Unable to load dictionary from {cls.__name__}")
        cls.set_deserialize_conf(cls)
        kwargs = cls._get_load_kwargs(cls, data=data)
        return cls(**kwargs)

    def _get_load_kwargs(cls, data: dict):
        property_modifier = cls._get_property_modifier(cls)
        field_name_type = {field.name: field.type for field in dataclasses.fields(cls)}
        kwargs = {}

        for key, value in data.items():
            if property_modifier and (not cls._exclude_props_mod or key not in cls._exclude_props_mod):
                key = property_modifier(cls, text=key)

            if key not in field_name_type:
                continue

            field_type = field_name_type[key]
            origin = get_origin(field_type)

            # list[...] or List[...]
            if isinstance(value, list) and origin is list:
                item_type = get_args(field_type)[0]
                if dataclasses.is_dataclass(item_type):
                    kwargs[key] = [
                        cls._load_data_class(item_type, item)
                        for item in value
                    ]
                else:
                    kwargs[key] = value

            # dict[...] or Dict[...]
            elif isinstance(value, dict) and origin is dict:
                _, value_type = get_args(field_type)
                if dataclasses.is_dataclass(value_type):
                    kwargs[key] = {
                        k: cls._load_data_class(value_type, v)
                        for k, v in value.items()
                    }
                else:
                    kwargs[key] = value

            # Nested SDLize object
            elif (
                    isinstance(value, dict)
                    and isinstance(field_type, type)
                    and issubclass(field_type, SDLize)
            ):
                kwargs[key] = cls._load_data_class(field_type, value)

            else:
                kwargs[key] = value

        return kwargs

    @classmethod
    def load_dict(cls, data: dict):
        return cls._load_data_class(cls, data=data)

    def _dict_factory(self, fields):
        dict_field = OrderedDict()
        property_modifier = self._get_property_modifier()
        for (key, value) in fields:
            if property_modifier and (not self._exclude_props_mod or key not in self._exclude_props_mod):
                key = property_modifier(text=key)
            if value is not None or self._include_null:
                dict_field[key] = value
        return dict_field

    def to_dict(self, include_null=False):
        self._include_null = include_null
        self.set_serialize_conf()
        return dataclasses.asdict(self, dict_factory=self._dict_factory)

    def to_json(self, include_null=False):
        data = self.to_dict(include_null=include_null)
        return json.dumps(data)

    def set_serialize_conf(self):
        pass

    def set_deserialize_conf(self):
        pass
