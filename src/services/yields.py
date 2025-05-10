from configs.components import Text
from configs.yield_types import YieldType
from models.yields import Operations

class YieldService:
    def __init__(self, base_yields: dict, yield_input: str, bond_type: YieldType):
        self._base_yields = base_yields
        self._yield_input = self._sanitize_yield(yield_input)
        self._bond_type = bond_type

    def _sanitize_yield(self, value):
        return float(str(value).replace(",", "."))

    def compound_yield(self):
        strategy = {
            YieldType.PRE_FIXED: lambda: self._yield_input,
            YieldType.POST_FIXED: lambda: (
                self._yield_input / Operations.percent_value
            ) * self._base_yields[YieldType.CDI.base_key()],
            YieldType.CDI: lambda: self._yield_input + self._base_yields.get(self._bond_type.base_key()),
            YieldType.SELIC: lambda: self._yield_input + self._base_yields.get(self._bond_type.base_key()),
            YieldType.INFLATION: lambda: self._yield_input + self._base_yields.get(self._bond_type.base_key()),
        }.get(self._bond_type)

        if strategy is None:
            raise ValueError(Text.invalid_bond_type_message)

        return strategy()
