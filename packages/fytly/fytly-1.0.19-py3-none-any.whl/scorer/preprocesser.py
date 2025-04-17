# preprocessor.scorer
import re
import string
import stanza
from nltk.corpus import stopwords
import nltk

# Download NLTK stopwords (run once or ensure it’s available)
nltk.download('stopwords')

# Download Stanza English model (only once)
stanza.download('en')

class GraderPreprocessor:
    nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma')  # Stanza pipeline
    stop_words = set(stopwords.words('english'))  # NLTK stopwords

    # Custom noise words (common resume "filler" terms)
    custom_noise = {
        "standard", "ix", "x", "class", "email", "phone", "number", "pin", "code",
        "address", "dob", "status", "unmarried", "gender", "female", "name",
        "language", "known", "detail", "percentage", "cgpa"
    }

    @staticmethod
    def preprocess(text: str) -> str:
        """
        Preprocess text by lowercasing, removing digits/punctuation, and lemmatizing.

        Args:
            text (str): Input text to preprocess

        Returns:
            str: Preprocessed text
        """
        # Lowercase the text
        text = text.lower()

        # Remove digits and punctuation
        text = re.sub(r'\d+', ' ', text)
        text = text.translate(str.maketrans('', '', string.punctuation))

        # Process text with Stanza
        doc = GraderPreprocessor.nlp(text)

        lemmatized_words = []
        for sentence in doc.sentences:
            for word in sentence.words:
                lemma = word.lemma
                if lemma and lemma not in GraderPreprocessor.stop_words and lemma not in GraderPreprocessor.custom_noise:
                    lemmatized_words.append(lemma)

        return ' '.join(lemmatized_words)
