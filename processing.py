from math import sqrt
from scipy.stats import norm


class Processor:
    def __init__(self, data: str) -> None:
        self.init_data = data
        self.variations_list = self._parse_init_data()
        self.variations_dict = self.to_dict()

    def _parse_init_data(self) -> list:
        data = self.init_data

        lst = [item.split(":") for item in data.split(";")]
        for i, l in enumerate(lst):
            lst[i] = [int(item) for item in l]
        return lst

    def to_dict(self) -> dict:
        var_list = self.variations_list.copy()
        variations = [
            {"size": item[0], "conv": item[1], "cr": item[1] / item[0]}
            for item in var_list
        ]

        for v in variations:
            rate = v["cr"]
            v["std"] = sqrt(rate * (1 - rate) / v["size"])
        control = variations[0]
        for v in variations[1:]:
            v["z"] = (v["cr"] - control["cr"]) / sqrt(
                control["std"] ** 2 + v["std"] ** 2
            )
            v["p"] = norm().sf(v["z"])


        return {"variations": variations}
