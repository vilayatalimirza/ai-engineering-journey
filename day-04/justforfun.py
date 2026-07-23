import json

data = {"aaa":"bbb","count":2}

json_string = json.dumps(data)
with open("output.json","w") as f:
    json.dump(data,f)

loaded = json.loads(json_string)
with open("output.json","r") as f:
    loaded_from_file = json.load(f)





from file_word_counter import count_words
text = input("SAy sunm: ").strip()
frequency = count_words(text)
words = []
counts = []
for word,count in frequency.items():
    print(word,count)
    words.append(word)
    counts.append(count)
    print(words,counts)



