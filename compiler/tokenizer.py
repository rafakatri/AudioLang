class Token:
    def __init__(self):
        self.type = ""
        self.value = 0


class Tokenizer:
    def __init__(self, source : str):
        self.source = source
        self.position = 0
        self.next = None

    def select_next(self):
        token = Token()

        if self.position == len(self.source):
            token.type = "EOF"
            token.value = 0
            self.next = token
            return
        
        current = self.source[self.position]

        while current == " " or current == "\t":
            self.position += 1
            current = self.source[self.position]
        
        if current.isdigit():
            token.type = "INT"
            val = ""
            while True:
                if self.position == len(self.source):
                    token.value += int(val)
                    break
                current = self.source[self.position]
                if current.isdigit():
                    val += current
                    self.position += 1
                elif current == " ":
                    self.position += 1
                else:
                    token.value += int(val)
                    break
        
        elif current == "+":
            token.type = "PLUS"
            token.value = 0
            self.position += 1

        elif current == '-':
            token.type = "MINUS"
            token.value = 0
            self.position += 1

        elif current == '*':
            token.type = "MULT"
            token.value = 0
            self.position += 1

        elif current == '/':
            token.type = "DIV"
            token.value = 0
            self.position += 1

        elif current == '(':
            token.type = "PAR_OP"
            token.value = 0
            self.position += 1

        elif current == ')':
            token.type = "PAR_CL"
            token.value = 0
            self.position += 1

        elif current == '=':
            token.type = "ASSIGN"
            token.value = 0
            self.position += 1

        elif current == "\n":
            token.type = "ENDL"
            token.value = 0
            self.position += 1

        elif current == '>':
            token.type = "GREATER"
            token.value = 0
            self.position += 1

        elif current == '<':
            token.type = "LESSER"
            token.value = 0
            self.position += 1

        elif current == '.':
            token.type = "DOT"
            token.value = 0
            self.position += 1

        elif current == ',':
            token.type = "COMMA"
            token.value = 0
            self.position += 1

        elif current == ';':
            token.type = "END"
            token.value = 0
            self.position += 1

        elif current == '{':
            token.type = "BR_OP"
            token.value = 0
            self.position += 1

        elif current == '}':
            token.type = "BR_CL"
            token.value = 0
            self.position += 1

        elif current == '"':
            self.position += 1
            value = ''

            while self.position < len(self.source) and (self.source[self.position] != '"'):
                value += self.source[self.position]
                self.position += 1

            if self.source[self.position] != '"':
                raise Exception("String Error")
            
            self.position += 1

            token.type = "STRING"
            token.value = value

        elif current.isalpha() or current == "_":
            value = ""

            reserved_words = ['print', 'while', 'output', 'play', 'from', 'to', 'rcut', 'lcut', 'insert', 'at', 'source', 'int', 'or', 'and', 'read', 'not', 'if', 'else']

            while self.position < len(self.source) and (self.source[self.position].isalpha() or self.source[self.position].isdigit() or self.source[self.position] == "_"):
                value += self.source[self.position]
                self.position += 1

            if value in reserved_words:
                token.type = value.upper()
                token.value = 0

            else:
                token.type = "IDENTIFIER"
                token.value = value
        self.next = token