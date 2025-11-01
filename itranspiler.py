
class ITranspiler:
    def __init__(self, source_code: str):
        self.source_code = source_code

    def transpile(self) -> None:
        ...
