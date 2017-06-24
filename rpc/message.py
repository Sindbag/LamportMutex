import json


class Message:
    REQUEST = 'l'
    RELEASE = 'u'
    REPLY = 'a'

    def __init__(self, type=None, from_=None, to=None, time=None):
        self.from_ = from_
        self.to = to
        self.type = type
        self.time = time

    @classmethod
    def from_data(cls, data):
        instance = cls()
        instance.load(data)
        return instance

    def __lt__(self, other):
        return self.time < other.time

    def __repr__(self):
        return str(self.time)

    def __str__(self):
        return self.dump().decode('utf-8')

    def dump(self):
        return json.dumps({
            'from_': self.from_,
            'to': self.to,
            'type': self.type,
            'time': self.time
        }).encode('utf-8')

    def load(self, raw):
        data = json.loads(raw.decode('utf-8'))
        for k, v in data.items():
            setattr(self, k, v)


if __name__ == "__main__":
    msg1, msg2 = Message(), Message()
    dump = msg1.dump()
    msg2.load(dump)
