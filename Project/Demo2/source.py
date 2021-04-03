#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from datetime import datetime
from datetime import date
import time
import numpy as np
from tkinter import Tk, Canvas, BOTH, Label


now = datetime.now()
driver = webdriver.Chrome()

#https://www.nytimes.com/crosswords/game/special/tricky-clues-mini
driver.get('https://www.nytimes.com/crosswords/game/mini')
time.sleep(0.2)
driver.find_element_by_xpath("/html/body/div[1]/div/div/div[4]/div/main/div[2]/div/div[2]/div[3]/div/article/div[2]/button/div/span").click()
time.sleep(0.2)
driver.find_element_by_xpath("/html/body/div[1]/div/div/div[4]/div/main/div[2]/div/div/ul/div[2]/li[2]/button").click()
time.sleep(0.2)
driver.find_element_by_xpath("/html/body/div[1]/div/div/div[4]/div/main/div[2]/div/div/ul/div[2]/li[2]/ul/li[3]/a").click()
time.sleep(0.2)
driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/article/div[2]/button[2]/div").click()
time.sleep(0.2)
driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/span").click()

hint_list = {} #fill later
keywords = ("Across", "Down")

index = 0
prev_no = 0

clues_of_across = []
clues_of_down = []

clues = driver.find_elements_by_class_name("Clue-text--3lZl7")
numbers = driver.find_elements_by_class_name("Clue-label--2IdMY")

for number, clue in zip(numbers, clues):
    no = number.get_property("textContent")
    content = clue.get_property("textContent")
    if (int(no) < prev_no):
        index = 1
    s = keywords[index] + ":\t" + no + " " + content + "\n"
    print(s)
    if index == 0:
        clues_of_across.append([keywords[0],no,content])
    else:
        clues_of_down.append([keywords[1], no, content])
    prev_no = int(no)


reveals = {}
for i in range(25):
    reveal = driver.find_element_by_id("cell-id-{i}".format(i=i))
    reveal_sibs = reveal.get_property("parentNode").get_property("childElementCount")
    if reveal_sibs == 1:
        s = str(i + 1) + ":\tblack" + "\n"
        reveals[i + 1] = ("black","","")
    elif reveal_sibs == 3:
        value = reveal.get_property("parentNode").get_property("childNodes")[1].get_property("textContent")
        s = str(i + 1) + ":\twhite " + value + "\n"

        reveals[i + 1] = ("white", value,"")
    elif reveal_sibs == 4:
        number = reveal.get_property("parentNode").get_property("childNodes")[1].get_property("textContent")
        value = reveal.get_property("parentNode").get_property("childNodes")[2].get_property("textContent")
        s = str(i + 1) + ":\twhite " + value + " " + number + "\n"
        reveals[i + 1] = ("white", value, number)

print(reveals)

#drawing shape part
# x = 0
# root = Tk()
# canvas = Canvas(root, width=1500, height=750)
# canvas.configure(bg="white")

# for i in range(5):
#     for j in range(5):
#         x += 1
#         if reveals[x][0] == "black":
#             canvas.create_rectangle(100 * (j + 1), 100 * (i + 1), 100 + (100 * (j + 1)), 100 + (100 * (i + 1)), fill="black")
#         elif reveals[x][2] != "":
#             canvas.create_rectangle(100 * (j + 1), 100 * (i + 1), 100 + (100 * (j + 1)), 100 + (100 * (i + 1)), fill="white")
#             canvas.create_text((100 * (j + 1)) + 50, (100 * (i + 1)) + 50, fill="blue", font="Arial 40 bold", text=reveals[x][1][0])
#             canvas.create_text((100 * (j + 1)) + 10, (100 * (i + 1)) + 10, fill="black", font="Arial 15 ", text=reveals[x][2])
#         else:
#             canvas.create_rectangle(100 * (j + 1), 100 * (i + 1), 100 + (100 * (j + 1)), 100 + (100 * (i + 1)), fill="white")
#             canvas.create_text((100 * (j + 1)) + 50, (100 * (i + 1)) + 50, fill="blue", font="Arial 40 bold",text=reveals[x][1][0])

