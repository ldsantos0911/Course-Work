file = open('Prob10Num.txt', 'r')
un_lines = file.readlines()
lines = [[]]
for i, j in enumerate(un_lines):
	j = j.split()
	lines.append([])
	for num in j:
		lines[i].append(int(num))

product = 0
mid_modifiers = [(-1, -1), (-1, 1), (1, -1), (1, 1), (1, 0), (-1, 0), (0, 1), (0, -1)]

for row in range(20):
	for col in range(20):
		total_temp = 1
		if row >= 3 and row <= 16 and col >= 3 and col <= 16:
			for i, j in enumerate(mid_modifiers):
				for k in range(4):
					total_temp *= lines[row + k * j[0]][col + k * j[1]]
				if total_temp > product:
					product = total_temp
				total_temp = 1
		elif (col < 3 and row <= 16) or (col > 16 and row <= 16):
			for i in range(4):
				total_temp *= lines[row + i][col]
		elif (row < 3 and col <= 16) or (row > 16 and col <= 16):
			for i in range(4):
				total_temp *= lines[row][col + i]
		if total_temp > product:
			product = total_temp

print(product)