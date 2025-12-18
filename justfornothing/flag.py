import random

table = ('Aa4@', 'Bb8', 'Cc', 'Dd', 'Ee3', 'Ff', 'Gg69', 'Hh', 'Ii', 'Jj', 'Kk', 'Ll1', 'Mm', 'Nn', 'Oo0', 'Pp', 'Qq', 
'Rr', 'Ss5$', 'Tt7', 'Uu', 'Vv', 'Ww', 'Xx', 'Yy', 'Zz2')
alpha = "abcdefghijklmnopqrstuvwxyz"

def findalpha(ch):
    for i in range(len(table)):
        if ch in table[i]:
            return alpha[i]
    return None

def flag2plain(flag : str) -> str:
    start = flag.index('{')
    plain = flag[:start+1]
    flag = flag[start+1:-1]
    for i in flag:
        c = findalpha(i)
        if c:
            plain += c
        else:
            plain += i
    return plain+'}'

def plain2flag(plain : str) -> str:
    random.seed(plain.encode())
    start = plain.index('{')
    flag = plain[:start+1]
    plain = str.lower(plain[start+1:-1])
    for i in plain:
        if i in alpha:
            idx = alpha.index(i)
            k = random.randrange(0, len(table[idx]))
            flag += table[idx][k]
        else:
            flag += i
    return flag+'}'

s = plain2flag("flag{This_is_flag}")
print(s)
s = flag2plain(s)
print(s)
