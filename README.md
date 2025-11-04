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

## Technical Overview

We wrote all of our code in one python project. We load in the C file, and start by cleaning it by removing any whitespace, and separating based on instructions. We then replace the C inputs with the inputs passed into the program and convert it into a recursive data structure modelling variable, values, expressions, conditions and outputs. This is done by turning the code into a recursive list structure storing lines of code by what they contain, which is then passed into a main converter which repeatedly breaks the code down into different blocks. Expressions are similarly passed looking at operator precedent.

The final structure is then passed into each of our five transpires. 
Python: Opens the python app and then a transpiler that wrote the corresponding python line for each expression / part.

Scratch: The Scratch transpiler relies on moving the mouse to specific coordinates on the screen to build up our program. The _get_variable and _get_block methods use hard-coded screen coordinates to fetch the relevant block from the Scratch sidebar, then place it at the requested location. The _parse_code_block method builds up the program from top to bottom, keeping track of the location of the last command using the pixel heights of each block (and width, in the case of if/else statements). When we want to use expressions (e.g. for variable assignment or conditions), we first build them up in a separate area with the _parse_expression method, then move them into position. Expressions can be highly recursive: we create the right hand side first (by building it below the parent expression), then move it into the parent, then do the same for left hand side. If instead we did the left hand side first, we'd need to account for the growing width of the expression as we add more values. When we want to add a literal value to an expression, unfortunately Scratch does not provide a block that is just a number, so instead we use an "add" block with one operand empty (which is why the final program generated has lots of empty operands!). This means we don't need special cases in our code to account for literals, and can treat them like any other block.

Excel: Opens the excel app and uses an API to dynamically fill the cells with some values to explain each command. Behind the scenes creates an excel command that takes a RUN value and propagates it through the cells in order to determine the flow of execution. Variables are stored as values in cells, using the lookup command to find the most recent change to the variable.
Mindustry: Mindustry has an assembly-like programming language in it, where programs can be loaded in via the clipboard. Then transpiles this coding language (having to keep in mind line numbers in order to translate if statements into jumps) and saves it to the clipboard. Mouse controls on the computer then open it and paste it in.
Minecraft: Translating each part of an expression into a temporary person’s value on a scoreboard in Minecraft. Conditions are done with Minecraft execute commands which can check a player’s scoreboard value to see if it matches some condition in order to run the line or not.

The program then propagates back down the layer running the program, and displaying the output (using a library to minimise the applications and clean up as they shut)
