def sumSq():
	total = 0
	for i in range(1, 101):
		total += i ** 2
	return total

def sqSum():
	total = 0
	for i in range(1, 101):
		total += i
	return total ** 2

print(sqSum() - sumSq())
