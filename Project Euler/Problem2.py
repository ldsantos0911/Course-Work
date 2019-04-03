total = 0
b = 1
a = 1
while b <= 4000000:
	if (a + b) % 2 == 0:
		total += (a + b)
	b += a
	a = (b - a)

print(total)