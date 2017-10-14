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
def run(data):
    for cmd in data:
        #print(cmd)
        while len(cmd) == 1:
            cmd = cmd[0]
        if cmd[0] == 'int':
            return float(cmd[1])
        if cmd[0] == 'bin':
            return int(cmd[1],2)
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
            if cmd[1] == 'mod':
                ret = run([cmd[2][0][0]])
                ret %= run([cmd[2][0][1]])
                return ret
            if cmd[1] == 'b_i':
                int(run([cmd[2][0][0]]),2)
                return ret
            if cmd[1] == 'i_b':
                bin(run([cmd[2][0][0]]),10)
                return ret
    return None
file1 = open('test.txt','r').read().replace('\n',"")
##print(file1)
file2 = tok.make(file1)
print(file2) #print the raw what data
file3 = tree.split(file2)
#print(file3)
file4 = tree.tree(file3)
##lv.view(file4) # view the tree
##print(file4)
run(file4)
