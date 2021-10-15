import rpyc
from rpyc.utils.server import ThreadedServer


class MyService(rpyc.Service):
    def __init__(self):
        self.data = '00000I am the server, this is a 100-byte string. I am the server,' \
                    ' this is a 100-byte string. I000000'
        print(f'Server initialized data:\n{self.data}')

    def exposed_read(self) -> str:
        print(f'Read data:\n{self.data}')
        return self.data

    def exposed_write(self, client_data: str) -> str:
        self.data = client_data
        print(f'Write data:\n{self.data}')
        return self.data

    def exposed_modify(self, client_data: str, start_index: int,
                       n: int) -> str:
        if n > 100:
            return ''
        for i in range(100):
            tmp = self.data[0:start_index] + client_data[0:n] + self.data[start_index + n:len(self.data)]
        self.data = tmp
        print(f'Modify data:\n{self.data}')
        return self.data


if __name__ == "__main__":
    print('RPC server started!')
    t = ThreadedServer(MyService, port=18861)
    t.start()
