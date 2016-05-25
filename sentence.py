
f = open("sentences_txt/kowiki_sentence_total.txt", "r", encoding="utf-8")

cnt = 0
index = 1
size = 5000
file_name = "sentences_txt/kowiki_sentence_" + str(index) + ".txt"
fs = open(file_name, "w", encoding="utf-8")
for line in f.readlines() :

    if cnt == size :
        cnt = 0
        index += 1
        file_name = "sentences_txt/kowiki_sentence_" + str(index) + ".txt"
        fs.close()
        fs = open(file_name, "w", encoding="utf-8")
        print(index)

    fs.write(line)
    cnt += 1

