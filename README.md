# GCode Interpreter

This is a GCode Interpreter which can parse basic GCode commands and print a response using stub methods to simulate machine actions.

## Installation

To run this project, make sure you have Python 3.10 or higher installed on your system.

1. Clone this repository using `git clone https://github.com/FirePlank/G-Code-Interpreter.git`.
2. Go to the project directory using `cd G-Code-Interpreter`.
3. Run the project using `python cnc.py <filename.gcode>` in the terminal.

## Note

This interpreter is not designed to handle all the GCode commands. Adding more commands is fairly easy, and the code is structured in such a way that it will be easy to extend the functionality if needed. The commands are handled using match statements for clarity and readability, so make sure you have Python version 3.10 or higher if you intend to run the software.