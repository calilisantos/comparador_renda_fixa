from enum import Enum
from configs.components import Text


class YieldType(Enum):
    PRE_FIXED = "pre_fixed"
    POST_FIXED = "post_fixed"
    CDI = "cdi"
    SELIC = "selic"
    INFLATION = "inflation"

    @classmethod
    def label_map(cls):
        return {
            cls.PRE_FIXED: Text.pre_fixed_option_label,
            cls.POST_FIXED: Text.post_fixed_option_label,
            cls.CDI: Text.cdi_option_label,
            cls.SELIC: Text.selic_option_label,
            cls.INFLATION: Text.inflation_option_label,
        }

    @classmethod
    def from_label(cls, label: str):
        reversed_map = {value: key for key, value in cls.label_map().items()}
        return reversed_map.get(label)

    @classmethod
    def to_label(cls, yield_type):
        return cls.label_map().get(yield_type)

    @classmethod
    def choices(cls):
        return list(cls.label_map().values())

    def base_key(self):
        base_keys = {
            YieldType.CDI: "CDI",
            YieldType.SELIC: "SELIC",
            YieldType.INFLATION: "INFLATION",
        }
        return base_keys.get(self)
