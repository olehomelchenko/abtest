class Processor:
    def __init__(self, data: str) -> None:
        self.init_data = data

    def parse_init_data(self) -> dict:
        data = self.init_data

        self.variations_list = [item.split(":") for item in data.split(";")]
