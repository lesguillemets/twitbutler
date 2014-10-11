#!/usr/bin/env python3
import numpy as np

def generate_primes(seedn):
    """generates primes upto n**2. """
    
    maximum = seedn*seedn
    # generate list of our knowledge. data[i] denotes if i is a prime.
    data = np.ones(maximum+1, dtype=bool)
    for n in (0,1):
        data[n] = False  # 0 and 1 are not primes.
    
    for n in range(2,seedn+1):
        if data[n]:
            # n is a prime!
            for pn in range(n*n, maximum+1, n):
                data[pn] = False
            yield n
        else:
            # n is not a prime.
            pass
    
    # the numbers left to be True are primes.
    for p in (n for (n,is_p) in enumerate(data[seedn+1:],seedn+1)
              if is_p):
        yield p

class PrimeHandler(object):
    """Handles prime-related functions."""
    
    def __init__(self,n):
        self.primes = list(generate_primes(n))
    
    def factorise(self,n):
        """
        Int -> [(prime,Int)]
        """
        if n == 0:
            raise ValueError("Don't pass me 0")
        elif n != int(n):
            raise ValueError("Pass me an integer")
        factors = []
        for p in self.primes:
            i = 0
            while n%p == 0:
                i += 1
                n = n//p
            if i != 0:  # found a factor!
                factors.append((p,i))
            if p*p > n: # came so far!
                break
        if n != 1:
            factors.append((n,1))
        return factors


if __name__ == "__main__":
    ph = PrimeHandler(1000)
    print(ph.factorise(45))
    print(ph.factorise(81))
    print(ph.factorise(9493947))
