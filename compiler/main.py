import sys
from parser_ import Parser
from pre_processing import PrePro

if __name__ == "__main__":
    
    if len(sys.argv) == 2:
        file = sys.argv[1]
        with open(file) as f:
            data = f.read()
        data = PrePro.filter(data)
        parser = Parser()
        parser.run(data)
    else:
        raise Exception("Error: Empty string or invalid input")


                       
        
