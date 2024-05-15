class CallbackData:
    cb_processor: str
    cb_type: str
    word: str | None

    TEMPLATE = ","

    def __init__(self, cb_processor: str, cb_type: str, word: str = None):
        self.cb_processor = cb_processor
        self.cb_type = cb_type
        self.word = word

    def to_string(self) -> str:
        fields = [self.cb_processor, self.cb_type, self.word]
        filled_fields = [
            field if field is not None else "_" for field in fields
        ]
        template = self.TEMPLATE.join(["{}"] * len(filled_fields))
        return template.format(*filled_fields)

    def from_string(string: str):
        parts = [
            part.strip() if part != "_" else None
            for part in string.split(CallbackData.TEMPLATE)
        ]
        cb_processor, cb_type, word = parts
        return CallbackData(cb_processor, cb_type, word)
