class Terminal:
    def __init__(self) -> None:
        self.x = None
        self.y = None
        self.label = None

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Terminal) and o.label == self.label:
            return True
        else:
            return False
