import pair
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
        ##print(toks)
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
                            iargs += [carg] # add the current a rg to iargs,
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
            elif t in [['name','if'],['name','while']]:
                whatdat = tree([toks[pl+1:-1]])
                codes = toksls[lpl+1:pairs[lpl]]
                codes = tree(codes)
                subret += [[t[1],whatdat,codes]]
                lpl = pairs[lpl]
                pl = len(toks)
            elif t[0] == 'name':
                if len(toks) > pl+1 and  toks[pl+1][0] == 'lparen':
                    beg = pl+2
                    ##print(parens,pl+1)
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
