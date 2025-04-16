from ast import literal_eval
from rich_argparse import RichHelpFormatter
from argparse import ArgumentParser
from functools import partial


class Field:
    def __init__(self, type_, default=None, required=False, help="", freeze=False, alias=None):
        self.type_ = type_
        self.default = default
        self.data = default
        self.required = required
        self.help = help
        self.freeze = freeze
        self._init_alias(alias)

    def _init_alias(self, alias):
        if alias is None:
            self.alias = []
        elif type(alias) == str:
            self.alias = [alias]
        else:
            self.alias = alias
    
    def __get__(self, instance, owner):
        return self.data
    
    def set_value(self, value):
        if not isinstance(value, self.type_):
            raise ValueError(f"Expecting {self.type_}, got {type(value)}")
        self.data = value
    
    def as_args_kwargs(self):
        args = self.alias
        kwargs = dict(
            default=self.default, required=self.required, help=self.help,
        )
        if self.type_ == bool:
            kwargs["action"] = "store_false" if self.default else "store_true"
        elif self.type_ in [list, tuple]:
            kwargs["type"] = lambda value: literal_eval(value)
            kwargs["metavar"] = self.type_.__name__
        elif hasattr(self.type_, '_name'):
            kwargs['type'] = lambda value: literal_eval(value)
            kwargs['metavar'] = self.type_._name
        else:
            kwargs['type'] = self.type_
            kwargs['metavar'] = self.type_.__name__
        return args, kwargs
    
class Meta(type):
    def __setattr__(cls, name, value):
        if name in cls.__dict__:
            attr = cls.__dict__[name]
            if isinstance(attr, Field):
                attr.set_value(value)
            else:
                super().__setattr__(name, value)
        else:
            raise AttributeError(f"Cannot set new attribute {name} on {cls.__class__.__name__}")

class Configure(metaclass=Meta):

    @classmethod
    def as_dict(cls):
        dict_to_return = {}
        for attr_name, value in cls.__dict__.items():
            if isinstance(value, Field):
                dict_to_return[attr_name] = value.data
            elif isinstance(value, type) and issubclass(value, Configure):
                dict_to_return[attr_name] = value.as_dict()
        return dict_to_return

    @classmethod
    def as_json(cls):
        import json
        return json.dumps(cls.as_dict(), indent=2)
    
    @classmethod
    def _parse_sys_args(cls, parser: ArgumentParser):
        parser.description = cls.__doc__
        prefix = f"{parser.title}." if hasattr(parser, "title") else ""
        for attr_name, value in cls.__dict__.items():
            if isinstance(value, Field) and not value.freeze:
                args, kwargs = value.as_args_kwargs()
                parser.add_argument(f"--{prefix}{attr_name}", *args, **kwargs)
            elif isinstance(value, type) and issubclass(value, Configure):
                group = parser.add_argument_group(title=prefix + value.__name__)
                group = value._parse_sys_args(group)
        return parser
    
    @classmethod
    def _extract_sys_args(cls, parser: ArgumentParser):
        args = parser.parse_args()
        for key, value in vars(args).items():
            *namespaces, attr_name = key.split(".")
            cls_temp = cls
            for cls_name in namespaces:
                cls_temp = getattr(cls_temp, cls_name)
            cls_temp.__dict__[attr_name].set_value(value)

    @classmethod
    def parse_sys_args(cls):
        parser = ArgumentParser(formatter_class=partial(RichHelpFormatter, max_help_position=80))
        cls._extract_sys_args(cls._parse_sys_args(parser))

    @classmethod
    def update(cls, name, value):
        cls.__dict__[name].set_value(value)
