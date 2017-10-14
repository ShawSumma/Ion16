import re
import pair
def make(sin): # this is the tokenizer, sin is the string in
    cur = '' # the current charactor
    ret = [] # retunr this
    flags = [] # flags to see if it is in a string or other special case
    for i in sin:

        if i == '"':
            if 'dstr' in flags:
                del flags['dstr']
                ret.append(['str',cur[1:]])
            else:
               flags += ['dstr']

        if i in [' ',';','|','(',')',',','{','}','='] and len(flags) == 0: # checks if the next charactor is the end of an expression
            if re.match(r'(?i)([a-z]|\*|\+|\-|\\|\^|\%|\$|\#|\@|\!)+([0-9])*',cur) != None: # if it matches the string classs
                ret.append(['name',cur])
                cur = ''
            elif re.match(r'(?i)(0x|[1-9]|\.)([0-9]|\.)*',cur) != None: # if it mathces the int class
                if cur[0] == '.':
                    cur = '0'+cur
                ret.append(['int',cur])
                cur = ''
            elif re.match(r'(?i)0h([0-9]|[a-f]|\.)*',cur) != None: # if it matches the hex class
                ret.append(['hex',cur])
                cur = ''
            elif re.match(r'(?i)0b([0-1])*',cur) != None: # if it matches the binary class
                ret.append(['bin',cur])
                cur = ''
        # these test for charactors that split
        if i == '|': # the from char
            ret.append(['from',i])
            i = ''
        if i == ')': # the right paren
            ret.append(['rparen',i])
            i = ''
        if i == '(': # the left paren
            ret.append(['lparen',i])
            i = ''
        if i == '}': # the right bracket
            ret.append(['rcurl',i])
            ret.append(['endl',i])
            i = ''
        if i == '{': # the left bracket
            ret.append(['lcurl',i])
            ret.append(['endl',i])
            i = ''
        if i == ',': # the comma, this is the seperator charactor
            ret.append(['comma',i])
            i = ''
        if i == ';': # end of lines
            ret.append(['endl',i])
            i = ''
        if i == '=': # euals
            ret.append(['set',i])
            i = ''
        if i == " " and cur=='': #if the current charactor is a space, and there is nothing in the current sored charactor, this is so whitespace can be ignored
            pass
        else: # add the current charactor to the chars
            cur += i
    return ret #reurn the ret that has been growing
