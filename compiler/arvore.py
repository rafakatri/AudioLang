from symbol_table import Symbol_Table
from pydub import AudioSegment
from pydub.playback import play

class Node:
    
    def __init__(self, value, children, symbol_table, func_table):
        self.value = value
        self.children = children
        self.symbol = symbol_table
        self.func = func_table

    def evaluate(self):
        pass

    def update_symbol(self, symbol_table):
        self.symbol = symbol_table
        for child in self.children:
            child.update_symbol(symbol_table)

class BinOp(Node):
    
    def __init__(self, value, children, symbol_table, func_table):
        super().__init__(value, children, symbol_table, func_table)

    def evaluate(self):
        value_0, type_0 =  self.children[0].evaluate()
        value_1, type_1 =  self.children[1].evaluate()

        if self.value == "+":
            if type_0 == 'int' and type_1 == 'int':
                return (int(value_0 + value_1), "int")
            
            elif type_0 == 'audio' and type_1 == 'audio':
                return (value_0 + value_1, "audio")
            
            raise Exception('Error')
        
        elif self.value == "-":
            if type_0 == 'int' and type_1 == 'int':
                return (int(value_0 - value_1), "int")
            raise Exception('Error')
        
        elif self.value == "*":
            if type_0 == 'int' and type_1 == 'int':
                return (int(value_0 * value_1), "int")

            elif (type_0 == 'audio' and type_1 == 'int') or (type_0 == "int" and type_1 == "audio"):
                return (value_0 * value_1, "audio")
            
            raise Exception('Error')
        
        elif self.value == "/":
            if type_0 == 'int' and type_1 == 'int':
                return (int(value_0 / value_1), "int")
            raise Exception('Error')
        
        elif self.value == "and":
            if type_0 == 'int' and type_1 == 'int':
                return (int(value_0 and value_1), "int")
            raise Exception('Error')
        
        elif self.value == "or":
            if type_0 == 'int' and type_1 == 'int':
                return (int(value_0 or value_1), "int")
            raise Exception('Error')
        
        elif self.value == "==":
            if type_0 == type_1:
                return (int(value_0 == value_1), "int")
            raise Exception('Error')
        
        elif self.value == ">":
            if type_0 == type_1:
                return (int(value_0 > value_1), "int")
            raise Exception('Error')
        
        elif self.value == "<":
            if type_0 == type_1:
                return (int(value_0 < value_1), "int")
            raise Exception('Error')
        
        elif self.value == "..":
            return (str(value_0) + str(value_1), "str")

class UnOp(Node):
    
    def __init__(self, value, children, symbol_table, func_table):
        super().__init__(value, children, symbol_table, func_table)

    def evaluate(self):
        value_0, type_0 =  self.children[0].evaluate()

        if self.value == "+":
            if type_0 == 'int':
                return (int(value_0), 'int')
            raise Exception('Error')
        
        elif self.value == "-":
            if type_0 == 'int':
                return (int(-value_0), 'int')
            raise Exception('Error')
        
        elif self.value == "not":
            if type_0 == 'int':
                return (int(not value_0), 'int')
            raise Exception('Error')


class StrOp(Node):
    
    def __init__(self, value, children, symbol_table, func_table):
        super().__init__(value, children, symbol_table, func_table)

    def evaluate(self):
        return (self.value, "str")
    

class IntOp(Node):
    
    def __init__(self, value, children, symbol_table, func_table):
        super().__init__(value, children, symbol_table, func_table)

    def evaluate(self):
        return (self.value, "int")


class NoOp(Node):
    
    def __init__(self, value, children, symbol_table, func_table):
        super().__init__(value, children, symbol_table, func_table)

    def evaluate(self):
        return (None, None)
    

class Assign(Node):
    
    def __init__(self, value, children, symbol_table, func_table):
        super().__init__(value, children, symbol_table, func_table)

    def evaluate(self):
        if (not self.symbol.exists_key(self.children[0].value)):
            raise Exception("Error")
        
        value_1, type_1 = self.children[1].evaluate()
        if (type_1 == "str"):
            value_1 = AudioSegment.from_file(value_1)
            type_1 = "audio"

        var_type = self.symbol.get_value(self.children[0].value)[1]
        if (type_1 != var_type):
            raise Exception("Error")
        
        self.symbol.set_value(self.children[0].value, (value_1, type_1)) 
    

class Identifier(Node):
    
    def __init__(self, value, children, symbol_table, func_table):
        super().__init__(value, children, symbol_table, func_table)

    def evaluate(self):
        return self.symbol.get_value(self.value)


