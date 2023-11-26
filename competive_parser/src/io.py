import sys
from typing import Optional, Union, List

class IO:
    def __init__(self, input: Optional[str] = sys.stdin, output: Optional[str] = sys.stdout):
        self.input = open(input) if isinstance(input, str) else input
        self.output = open(output, 'w') if isinstance(output, str) else output 
    
    def __del__(self):
        self.input.close()
        self.output.close()

    def __call__(self, *items):
        if len(items) == 1:
            items = items[0]

        if isinstance(items, (list, tuple)):
            if isinstance(items[0], (list, tuple)):
                for item in items:
                    print(*item, file=self.output)
            else:
                print(*items, file=self.output)
        else:
            print(items, file=self.output)
                
    
    def __getitem__(self, item: Union[type, List[Union[type, int, str]]]):
        if isinstance(item, type):
            return self._read_single(item)

        if all(map(lambda i: isinstance(i, type), item)):
            return self._read_list(item)
        
        type_, count = item

        if isinstance(type_, type):
            item = [type_] * count
            return self._read_list(item)
        
        if isinstance(type_, list):
            type_, count = item
            return [self[type_] for _ in range(count)]
        
        raise Exception("Invalid argument pattern")
            

    def _read_single(self, type_):
        return type_(self.input.readline().strip())

    def _read_list(self, types):
        return [type_(val) for type_, val in zip(types, self.input.readline().strip().split())]


if __name__ == "__main__":

    # Here we specify io files (defaults to stdin/stdout)
    IO = IO('input.txt', 'output.txt')

    T = IO[int] # Read single int on single line
    IO(T) # Output single number on new line

    for _ in range(T):
        N, D = IO[int, int] # Read 2 ints on single line
        R = IO[int, N] # Read N ints on single line
        KD = IO[[int, int], N-1] # Read 2 ints each on new line N-1 number of times

        IO(N, D) # Outputs 2 numbers on single line
        IO(R) # Outputs list of numbers
        IO(KD) # Outputs 2d list of numbers (each inner has new line)

