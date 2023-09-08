class objects_list(list):
    def __init__(self):
        self.data = []

    def append(self, value):
        self.data.append(value)

    def get(self, index):
        return self.data[index]

    def size(self):
        return len(self.data)