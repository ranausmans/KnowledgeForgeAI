import re
import nltk
from typing import List

nltk.download('punkt')
nltk.download('stopwords')

class TextCleaner:
    def __init__(self):
        self.stop_words = set(nltk.corpus.stopwords.words('english'))

    def clean_text(self, text: str) -> str:
        text = re.sub(r'<.*?>', '', text)
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        return text.lower()

    def tokenize(self, text: str) -> List[str]:
        return nltk.word_tokenize(text)

    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        return [token for token in tokens if token not in self.stop_words]

    def preprocess(self, text: str) -> List[str]:
        cleaned_text = self.clean_text(text)
        tokens = self.tokenize(cleaned_text)
        return self.remove_stopwords(tokens)