# #canvas.create_text(700, 140, fill="black", font="Arial 20 bold", text="ACROSS")
# #
# #for i in range(len(clues_of_across)):
# #    canvas.create_text(640, 170 + (i*20), fill="gray", font="Arial 15", text=clues_of_across[i][1] + " " + clues_of_across[i][2], anchor="w")
# #
# #canvas.create_text(680, 170 + (len(clues_of_across)+2)*20, fill="black", font="Arial 20 bold", text="DOWN")
# #
# #for i in range(len(clues_of_down)):
# #    canvas.create_text(640, 170 + (len(clues_of_across)+4)*20 + (i*20), fill="gray", font="Arial 15", text=clues_of_down[i][1] + " " + clues_of_down[i][2], anchor="w")
# #
# #
date = driver.find_element_by_class_name("PuzzleDetails-date--1HNzj").get_attribute("textContent")
# canvas.create_text(465, 615, fill="black", font="Arial 10", text="SWAPLIANO/ " + date)
# canvas.pack(fill=BOTH, expand=1)

# root.title("Swapliano")

downWords = []
acrossWords = []
aIndex = []
dIndex = []

for i in range(5):
    aWord = ''
    isFirst = True
    for k in range(5):
        (c1,l1,n1) = reveals[i * 5 + k +1]
        aWord += l1[0:1]
        if isFirst and n1 != '':
            aIndex.append(n1)
            isFirst = False
    acrossWords.append(aWord)

for i in range(5):
    dWord = ''
    isFirst = True
    for k in range(5):
        (c2,l2,n2) = reveals[k * 5 + i +1]
        dWord += l2[0:1]
        if isFirst and n2 != '':
            dIndex.append(n2)
            isFirst = False
    downWords.append(dWord)
print(downWords)
print(acrossWords)
aSort = np.argsort(np.asarray(aIndex).astype(int))
dSort = np.argsort(np.asarray(dIndex).astype(int))
print(aSort)
print(dSort)

downWords = np.asarray(downWords)[dSort]
acrossWords = np.asarray(acrossWords)[aSort]

print(downWords)
print(acrossWords)


# In[2]:


def fix_data(string):
    a = ['0','1','2','3','4','5','6','7','8','9']
    output = string.split('\n')
    for i in range(len(output)):
        for j in range(len(a)):
            if output[i][0] == a[j]:
                output[i] = output[i][3:]
    return output


# In[3]:


from collections import defaultdict

clueDict = defaultdict(list)
for word in acrossWords:
    clueDict[word] = []
    driver.get('https://www.urbandictionary.com/define.php?term=' + str.lower(word))
    for i in range(1,5):
        if i != 2:
            try:
                temp = driver.find_element_by_xpath('/html/body/div[2]/div[4]/div/div/div[1]/div[1]/div[' + str(i) + ']/div[3]').get_property('textContent')
                temp = fix_data(temp)
                for val in temp:
                    if len(val) < 90:
                        clueDict[word].append(val)
            except:
                break
for word in downWords:
    clueDict[word] = []
    driver.get('https://www.urbandictionary.com/define.php?term=' + str.lower(word))
    for i in range(1,5):
        if i != 2:
            try:
                temp = driver.find_element_by_xpath('/html/body/div[2]/div[4]/div/div/div[1]/div[1]/div[' + str(i) + ']/div[3]').get_property('textContent')
                temp = fix_data(temp)
                for val in temp:
                    if len(val) < 90:
                        clueDict[word].append(val)
            except:
                break


# In[4]:


for word in downWords:
    print('*****')
    print('WORD IS: ' + word)
    print(clueDict[word])
    print('**********')
    
for word in acrossWords:
    print('*****')
    print('WORD IS: ' + word)
    print(clueDict[word])
    print('**********')


# In[5]:


for word in acrossWords:
    driver.get('https://www.dictionary.com/browse/' + str.lower(word))
    for i in range(1):
        try:
            temp = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div/main/section/section/div[1]/section[2]/div/div').get_property('textContent')
            if len(temp) < 90:
                clueDict[word].append(temp)
        except:
            break

for word in downWords:
    driver.get('https://www.dictionary.com/browse/' + str.lower(word))
    for i in range(1):
        try:
            temp = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div/main/section/section/div[1]/section[2]/div/div').get_property('textContent')
            if len(temp) < 90:
                clueDict[word].append(temp)
        except:
            break


# In[6]:


for word in downWords:
    print('*****')
    print('WORD IS: ' + word)
    print(clueDict[word])
    print('**********')
    
for word in acrossWords:
    print('*****')
    print('WORD IS: ' + word)
    print(clueDict[word])
    print('**********')


# In[7]:


from nltk.corpus import wordnet

for word in downWords:
    syns = wordnet.synsets(word)
    if syns:
        clueDict[word].append(syns[0].definition())
for word in acrossWords:
    syns = wordnet.synsets(word)
    if syns:
        clueDict[word].append(syns[0].definition())


# In[8]:


