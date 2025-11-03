# The Mis-Interpreter

### 2nd place CamHack '25 project

Theme: Unintended Behavior

Created by The Misinterpreters: Archie Macrae, Rohan Wadhawan, and Samuel Latimer

This program accepts code in the C programming language and transpiles it into various high-level languages and games. These include:
```
Python
Scratch
Excel
Mindustry
Minecraft
```

At the moment, the program implements the following constructs:
- Addition, subtraction and multiplication with integer values
- If and else statements (else statements may be null) using standard comparisons (>, <, !=, ==)
- Inputs and outputs

Repo structure:
- `examples` contains example C programs we use as input
- `programs` contains the code for parsing C code into an AST
- `transpilers` contains the transpilers for each platform we convert to
- `main.py` is the Mis-Interpreter, taking in a C program and its arguments, and running the transpilers for each platform
