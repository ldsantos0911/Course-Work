def isPalindrome(num):
	num = str(num)
	for i in range(len(num) // 2):
		if num[i] != num[-(i + 1)]:
			return False
	return True

def findHighest():
	highest = 0
	for i in range(1000):
		for j in range(1000):
			if isPalindrome(i * j) and (i * j) > highest:
				highest = i * j
	return highest

print(findHighest())