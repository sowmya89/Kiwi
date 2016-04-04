infile = "result_neg.txt"
outfile = "cleaned_neg.txt"

delete_list = ["<br />", "< br>"]
fin = open(infile)
fout = open(outfile, "w+")
for line in fin:
    for word in delete_list:
        line = line.replace(word, "")
    fout.write(line)
fin.close()
fout.close()