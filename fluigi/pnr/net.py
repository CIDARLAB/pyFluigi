class Net:
    def __init__(self, ID, source, sinks) -> None:
        self.ID = ID
        self.source = source
        self.sinks = sinks

    def __hash__(self):
        return hash(self.ID)

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Net) and o.ID == self.ID:
            return True
        else:
            return False
