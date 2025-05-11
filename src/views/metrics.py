from models.yields import Operations


class MetricBuilder:
    @staticmethod
    def build_comparison(column, base_value, compared_value, label):
        delta = round(
            ((compared_value - base_value) / base_value) * Operations.percent_value,
            Operations.round_value
        )
        return column.metric(
            border=True,
            delta=f"{delta}%",
            label=label,
            value=f"{base_value}%"
        )

    @staticmethod
    def build_index(column, index_yield, compared_value, label, suffix=""):
        value = round(compared_value - index_yield, Operations.round_value)
        return column.metric(
            border=True,
            label=label,
            value=f"{value}%+{suffix}"
        )
