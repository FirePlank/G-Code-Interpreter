from MachineClient import MachineClient
import re
import sys

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Tokenizer:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def get_next_token(self):
        if self.pos >= len(self.text):
            return Token(None, None)

        c = self.text[self.pos]
        
        if self.pos == 0:
            return self.get_program_number()
        elif c.isspace():
            self.pos += 1
            return self.get_next_token()

        match c:
            case 'G':
                # get gcode
                return self.get_token('GCODE')
            case 'M':
                # get mcode
                return self.get_token('MCODE')
            case 'T':
                # get tool number
                return self.get_token('TOOL_NUMBER')
            case 'S':
                # get spindle speed
                return self.get_token('SPINDLE_SPEED')
            case 'F':
                # get feed rate
                return self.get_token('FEED_RATE')
            case 'X' | 'Y' | 'Z':
                # get coordinates
                return self.get_coordinates()

        if c.isalpha():
            return self.get_keyword()

        self.pos += 1
        return Token(c, c)

    def get_token(self, code):
        # get letters until next space
        start = self.pos+1
        self.pos += 1
        while self.pos < len(self.text) and self.text[self.pos] != ' ' and self.text[self.pos] != '\n':
            self.pos += 1

        return Token(code, self.text[start:self.pos])
    
    def get_coordinates(self):
        # get letters until next space
        start = self.pos
        self.pos += 1
        while self.pos < len(self.text) and self.text[self.pos] != ' ' and self.text[self.pos] != '\n':
            self.pos += 1

        return Token('COORDINATE', self.text[start:self.pos])
    
    def get_program_number(self):
        start = self.pos+1
        self.pos += 1
        while self.pos < len(self.text) and self.text[self.pos].isdigit():
            self.pos += 1
        
        if self.pos == start:
            raise Exception("Syntax error: Program number expected.")

        print("Program number: " + self.text[start:self.pos])

        return Token('PROGRAM_NUMBER', int(self.text[start:self.pos]))
    
    def get_keyword(self):
        start = self.pos
        while self.pos < len(self.text) and self.text[self.pos].isalpha():
            self.pos += 1

        return Token('KEYWORD', self.text[start:self.pos])

class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.current_token = self.tokenizer.get_next_token()
        self.client = MachineClient()

    def parse(self):
        while self.current_token.type != None:
            match self.current_token.type:
                case 'GCODE':
                    print("Gcode: " + self.current_token.value)
                    match self.current_token.value:
                        case '01' | '1':
                            self.parse_move_command()

                        case default:
                            self.client.handle_gcode(self.current_token.value)

                case 'MCODE':
                    print("Mcode: " + self.current_token.value)
                    self.client.handle_mcode(self.current_token.value)

                case 'SPINDLE_SPEED':
                    self.client.set_spindle_speed(self.current_token.value)
                
                case 'FEED_RATE':
                    self.client.set_feed_rate(self.current_token.value)
                                            
                case 'TOOL_NUMBER':
                    self.client.change_tool(self.current_token.value)
                
                case 'COORDINATE':
                    self.parse_move_command()
                    continue
                
                case 'KEYWORD' | 'PROGRAM_NUMBER':
                    self.eat(self.current_token.type)
                
                case default:
                    self.error("Unknown token: {}".format(self.current_token.value))
                
            self.eat(self.current_token.type)
        
    def parse_move_command(self):
        # linear movement
        x, y, z = self.parse_coordinate()
        # if 2 axes are None but 1 is not, move in that axis through functions move_x, move_y, move_z
        if x == None and y == None and z != None:
            self.client.move_z(z)
        elif x == None and y != None and z == None:
            self.client.move_y(y)
        elif x != None and y == None and z == None:
            self.client.move_x(x)
        else:
            self.client.move(x, y, z)

    def parse_coordinate(self):
        x = y = z = None
        while self.current_token.type == 'COORDINATE':
            if self.current_token.value[0] == 'X':
                x = self.current_token.value[1:]
            elif self.current_token.value[0] == 'Y':
                y = self.current_token.value[1:]
            elif self.current_token.value[0] == 'Z':
                z = self.current_token.value[1:]
            
            self.eat('COORDINATE')

        return x, y, z
    
    def eat(self, token_type):
        """ Compare the current token type with the passed token """
        if self.current_token.type == token_type:
            self.current_token = self.tokenizer.get_next_token()
        else:
            self.error("Expected token of type {}.".format(token_type))
    
    def error(self, message=""):
        raise Exception("An Error occured while parsing: {}".format(message))

class Interpreter:
    def __init__(self, filename):
        self.filename = filename

    def interpret(self):
        with open(self.filename, 'r') as f:
            text = f.read()

        # set text to start at % and end at %
        text = text[text.find('%')+2:text.rfind('%')-1]
        # regex to remove all comments and the new lines that follow
        text = re.sub(r'\(.*?\)\s*', '', text)
        # regex to remove optional line numbers at start of line (e.g. N10)
        text = re.sub(r'^N\d+\s*', '', text, flags=re.MULTILINE)

        # initialize tokenizer and parser
        tokenizer = Tokenizer(text)
        parser = Parser(tokenizer)
        # start parsing
        parser.parse()
    
    
if __name__ == '__main__':
    # get command line argument for the file
    if len(sys.argv) != 2:
        print("Usage: python cnc.py <file>")
        sys.exit(1)

    # get filename from command line argument
    filename = sys.argv[1]
    interpreter = Interpreter(filename)
    interpreter.interpret()