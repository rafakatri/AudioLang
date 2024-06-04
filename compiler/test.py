import sys
from parser_ import Parser
from pre_processing import PrePro
from tokenizer import Tokenizer

if __name__ == "__main__":
    
    if len(sys.argv) == 2:
        file = sys.argv[1]
        with open(file) as f:
            data = f.read()
        data = PrePro.filter(data)
        tokenizer = Tokenizer(data)
        tokenizer.select_next()
        while tokenizer.next.type != "EOF":
            print(tokenizer.next.type, tokenizer.next.value)
            tokenizer.select_next()

    else:
        raise Exception("Error: Empty string or invalid input")


                       
        
