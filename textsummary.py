from heapq import nlargest
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation

text = """"A fan ran onto the pitch to get a selfie with Casemiro during Manchester United's Premier League clash with Crystal Palace.
The bizarre incident took place in the 55th minute at Selhurst Park with United leading 1-0 thanks to a late first-half strike from Bruno Fernandes, although they eventually drew 1-1 thanks to a late free-kick from Michael Olise.
The match was briefly interrupted when a fan from the home end wearing a bomber jacket ran onto the pitch and took a selfie with Casemiro in the middle of the pitch. The former Real Madrid star paused and put his arm around the fan to pose for the picture. Stewards appeared slow to react in attempting to stop the supporter and he was almost off the pitch again before he was met by security, as he was able to continue recording as he wandered off.
A Crystal Palace statement confirmed the supporter had been detained, writing: 'A single individual entered the field of play before being led away by security, and was later arrested.'
Fans have taken to social media to praise the Brazilian midfielder for his composed reaction to the fan.
"""

stopwords = list(STOP_WORDS)

nlp = spacy.load('en_core_web_sm')
doc = nlp(text)

tokens = [token.text for token in doc]

word_freq = {}
for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text] += 1

max_freq = max(word_freq.values())

for word in word_freq.keys():
        word_freq[word] = word_freq[word]/max_freq

sent_tokens = [sent for sent in doc.sents]

sent_scores = {}
for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] = word_freq[word.text]
                else:
                    sent_scores[sent] += word_freq[word.text]

select_len = int(len(sent_tokens) * 0.3)

summary = nlargest(select_len,sent_scores, key =sent_scores.get)

final_summary = [word.text for word in summary]
summary = ' '.join(final_summary)

print(text)

print(summary)

print("lenght of original text", len(text.split(' ')))
print("lenght of summary text", len(summary.split(' ')))
