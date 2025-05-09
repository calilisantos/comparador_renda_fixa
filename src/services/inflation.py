from models.inflation import InflationTypes


class InflationService:
    def __init__(self, yields, index_type=InflationTypes.DEFAULT):
        self.__index_type = index_type
        self.__yields = yields
    
    def resolve_yield(self):
        return self.__yields.get(self.__index_type)
