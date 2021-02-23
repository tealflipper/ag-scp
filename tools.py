import secrets
import random 


def overlap(x, y):
    ''' Return length of longest suffix of x that
        matches a prefix of y and overlap string.  Return 0,"" if there no overlap. '''
    # Search left to right in y for length-k suffix of x
    ln=0
    k=1
    res = 0, ""
    while k <= len(y) and k <= len(x):
        hit = x.rfind(y[:k], len(x)-k)
        if hit != -1: 
            # print(x, y[:k], hit, k)
            res = k, y[:k]
        k+=1
    return res

def prefix(x, y):
    ''' return length and prefix of x that results fron overlap of x and y. '''
    ln=0
    k=1
    res = 0, ""
    while k <= len(y) and k <= len(x):
        hit = x.rfind(y[:k], len(x)-k)
        if hit != -1: 
            #print(x, y[:k], hit, k)
            res = len(x)-k, x[:-k]
        k+=1
    return res

def merge(x,y):
    if x == y :
        return x
    opt1=overlap(x,y)
    opt2=overlap(y,x)
    # print(opt1[0] >= opt2[0])
    if opt1[0] >= opt2[0]:
        return prefix(x,y)[1]+y
    else:
        return prefix(y,x)[1]+x

def generate_string(size):
    res = ''.join(secrets.choice(["1","0"]) for i in range(size))
    return res

def generate_blocks(size):
    block_sizes = []
    total_size = 0
    i=0
    while total_size <= size:
        block_size = random.randint(20,30)
        print(block_size)
        block_sizes.append(block_size)
        total_size += block_size


    string=generate_string(size)
    string_copies=[string]*5
    blocks = string_copies

    return blocks


# i=1 
# while i <= len(y) and i <= len(x):
#     print(x,y[:i], x.rfind(y[:i], len(x)-i))
#     i+=1