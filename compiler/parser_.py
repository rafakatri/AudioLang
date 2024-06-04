from tokenizer import Tokenizer
from arvore import *
from symbol_table import Symbol_Table
from pydub import AudioSegment

class Parser:

    def __init__(self):
        self.tokenizer = None


    def parse_factor(self, symbol_table, func_table):
        if self.tokenizer.next.type == "INT":
            val = IntOp(self.tokenizer.next.value, [], symbol_table, func_table)
            self.tokenizer.select_next()
            return val
        
        elif self.tokenizer.next.type == "STRING":
            val = StrOp(self.tokenizer.next.value, [], symbol_table, func_table)
            self.tokenizer.select_next()
            return val
        
        elif self.tokenizer.next.type == "PLUS":
            self.tokenizer.select_next()
            return UnOp("+", [self.parse_factor(symbol_table, func_table)], symbol_table, func_table)
        
        elif self.tokenizer.next.type == "MINUS":
            self.tokenizer.select_next()
            return UnOp("-", [self.parse_factor(symbol_table, func_table)], symbol_table, func_table)
        
        elif self.tokenizer.next.type == "NOT":
            self.tokenizer.select_next()
            return UnOp("not", [self.parse_factor(symbol_table, func_table)], symbol_table, func_table)
        
        elif self.tokenizer.next.type == "PAR_OP":
            self.tokenizer.select_next()
            val = self.bool_expression(symbol_table, func_table)
            if self.tokenizer.next.type != "PAR_CL":
                raise Exception("Parenthesis error")
            if self.tokenizer.next.type != "EOF":
                self.tokenizer.select_next()
            return val
        
        elif self.tokenizer.next.type == "PAR_CL":
            raise Exception("Parenthesis error")
        
        elif self.tokenizer.next.type == "IDENTIFIER":
            val = Identifier(self.tokenizer.next.value, [], symbol_table, func_table)
            self.tokenizer.select_next()
            
            if (self.tokenizer.next.type == "FROM"):
                self.tokenizer.select_next()
                l_bound = self.parse_expression(symbol_table, func_table)
                
                if (self.tokenizer.next.type != "TO"):
                    raise Exception("Error")
                self.tokenizer.select_next()

                r_bound = self.parse_expression(symbol_table, func_table)
                return From("from", [val, l_bound, r_bound], symbol_table, func_table)
            
            elif (self.tokenizer.next.type == "LCUT"):
                self.tokenizer.select_next()
                bound = self.parse_expression(symbol_table, func_table)
                return Lcut("lcut", [val, bound], symbol_table, func_table)

            elif (self.tokenizer.next.type == "RCUT"):
                self.tokenizer.select_next()
                bound = self.parse_expression(symbol_table, func_table)
                return Rcut("rcut", [val, bound], symbol_table, func_table)
            

            if (self.tokenizer.next.type == "INSERT"):
                self.tokenizer.select_next()
                other = self.parse_expression(symbol_table, func_table)
                
                if (self.tokenizer.next.type != "AT"):
                    raise Exception("Error")
                self.tokenizer.select_next()

                bound = self.parse_expression(symbol_table, func_table)
                return Insert("insert", [val, other, bound], symbol_table, func_table)


            return val
        
        elif self.tokenizer.next.type == "READ":
            self.tokenizer.select_next()
            if self.tokenizer.next.type != "PAR_OP":
                raise Exception("Error")
            self.tokenizer.select_next()
            if self.tokenizer.next.type != "PAR_CL":
                raise Exception("Error")
            self.tokenizer.select_next()
            return Read('read', [], symbol_table, func_table)

        else:
            raise Exception("Error")
        

    def parse_term(self, symbol_table, func_table):
        retval = self.parse_factor(symbol_table, func_table)

        while self.tokenizer.next.type in ["MULT", "DIV"]: 
            if self.tokenizer.next.type == "MULT":
                self.tokenizer.select_next()
                retval = BinOp("*", [retval, self.parse_factor(symbol_table, func_table)], symbol_table, func_table)
                
            elif self.tokenizer.next.type == "DIV":
                self.tokenizer.select_next()
                retval = BinOp("/", [retval, self.parse_factor(symbol_table, func_table)], symbol_table, func_table)
      
        return retval
    

    def parse_expression(self, symbol_table, func_table):
        retval = self.parse_term(symbol_table, func_table)

        while self.tokenizer.next.type in ["PLUS", 'MINUS', 'DOT']:
            if self.tokenizer.next.type == "PLUS":
                self.tokenizer.select_next()
                retval = BinOp("+", [retval, self.parse_term(symbol_table, func_table)], symbol_table, func_table)
                
            elif self.tokenizer.next.type == "MINUS":
                self.tokenizer.select_next()
                retval = BinOp("-", [retval, self.parse_term(symbol_table, func_table)], symbol_table, func_table)

            elif self.tokenizer.next.type == "DOT":
                self.tokenizer.select_next()
                if self.tokenizer.next.type != "DOT":
                    raise Exception("Error")
                self.tokenizer.select_next()
                retval = BinOp("..", [retval, self.parse_term(symbol_table, func_table)], symbol_table, func_table)

        return retval
    

    def bool_expression(self, symbol_table, func_table):
        retval = self.bool_term(symbol_table, func_table)
        while self.tokenizer.next.type == "OR":
            self.tokenizer.select_next()
            retval = BinOp("or", [retval, self.bool_term(symbol_table, func_table)], symbol_table, func_table)
        return retval
    

    def bool_term(self, symbol_table, func_table):
        retval = self.rel_expression(symbol_table, func_table)
        while self.tokenizer.next.type == "AND":
            self.tokenizer.select_next()
            retval = BinOp("and", [retval, self.rel_expression(symbol_table, func_table)], symbol_table, func_table)
        return retval


    def rel_expression(self, symbol_table, func_table):
        retval = self.parse_expression(symbol_table, func_table)
        while self.tokenizer.next.type in ['ASSIGN', 'GREATER', 'LESSER']:
            if self.tokenizer.next.type == "ASSIGN":
                self.tokenizer.select_next()
                if self.tokenizer.next.type != "ASSIGN":
                    raise Exception("Error")
                self.tokenizer.select_next()
                retval = BinOp("==", [retval, self.parse_expression(symbol_table, func_table)], symbol_table, func_table)

            elif self.tokenizer.next.type == "GREATER":
                self.tokenizer.select_next()
                retval = BinOp(">", [retval, self.parse_expression(symbol_table, func_table)], symbol_table, func_table)

            elif self.tokenizer.next.type == "LESSER":
                self.tokenizer.select_next()
                retval = BinOp("<", [retval, self.parse_expression(symbol_table, func_table)], symbol_table, func_table)

        return retval


    def parse_statement(self, symbol_table : Symbol_Table, func_table):
        if self.tokenizer.next.type == "ENDL":
            self.tokenizer.select_next()
            return NoOp(None, [], symbol_table, func_table)
        
        elif self.tokenizer.next.type == "INT":
            self.tokenizer.select_next()
            if self.tokenizer.next.type != "IDENTIFIER":
                raise Exception("Error")
            id = Identifier(self.tokenizer.next.value, [], symbol_table, func_table)
            self.tokenizer.select_next()
            if self.tokenizer.next.type == "END":
                self.tokenizer.select_next()
                return VarDec('int', [id], symbol_table, func_table)
            elif self.tokenizer.next.type == "ASSIGN":
                self.tokenizer.select_next()
                retval = self.bool_expression(symbol_table, func_table)
                if (self.tokenizer.next.type != "END"):
                    raise Exception("Error")
                self.tokenizer.select_next()
                return VarDec("int", [id, retval], symbol_table, func_table)
            else:
                raise Exception("Error")


        elif self.tokenizer.next.type == "SOURCE":
            self.tokenizer.select_next()
            if self.tokenizer.next.type != "IDENTIFIER":
                raise Exception("Error")
            id = Identifier(self.tokenizer.next.value, [], symbol_table, func_table)
            self.tokenizer.select_next()
            if self.tokenizer.next.type == "END":
                self.tokenizer.select_next()
                return VarDec('audio', [id], symbol_table, func_table)
            elif self.tokenizer.next.type == "ASSIGN":
                self.tokenizer.select_next()
                retval = self.bool_expression(symbol_table, func_table)
                if (self.tokenizer.next.type != "END"):
                    raise Exception("Error")
                self.tokenizer.select_next()
                return VarDec("audio", [id, retval], symbol_table, func_table)
            else:
                raise Exception("Error")
        
        
        elif self.tokenizer.next.type == "IDENTIFIER":
            id = Identifier(self.tokenizer.next.value, [], symbol_table, func_table)
            self.tokenizer.select_next()
            if self.tokenizer.next.type == "ASSIGN":
                self.tokenizer.select_next()
                retval = self.bool_expression(symbol_table, func_table)
                if (self.tokenizer.next.type != "END"):
                    raise Exception("Error")
                self.tokenizer.select_next()
                return Assign("=", [id, retval], symbol_table, func_table)
            
            else:
                raise Exception("Error")
        
        elif self.tokenizer.next.type == "PRINT":
            self.tokenizer.select_next()
            
            if self.tokenizer.next.type != "PAR_OP":
                raise Exception("Print error")
            
            self.tokenizer.select_next()
            retval = self.bool_expression(symbol_table, func_table)

            if self.tokenizer.next.type != "PAR_CL":
                raise Exception("Print error")
            self.tokenizer.select_next()
            
            if (self.tokenizer.next.type != "END"):
                    raise Exception("Error")
            self.tokenizer.select_next()
            return Print("print", [retval], symbol_table, func_table)
        
        elif self.tokenizer.next.type == "WHILE":
            self.tokenizer.select_next()
            if self.tokenizer.next.type != "PAR_OP":
                raise Exception("Error")
            self.tokenizer.select_next()
            condition = self.bool_expression(symbol_table, func_table)
            if self.tokenizer.next.type != "PAR_CL":
                raise Exception("Error")
            self.tokenizer.select_next()
            statements = []
            if self.tokenizer.next.type != "BR_OP":
                raise Exception("Error")
            self.tokenizer.select_next()
            while self.tokenizer.next.type != "BR_CL":
                statement = self.parse_statement(symbol_table, func_table)
                statements.append(statement)
            self.tokenizer.select_next()
            block =  Block("while_block", statements, symbol_table, func_table)
            return While('while', [condition, block], symbol_table, func_table)


        elif self.tokenizer.next.type == "IF":
            self.tokenizer.select_next()
            if self.tokenizer.next.type != "PAR_OP":
                raise Exception("Error")
            self.tokenizer.select_next()
            condition = self.bool_expression(symbol_table, func_table)
            if self.tokenizer.next.type != "PAR_CL":
                raise Exception("Error")
            self.tokenizer.select_next()
            statements = []
            if self.tokenizer.next.type != "BR_OP":
                raise Exception("Error")
            self.tokenizer.select_next()
            while self.tokenizer.next.type != "BR_CL":
                statement = self.parse_statement(symbol_table, func_table)
                statements.append(statement)
            self.tokenizer.select_next()
            if (self.tokenizer.next.type == "ELSE"):
                self.tokenizer.select_next()
                first_block =  Block("if_block", statements, symbol_table, func_table)
                statements = []
                if self.tokenizer.next.type != "BR_OP":
                    raise Exception("Error")
                self.tokenizer.select_next()
                while self.tokenizer.next.type != "BR_CL":
                    statement = self.parse_statement(symbol_table, func_table)
                    statements.append(statement)
                self.tokenizer.select_next()
                second_block =  Block("if_block", statements, symbol_table, func_table)
                return If("if", [condition, first_block, second_block], symbol_table, func_table)
            block =  Block("if_block", statements, symbol_table, func_table)
            return If('if', [condition, block], symbol_table, func_table)

        elif self.tokenizer.next.type == "PLAY":
            self.tokenizer.select_next()
            id = self.parse_expression(symbol_table, func_table)
            if(self.tokenizer.next.type != "END"):
                raise Exception("Error")
            self.tokenizer.select_next()
            return Play("play", [id], symbol_table, func_table)


        elif self.tokenizer.next.type == "OUTPUT":
            self.tokenizer.select_next()
            if (self.tokenizer.next.type != "PAR_OP"):
                raise Exception("Error")
            self.tokenizer.select_next()

            id = self.parse_expression(symbol_table, func_table)
            if (self.tokenizer.next.type != "COMMA"):
                raise Exception("Error")
            self.tokenizer.select_next()

            path = self.parse_expression(symbol_table, func_table)
            if(self.tokenizer.next.type != "PAR_CL"):
                raise Exception("Error")
            self.tokenizer.select_next()

            if(self.tokenizer.next.type != "END"):
                raise Exception("Error")
            self.tokenizer.select_next()

            return Output("output", [id, path], symbol_table, func_table)


        else:
            print(self.tokenizer.next.type)
            raise Exception("Statement error") 


    def parse_block(self, symbol_table, func_table):
        children = []
        while self.tokenizer.next.type != "EOF":
            children.append(self.parse_statement(symbol_table, func_table))
        block = Block("bloco", children, symbol_table, func_table)
        return block
        


    def run(self, code : str):
        table = Symbol_Table()
        func_table = Symbol_Table()
        self.tokenizer = Tokenizer(code)
        self.tokenizer.select_next()
        return self.parse_block(table, func_table).evaluate()