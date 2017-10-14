def view(lis,d=0,):
    d += 1
    for i in range(len(lis)):
        j = lis[i]
        if isinstance(j,list):
            print('  '*(d-1)+'[')
            view(j,d=d)
            print('  '*(d-1)+']')
        else:
            print('  '*(d-1)+str(j))
