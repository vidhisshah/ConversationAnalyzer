# coding: utf-8

## Objective: Analyze a whatsapp conversation

import matplotlib.pyplot as plt
import wordcloud
import re
import collections

date_and_name = '\d{1,}/\d{1,}/\d\d,\s\d\d:\d\d\s-(\s\w+){1,}:'
all_words_in_chat = ""
time_list = ""
chat_string = ""
chat_string_without_stopwords = ""
person_set = set()
person_list = []
person_dict = {}
chat_per_person = {}

#Read a whatsapp conversation
with open('demo.txt', 'r') as text:
    all_content = text.readlines()

#Creates list of statements while stripping the time stamp and name
def create_corpus_complete():
    global all_words_in_chat, time_list, all_content, chat_string, chat_string_without_stopwords
    chat_statements = []
    time_list = []
    for statement in all_content:
         if(re.match(date_and_name, statement)):
            chat_statements.append(re.sub(date_and_name,'',statement))
            time_list.append(re.search('\d\d:', statement).group(0))
    chat_string = ' '.join(word for word in chat_statements)
    chat_string = chat_string.replace("<Media omitted>\n", "")
    chat_string = chat_string.replace("Missed voice call", "")
    all_words_in_chat = re.findall(r'\w+', chat_string)
    chat_string_without_stopwords = [word for word in all_words_in_chat if word not in wordcloud.STOPWORDS]

#who texts more
def who_texts_more():
    global person_set, person_list, person_dict
    for statement in all_content:
         if(re.match(date_and_name, statement)):
                temp = re.sub('\d{1,}/\d{1,}/\d\d,\s\d\d:\d\d\s-','',statement)
                person_list.append(temp.split()[0])
                person_set.add(temp.split()[0])    
    for person_num in range(len(person_set)):
        person_dict[list(person_set)[person_num]] = person_list.count(list(person_set)[person_num])  


#create strings for individual persons
def create_corpus_per_person():
    global chat_per_person
    for person in person_dict.keys():
        chat_statements_per_person = []
        for statement in all_content:
            if(re.findall(person, statement)):
                chat_statements_per_person.append(re.sub(date_and_name,'',statement))
            chat_string_per_person = ' '.join(word for word in chat_statements_per_person)
            chat_string_per_person = chat_string_per_person.replace('<Media omitted>\n', "")
        chat_per_person[person] = chat_string_per_person   


#finds the most common word in a list of words
def most_common(list_of_words):
    return max(set(list_of_words), key=list_of_words.count)


def display_stats():
    global person_set, person_list, person_dict, all_words_in_chat, time_list
    print("=============================Stats for chat================================")
    print("Number of words:", len(all_words_in_chat))
    print("Number of Unique words:", len(set(all_words_in_chat)))
    print("Most common word:", collections.Counter(all_words_in_chat).most_common(1)[0][0])
    print("Time when you text each other the most:", most_common(time_list)[:2]+" 'o' clock")
    print()
    print("Individual stats per person" )
    print("Message count per person:")
    for key, val in person_dict.items():
        print(key +': '+ str(val))
    print("Most common word per person:")
    for key in person_dict.keys():
        print(key +": "+most_common(re.findall(r'\w+', chat_per_person[key])))
    print("===========================================================================")    

# Create and save word cloud 
def create_word_cloud():    
    global chat_string_without_stopwords
    word_cloud = wordcloud.WordCloud(width=600, height=300, max_words=300).generate(' '.join(word for word in chat_string_without_stopwords))
    plt.figure(figsize=(25,25))
    plt.imshow(word_cloud)
    plt.axis("off")
    plt.savefig('conversation.png')
    plt.close()

create_corpus_complete()
who_texts_more()
create_corpus_per_person()
display_stats()
create_word_cloud()