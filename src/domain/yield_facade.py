from configs.components import Text
from models.yields import Operations, Tax
from configs.yield_types import YieldType
from services.yields import YieldService

class YieldFacade:
    def __init__(self, base_yields):
        self._base_yields = base_yields

    def _get_tax_by_maturity(self, days):
        if days <= Tax.semester_range:
            return Tax.semester_yield
        elif days <= Tax.anual_range:
            return Tax.anual_yield
        elif days <= Tax.bianual_range:
            return Tax.bianual_yield
        return Tax.beyond_yield

    def _set_tax_adjusted(self, value, tax):
        return round(value * (Operations.factor_base - tax), Operations.round_value)

    def calculate(self, bond_type_label, yield_input, maturity_days, tax_free=False):
        bond_type = YieldType.from_label(bond_type_label)
        if not bond_type:
            raise ValueError(Text.invalid_bond_type_message)

        yield_service = YieldService(
            base_yields=self._base_yields,
            yield_input=yield_input,
            bond_type=bond_type
        )

        raw_yield = yield_service.compound_yield()
        tax = self._get_tax_by_maturity(maturity_days)

        if tax_free:
            gross_yield = self._set_tax_adjusted(value=raw_yield, tax=-tax)
            net_yield = self._set_tax_adjusted(value=raw_yield, tax=Tax.free_tax)
        else:
            gross_yield = raw_yield
            net_yield = self._set_tax_adjusted(gross_yield, tax)

        return gross_yield, net_yield