class Print(Node):
    
    def __init__(self, value, children, symbol_table, func_table):
        super().__init__(value, children, symbol_table, func_table)

    def evaluate(self):
        val_0, type_0 = self.children[0].evaluate()
        if type_0 is None:
            raise Exception("Error")
        print(val_0)


class Block(Node):
    
    def __init__(self, value, children, symbol_table, func_table):
        super().__init__(value, children, symbol_table, func_table)

    def evaluate(self):
        for child in self.children:
            child.evaluate()


class While(Node):
    
    def __init__(self, value, children, symbol_table, func_table):
        super().__init__(value, children, symbol_table, func_table)

    def evaluate(self):
        while(self.children[0].evaluate()[0]):
            self.children[1].evaluate()


class If(Node):
    
    def __init__(self, value, children, symbol_table, func_table):
        super().__init__(value, children, symbol_table, func_table)

    def evaluate(self):
        if self.children[0].evaluate()[0]:
            self.children[1].evaluate()
        elif len(self.children) == 3:
            self.children[2].evaluate()

        
class Read(Node):
    
    def __init__(self, value, children, symbol_table, func_table):
        super().__init__(value, children, symbol_table, func_table)

    def evaluate(self):
        return (int(input()), 'int')
    

class VarDec(Node):
    def __init__(self, value, children, symbol_table, func_table):
        super().__init__(value, children, symbol_table, func_table)

    def evaluate(self):
        if (self.symbol.exists_key(self.children[0].value)):
            raise Exception("Error")
        if len(self.children) == 1:
            self.symbol.set_value(self.children[0].value, (None, self.value)) 
        else:
            value_1, type_1 = self.children[1].evaluate()
            if (type_1 == "str"):
                value_1 = AudioSegment.from_file(value_1)
                type_1 = "audio"
            
            if (self.value != type_1):
                raise Exception("Error")
            
            self.symbol.set_value(self.children[0].value, (value_1, type_1)) 
    


class Play(Node):
    def __init__(self, value, children, symbol_table, func_table):
        super().__init__(value, children, symbol_table, func_table)

    def evaluate(self):
        value_0, type_0 =  self.children[0].evaluate()
        if (type_0 != "audio"):
            raise Exception("Error")
        play(value_0)



class Output(Node):
    def __init__(self, value, children, symbol_table, func_table):
        super().__init__(value, children, symbol_table, func_table)

    def evaluate(self):
        value_0, type_0 =  self.children[0].evaluate()
        value_1, type_1 =  self.children[1].evaluate()

        if (type_0 != "audio" or type_1 != "str"):
            raise Exception("Error")
        value_0.export(value_1, format="mp3")


class From(Node):
    def __init__(self, value, children, symbol_table, func_table):
        super().__init__(value, children, symbol_table, func_table)

    def evaluate(self):
        value_0, type_0 =  self.children[0].evaluate()
        value_1, type_1 =  self.children[1].evaluate()
        value_2, type_2 =  self.children[2].evaluate()

        if (type_0 != "audio" or type_1 != "int" or type_2 != "int"):
            raise Exception("Error")
        
        return (value_0[value_1: value_2], "audio")
    


class Rcut(Node):
    def __init__(self, value, children, symbol_table, func_table):
        super().__init__(value, children, symbol_table, func_table)

    def evaluate(self):
        value_0, type_0 =  self.children[0].evaluate()
        value_1, type_1 =  self.children[1].evaluate()

        if (type_0 != "audio" or type_1 != "int"):
            raise Exception("Error")
        
        return (value_0[0: value_1], "audio")
    


class Lcut(Node):
    def __init__(self, value, children, symbol_table, func_table):
        super().__init__(value, children, symbol_table, func_table)

    def evaluate(self):
        value_0, type_0 =  self.children[0].evaluate()
        value_1, type_1 =  self.children[1].evaluate()

        if (type_0 != "audio" or type_1 != "int"):
            raise Exception("Error")
        
        return (value_0[value_1:], "audio")
    


class Insert(Node):
    def __init__(self, value, children, symbol_table, func_table):
        super().__init__(value, children, symbol_table, func_table)

    def evaluate(self):
        value_0, type_0 =  self.children[0].evaluate()
        value_1, type_1 =  self.children[1].evaluate()
        value_2, type_2 =  self.children[2].evaluate()

        if (type_0 != "audio" or type_1 != "audio" or type_2 != "int"):
            raise Exception("Error")
        
        return (value_0[0:value_2] + value_1 + value_0[value_2:], "audio")