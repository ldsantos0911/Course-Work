import math

def isPrime(i):
	for j in range(2, int(math.sqrt(i)) + 1):
		if i % j == 0:
			return False
	return True

count = 0
n = 2
while True:
	if isPrime(n):
		count += 1
	if count == 10001:
		print(n)
		break
	n += 1