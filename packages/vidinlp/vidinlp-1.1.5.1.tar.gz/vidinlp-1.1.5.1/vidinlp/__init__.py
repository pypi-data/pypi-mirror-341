import os
from pathlib import Path
import spacy
from typing import List, Tuple, Dict, Any, Optional, Union
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.metrics.pairwise import cosine_similarity
from functools import lru_cache
from collections import Counter, defaultdict
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import pandas as pd
import numpy as np


class VidiNLP:
    def __init__(
        self,
        model="en_core_web_sm",
        lexicon_path: Optional[str] = None,
        easy_word_list: Optional[str] = None,
    ):
        """
        Initialize VidiNLP with improved file handling.

        Args:
            model (str): Name of the spaCy model to load
            lexicon_path (str, optional): Path to the lexicon file
            easy_word_list (str, optional): Path to the Dale-Chall word list
        """
        try:
            self.nlp = spacy.load(model)
        except OSError:
            raise OSError(
                f"SpaCy model '{model}' not found. Please install it using: python -m spacy download {model}"
            )

        self.sia = SentimentIntensityAnalyzer()
        self.dictionary = None
        self.lda_model = None
        self.vectorizer = None
        self.classifier = None

        # Set default paths relative to the current file's location
        current_dir = Path(__file__).parent
        default_lexicon = current_dir / "data" / "lexicon.txt"
        default_word_list = current_dir / "data" / "chall_word_list.txt"

        # Try loading the word list
        try:
            self.easy_words = self.load_easy_word_list(
                easy_word_list if easy_word_list else default_word_list
            )
        except FileNotFoundError as e:
            print(
                f"Warning: Could not find word list file. Creating empty word list. Error: {e}"
            )
            self.easy_words = []

        # Initialize TF-IDF vectorizer
        self.tfidf_vectorizer = TfidfVectorizer(
            stop_words="english", ngram_range=(1, 2)
        )

        # Try loading the emotion lexicon
        try:
            self.emotion_lexicon = self.load_nrc_emotion_lexicon(
                lexicon_path if lexicon_path else default_lexicon
            )
        except FileNotFoundError as e:
            print(
                f"Warning: Could not find lexicon file. Creating empty lexicon. Error: {e}"
            )
            self.emotion_lexicon = {}

    @staticmethod
    def load_easy_word_list(file_path: str | Path) -> List[str]:
        """Load the Dale-Chall easy word list with better error handling."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return [line.strip().lower() for line in file if line.strip()]
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Could not find the word list file at {file_path}. "
                "Please ensure the file exists in the correct location or provide the correct path."
            )
        except Exception as e:
            raise Exception(f"Error reading word list file: {e}")

    @staticmethod
    def load_nrc_emotion_lexicon(lexicon_path: str | Path) -> Dict[str, Dict[str, int]]:
        """Load the NRC Emotion Lexicon with better error handling."""
        try:
            lexicon = {}
            with open(lexicon_path, "r", encoding="utf-8") as file:
                for line in file:
                    try:
                        word, emotion, score = line.strip().split("\t")
                        if word not in lexicon:
                            lexicon[word] = {}
                        lexicon[word][emotion] = int(score)
                    except ValueError:
                        print(
                            f"Warning: Skipping malformed line in lexicon: {line.strip()}"
                        )
                        continue
            return lexicon
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Could not find the lexicon file at {lexicon_path}. "
                "Please ensure the file exists in the correct location or provide the correct path."
            )
        except Exception as e:
            raise Exception(f"Error reading lexicon file: {e}")

    def tokenize(self, text: str) -> List[str]:
        """Tokenize the input text and returns a list of tokens."""
        doc = self.nlp(text)
        return [token.text for token in doc]

    def lemmatize(self, text: str) -> List[str]:
        """Lemmatize the input text and returns a list of lemmatized words."""
        doc = self.nlp(text)
        return [token.lemma_ for token in doc]

    def pos_tag(self, text: str) -> List[Tuple[str, str]]:
        """Returns a list of tuples wit the token and its part of speech tag."""
        doc = self.nlp(text)
        return [(token.text, token.pos_) for token in doc]

    def get_ngrams(
        self,
        text: str,
        n: int,
        top_n: int = 10,
        lowercase: bool = True,
        ignore_punct: bool = True,
    ) -> List[Tuple[str, int]]:
        """Lightning-fast n-gram extraction with punctuation handling.

        Args:
            text: Input text
            n: N-gram length (1=unigram, 2=bigram, etc.)
            top_n: Return top K most frequent n-grams
            lowercase: Convert text to lowercase
            ignore_punct: Skip punctuation-only tokens

        Returns:
            List of (ngram, count) tuples sorted by count (descending)
        """
        if lowercase:
            text = text.lower()

        # Tokenize with regex (faster than str.split() for punctuation handling)
        tokens = re.findall(r"\w+(?:'\w+)?", text) if ignore_punct else text.split()

        # Generate n-grams and count
        ngrams = zip(*[tokens[i:] for i in range(n)])
        counts = Counter(" ".join(g) for g in ngrams)

        return counts.most_common(top_n)

    def get_tfidf_ngrams_corpus(self, corpus, n=2, top_n=10, filter_stop=False):
        """
        Extract top n-grams from a corpus based on TF-IDF scores.

        :param corpus: A list of documents (strings) to use as the corpus.
        :param n: The value of 'n' for the n-grams (default is 2 for bigrams).
        :param top_n: The number of top n-grams to return based on TF-IDF score.
        :return: A list of tuples with the top n-grams and their respective TF-IDF scores.
        """
        # Initialize the TF-IDF Vectorizer with n-grams
        tfidf_vectorizer = TfidfVectorizer(ngram_range=(n, n))
        if filter_stop:
            tfidf_vectorizer.set_params(stop_words="english")

        # Fit and transform the corpus
        tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)

        # Get feature names (n-grams) and corresponding scores for the last document
        feature_names = tfidf_vectorizer.get_feature_names_out()
        scores = (
            tfidf_matrix[-1].toarray().flatten()
        )  # Get scores for the last document

        # Create a dictionary of n-grams and their TF-IDF scores
        ngram_scores = dict(zip(feature_names, scores))

        # Sort the n-grams by their scores in descending order
        sorted_ngrams = sorted(ngram_scores.items(), key=lambda x: x[1], reverse=True)

        # Return the top n n-grams
        return sorted_ngrams[:top_n]

    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze the sentiment of the input text using VADER."""
        return self.sia.polarity_scores(text)

    def clean_text(
        self,
        text: str,
        remove_stop_words: bool = False,
        remove_none_alpha: bool = False,
        remove_punctuations: bool = False,
        remove_numbers: bool = False,
        remove_html: bool = False,
        remove_urls: bool = False,
        remove_emojis: bool = False,
    ) -> str:
        """Clean and preprocess the input text with optional filters.
        Args: remove_stop_words: bool = False, remove_none_alpha: bool = False, remove_punctuations: bool = False, remove_html: bool = False, remove_urls: bool = False, remove_emojis: bool = False, remove_numbers: bool = False
        """
        # Early return for empty input
        if not text.strip():
            return ""

        # Remove HTML tags
        if remove_html:
            text = re.sub(r"<[^>]+>", "", text)
        if remove_urls:
            text = re.sub(r"https?://\S+|www\.\S+", "", text)
        if remove_emojis:
            emoji_pattern = re.compile(
                "["
                "\U0001f600-\U0001f64f"  # emoticons
                "\U0001f300-\U0001f5ff"  # symbols & pictographs
                "\U0001f680-\U0001f6ff"  # transport & map symbols
                "]+",
                flags=re.UNICODE,
            )
            text = emoji_pattern.sub("", text)
        # Remove extra spaces
        text = re.sub(r"\s+", " ", text).strip()

        # Process the text with the NLP model
        doc = self.nlp(text)

        # Clean tokens based on the provided options
        cleaned_tokens = []

        for token in doc:
            if remove_punctuations and token.is_punct:
                continue  # Skip punctuation if is_punct is True
            if remove_stop_words and token.is_stop:
                continue  # Skip stopwords if is_stop is True
            if remove_none_alpha and not token.is_alpha:
                continue  # Skip non-alphabetic words if is_alpha is True
            if remove_numbers and token.like_num:
                continue  # Skip numbers if is_num is True

            # Add the cleaned token (lowercased)
            cleaned_tokens.append(token.text.lower())

        # Return the cleaned text as a single string
        return " ".join(cleaned_tokens)

    def get_named_entities(self, text: str) -> List[Tuple[str, str]]:
        """Extract named entities from the input text and returns a list of tuples with entities and labels."""
        doc = self.nlp(text)
        return [(ent.text, ent.label_) for ent in doc.ents]

    def extract_keywords(self, text: str, top_n: int = 10) -> List[Tuple[str, float]]:
        """
        Extract keywords from the input text using TF-IDF and POS tagging.

        Args:
        text (str): The input text to extract keywords from.
        top_n (int): The number of top keywords to return.

        Returns:
        List[Tuple[str, float]]: A list of tuples containing keywords and their scores, rounded to 2 decimal points.
        """
        doc = self.nlp(text)

        # Preprocess text: lemmatize and remove stopwords, punctuation, and non-alphabetic tokens
        processed_text = " ".join(
            [
                token.lemma_.lower()
                for token in doc
                if not token.is_stop and not token.is_punct and token.is_alpha
            ]
        )

        # Calculate TF-IDF scores
        tfidf_matrix = self.tfidf_vectorizer.fit_transform([processed_text])
        feature_names = self.tfidf_vectorizer.get_feature_names_out()
        tfidf_scores = dict(zip(feature_names, tfidf_matrix.toarray()[0]))

        # Calculate POS tag scores (prioritize nouns, adjectives, and verbs)
        pos_scores = Counter()
        for token in doc:
            if token.pos_ in ["NOUN", "PROPN"]:
                pos_scores[token.lemma_.lower()] += 3
            elif token.pos_ in ["ADJ", "VERB"]:
                pos_scores[token.lemma_.lower()] += 2
            elif token.pos_ == "ADV":
                pos_scores[token.lemma_.lower()] += 1

        # Combine TF-IDF and POS scores
        combined_scores = {
            word: tfidf_scores.get(word, 0) * (1 + 0.1 * pos_scores.get(word, 0))
            for word in set(tfidf_scores) | set(pos_scores)
        }

        # Sort and return top k keywords with scores rounded to 2 decimal points
        top_keywords = sorted(
            [(word, round(float(score), 2)) for word, score in combined_scores.items()],
            key=lambda x: x[1],
            reverse=True,
        )[:top_n]

        return top_keywords

    def analyze_emotions(self, text: str) -> Dict[str, int]:
        """
        Analyze the emotions in the input text using the NRC Emotion Lexicon.

        Args:
        text (str): The input text to analyze emotions from.

        Returns:
        Dict[str, int]: A dictionary of emotions and their respective scores.
        """
        doc = self.nlp(text)
        emotion_scores = Counter()

        for token in doc:
            lemma = token.lemma_.lower()
            if lemma in self.emotion_lexicon:
                for emotion, score in self.emotion_lexicon[lemma].items():
                    emotion_scores[emotion] += score

        return dict(
            sorted(emotion_scores.items(), key=lambda item: item[1], reverse=True)
        )

    def topic_modelling(
        self,
        texts: List[str],
        num_topics: int = 5,
        min_df: int = 2,
        max_df: float = 0.95,
        min_word_length: int = 3,
    ) -> List[Dict[str, float]]:
        """
        Perform advanced topic modeling on text corpus.

        Args:
            texts: List of input text documents
            num_topics: Number of topics to extract
            min_df: Minimum document frequency for terms
            max_df: Maximum document frequency for terms
            min_word_length: Minimum length of words to consider

        Returns:
            List of topics with keywords and their weights
        """
        processed_texts = []
        for text in texts:
            doc = self.nlp(text)
            processed_texts.append(
                " ".join(
                    [
                        token.lemma_.lower()
                        for token in doc
                        if (
                            not token.is_stop
                            and token.is_alpha
                            and len(token.lemma_) >= min_word_length
                        )
                    ]
                )
            )

        vectorizer = CountVectorizer(stop_words="english", min_df=min_df, max_df=max_df)
        doc_term_matrix = vectorizer.fit_transform(processed_texts)

        lda = LatentDirichletAllocation(
            n_components=num_topics,
            random_state=42,
            max_iter=15,
            learning_method="online",
        )
        lda_output = lda.fit_transform(doc_term_matrix)

        feature_names = vectorizer.get_feature_names_out()
        topics = []

        for topic_idx, topic in enumerate(lda.components_):
            top_features_ind = topic.argsort()[: -10 - 1 : -1]
            top_features = [
                {"keyword": feature_names[i], "weight": topic[i]}
                for i in top_features_ind
            ]
            topics.append({f"Topic_{topic_idx+1}": top_features})

        return topics

    def compute_document_similarity(self, doc1, doc2):
        """Compute the similarity between two documents using TF-IDF and cosine similarity."""
        # Preprocess documents
        preprocessed_docs = [self.clean_text(doc) for doc in [doc1, doc2]]

        # Create TF-IDF matrix
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(preprocessed_docs)

        # Compute cosine similarity
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

        return similarity

    def find_similar_documents(self, query_doc, document_list, top_n=5):
        """Find the top N most similar documents to the query document."""
        # Preprocess all documents including the query
        preprocessed_docs = [
            self.clean_text(doc) for doc in [query_doc] + document_list
        ]

        # Create TF-IDF matrix
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(preprocessed_docs)

        # Compute cosine similarity between query and all other documents
        cosine_similarities = cosine_similarity(
            tfidf_matrix[0:1], tfidf_matrix[1:]
        ).flatten()

        # Get indices of top N similar documents
        similar_doc_indices = cosine_similarities.argsort()[: -top_n - 1 : -1]

        # Return list of tuples (document index, similarity score)
        return [(idx, cosine_similarities[idx]) for idx in similar_doc_indices]

    def aspect_based_sentiment_analysis(self, text: str) -> Dict[str, Dict[str, float]]:
        """
        Perform aspect-based sentiment analysis on the input text using custom sentiment analysis.

        Args:
        text (str): The input text to analyze.

        Returns:
        Dict[str, Dict[str, Any]]: A dictionary where keys are aspects and values are dictionaries
                                containing sentiment scores, confidence, and the associated text snippet.
        """
        doc = self.nlp(text)
        aspects = defaultdict(list)

        # Extract aspects (nouns) and their associated descriptors
        for token in doc:
            # Check if the token is a noun (aspect)
            if token.pos_ == "NOUN" or token.dep_ == "compound":
                has_modifier = False  # Track if aspect has any modifiers

                # Check for adjectives, adverbs, or other descriptors linked to the noun
                for child in token.children:
                    if child.dep_ in ["amod", "advmod", "nsubj", "attr", "prep"]:
                        aspects[token.text].append((child.text, token.sent))
                        has_modifier = True

                # If no modifiers are found, associate the whole sentence with the aspect
                if not has_modifier:
                    aspects[token.text].append((None, token.sent))

        # Analyze sentiment for each aspect
        results = {}

        for aspect, modifiers_and_sentences in aspects.items():
            sentiment_scores = []
            confidence_scores = []
            snippets = []

            for modifier, sentence in modifiers_and_sentences:
                if modifier:  # If there's a modifier, analyze the phrase
                    phrase = f"{modifier} {aspect}"
                    sentiment = self.analyze_sentiment(phrase)
                    sentiment_scores.append(sentiment["compound"])
                    confidence_scores.append(
                        abs(sentiment["compound"])
                    )  # Confidence based on absolute compound score
                    snippets.append(phrase)
                else:  # If no modifier, analyze the full sentence
                    sentence_text = sentence.text
                    sentiment = self.analyze_sentiment(sentence_text)
                    sentiment_scores.append(sentiment["compound"])
                    confidence_scores.append(
                        abs(sentiment["compound"])
                    )  # Confidence based on absolute compound score
                    snippets.append(sentence_text)

            # Average sentiment and confidence for the aspect
            avg_sentiment = (
                sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
            )
            avg_confidence = (
                sum(confidence_scores) / len(confidence_scores)
                if confidence_scores
                else 0
            )

            results[aspect] = {
                "sentiment": avg_sentiment,
                "confidence": avg_confidence,
                "snippets": snippets,
            }

        return results

    def summarize_absa_results(self, absa_results: Dict[str, Dict[str, float]]) -> str:
        """
        Summarize the aspect-based sentiment analysis results into a human-readable format.

        Args:
        absa_results (Dict[str, Dict[str, float]]): The aspect-based sentiment analysis results.

        Returns:
        str: A summary of the results.
        """
        summary = []

        for aspect, sentiment_data in absa_results.items():
            # Extract sentiment and confidence scores directly as floats
            sentiment_score = sentiment_data["sentiment"]  # This is already a float
            confidence = sentiment_data["confidence"]

            if sentiment_score > 0.25:
                sentiment_desc = "positive"
            elif sentiment_score < -0.25:
                sentiment_desc = "negative"
            else:
                sentiment_desc = "neutral"

            summary.append(
                f"The aspect '{aspect}' has a {sentiment_desc} sentiment "
                f"with a confidence of {confidence:.2f}."
            )

        return "\n".join(summary)

    def detect_linguistic_patterns(self, text: str) -> Dict[str, Any]:
        """
        Detect various linguistic patterns in the text including voice, sentence types,
        modality, and rhetorical devices.

        Args:
            text: Input text for analysis

        Returns:
            Dictionary containing detected patterns categorized by type
        """
        doc = self.nlp(text)

        patterns = {
            "voice": {"passive": [], "active": []},
            "sentence_structure": {
                "simple": [],
                "complex": [],
                "compound": [],
                "compound_complex": [],
            },
            "modality": {
                "conditionals": [],
                "hypotheticals": [],
                "imperatives": [],
                "subjunctive": [],
            },
            "cohesion_devices": {
                "temporal_markers": [],
                "causal_markers": [],
                "contrastive_markers": [],
            },
        }

        # Pattern matching rules
        modal_verbs = {
            "can",
            "could",
            "may",
            "might",
            "shall",
            "should",
            "will",
            "would",
            "must",
            "ought",
            "need",
            "dare",
            "used to",
            "have to",
            "has to",
            "had to",
        }

        temporal_markers = {
            "when",
            "while",
            "before",
            "after",
            "since",
            "as soon as",
            "once",
            "until",
            "by the time",
            "during",
            "then",
            "eventually",
            "meanwhile",
            "later",
            "soon",
        }

        causal_markers = {
            "because",
            "as",
            "since",
            "so",
            "therefore",
            "thus",
            "hence",
            "consequently",
            "as a result",
            "due to",
            "owing to",
            "that’s why",
        }

        contrastive_markers = {
            "but",
            "however",
            "although",
            "though",
            "even though",
            "yet",
            "still",
            "nevertheless",
            "nonetheless",
            "in contrast",
            "whereas",
            "on the other hand",
        }

        for sent in doc.sents:
            sent_text = sent.text.strip()
            verb_phrase = ""
            subject = ""

            # Voice detection with context
            has_passive = False
            has_active = False
            for token in sent:
                # Build verb phrase for better context
                if token.dep_ in {"aux", "auxpass", "ROOT"} and token.pos_ == "VERB":
                    verb_phrase += token.text + " "
                # Track subject for voice determination
                if token.dep_ in {"nsubj", "nsubjpass"}:
                    subject = token.text

                if token.dep_ == "nsubjpass":
                    has_passive = True
                elif token.dep_ == "nsubj" and not has_passive:
                    has_active = True

            if has_passive:
                patterns["voice"]["passive"].append(
                    {
                        "text": sent_text,
                        "subject": subject.strip(),
                        "verb_phrase": verb_phrase.strip(),
                    }
                )
            elif has_active:
                patterns["voice"]["active"].append(
                    {
                        "text": sent_text,
                        "subject": subject.strip(),
                        "verb_phrase": verb_phrase.strip(),
                    }
                )

            # Enhanced sentence structure detection
            clause_markers = [token for token in sent if token.dep_ == "mark"]
            coordinators = [token for token in sent if token.dep_ == "cc"]

            if len(clause_markers) == 0 and len(coordinators) == 0:
                patterns["sentence_structure"]["simple"].append(sent_text)
            elif len(clause_markers) > 0 and len(coordinators) == 0:
                patterns["sentence_structure"]["complex"].append(sent_text)
            elif len(clause_markers) == 0 and len(coordinators) > 0:
                patterns["sentence_structure"]["compound"].append(sent_text)
            elif len(clause_markers) > 0 and len(coordinators) > 0:
                patterns["sentence_structure"]["compound_complex"].append(sent_text)

            # Enhanced modality detection
            tokens_lower = [token.text.lower() for token in sent]

            # Conditional patterns
            if any(token in {"if", "unless", "whether"} for token in tokens_lower):
                patterns["modality"]["conditionals"].append(sent_text)

            # Hypothetical patterns
            if any(token in modal_verbs for token in tokens_lower):
                patterns["modality"]["hypotheticals"].append(sent_text)

            # Imperative patterns
            if (
                (sent[0].pos_ == "VERB" and sent[0].tag_ == "VB")
                or (sent[0].text.lower() == "please" and sent[1].pos_ == "VERB")
                or (sent[0].text.lower() == "don't" and sent[1].pos_ == "VERB")
                or (sent[0].text.lower() == "never" and sent[1].pos_ == "VERB")
                or (sent[0].text.lower() == "always" and sent[1].pos_ == "VERB")
            ):
                patterns["modality"]["imperatives"].append(sent_text)

            # Subjunctive patterns
            if any(
                token.text.lower() in {"wish", "if only", "as if", "would that"}
                for token in sent
            ):
                patterns["modality"]["subjunctive"].append(sent_text)

            # Cohesion devices
            if any(marker in tokens_lower for marker in temporal_markers):
                patterns["cohesion_devices"]["temporal_markers"].append(sent_text)

            if any(marker in tokens_lower for marker in causal_markers):
                patterns["cohesion_devices"]["causal_markers"].append(sent_text)

            if any(marker in tokens_lower for marker in contrastive_markers):
                patterns["cohesion_devices"]["contrastive_markers"].append(sent_text)

        # Add pattern statistics
        patterns["statistics"] = {
            "voice_distribution": {
                "passive_count": len(patterns["voice"]["passive"]),
                "active_count": len(patterns["voice"]["active"]),
            },
            "sentence_structure_distribution": {
                category: len(sentences)
                for category, sentences in patterns["sentence_structure"].items()
            },
            "modality_distribution": {
                category: len(sentences)
                for category, sentences in patterns["modality"].items()
            },
            "cohesion_device_distribution": {
                category: len(sentences)
                for category, sentences in patterns["cohesion_devices"].items()
            },
        }

        return patterns

    def analyze_text_structure(self, text: str) -> Dict[str, Any]:
        """
        Analyze the structural elements of the text and provide insights
        into syntax, lexical diversity, coherence, and complexity.

        Returns:
            Dictionary containing detailed structural analysis
        """
        doc = self.nlp(text)

        # Sentence analysis
        sentences = list(doc.sents)
        sentence_lengths = [len(sent) for sent in sentences]

        # Paragraph detection
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        paragraph_lengths = [len(p.split()) for p in paragraphs]

        # Discourse markers and connectives
        discourse_markers = [
            token.text
            for token in doc
            if token.dep_ == "mark"
            or token.text.lower()
            in {
                "however",
                "therefore",
                "thus",
                "moreover",
                "furthermore",
                "in conclusion",
                "as a result",
            }
        ]

        # Lexical diversity
        words = [token.text.lower() for token in doc if token.is_alpha]
        unique_words = set(words)
        lexical_diversity = len(unique_words) / len(words) if words else 0

        # Pronoun reference analysis
        pronoun_references = [
            token.text.lower() for token in doc if token.pos_ == "PRON"
        ]
        pronoun_ratio = len(pronoun_references) / len(words) if words else 0

        # POS tag distribution
        pos_counts = Counter([token.pos_ for token in doc])

        # Noun-Verb-Adjective Ratios
        noun_count = pos_counts["NOUN"]
        verb_count = pos_counts["VERB"]
        adj_count = pos_counts["ADJ"]
        noun_verb_ratio = noun_count / verb_count if verb_count > 0 else 0
        noun_adj_ratio = noun_count / adj_count if adj_count > 0 else 0

        # Sentence complexity (simple, compound, complex, compound-complex)
        simple_sentences = sum(
            1
            for sent in sentences
            if not any(token.dep_ == "mark" or token.pos_ == "CCONJ" for token in sent)
        )
        compound_sentences = sum(
            1
            for sent in sentences
            if any(token.pos_ == "CCONJ" for token in sent)
            and not any(token.dep_ == "mark" for token in sent)
        )
        complex_sentences = sum(
            1
            for sent in sentences
            if any(token.dep_ == "mark" for token in sent)
            and not any(token.pos_ == "CCONJ" for token in sent)
        )
        compound_complex_sentences = sum(
            1
            for sent in sentences
            if any(token.dep_ == "mark" for token in sent)
            and any(token.pos_ == "CCONJ" for token in sent)
        )

        return {
            "num_sentences": len(sentences),
            "avg_sentence_length": np.mean(sentence_lengths),
            "sentence_length_variability": {
                "variance": np.var(sentence_lengths),
                "iqr": np.percentile(sentence_lengths, 75)
                - np.percentile(sentence_lengths, 25),
            },
            "num_paragraphs": len(paragraphs),
            "avg_paragraph_length": (
                np.mean(paragraph_lengths) if paragraph_lengths else 0
            ),
            "paragraph_length_variability": {
                "variance": np.var(paragraph_lengths),
                "iqr": np.percentile(paragraph_lengths, 75)
                - np.percentile(paragraph_lengths, 25),
            },
            "discourse_markers": set(discourse_markers),
            "pronoun_reference_ratio": pronoun_ratio,
            "lexical_diversity": lexical_diversity,
            "pos_distribution": dict(pos_counts),
            "noun_verb_ratio": round(noun_verb_ratio, 2),
            "noun_adj_ratio": round(noun_adj_ratio, 2),
            "sentence_type_distribution": {
                "simple": simple_sentences,
                "compound": compound_sentences,
                "complex": complex_sentences,
                "compound_complex": compound_complex_sentences,
            },
            "complex_sentence_ratio": (
                (complex_sentences + compound_complex_sentences) / len(sentences)
                if sentences
                else 0
            ),
        }

    def analyze_readability(self, text: str) -> Dict[str, float]:
        doc = self.nlp(text)

        # Basic counts
        words = [token.text.lower() for token in doc if not token.is_punct]
        word_count = len(words)
        sentence_count = len(list(doc.sents))
        syllable_count = sum(self._count_syllables(word) for word in words)

        if sentence_count == 0:
            return {"error": "No sentences found in text"}

        avg_words_per_sentence = word_count / sentence_count
        avg_syllables_per_word = syllable_count / word_count if word_count > 0 else 0

        # Readability scores
        flesch = (
            206.835 - 1.015 * avg_words_per_sentence - 84.6 * avg_syllables_per_word
        )
        complex_words = len(
            [word for word in words if self._count_syllables(word) >= 3]
        )
        fog_index = 0.4 * (avg_words_per_sentence + 100 * (complex_words / word_count))

        difficult_words = sum(1 for word in words if word not in self.easy_words)
        difficult_word_ratio = difficult_words / word_count if word_count > 0 else 0
        dale_chall_score = (
            0.1579 * (difficult_word_ratio * 100) + 0.0496 * avg_words_per_sentence
        )
        if difficult_word_ratio > 0.05:
            dale_chall_score += 3.6365

        # Additional metrics
        content_words = [
            token for token in doc if token.pos_ in {"NOUN", "VERB", "ADJ", "ADV"}
        ]
        lexical_density = len(content_words) / word_count if word_count > 0 else 0

        unique_words = set(words)
        type_token_ratio = len(unique_words) / word_count if word_count > 0 else 0

        avg_word_length = (
            sum(len(word) for word in words) / word_count if word_count > 0 else 0
        )

        named_entities = [ent.text for ent in doc.ents]
        named_entity_ratio = len(named_entities) / word_count if word_count > 0 else 0

        verbs = [token for token in doc if token.pos_ == "VERB"]
        nouns = [token for token in doc if token.pos_ == "NOUN"]
        verb_noun_ratio = len(verbs) / len(nouns) if len(nouns) > 0 else 0

        avg_sentence_length_syllables = (
            syllable_count / sentence_count if sentence_count > 0 else 0
        )

        return {
            "flesch_reading_ease": round(flesch, 2),
            "gunning_fog_index": round(fog_index, 2),
            "dale_chall_score": round(dale_chall_score, 2),
            "avg_words_per_sentence": round(avg_words_per_sentence, 2),
            "avg_syllables_per_word": round(avg_syllables_per_word, 2),
            "complex_word_ratio": round(complex_words / word_count, 3),
            "lexical_density": round(lexical_density, 3),
            "type_token_ratio": round(type_token_ratio, 3),
            "avg_word_length": round(avg_word_length, 2),
            "named_entity_ratio": round(named_entity_ratio, 3),
            "verb_noun_ratio": round(verb_noun_ratio, 2),
            "avg_sentence_length_syllables": round(avg_sentence_length_syllables, 2),
        }

    @staticmethod
    def _count_syllables(word: str) -> int:
        """Helper method to count syllables in a word."""
        word = word.lower()
        count = 0
        vowels = "aeiouy"
        if word[0] in vowels:
            count += 1
        for index in range(1, len(word)):
            if word[index] in vowels and word[index - 1] not in vowels:
                count += 1
        if word.endswith("e"):
            count -= 1
        if count == 0:
            count += 1
        return count

    def export_analysis(
        self, text: str, format: str = "json"
    ) -> Union[str, Dict, pd.DataFrame]:
        """
        Export comprehensive text analysis in various formats.

        Args:
            text (str): The text to analyze.
            format (str): Output format - 'json' or 'dataframe'.

        Returns:
            Union[str, Dict, pd.DataFrame]: Analysis results in the specified format.
        """
        # Convert analysis results to dictionary format
        analysis = {
            "basic_stats": {
                "word_count": len(self.tokenize(text)),
                "sentence_count": len(list(self.nlp(text).sents)),
            },
            "sentiment": self.analyze_sentiment(text),
            "emotions": {
                emotion: score for emotion, score in self.analyze_emotions(text).items()
            },
            "keywords": {
                f"keyword_{i+1}": {"text": kw[0], "score": float(kw[1])}
                for i, kw in enumerate(self.extract_keywords(text))
            },
            "readability": self.analyze_readability(text),
            "linguistic_patterns": {
                pattern_type: len(patterns)
                for pattern_type, patterns in self.detect_linguistic_patterns(
                    text
                ).items()
            },
            "named_entities": {
                f"entity_{i+1}": {"text": ent[0], "label": ent[1]}
                for i, ent in enumerate(self.get_named_entities(text))
            },
        }

        # Flatten nested dictionaries for DataFrame conversion
        if format == "dataframe":
            flattened_data = []
            for category, values in analysis.items():
                if isinstance(values, dict):
                    for key, value in values.items():
                        if isinstance(value, dict):
                            for subkey, subvalue in value.items():
                                flattened_data.append(
                                    {
                                        "category": category,
                                        "key": f"{key}_{subkey}",
                                        "value": subvalue,
                                    }
                                )
                        else:
                            flattened_data.append(
                                {"category": category, "key": key, "value": value}
                            )
                else:
                    flattened_data.append(
                        {"category": category, "key": "", "value": values}
                    )

            df = pd.DataFrame(flattened_data)
            return df

        # Return JSON format
        return analysis

    # Adding a classifier based on Naive Bayes

    def train_text_classifier(
        self, csv_path, text_column, label_column, split_ratio=0.8
    ):
        """
        Train a Naive Bayes text classifier.

        Parameters:
        csv_path (str): Path to the CSV dataset.
        text_column (str): Column containing text data.
        label_column (str): Column containing labels.
        split_ratio (float): Ratio of training to testing data.
        """
        # Load data
        try:
            data = pd.read_csv(csv_path)
        except Exception as e:
            raise ValueError(f"Error reading CSV file: {e}")

        # Validate columns
        if text_column not in data.columns or label_column not in data.columns:
            raise ValueError(
                f"Columns '{text_column}' or '{label_column}' not found in the dataset."
            )

        # Split data
        X = data[text_column]
        y = data[label_column]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=1 - split_ratio, random_state=42
        )

        # Preprocessing and vectorization
        self.vectorizer = TfidfVectorizer()
        X_train_tfidf = self.vectorizer.fit_transform(X_train)
        X_test_tfidf = self.vectorizer.transform(X_test)

        # Train classifier
        self.classifier = MultinomialNB()
        self.classifier.fit(X_train_tfidf, y_train)

        # Evaluate
        y_pred = self.classifier.predict(X_test_tfidf)
        print("Model Accuracy:", accuracy_score(y_test, y_pred))
        print("Classification Report:\n", classification_report(y_test, y_pred))

        print("Model trained successfully!")

    def predict_text(self, text):
        """
        Predict the class of a given text using the trained classifier.

        Parameters:
        text (str): Input text to classify.

        Returns:
        str: Predicted label.
        """
        if not self.classifier or not self.vectorizer:
            raise ValueError("Model not trained. Please train the model first.")

        # Preprocess and predict
        text_tfidf = self.vectorizer.transform([text])
        return self.classifier.predict(text_tfidf)[0]


# Additional utility function
@lru_cache(maxsize=1)
def load_spacy_model(model_name: str):
    """Load and cache the spaCy model."""
    return spacy.load(model_name)
