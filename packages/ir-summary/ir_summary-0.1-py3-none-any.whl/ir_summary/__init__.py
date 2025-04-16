#initiator
# Abstractive Summarization using T5 model
from transformers import pipeline
text = """
Natural language processing (NLP) is a field of computer science, artificial intelligence, and computational linguistics 
concerned with the interactions between computers and human (natural) languages. As such, NLP is related to the area of 
human-computer interaction. Many challenges in NLP involve natural language understanding, natural language generation, 
and machine learning. Text summarization is the process of distilling the most important information from a source (text) 
to produce an abridged version for a particular user or task. Automatic text summarization methods are greatly needed to address 
the ever-growing amount of text data available online to both better help discover relevant information and to consume the vast 
amount of text data available more efficiently.
"""
summarization_pipeline = pipeline("summarization", model="t5-small", tokenizer="t5-small")
input_text = "summarize: " + text
summary = summarization_pipeline(input_text, max_length=100, min_length=20, do_sample=False)[0]['summary_text']
print("Abstractive Summary:")
print(summary)

# ---------------------------------------------------------------------------------------------------

# Extractive Summarization using TF-IDF and Cosine Similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def extractive_summarize(text, num_sentences=2):
    """
    Extractive text summarization using TF-IDF and cosine similarity.

    :param text: Input text (string).
    :param num_sentences: Number of sentences to extract for the summary.
    :return: Extracted summary as a string.
    """
    # Tokenize the text into sentences
    sentences = text.split(". ")

    # Calculate TF-IDF matrix
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(sentences)

    # Compute pairwise cosine similarity between sentences
    cosine_similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Initialize sentence scores
    sentence_scores = {}
    for i in range(len(sentences)):
        sentence_scores[i] = np.sum(cosine_similarities[i])

    # Select the top 'num_sentences' sentences with highest scores
    top_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]

    # Generate the summary
    summary = [sentences[i] for i in sorted(top_sentences)]
    return " ".join(summary)

# Example usage for Extractive Summarization
if __name__ == "__main__":
    text = """Natural Language Processing (NLP) is a field of computer science, artificial intelligence, and 
    computational linguistics concerned with the interactions between computers and human (natural) languages. 
    As such, NLP is related to the area of human-computer interaction. Many challenges in NLP involve natural 
    language understanding, that is, enabling computers to derive meaning from human or natural language input. 
    Other challenges involve natural language generation."""

    summary = extractive_summarize(text, num_sentences=2)
    print("\nExtractive Summary:")
    print(summary)
