def find_special():
	for a in range(1 , 400):
		for b in range(1, 400):
			for c in range(1, 600):
				if a ** 2 + b ** 2 == c ** 2 and a + b + c == 1000:
					return (a * b * c, [a, b, c])

print(find_special())

