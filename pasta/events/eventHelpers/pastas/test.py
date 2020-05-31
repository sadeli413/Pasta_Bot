def main():
	items = sorted(file2list("../triggers.txt"))
	write = open("new.txt", "w")

	for item in items:
		write.write(item + "\n")
		
	write.close()

def file2list(filename):
	lines = []
	file = open(filename, "r")

	for line in file:
		# remove '\n'
		line = line[:len(line) - 1]
		lines.append(line)

	file.close()
	return lines
	
if __name__ == "__main__":
	main()