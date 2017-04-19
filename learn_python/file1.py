infile = open("out.txt","rb")
outfile = open("out.mp3","wb")
def main():
	while 1:
		c = infile.read(1)
		if not c:
			break
		b = chr(c)
	outfile.write(b)
	outfile.close()
	infile.close()
if __name__ == '__main__':
	main()
