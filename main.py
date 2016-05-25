#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
import konlpy
import re, sys

def extract_concept(start,end) :

    p1 = open("dict/wiki_terms.pickle", "rb")
    p2 = open("dict/doosan_terms.pickle", "rb")
    wiki_term = pickle.load(p1)
    doosan_term = pickle.load(p2)

    #1-1266

    for n in range(start,end+1) :

        f = open("sentences_txt/kowiki_sentence_"+str(n)+".txt", "r", encoding="utf-8")
        output_file = open("result/kowiki_sentence_"+str(n)+"_result.txt", "w", encoding="utf-8")
        error_file = open("result/kowiki_sentence_"+str(n)+"_error.txt", "w", encoding="utf-8")

        cnt = 1
        for line in f.readlines() :

            while(1) :
                try :
                    print(cnt)
                    #print(line)
                    sentence = line.split("\t")[3]
                    original_sentence = sentence

                    for ch in ["\"","\'","“","”","‘","’","《","》",".",",", "•", "-"] :
                        sentence = sentence.replace(ch,"")
                    for ch in ["·", "-","."] :
                        sentence = sentence.replace(ch, " ")
                    tagger = konlpy.tag.Twitter()
                    pos = tagger.pos(sentence)

                    nouns = []
                    for p in pos :
                        if p[1] == 'Alpha' or p[1] == 'Number' or p[1] == 'Noun' :
                            nouns.append(p[0])

                    result = []
                    except_list = ["단계", "대해", "다소", "두", "세", "네", "오늘날", "하나하나", "정도", "처음","경", "자체", "후","하나", "앞", "뒤", "위","아래", "수","데", "내", "음", "번", "그후", "이하","이상", "여기", "권", "당시", "책", "년", "달", "월", "해", "일", "말", "초", "째", "사실상", "자신", "역시", "각종", "의", "앞", "지","속", "대", "전", "주요", "일", "제", "해도", "처", "이", "저", "수", "그", "때", "가지", "이후", "매우", "등", "못", "스스로", "오직", "이기", "볼", "초", "약", "중", "상", "개", "주", "예", "이전", "이번", "채", "안", "경우"]

                    while not len(nouns) == 0 :
                        candidates = nouns[:]
                        while not len(candidates) == 0 :
                            ph = " ".join(candidates)
                            no_sp_ph = "".join(candidates)

                            if no_sp_ph in doosan_term or no_sp_ph in wiki_term:
                                if not no_sp_ph in except_list :
                                    try :
                                        test = int(no_sp_ph)
                                    except :
                                        result.append(ph)
                                break
                            else :
                                candidates = candidates[:-1]

                        if len(candidates) == 0 :
                            nouns = nouns[1:]
                        else :
                            nouns = nouns[len(candidates):]

                    result1 = result
                    #print(result, end="\n")


                    tagger = konlpy.tag.Hannanum()

                    nouns = []
                    pos = tagger.pos(sentence)

                    for p in pos :
                        if p[1] == 'N' or p[1] == 'F' :
                            nouns.append(p[0])

                    result = []
                    while not len(nouns) == 0:
                        candidates = nouns[:]
                        while not len(candidates) == 0:
                            ph = " ".join(candidates)
                            no_sp_ph = "".join(candidates)

                            if no_sp_ph in doosan_term or no_sp_ph in wiki_term:
                                if not no_sp_ph in except_list:
                                    result.append(ph)
                                break
                            else:
                                candidates = candidates[:-1]

                        if len(candidates) == 0:
                            nouns = nouns[1:]
                        else:
                            nouns = nouns[len(candidates):]

                    result2 = result
                    #print(result, end="\n")

                    result = []
                    split_result1 = []
                    for r in result1 :
                        for token in r.split():
                            split_result1.append(token)

                    split_result2 = []
                    for r in result2:
                        for token in r.split():
                            split_result2.append(token)

                    result = []
                    for a in result1 :
                        for token in split_result2 :
                            if token in a or token == a:
                                if a not in result :
                                    result.append(a)
                                break

                    for b in result2 :
                        for token in split_result1 :
                            if token in b or token == b :
                                if b not in result:
                                    result.append(b)
                                break

                    cds_sentence = original_sentence.replace(" ","")
                    cds_result = []
                    for r in result :
                        cds_result.append(r.replace(" ",""))

                    for concept in cds_result :

                        index = [m.start() for m in re.finditer(concept, cds_sentence)]
                        ts_index = [m.start() for m in re.finditer("<", cds_sentence)]
                        te_index = [m.start() for m in re.finditer(">", cds_sentence)]

                        new_index = []
                        if not ("<" in cds_sentence):
                            new_index = index
                            pass
                        else :
                            for i in index :
                                contained = False
                                for k in range(len(ts_index)) :
                                    if (i > ts_index[k] and i < te_index[k]) :
                                        contained = True
                                        break
                                if not contained :
                                    new_index.append(i)

                        index = new_index


                        if concept in doosan_term :
                            doosan_type = doosan_term[concept]
                        if concept in wiki_term :
                            wiki_type = wiki_term[concept]

                        p_index = [m.start() for m in re.finditer("'", doosan_type)]
                        type = []
                        type_except = ["두산대백과"]
                        for i in range(len(p_index)) :
                            if i % 2 == 0 :
                                _type = doosan_type[p_index[i]+1:p_index[i+1]]
                                if not _type in type and not _type in type_except :
                                    type.append(_type)
                        str_type=",".join(type)

                        for i in index :
                            cds_sentence = cds_sentence[:i] + "<C type=\"" +str_type+ "\">" + cds_sentence[i:i+len(concept)] + "</C>" + cds_sentence[i+len(concept):]

                    ts_index = [m.start() for m in re.finditer("<", cds_sentence)]
                    te_index = [m.start() for m in re.finditer(">", cds_sentence)]
                    #print(original_sentence, end="")
                    final_sentence = ""
                    pointer = 0
                    i = 0
                    while(pointer < len(original_sentence)) :
                        if original_sentence[pointer] != cds_sentence[i] :
                            if cds_sentence[i] != "<":
                                final_sentence += original_sentence[pointer]
                                pointer += 1
                            else :
                                while (cds_sentence[i] != ">"):
                                    final_sentence += cds_sentence[i]
                                    i += 1
                                final_sentence += ">"
                                i += 1
                                continue

                        else :
                            final_sentence += original_sentence[pointer]
                            i += 1
                            pointer += 1



                    #print(final_sentence)

                    result_list = line.split("\t")
                    result_list[3] = final_sentence
                    output = "\t".join(result_list) + "\n"
                    output_file.write(output)
                    cnt += 1
                    break

                except :
                    cnt += 1
                    print("Error occured. Saved in Error log file")
                    error_file.write(str(line) + "\n")
                    break

        p1.close()
        p2.close()
        f.close()
        output_file.close()
        error_file.close()

def main(args) :
    extract_concept(int(args[0]), int(args[1]))

if __name__ == '__main__' :
    main(sys.argv[1:])