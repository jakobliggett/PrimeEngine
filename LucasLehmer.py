import math

def mersenne(m):
    return (2**m) -1

def mersenne_test(n):
    potential_prime = mersenne(n)
    checks = n-2
    mult = 4
    while checks > 0:
        mult = (((mult**2) - 2) % potential_prime)
        checks -= 1
    if mult == 0:
        return True
    else:
        return False

def mersennes_under(n):
    m_primes = [x for x in range(n) if mersenne_test(x)]
    return m_primes

def continuous_mersenne(writefile):
    i = 1
    while True:
        if mersenne_test(i):
            with open(writefile, 'a') as f:
                f.write('M{} \n'.format(i))