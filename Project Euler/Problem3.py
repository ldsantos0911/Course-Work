import math
def prime_GCF(x):
	for i in range(int(math.sqrt(x)), 1, -1):
		if x % i == 0 and isPrime(i):
			return i
			
def isPrime(i):
	for j in range(2, int(math.sqrt(i)) + 1):
		if i % j == 0:
			return False
	return True

print(prime_GCF(600851475143))