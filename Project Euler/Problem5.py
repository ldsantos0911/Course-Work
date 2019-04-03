def findSmallest():
	n = 40
	while True:
		for i in range(2, 21):
			if n % i != 0:
				n += 1
				break
			elif i == 20:
				return n
print(findSmallest())