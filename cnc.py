from MachineClient import MachineClient
import re

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
        if c.isspace():
            self.pos += 1
            return self.get_next_token()
        if c.isdigit() or c == '.':
            return self.get_number()
        elif c == 'N':
            # optional line number
            return self.get_line_number()
        elif c == 'G':
            return self.get_gcode()
        elif c == "X" or c == "Y" or c == "Z" or c == "F":
            # get coordinates
            return self.get_coordinates()
        if c.isalpha():
            return self.get_keyword()
        self.pos += 1
        return Token(c, c)

    def get_number(self):
        start = self.pos
        while self.pos < len(self.text) and (self.text[self.pos].isdigit() or self.text[self.pos] == '.'):
            self.pos += 1
        return Token('NUMBER', float(self.text[start:self.pos]))
    
    def get_line_number(self):
        # only the next letter is a number
        if self.text[self.pos+1].isdigit():
            start = self.pos+1
            self.pos += 2
            while self.pos < len(self.text) and self.text[self.pos].isdigit():
                self.pos += 1
            print("Line number: " + self.text[start:self.pos])
            return Token('LINE_NUMBER', int(self.text[start:self.pos]))
        else:
            return Token(None, None)

    def get_keyword(self):
        start = self.pos+1
        self.pos += 1
        while self.pos < len(self.text) and self.text[self.pos] != ' ':
            self.pos += 1
        return Token('KEYWORD', self.text[start:self.pos])

    def get_gcode(self):
        # get letters until next space
        start = self.pos+1
        self.pos += 1
        while self.pos < len(self.text) and self.text[self.pos] != ' ':
            self.pos += 1
        return Token('GCODE', self.text[start:self.pos])
    
    def get_coordinates(self):
        # get letters until next space
        start = self.pos
        self.pos += 1
        while self.pos < len(self.text) and self.text[self.pos] != ' ':
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

class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.current_token = self.tokenizer.get_next_token()
        self.client = MachineClient()

    def parse(self):
        while self.current_token.type != None:
            if self.current_token.type == 'KEYWORD':
                self.eat('KEYWORD')
                # print("Keyword: " + self.current_token.value)

            elif self.current_token.type == 'GCODE':
                print("Gcode: " + self.current_token.value)
                match self.current_token.value:
                    case '00' | '0' | '91' | '90' | '17' | '18' | '19' | '20' | '21' | '28':
                        self.client.handle_gcode(self.current_token.value)
                    case '01' | '1':
                        # print("Gcode: " + self.current_token.value)
                        self.parse_move_command()

                    case default:
                        print("Unknown Gcode: " + self.current_token.value)

                self.eat('GCODE')
            elif self.current_token.type == 'NUMBER':
                self.parse_feed_rate_command()

            elif self.current_token.type not in ['COMMENT', 'LINE_NUMBER', 'PROGRAM_NUMBER']:
                self.error("Unknown token: {}".format(self.current_token.value))
            
            self.eat(self.current_token.type)
        
    def parse_move_command(self):
        # linear movement
        self.eat('GCODE')
        print("next token: " + self.current_token.value)
        x, y, z = self.parse_coordinate()
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

    def parse_change_tool_command(self):
        MachineClient.change_tool('T01')
    
    def parse_set_spindle_speed_command(self):
        MachineClient.set_spindle_speed(2000)

    def parse_spindle_on_command(self):
        MachineClient.spindle_on()
    
    def parse_spindle_off_command(self):
        MachineClient.spindle_off() 
    
    def parse_coolant_on_command(self):
        MachineClient.coolant_on()
    
    def parse_coolant_off_command(self):
        MachineClient.coolant_off()
    
    def parse_feed_rate_command(self):
        self.eat('NUMBER')
        print("Setting feed rate to {:.3f} [mm/min].".format(self.current_token.value))
    
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
        # print(text)
        tokenizer = Tokenizer(text)
        parser = Parser(tokenizer)
        parser.parse()
    
    
if __name__ == '__main__':
    # get command line argument for the file
    import sys
    if len(sys.argv) != 2:
        print("Usage: python cnc.py <file>")
        sys.exit(1)
    filename = sys.argv[1]
    interpreter = Interpreter(filename)
    interpreter.interpret()