from transpilers.transpiler import ITranspiler

import keyboard
import mouse
import subprocess

class Scratch(ITranspiler):
    def transpile(self) -> None:
        subprocess.Popen(r'C:\Program Files\WindowsApps\ScratchFoundation.ScratchDesktop_3.31.1.0_x64__wmbdy4q6dbx4t\Scratch 3.exe')


if __name__ == "__main__":
    scratch = Scratch(None)
    scratch.transpile()