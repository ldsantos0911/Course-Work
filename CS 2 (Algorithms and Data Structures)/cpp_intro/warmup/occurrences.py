def occurrences(string):
	'''
	Accepts a string. Returns a list of 26 ints corresponding to the 26
	letters of the English alphabet. Each element represents the number
	of occurrences of its corresponding letter. 
	
	e.g. 
	- 4 a's will place 4 in the first element of the list.
	- 3 b's will place 3 in the first element.
	- an empty string or a string not containing any letters will 
	  consist entirely of 0's
	'''
	string = string.upper()
	occur = [0]*26
	for char in string:
		if ord(char) <= 90 and ord(char) >= 65:
			occur[ord(char) - 65] += 1
	return occur

