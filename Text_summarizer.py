import bs4 as bs
import urllib.request
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

class WebsiteSummarizer:
    def __init__(self, url):
        self.url = url

    def fetch_data(self):
        try:
            scraped_data = urllib.request.urlopen(self.url)
            data = scraped_data.read()
            return data
        except urllib.error.URLError as e:
            print(f"An error occurred while fetching the URL: {e}")
            return None

    @staticmethod
    def clean_text(text):
        # Remove square brackets and content within them
        text = re.sub(r'\[[0-9]*\]', '', text)
        # Remove extra whitespaces
        text = re.sub(r'\s+', ' ', text)
        return text

    def summarize(self):
        data = self.fetch_data()
        if data is None:
            return

        parsed_data = bs.BeautifulSoup(data, 'lxml')
        paragraphs = parsed_data.find_all('p')
        data_text = ""

        for p in paragraphs:
            data_text += p.text

        data_text = self.clean_text(data_text)
        sentence_list = nltk.sent_tokenize(data_text)

        stop_words = stopwords.words('french')

        word_frequencies = {}
        for word in word_tokenize(data_text):
            if word not in stop_words:
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1

        maximum_frequency = max(word_frequencies.values())

        for word in word_frequencies.keys():
            word_frequencies[word] = word_frequencies[word] / maximum_frequency

        sentence_scores = {}
        for sent in sentence_list:
            for word in word_tokenize(sent.lower()):
                if word in word_frequencies.keys():
                    if len(sent.split(' ')) < 30:
                        if sent not in sentence_scores.keys():
                            sentence_scores[sent] = word_frequencies[word]
                        else:
                            sentence_scores[sent] += word_frequencies[word]

        import heapq
        summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

        summary = ' '.join(summary_sentences)
        return summary

def main():
    url = 'http://www.istic.rnu.tn/fr/presentation/presentation.html'
    summarizer = WebsiteSummarizer(url)
    summary = summarizer.summarize()
    
    if summary:
        print(summary)

if __name__ == "__main":
    main()
