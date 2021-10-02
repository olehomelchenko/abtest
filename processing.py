class Processor:
    def __init__(self, data: str) -> None:
        self.init_data = data

    def process_to_json(self) -> dict:
        data = self.init_data

        variations = [item.split(":") for item in data.split(";")]
        return variations