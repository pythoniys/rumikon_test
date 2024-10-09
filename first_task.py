import re


def expand_brackets(line):
    pattern_replace = r'(\()?\s*([a-zA-Z])'
    result = ''.join(re.sub(pattern_replace, r'\1 1 * \2', line).split())
    counter = line.count('(')
    for i in range(counter):
        
    return result

def verification_data(line):
    pattern_symbols = '1234567890+-*xyz() '
    check = lambda s: all(x in pattern_symbols for x in s.lower())
    pattern_multiplication = r'\b\d+\s*(?=[a-zA-Z(])'
    
    if not check(line) or re.search(pattern_multiplication, line) \
        or line.count('(') != line.count(')'):
        return False
    else:
        return True

if __name__ == '__main__':
    string = input()
    if verification_data(string):
        expand = expand_brackets(string)
        print(expand)
    else:
        print('Недопустимое выражение')
