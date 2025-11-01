import sys

class ExecutionController:
    def __init__(self):
        self.file = sys.argv[0]

    def runProgram(self) -> None:
        ...
    
    def takeInputs(self) -> list[int]:
        ...

if __name__ == "__main__":
    controller = ExecutionController()
    controller.runProgram()