for word in downWords:
    print('*****')
    print('WORD IS: ' + word)
    print(clueDict[word])
    print('**********')
    
for word in acrossWords:
    print('*****')
    print('WORD IS: ' + word)
    print(clueDict[word])
    print('**********')


# In[9]:


badWords2 = ['pussy', 'vagina', 'dick', 'cock', 'penis', 'booty', 'boobs', 'fuck']
def profanityFilter2(clue, badWords):
    bool = False
    for i in range(len(badWords)):
        if(badWords[i] in clue):
            bool = True
    return bool


# In[10]:


for word in downWords:
    bool2 = False
    for i in range(clueDict[word].__len__()):
        bool = profanityFilter2(clueDict[word][i], badWords2)
        if bool == True:
            print('Word: ' + word + ' index: ' + str(i))
            print('Clue: ' + clueDict[word][i])
            temp1 = word
            temp2 = i
            bool2 = True
    if bool2 == True:
        del clueDict[temp1][temp2]
for word in acrossWords:
    bool2 = False
    for i in range(clueDict[word].__len__()):
        bool = profanityFilter2(clueDict[word][i], badWords2)
        if bool == True:
            print('Word: ' + word + ' index: ' + str(i))
            print('Clue: ' + clueDict[word][i])
            temp1 = word
            temp2 = i
            bool2 = True
    if bool2 == True:
        del clueDict[temp1][temp2]


# In[11]:


for word in downWords:
    print('*****')
    print('WORD IS: ' + word)
    print(clueDict[word])
    print('**********')
    
for word in acrossWords:
    print('*****')
    print('WORD IS: ' + word)
    print(clueDict[word])
    print('**********')


# In[12]:


for word in downWords:
    if len(clueDict[word]) == 0:
        first = word[0]
        print(first)
        rest = word[1:]
        driver.get('https://www.urbandictionary.com/define.php?term=' + str.lower(rest))
        for i in range(1,5):
            if i != 2:
                try:
                    temp = driver.find_element_by_xpath('/html/body/div[2]/div[4]/div/div/div[1]/div[1]/div[' + str(i) + ']/div[3]').get_property('textContent')
                    temp = fix_data(temp)
                    for val in temp:
                        if len(val) < 90:
                            clueDict[word].append(first + '  +  ' + val)
                except:
                    break
                    
        driver.get('https://www.dictionary.com/browse/' + str.lower(rest))
        for i in range(1):
            try:
                temp = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div/main/section/section/div[1]/section[2]/div/div').get_property('textContent')
                if len(temp) < 90:
                    clueDict[word].append(first + '  +  ' + temp)
            except:
                break 
            
for word in acrossWords:
    if len(clueDict[word]) == 0:
        first = word[0]
        print(first)
        rest = word[1:]
        driver.get('https://www.urbandictionary.com/define.php?term=' + str.lower(rest))
        for i in range(1,5):
            if i != 2:
                try:
                    temp = driver.find_element_by_xpath('/html/body/div[2]/div[4]/div/div/div[1]/div[1]/div[' + str(i) + ']/div[3]').get_property('textContent')
                    temp = fix_data(temp)
                    for val in temp:
                        if len(val) < 90:
                            clueDict[word].append(first + '  +  ' + val)
                except:
                    break
        driver.get('https://www.dictionary.com/browse/' + str.lower(rest))
        for i in range(1):
            try:
                temp = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div/main/section/section/div[1]/section[2]/div/div').get_property('textContent')
                if len(temp) < 90:
                    clueDict[word].append(first + '  +  ' + temp)
            except:
                break


# In[13]:


for word in downWords:
    print('*****')
    print('WORD IS: ' + word)
    print(clueDict[word])
    print('**********')
    
for word in acrossWords:
    print('*****')
    print('WORD IS: ' + word)
    print(clueDict[word])
    print('**********')


# In[14]:


for word in downWords:
    if clueDict[word].__len__() == 0:
        clueDict[word].append('NOT FOUND')
        
for word in acrossWords:
    if clueDict[word].__len__() == 0:
        clueDict[word].append('NOT FOUND')
        
for word in downWords:
    if clueDict[word].__len__() == 1:
        clueDict[word].append(clueDict[word][0])
        
for word in acrossWords:
    if clueDict[word].__len__() == 1:
        clueDict[word].append(clueDict[word][0])


# In[15]:


for word in downWords:
    print('*****')
    print('WORD IS: ' + word)
    print(clueDict[word])
    print('**********')
    
for word in acrossWords:
    print('*****')
    print('WORD IS: ' + word)
    print(clueDict[word])
    print('**********')


# In[16]:


