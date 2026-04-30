class ShortTermMemory:
    def __init__(self):
        self.data = []

    def add(self, item):
        self.data.append(item)

    def get(self):
        return self.data
