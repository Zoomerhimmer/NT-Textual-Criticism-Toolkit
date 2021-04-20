import re
import sys
from normalize import normalize

arg_num = len(sys.argv)
if  arg_num == 1:
    sys.exit('Program needs a file to process.')

def main():
    file = open(sys.argv[1])
    data = file.read()
    data = normalize(data)
    punctuations = list(set(re.findall(r'[^\w\s]', data)))
    print(punctuations)

if __name__ == '__main__':
    main()
