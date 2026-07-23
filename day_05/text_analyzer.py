from day_04.file_word_counter import read_file,count_words,find_top
import json

def main():
    filepath = input("Enter the filepath:")
    file_content = read_file(filepath)
    frequency = count_words(file_content)
    top_words = find_top(frequency)
    if top_words is None:
        print("Could not process file. Please check the filepath and try again.")
        return
    output_path = "text_analyzer_report.json"
    save_reports(top_words,output_path)
    text_size(file_content,output_path)

def save_reports(top_words,outputpath):
    report = {"top_words": [{"word":w,"count":c} for w,c in top_words]}
    with open(outputpath,"w") as f:
        json.dump(report,f,indent=2)

def text_size(file_content,outputpath):
    with open(outputpath,"r") as f:
        data = json.load(f)
    if file_content is None:
        return None
    elif len(file_content.split()) <= 50:
        data["size"] = "Short"
    elif len(file_content.split()) <= 200:
        data["size"] = "Medium"
    elif len(file_content.split()) > 200:
        data["size"] = "Long"
    with open(outputpath,"w") as f:
        json.dump(data,f,indent=4)    

if __name__ == "__main__":
    main()


