import random
from timeit import default_timer as timer
import string
from typing import Any
import rpyc


def get_n_random_chars(n: int) -> str:
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))


class RemoteProcedureCall:
    def __init__(self, connection: Any) -> None:
        self.data: str = ''
        self.conn: Any = connection

    def read_operation(self) -> None:
        print(f'Read data:\n{self.conn.root.read()}')

    def write_operation(self, n: int) -> None:
        self.data = get_n_random_chars(n)
        print(f'Write data:\n{self.conn.root.write(self.data)}')

    def modify_operation(self, start_index: int, n: int) -> None:
        # Make the size of the sent data consistent
        self.data = get_n_random_chars(n * 2)
        print(
            f'Modify data:\n{self.conn.root.modify(self.data, start_index, n)}'
        )


if __name__ == "__main__":
    total_time = 0
    cycles = 100
    string_len = 100
    print('RPC client started!')
    conn = rpyc.connect("13.87.134.248", 18861)
    rpc = RemoteProcedureCall(connection=conn)
    # print(rpc.read_operation())
    for i in range(cycles):
        start_time = timer()
        # rpc.read_operation()
        # rpc.write_operation(string_len)
        rpc.modify_operation(start_index=random.randint(0, string_len),
                             n=int(string_len/2))
        end_time = timer()
        elapsed_time = end_time - start_time
        print(f'{elapsed_time} seconds')
        total_time += elapsed_time

    print(f'Average time: {total_time / cycles}')
