"""
Tokenizer for text processing optimized for word embedding models like Word2Vec and GloVe.
"""

import re
import string
import unicodedata
from typing import List, Dict, Set, Tuple, Optional, Callable, Union, Iterator
import logging
from collections import Counter
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords

# Ensure NLTK resources are available
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')


class Tokenizer:
    """Flexible tokenizer for text preprocessing and tokenization."""
    
    def __init__(
        self,
        lowercase: bool = True,
        remove_punctuation: bool = True,
        remove_digits: bool = False,
        remove_stopwords: bool = False,
        stem: bool = False,
        lemmatize: bool = False,
        min_token_length: int = 1,
        max_token_length: Optional[int] = None,
        language: str = 'english',
        custom_stopwords: Optional[Set[str]] = None,
        custom_filters: Optional[List[Callable[[str], str]]] = None,
        keep_n_grams: Optional[List[int]] = None,
        n_gram_delimiter: str = '_'
    ):
        """
        Initialize the tokenizer with specified preprocessing options.
        
        Args:
            lowercase: Convert text to lowercase
            remove_punctuation: Remove punctuation
            remove_digits: Remove numeric digits
            remove_stopwords: Remove common stopwords
            stem: Apply stemming (Porter stemmer)
            lemmatize: Apply lemmatization (WordNet lemmatizer)
            min_token_length: Minimum length for a token to be kept
            max_token_length: Maximum length for a token to be kept (None = no limit)
            language: Language for stopwords and other language-specific processing
            custom_stopwords: Additional stopwords to remove
            custom_filters: List of custom filter functions for additional preprocessing
            keep_n_grams: List of n-gram sizes to generate (e.g., [2, 3] for bigrams and trigrams)
            n_gram_delimiter: Character to join n-gram components
        """
        self.lowercase = lowercase
        self.remove_punctuation = remove_punctuation
        self.remove_digits = remove_digits
        self.remove_stopwords = remove_stopwords
        self.stem = stem
        self.lemmatize = lemmatize
        self.min_token_length = min_token_length
        self.max_token_length = max_token_length
        self.language = language
        self.custom_filters = custom_filters or []
        self.keep_n_grams = keep_n_grams or []
        self.n_gram_delimiter = n_gram_delimiter
        
        # Set up stopwords
        if remove_stopwords:
            self.stopwords = set(stopwords.words(language))
            if custom_stopwords:
                self.stopwords.update(custom_stopwords)
        else:
            self.stopwords = set()
            if custom_stopwords:
                self.stopwords = custom_stopwords
        
        # Set up stemmers and lemmatizers if needed
        if stem:
            self.stemmer = PorterStemmer()
        
        if lemmatize:
            self.lemmatizer = WordNetLemmatizer()
        
        # Set up punctuation translation table
        if remove_punctuation:
            self.punctuation_table = str.maketrans('', '', string.punctuation)
        
        # Set up digit translation table
        if remove_digits:
            self.digit_table = str.maketrans('', '', string.digits)
    
    def _preprocess_text(self, text: str) -> str:
        """Apply preprocessing steps to text."""
        # Apply lowercasing
        if self.lowercase:
            text = text.lower()
        
        # Apply custom filters
        for filter_fn in self.custom_filters:
            text = filter_fn(text)
        
        # Remove punctuation
        if self.remove_punctuation:
            text = text.translate(self.punctuation_table)
        
        # Remove digits
        if self.remove_digits:
            text = text.translate(self.digit_table)
        
        return text
    
    def _process_token(self, token: str) -> str:
        """Apply token-level processing (stemming, lemmatization)."""
        # Apply stemming
        if self.stem:
            token = self.stemmer.stem(token)
        
        # Apply lemmatization
        if self.lemmatize:
            token = self.lemmatizer.lemmatize(token)
        
        return token
    
    def _is_valid_token(self, token: str) -> bool:
        """Check if token meets criteria for inclusion."""
        # Check minimum length
        if len(token) < self.min_token_length:
            return False
        
        # Check maximum length
        if self.max_token_length and len(token) > self.max_token_length:
            return False
        
        # Check if token is a stopword
        if token in self.stopwords:
            return False
        
        # Remove tokens that are just whitespace
        if token.strip() == '':
            return False
        
        return True
    
    def _generate_n_grams(self, tokens: List[str]) -> List[str]:
        """Generate n-grams from tokens."""
        result = tokens.copy()
        
        for n in self.keep_n_grams:
            if n < 2 or n > len(tokens):
                continue
                
            for i in range(len(tokens) - n + 1):
                n_gram = self.n_gram_delimiter.join(tokens[i:i+n])
                result.append(n_gram)
        
        return result
    
    def tokenize_text(self, text: str) -> List[str]:
        """
        Tokenize a single text string according to configured options.
        
        Args:
            text: Input text to tokenize
            
        Returns:
            List of processed tokens
        """
        # Normalize unicode
        text = unicodedata.normalize('NFKD', text)
        
        # Apply preprocessing
        text = self._preprocess_text(text)
        
        # Tokenize into words
        tokens = word_tokenize(text, language=self.language)
        
        # Process tokens
        processed_tokens = []
        for token in tokens:
            # Apply token-level processing
            processed = self._process_token(token)
            
            # Check if token is valid
            if self._is_valid_token(processed):
                processed_tokens.append(processed)
        
        # Generate n-grams if specified
        if self.keep_n_grams:
            processed_tokens = self._generate_n_grams(processed_tokens)
        
        return processed_tokens
    
    def tokenize_texts(self, texts: List[str]) -> List[List[str]]:
        """
        Tokenize a list of texts.
        
        Args:
            texts: List of texts to tokenize
            
        Returns:
            List of lists of tokens
        """
        return [self.tokenize_text(text) for text in texts]
    
    def tokenize_into_sentences(self, text: str) -> List[List[str]]:
        """
        Tokenize text into sentences, then tokenize each sentence into words.
        
        Args:
            text: Input text
            
        Returns:
            List of lists of tokens, where each inner list represents a sentence
        """
        # Split into sentences
        sentences = sent_tokenize(text, language=self.language)
        
        # Tokenize each sentence
        return self.tokenize_texts(sentences)
    
    def build_vocab(
        self, 
        texts: List[str], 
        min_count: int = 5, 
        max_vocab_size: Optional[int] = None
    ) -> Dict[str, int]:
        """
        Build vocabulary from texts.
        
        Args:
            texts: List of texts to process
            min_count: Minimum occurrence count to include a token
            max_vocab_size: Maximum vocabulary size (None = no limit)
            
        Returns:
            Dictionary mapping tokens to their indices
        """
        # Tokenize all texts
        all_tokens = []
        for text in texts:
            all_tokens.extend(self.tokenize_text(text))
        
        # Count tokens
        counter = Counter(all_tokens)
        
        # Filter by min_count
        filtered_tokens = [(token, count) for token, count in counter.items() 
                           if count >= min_count]
        
        # Sort by frequency (most frequent first)
        sorted_tokens = sorted(filtered_tokens, key=lambda x: x[1], reverse=True)
        
        # Limit vocab size if specified
        if max_vocab_size:
            sorted_tokens = sorted_tokens[:max_vocab_size]
        
        # Create word to index mapping
        vocab = {token: idx for idx, (token, _) in enumerate(sorted_tokens)}
        
        return vocab
    
    def prepare_for_word_embeddings(
        self, 
        texts: List[str],
        min_count: int = 5,
        max_vocab_size: Optional[int] = None
    ) -> Tuple[List[List[str]], Dict[str, int]]:
        """
        Prepare texts for word embedding models like Word2Vec or GloVe.
        
        Args:
            texts: List of raw text strings
            min_count: Minimum occurrence count to include a token
            max_vocab_size: Maximum vocabulary size (None = no limit)
            
        Returns:
            Tuple of (tokenized_texts, vocabulary)
        """
        # Tokenize texts
        tokenized_texts = self.tokenize_texts(texts)
        
        # Count all tokens
        counter = Counter()
        for tokens in tokenized_texts:
            counter.update(tokens)
        
        # Filter by min_count
        filtered_tokens = [(token, count) for token, count in counter.items() 
                          if count >= min_count]
        
        # Sort by frequency
        sorted_tokens = sorted(filtered_tokens, key=lambda x: x[1], reverse=True)
        
        # Limit vocab size if specified
        if max_vocab_size:
            sorted_tokens = sorted_tokens[:max_vocab_size]
        
        # Create vocab
        vocab = {token: idx for idx, (token, _) in enumerate(sorted_tokens)}
        
        return tokenized_texts, vocab


