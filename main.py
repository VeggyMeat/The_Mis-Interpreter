import sys

class ExecutionController:
    def __init__(self):
        self.file = sys.argv[0]

    def run_program(self) -> None:
        ...
    
    def take_inputs(self) -> list[int]:
        ...

if __name__ == "__main__":
    controller = ExecutionController()
    controller.run_program()
