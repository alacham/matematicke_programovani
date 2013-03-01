import math
from euclid_alg import nsd_mod

# x na cele y
def cx_na_y(x, y):
    if y <= 1:
        if y == 0:
            return 1
        else: # y == 1
            return x
    elif y & 1 == 0:
        tmp = cx_na_y(x, y >> 1)
        return tmp * tmp
    else:
        return x * cx_na_y(x, y - 1)

def n_odmocnina(x, n, acc=0.01):
    if x == float('inf'):
        print "shit got real"
        return 0
    diff = 1000 * x
    nit = 0
    if x == 1:
        return 1
    if x < 1:
        h = 1
        l = x
    elif x < 2:# merge with else branch?
        l = 1
        h = 2
    else:
        l = 1
        h = 2
        cop = x
        nshift = 1
        while cop >= (1 << (nshift * n)):
            nshift += 1
            h <<= 1
            l <<= 1
#    print x**(1.0/n), l, h
    prev_diff = float('inf')
    while diff > acc and abs(prev_diff - diff) > acc:
        nit += 1
        s = (h + l) / 2.0
        #print l, h ,s
        s_to_n = cx_na_y(s, n)
        prev_diff = diff
        diff = abs(x - s_to_n)
        #print diff
        if s_to_n > x:
            h = s
        else:
            l = s
    #print nit
    return s

def nsd_mod(a, b, nth=0):
    if b == 0:
        return a, nth
    else:
        return nsd_mod(b, a % b, nth + 1)

def x_to_real(x, n, acc=0.001):
    whole_part = cx_na_y(x, int(n))
    diff = n - int(n)
    fp = int(diff * 100)
    lcd = nsd_mod(fp, 100)[0]
    pw = fp / lcd
    n_root = 100 / lcd
    umocneno = cx_na_y(x, pw)
    odmocneno = n_odmocnina(umocneno, n_root, acc)
    return odmocneno * whole_part

def x_to_real2(x, n, acc=0.001):
    fp = int(round(n * 100))
    lcd = nsd_mod(fp, 100)[0]
    pw = fp / lcd
    n_root = 100 / lcd
    umocneno = cx_na_y(x, pw)
#    print umocneno, n_root
    odmocneno = n_odmocnina(umocneno, n_root, acc)
    return odmocneno


# chci dostat cislo do intervalu -0.55,0.5
def nat_log_conv(x):
    sign = 1
    if x < 0.55: # 0.55~=1.5/e
        x = 1.0 / x
        sign = -1
    shift = 0
    while x > 1.5:
        x = x / math.e
        shift += 1
    # do ted 0.55,1.5
    x -= 1
    return x, shift, sign

def nat_log(x, acc=0.00001):
    if x < 0 or x == float('nan'):
        return float('nan')
    elif x == float('inf'):
        return float('inf')
    elif x == 0:
        return -float('inf')
    
    x, shift, sign = nat_log_conv(x)
    summed = x
    helper = float(x)
    diff = x
    i = 1
    # taylor series for ln(x+1)
    while abs(diff) > acc:
        i += 1
        helper *= -x
        diff = helper / i
        summed += diff
    return sign * (summed + shift)

# using taylor series for e^x
def e_to_pow(x, acc=0.00001):
    summed = 1
    facthelp = 1
    powhelp = float(1)
    diff = acc * 100
    i = 0
    while abs(diff) > acc:
        i += 1
        facthelp *= i
        powhelp *= x 
        diff = powhelp/facthelp
        summed += diff
    return summed

def x_to_real3(x, n, acc=0.00001):
    new_pow = n * nat_log(x, acc)
    return e_to_pow(new_pow, acc)


print x_to_real3(5, 2.17)
print x_to_real2(5, 2.17)
print x_to_real(5, 2.17)
print 5 ** 2.17

print 5125.45089 ** math.pi
print x_to_real(5125.45089, math.pi)
print x_to_real2(5125.45089, math.pi)
print x_to_real3(5125.45089, math.pi)
