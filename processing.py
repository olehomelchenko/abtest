from math import sqrt


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

    def _add_std(self, variations):
        for v in variations:
            rate = v["cr"]
            v["std"] = sqrt(rate * (1 - rate) / v["size"])

    def to_dict(self) -> dict:
        var_list = self.variations_list.copy()
        cb = var_list.pop(0)
        control_dict = {"size": cb[0], "conv": cb[1], "cr": cb[1] / cb[0]}
        variations = [
            {"size": item[0], "conv": item[1], "cr": item[1] / item[0]}
            for item in var_list
        ]

        self._add_std(variations)

        return {"control": control_dict, "variations": variations}
