import Constants
from nltk.corpus import stopwords

def getSubString(msg, skip_words = []):
    msg = msg.lower()
    words = msg.split(" ")
    stop_words = stopwords.words('english')
    stop_words.extend(Constants.USELESS_WORDS)
    stop_words.extend(skip_words)

    msg_list = []
    for word in words:
        for char in Constants.SPECIAL_CHARS:
            if char in word:
                word = word.replace(char, "")
        if word not in stop_words:
            msg_list.append(word)
    
    new_str = ""
    for i, word in enumerate(msg_list):
        if i>0:
            new_str = new_str + " " + word
        else:
            new_str = new_str + word
    
    return new_str

if __name__=="__main__":
    print(getSubString("Recommend me some movies similar to The Masked Gang.", skip_words=["recommend"]))