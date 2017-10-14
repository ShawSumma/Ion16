def pair(x,chs,depth=0):
    hold = {}
    dep = 0
    pl = 0
    ret = {}
    for i in x:
        if i == chs[0]:
            dep += 1
            hold[dep] = pl
        elif i == chs[1]:
            if depth == 0 or dep <= depth:
                ret[hold[dep]] = pl
            dep -= 1
        pl += 1
    return ret
class ion:
    def pair(x):
        sts = [i[1] for i in x]
        return pair(sts,'{}')
    def pairfn(x):
        sts = [i[1] for i in x]
        p = pair(sts,('(',')'))
        return p
    def flat(x):
        sts = [i[1] for i in x]
        return pair(sts,'{}',depth=1)
    def tree(x):
        sts = []
        for i in x:
            for j in i:
                sts = sts+[j]
        return ion.flat(sts)