# Helper functions for common text cleaning tasks
def clean_html(text: str) -> str:
    """Remove HTML tags from text."""
    html_pattern = re.compile('<.*?>')
    return html_pattern.sub('', text)

def clean_urls(text: str) -> str:
    """Remove URLs from text."""
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub('', text)

def clean_emojis(text: str) -> str:
    """Remove emojis from text."""
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F700-\U0001F77F"  # alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002702-\U000027B0"  # Dingbats
        "\U000024C2-\U0001F251" 
        "]+"
    )
    return emoji_pattern.sub('', text)

def clean_multiple_spaces(text: str) -> str:
    """Replace multiple spaces with single space."""
    return re.sub(r'\s+', ' ', text).strip()


# Example usage
def example_usage():
    texts = [
        "Hello world! This is an example sentence for tokenization.",
        "Word2Vec and GloVe are popular word embedding models.",
        "NLP tasks often require preprocessing steps like stemming and lemmatization.",
        "The quick brown fox jumps over the lazy dog.",
    ]
    
    # Basic tokenizer
    tokenizer = Tokenizer(
        lowercase=True,
        remove_punctuation=True,
        remove_stopwords=True,
        language='english'
    )
    
    # Tokenize texts
    tokenized_texts = tokenizer.tokenize_texts(texts)
    print(f"Tokenized texts: {tokenized_texts}")
    
    # Prepare for word embeddings
    processed_texts, vocab = tokenizer.prepare_for_word_embeddings(texts, min_count=1)
    print(f"Vocabulary size: {len(vocab)}")
    print(f"Vocabulary: {vocab}")
    
    # Demonstrate tokenizing with n-grams
    n_gram_tokenizer = Tokenizer(
        lowercase=True,
        remove_punctuation=True,
        keep_n_grams=[2, 3]
    )
    
    tokenized_with_ngrams = n_gram_tokenizer.tokenize_text(texts[0])
    print(f"With n-grams: {tokenized_with_ngrams}")