import re
from emoji import UNICODE_EMOJI

_nonbmp = re.compile(r'[\U00010000-\U0010FFFF]')

def _surrogatepair(match):
    char = match.group()
    assert ord(char) > 0xffff
    encoded = char.encode('utf-16-le')
    return (
        chr(int.from_bytes(encoded[:2], 'little')) + 
        chr(int.from_bytes(encoded[2:], 'little')))

def with_surrogates(text):
    return _nonbmp.sub(_surrogatepair, text)

def is_emoji(s):
    count = 0
    for emoji in UNICODE_EMOJI:
        count += s.count(emoji)
        if count > 1:
            return False
    return True


# In[25]:


import random
x = 0
root = Tk()
canvas = Canvas(root, width=1500, height=750)
canvas.configure(bg="white")

for i in range(5):
    for j in range(5):
        x += 1
        if reveals[x][0] == "black":
            canvas.create_rectangle(100 * (j + 1), 100 * (i + 1), 100 + (100 * (j + 1)), 100 + (100 * (i + 1)), fill="black")
        elif reveals[x][2] != "":
            canvas.create_rectangle(100 * (j + 1), 100 * (i + 1), 100 + (100 * (j + 1)), 100 + (100 * (i + 1)), fill="white")
            canvas.create_text((100 * (j + 1)) + 50, (100 * (i + 1)) + 50, fill="blue", font="Arial 40 bold", text=reveals[x][1][0])
            canvas.create_text((100 * (j + 1)) + 10, (100 * (i + 1)) + 10, fill="black", font="Arial 15 ", text=reveals[x][2])
        else:
            canvas.create_rectangle(100 * (j + 1), 100 * (i + 1), 100 + (100 * (j + 1)), 100 + (100 * (i + 1)), fill="white")
            canvas.create_text((100 * (j + 1)) + 50, (100 * (i + 1)) + 50, fill="blue", font="Arial 40 bold",text=reveals[x][1][0])

#canvas.create_text(700, 140, fill="black", font="Arial 20 bold", text="ACROSS")
#
#for i in range(len(clues_of_across)):
#    canvas.create_text(640, 170 + (i*20), fill="gray", font="Arial 15", text=clues_of_across[i][1] + " " + clues_of_across[i][2], anchor="w")
#
#canvas.create_text(680, 170 + (len(clues_of_across)+2)*20, fill="black", font="Arial 20 bold", text="DOWN")
#
#for i in range(len(clues_of_down)):
#    canvas.create_text(640, 170 + (len(clues_of_across)+4)*20 + (i*20), fill="gray", font="Arial 15", text=clues_of_down[i][1] + " " + clues_of_down[i][2], anchor="w")
#
#
canvas.create_text(465, 615, fill="black", font="Arial 10", text="SWAPLIANO/ " + date)
canvas.pack(fill=BOTH, expand=1)

root.title("Swapliano")

for i in range(len(clues_of_across)):
    temp = is_emoji(clues_of_across[i][2])
    if temp == True:
        new = with_surrogates(clues_of_across[i][2])
        clues_of_across[i][2] = new

for i in range(len(clues_of_down)):
    temp = is_emoji(clues_of_down[i][2])
    if temp == True:
        new = with_surrogates(clues_of_down[i][2])
        clues_of_down[i][2] = new

canvas.create_text(700, 140, fill="black", font="Arial 20 bold", text="ACROSS")
for i in range(len(clues_of_across)):  
   # if i != 0:
    canvas.create_text(640, 170 + (i*40), fill="gray", font="Arial 15", text=clues_of_across[i][1] + " " + clues_of_across[i][2], anchor="w")
    canvas.create_text(640, 170 + (i * 40) + 20, fill="purple", font="Arial 15",text=clues_of_across[i][1] + " "+ random.choice(clueDict[acrossWords[i]]), anchor="w")

canvas.create_text(680, 170 + (len(clues_of_across)+2)*40, fill="black", font="Arial 20 bold", text="DOWN")
for i in range(len(clues_of_down)):
    canvas.create_text(640, 130 + (len(clues_of_across)+4)*40 + (i*40), fill="gray", font="Arial 15", text=clues_of_down[i][1] + " " + clues_of_down[i][2], anchor="w")
    canvas.create_text(640, 130 + (len(clues_of_across) + 4) * 40 + (i * 40) + 20, fill="purple", font="Arial 15",text=clues_of_down[i][1] + " " + random.choice(clueDict[downWords[i]]), anchor="w")



root.mainloop()


#SIMIARITY ÖLÇEĞİ
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


# In[ ]:




