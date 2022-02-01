from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import re

#returns dictionary of {term:freq}
def parse(file_name):
    path = open(file_name, "r")
    try:
        #open document and parse
        html = path.read()
        soup = BeautifulSoup(html, "lxml")
        #remove js
        for s in soup(["script", "style"]):
            s.decompose()

        #get readable text
        text = soup.get_text()

        # break into tokens and increment the frequency for the token
        tokens = re.findall('\w+', text)
        token_freq = dict()
        stop_words = set(stopwords.words('english'))
        
        for token in tokens:
            token = token.lower()
            if token not in stop_words:
                if token not in token_freq:
                    token_freq[token] = 1
                else:
                    token_freq[token] += 1
        return token_freq
    except:
        return {}
