infile = open("in.mp3","rb")
outfile = open("out.txt","wb")
def main():
    while 1:
        c = infile.read(1)
        if not c:
            break
        outfile.write(hex(ord(c)))
    outfile.close()
    infile.close()
if __name__ == '__main__':
    main()