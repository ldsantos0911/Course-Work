import math
def isPrime(i):
	for j in range(2, int(math.sqrt(i)) + 1):
		if i % j == 0:
			return False
	return True

num = 2
total = 0
while num < 2000000:
	if isPrime(num):
		total += num
	num += 1

print(total)