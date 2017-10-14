# regex, this is used for testing if the current token matches in the tokenizer stage
import re
# listview is my list viewing program
import listview as lv
# it pairs things and is used widely throughtout the language
# for instance if you need to find all the curly brackets paired use this
import pair



def what(sin): # this is the tokenizer, sin is the string in
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
            elif re.match(r'(?i)0f([0-9]|[a-f]|\.)*',cur) != None: # if it matches the hex class
                ret.append(['hex',cur])
                cur = ''
            elif re.match(r'(?i)0b([0-1]\.)*',cur) != None: # if it matches the binary class
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


def split(toks): #not the same as .split on a string, this is used as a line splitter and
    ret = [[]] # the return varriable
    for i in toks: # iterate through tokens
        if i[0] == 'endl': # split baised on newline
            ret.append([]) # do this by adding a new sub-list to ret
        else: # if its not a newline
            ret[-1].append(i) # add the current token to the current (-1) ret index
    return ret # return the split lines

def tree(toksls): #make the tree from the tokens, toksls is the tokens list
    def tokpair(ipairs,toksls):
        places = {}
        k = 0
        for i in range(len(toksls)):
            for j in toksls[i]:
                places[k] = i
                k += 1
        pairs = {}
        for i in ipairs:
            pairs[places[i]] = places[ipairs[i]]
        return pairs
    pairs = pair.ion.tree(toksls)
    pairs = tokpair(pairs,toksls)
    lpl = 0 # place in tokensls
    ret = [] # return data
    while lpl < len(toksls): # iterate through tokensls
        toks = toksls[lpl] # the current line of tokens
        subret = []# sub return data
        pl = 0 # place in the current tokens
        parens = pair.ion.pairfn(toks)
        while pl < len(toks): # iterate through the current line of tokens by number
            t = toks[pl] # the current token
            if len(toks) > 1:
                if toks[1][0] == 'set':
                    names = toks[0]
                    vals = toks[2:]
                    subret += ['set',names,tree([vals])]
                    pl = len(toks) #end the iteraing current by number line loop
            if t == ['name','func']: # is it a function
                fnname = toks[pl+1] # the name of the function
                argst = toks[pl+3:-2] # argst is the arglist for the function
                ikwargs = {} # kwargs in
                iargs = [] # args in
                carg = [] # current arg
                for argt in argst+[]: # loop through argst as argt
                    if argt[0] == 'comma': # if its a new argumnet
                        if len(carg) == 1: # if carg is a reular arg
                            iargs += [carg] # add the current arg to iargs,
                        elif len(carg) == 3: # if carg is a keyword arg
                            ikwargs[carg[0]] = carg[2] # add the current arg to iargs
                        carg = []
                    else: #if its not a new arg
                        carg += [argt[1]] # add the current arg
                if len(carg) == 1: # endarg
                    iargs += [carg] # add the current arg to iargs
                elif len(carg) == 3: # endarg
                    ikwargs[carg[0]] = carg[2] # add the current arg to iargs
                carg = []
                codes = toksls[lpl+1:pairs[lpl]]
                subret += [['function',fnname[1],[iargs,ikwargs],tree(codes)]] #add the function to the sub return value
                lpl = pairs[lpl]
                pl = len(toks) #end the iteraing current by number line loop
            elif t[0] == 'name':
                if len(toks) > pl+1 and  toks[pl+1][0] == 'lparen':
                    beg = pl+2
                    end = parens[pl+1]
                    #print(toks[beg:end])
                    subret += [['call',t[1],tree([toks[beg:end]])]] # add the function and its tree
                    pl = end # jump to the end of the function
                else:
                    subret += [t] # add the token
            elif t[0] in ['int','hex','bin']: # is it a number
                subret += [t] # add the number
            pl += 1 #tick the place in line
        ret = ret + [subret] if subret != [] else ret # add the line if it is not nothing
        subret = [] # reset the line
        lpl += 1 # tick the line
    return ret # return the tree

def run(data):
    for cmd in data:
        #print(cmd)
        while len(cmd) == 1:
            cmd = cmd[0]
        if cmd[0] == 'int':
            return float(cmd[1])
        if cmd[0] == 'call':
            if cmd[1] == 'print':
                for i in cmd[2][0]:
                    print(run([i]),end=' ')
                print()
            if cmd[1] == 'add':
                ret = 0
                for arg in cmd[2][0]:
                    arg = [arg]
                    ret += run(arg)
                return ret
            if cmd[1] == 'mul':
                ret = 1
                for arg in cmd[2][0]:
                    arg = [arg]
                    ret *= run(arg)
                return ret
            if cmd[1] == 'sub':
                ret = 0
                for arg in cmd[2][0]:
                    arg = [arg]
                    ret += run(arg)
                return ret
            if cmd[1] == 'div':
                ret = 1
                for arg in cmd[2][0]:
                    arg = [arg]
                    ret /= run(arg)
                return ret
    return None
file1 = open('test.txt','r').read().replace('\n',"")
##print(file1)
file2 = what(file1)
##print(file2) #print the raw what data
file3 = split(file2)
#print(file3)
file4 = tree(file3)
##lv.view(file4) # view the tree
##print(file4)
run(file4)
