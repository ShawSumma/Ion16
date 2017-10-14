# regex, this is used for testing if the current token matches in the tokenizer stage
# there is currently no tesr file for safety
# it pairs things and is used widely throughtout the language
# for instance if you need to find all the curly brackets paired use this
# listview is my list viewing program
import re
import listview as lv
import pair
import tok
import tree
ionlocals = {}
ionglobals = {}
def run(data):
    #print(data)
    global ionlocals
    for cmd in data:
        while len(cmd) == 1:
            cmd = cmd[0]
        if cmd[0] == 'if':
            if run([cmd[1]]):
                run([cmd[2]])
        if cmd[0] == 'while':
            while run([cmd[1]]):
                run([cmd[2]])
        if cmd[0] == 'int':
            return float(cmd[1])
        if cmd[0] == 'name':
            return ionlocals[cmd[1]]
        if cmd[0] == 'bin':
            return int(cmd[1],2)
        if cmd[0] == 'call':
            if cmd[1] == 'set':
                c = run([cmd[2][0][1]])
                p = cmd[2][0][0][1]
                ionlocals[p] = c
            if cmd[1] == 'print':
                for i in cmd[2]:
                    print(run([i[0]]),end=' ')
                print()
            if cmd[1] == 'add':
                ret = 0
                for arg in cmd[2][0]:
                    arg = [arg]
                    ret += run(arg)
                return ret
            if cmd[1] == 'is':
                ret = True
                arg = cmd[2][0][0]
                las = run([arg])
                for arg in cmd[2][0]:
                    arg = [arg]
                    if ret:
                        ret = run(arg) == las
                return ret
            if cmd[1] == 'not':
                arg = cmd[2][0][0]
                las = run([arg])
                return not las
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
            if cmd[1] == 'mod':
                ret = run([cmd[2][0][0]])
                ret %= run([cmd[2][0][1]])
                return ret
            if cmd[1] == 'bin':
                int(run([cmd[2][0][0]]),2)
                return ret
            if cmd[1] == 'zero':
                return 0
    return run(cmd)
file1 = open('test.txt','r').read().replace('\n',"")
##print(file1)
file2 = tok.make(file1)
##print(file2) #print the raw what data
file3 = tree.split(file2)
#print(file3)
file4 = tree.tree(file3)
##lv.view(file4) # view the tree
##print(file4)
run(file4)
##print(ionlocals)
