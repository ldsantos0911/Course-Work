def find_500():
	add = 2 ** 250
	while True:
		num = (add * (add + 1)) / 2
		divisors = 0
		i = 1
		while i <= num / 2:
			if num % i == 0:
				divisors += 1
			if divisors + 1 > 500:
				return num
			# print(num, i)
			i += 1
		add += 1

print(find_500())

