def nlp():
    num = int(input())
    if (num == 1):
        print('''
        Q1. use nltk to tokenize the given sentence
import nltk
nltk.download('punkt')  # This downloads the necessary data for tokenization

sentence = "Natural Language processing with Python is fun!"
words = nltk.word_tokenize(sentence)


print(words)
################################################################################

Q2. use nltk to find frequency distribution of text moby dick
import nltk
from nltk.probability import FreqDist
from nltk.corpus import gutenberg

# Download the required NLTK datasets if not already installed
nltk.download('gutenberg')
nltk.download('punkt')

# Load the Moby Dick text
moby_dick_text = gutenberg.words('melville-moby_dick.txt')

# Filter out non-alphabetic words (to exclude punctuation and special characters)
filtered_words = [word.lower() for word in moby_dick_text if word.isalpha()]

# Calculate frequency distribution of words
freq_dist = FreqDist(filtered_words)

# Display the frequency distribution of the top 10 words
print(freq_dist.most_common(10))
########################################################################################

Q3.create bigram collocation text sense and sensibility
import nltk
from nltk.book import text2
from nltk.util import bigrams
from nltk.probability import FreqDist

# Download required NLTK datasets
nltk.download('book')
nltk.download('punkt')

# Load the text2 (romance fiction) from NLTK's book module
text2_words = text2

# Filter out non-alphabetic words (to exclude punctuation and special characters)
filtered_words = [word.lower() for word in text2_words if word.isalpha()]

# Generate bigrams from the filtered text
text2_bigrams = bigrams(filtered_words)

# Calculate frequency distribution of bigrams
bigram_freq_dist = FreqDist(text2_bigrams)

# Display the top 5 bigrams
top_5_bigrams = bigram_freq_dist.most_common(5)

print(top_5_bigrams)
#############################################################################################

Q4. nltk text 2 sense and sensibility total distinct words
import nltk
from nltk.book import text2

# Total number of words
total_words = len(text2)

# Number of distinct words (unique words)
distinct_words = len(set(text2))

# Output the results
print("Total number of words:", total_words)
print("Number of distinct words:", distinct_words)
########################################################################################

Q5. compare lexical diversity of humor and romance fiction using text 5 and 2
import nltk
from nltk.book import text2, text5

# Function to calculate lexical diversity
def lexical_diversity(text):
    return len(set(text)) / len(text)

# Calculate lexical diversity for both texts
lexical_diversity_text2 = lexical_diversity(text2)
lexical_diversity_text5 = lexical_diversity(text5)

# Output the results
print(f"Lexical Diversity of Romance Fiction (text2): {lexical_diversity_text2:.4f}")
print(f"Lexical Diversity of Human Humor (text5): {lexical_diversity_text5:.4f}")

# Compare which genre has more lexical diversity
if lexical_diversity_text2 > lexical_diversity_text5:
    print("Romance fiction has more lexical diversity.")
else:
    print("Human humor has more lexical diversity.")

''')
    elif(num == 2):
        print('''
#Q1 Question:1 Using the gutenberg corpus in NLTK list all available file identifiers.

import nltk
from nltk.corpus import gutenberg

# List available file identifiers
file_ids = gutenberg.fileids()
print(file_ids)
############################################
#Q2 2 Calculate the average word length, average sentence length (in words) and lexical diversity for "Moby Dick" by Herman Melville using gutenberg corpus.
import nltk
from nltk.corpus import gutenberg


# Load the text of Moby Dick
moby_text = gutenberg.words('melville-moby_dick.txt')
moby_sentences = gutenberg.sents('melville-moby_dick.txt')

# Calculate average word length
average_word_length = sum(len(word) for word in moby_text) / len(moby_text)

# Calculate average sentence length (in words)
average_sentence_length = sum(len(sentence) for sentence in moby_sentences) / len(moby_sentences)

# Calculate lexical diversity
lexical_diversity = len(set(moby_text)) / len(moby_text)

# Print results
print(f"Average word length: {average_word_length:.2f}")
print(f"Average sentence length: {average_sentence_length:.2f} words")
print(f"Lexical diversity: {lexical_diversity:.4f}")
###########################################################################################

#Q3 3 Using the brown corpus find the most frequent word in the news category
from nltk.corpus import brown
from collections import Counter

# Load words from the 'news' category
news_words = brown.words(categories='news')

# Count word frequencies
word_freq = Counter(news_words)

# Find the most common word
most_common_word, most_common_count = word_freq.most_common(1)[0]

# Print the result
print(f"Most frequent word: '{most_common_word}' (occurs {most_common_count} times)")
############################################################################################
#Q4 4 List the categories available in the brown corpus.**

from nltk.corpus import brown

# List available categories
categories = brown.categories()
print(categories)
######################################################################################
#Q5 5 Using the Revters corpus, find the number of documents categorized under both Barley and Corn.

from nltk.corpus import reuters

# Get document IDs for 'barley' and 'corn'
barley_docs = set(reuters.fileids('barley'))
corn_docs = set(reuters.fileids('corn'))

# Find documents categorized under both
common_docs = barley_docs.intersection(corn_docs)

# Print the result
print(f"Number of documents categorized under both 'barley' and 'corn': {len(common_docs)}")


''')
    elif(num == 3):
        print('''

        Q1. Write a Python program to download the text of "Pride and Prejudice" by Jane Austen from Project Gutenberg, tokenize the text, and display the first 10 tokens.
import nltk
from nltk.tokenize import word_tokenize
import requests

nltk.download('punkt')

url = "https://www.gutenberg.org/files/1342/1342-0.txt"
response = requests.get(url)
text = response.text

tokens = word_tokenize(text)
print(tokens[:10])

####################################################################
Q2. Using NLTK, write a function that takes a URL as input, fetches the raw text from the webpage, and returns the number of words in the text.

import requests
from nltk.tokenize import word_tokenize

def count_words_from_url(url):
    response = requests.get(url)
    text = response.text
    words = word_tokenize(text)
    return len(words)

url = "https://www.gutenberg.org/files/1342/1342-0.txt"
print(count_words_from_url(url))
#######################################################################

Q3.Explain how to remove HTML tags from a web page's content using Python and NLTK. Provide a code example that fetches a web page, removes HTML tags, and prints the cleaned text.
import requests
from bs4 import BeautifulSoup

def remove_html_tags(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text()

url = "https://www.example.com"
clean_text = remove_html_tags(url)
print(clean_text)
#########################################################################
Q4. Write a Python program that reads a text file, tokenizes its content into sentences, and prints the number of sentences in the file.

from nltk.tokenize import sent_tokenize

def count_sentences(filename):
    with open(filename, "r", encoding="utf-8") as file:
        text = file.read()
    sentences = sent_tokenize(text)
    return len(sentences)

print(count_sentences("CH3\sample.txt"))
##########################################################################
Q5. Using regular expressions in Python, write a function that takes a list of words and returns a list of words that end with 'ing'.

import re

def find_ing_words(words):
    return [word for word in words if re.search(r'ing$', word)]

word_list = ["playing", "running", "walked", "singing", "talking"]
print(find_ing_words(word_list))


''')
    elif(num == 4):
        print('''
Q1. Explain the difference between assigning a list to a new variable using direct assignment (=) and using the copy() method. Provide code examples to illustrate the difference.
# Direct Assignment
list1 = [1, 2, 3]
list2 = list1  # Both refer to the same object
list2.append(4)

print(list1)  # Output: [1, 2, 3, 4]
print(list2)  # Output: [1, 2, 3, 4]

# Using copy()
list3 = [1, 2, 3]
list4 = list3.copy()  # Creates a new independent list
list4.append(4)

print(list3)  # Output: [1, 2, 3]
print(list4)  # Output: [1, 2, 3, 4]
#####################################################################

Q2. Write a function extract_nouns(text) that takes a text string as input and returns a list of all nouns in the text. Use NLTK's part-of-speech tagging for this task.
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def extract_nouns(text):
    words = word_tokenize(text)
    tagged_words = pos_tag(words)
    nouns = [word for word, tag in tagged_words if tag in ["NN", "NNS", "NNP", "NNPS"]]
    return nouns

text = "John is a great software engineer working at Google."
print(extract_nouns(text))  # Output: ['John', 'software', 'engineer', 'Google']
#################################################################################################

Q3.Demonstrate how to use list comprehension to create a list of the lengths of each word in a given sentence

sentence = "Python is an amazing programming language"
word_lengths = [len(word) for word in sentence.split()]
print(word_lengths)  # Output: [6, 2, 2, 7, 11, 8]
##############################################################################################

Q4. Write a function word_frequency(text) that takes a text string and returns a dictionary with words as keys and their frequencies as values.
from collections import Counter
import re

def word_frequency(text):
    words = re.findall(r'\b\w+\b', text.lower())  # Extract words and convert to lowercase
    return dict(Counter(words))

text = "This is a test. This test is just a test."
print(word_frequency(text))  # Output: {'this': 2, 'is': 2, 'a': 2, 'test': 3, 'just': 1}
##################################################################################################

Q5. Explain the concept of variable scope in Python with an example demonstrating the difference between local and global variables.
x = 10  # Global variable

def my_function():
    x = 5  # Local variable
    print("Inside function:", x)

my_function()
print("Outside function:", x)

# Output:
# Inside function: 5
# Outside function: 10


''')
    elif(num == 5):
        print('''

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag import pos_tag
from nltk.corpus import brown
from collections import Counter

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('universal_tagset')
nltk.download('brown')

# 1. POS tagging of a single sentence
def pos_tag_sentence(sentence):
    words = word_tokenize(sentence)
    return pos_tag(words)
print(pos_tag_sentence("The quick brown fox jumps over the lazy dog."))
########################################
# 2. POS tagging for a list of sentences
def pos_tag_sentences(sentences):
    return [pos_tag(word_tokenize(sentence)) for sentence in sentences]
print(pos_tag_sentences(["Hello world!", "Natural Language Processing is interesting."]))
######################################
# 3. Map Penn Treebank POS tags to Universal POS tags
def map_to_universal(sentence):
    words = word_tokenize(sentence)
    return pos_tag(words, tagset='universal')
print(map_to_universal("The quick brown fox jumps over the lazy dog."))
####################################################
# 4. Extract all nouns from a sentence
def extract_nouns(sentence):
    return [word for word, tag in pos_tag(word_tokenize(sentence)) if tag in ['NN', 'NNS', 'NNP', 'NNPS']]
print(extract_nouns("The cat sat on the mat."))
####################################################
# 5. Most common POS tag in the news category of Brown Corpus
def most_common_pos_news():
    words = brown.tagged_words(categories='news', tagset='universal')
    return Counter(tag for _, tag in words).most_common(1)
print(most_common_pos_news())
####################################################
# 6. Train and evaluate a unigram tagger
def train_unigram_tagger():
    tagged_sents = brown.tagged_sents(categories='news')
    unigram_tagger = nltk.UnigramTagger(tagged_sents[:-500])
    return unigram_tagger.evaluate(tagged_sents[-500:])
print(train_unigram_tagger())



''')
    elif(num == 6):
        print('''

#Q1: Gender Classifier (Based on Last Letter).
import nltk
import random
from nltk.corpus import names
from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy


nltk.download('names')

# Extract names
male_names = [(name, 'male') for name in names.words('male.txt')]
female_names = [(name, 'female') for name in names.words('female.txt')]

# Combine and shuffle data
data = male_names + female_names
random.shuffle(data)

# Feature extractor (last letter)
def gender_features(name):
    return {'name': name}

# Prepare dataset
featuresets = [(gender_features(name), gender) for name, gender in data]

# Train classifier
classifier = NaiveBayesClassifier.train(featuresets)

# Evaluate
print("Accuracy:", accuracy(classifier, featuresets))
classifier.show_most_informative_features(5)
#############################################################
# Q2. Enhanced Gender Classifier (First Letter & Name Length)**

# Feature extractor with first letter and name length
def enhanced_gender_features(name):
    return {
        'last_letter': name[-1].lower(),
        'first_letter': name[0].lower(),
        'name_length': len(name),
    }

# Prepare dataset with enhanced features
enhanced_featuresets = [(enhanced_gender_features(name), gender) for name, gender in data]

# Train enhanced classifier
enhanced_classifier = NaiveBayesClassifier.train(enhanced_featuresets)

# Evaluate enhanced model
print("Enhanced Accuracy:", accuracy(enhanced_classifier, enhanced_featuresets))
enhanced_classifier.show_most_informative_features(5)
###############################################################################
# Q.3 document classifier to categorize movie reviews as positive or negative
import nltk
from nltk.corpus import movie_reviews
import random

nltk.download('movie_reviews')

# Prepare the data
documents = [(list(movie_reviews.words(fileid)), category)
             for category in movie_reviews.categories()
             for fileid in movie_reviews.fileids(category)]

# Shuffle documents
random.shuffle(documents)

# Feature extraction: Simple bag of words
def document_features(words):
    return {word: True for word in words}

# Create the feature sets
featuresets = [(document_features(d), c) for (d, c) in documents]

# Split into training and testing sets
train_set, test_set = featuresets[100:], featuresets[:100]

# Train Naive Bayes classifier
classifier = nltk.NaiveBayesClassifier.train(train_set)

# Evaluate accuracy
accuracy = nltk.classify.accuracy(classifier, test_set)
print(f"Document Classifier Accuracy: {accuracy * 100:.2f}%")
classifier.show_most_informative_features(10)

#########################################################################

# Q4.: movie review classifier that considers bigrams (pairs of consecutive words) in addition to unigrams (single words).

import nltk
from nltk.corpus import movie_reviews
from nltk.util import bigrams
import random

nltk.download('movie_reviews')

# Prepare the data
documents = [(list(movie_reviews.words(fileid)), category)
             for category in movie_reviews.categories()
             for fileid in movie_reviews.fileids(category)]

random.shuffle(documents)

# Custom feature extractor: Unigrams + Bigrams
def document_features(words):
    unigrams = {word: True for word in words}
    bigrams_list = bigrams(words)
    bigram_features = {f"bigram_{bigram[0]}_{bigram[1]}": True for bigram in bigrams_list}
    return {**unigrams, **bigram_features}

# Create the feature sets
featuresets = [(document_features(d), c) for (d, c) in documents]

# Split into training and testing sets
train_set, test_set = featuresets[100:], featuresets[:100]

# Train Naive Bayes classifier
classifier = nltk.NaiveBayesClassifier.train(train_set)

# Evaluate accuracy
accuracy = nltk.classify.accuracy(classifier, test_set)
print(f"Classifier with Unigrams and Bigrams Accuracy: {accuracy * 100:.2f}%")
classifier.show_most_informative_features(10))

###################################################################
#Q5.Predcit gender based on both the first and last letters of a name.

import nltk
from nltk.corpus import names
import random

nltk.download('names')

# Feature extraction: First and last letters
def gender_features(name):
    return {
        'first_letter': name[0],
        'last_letter': name[-1]
    }

# Prepare labeled data
labeled_names = ([(name, 'male') for name in names.words('male.txt')] +
                 [(name, 'female') for name in names.words('female.txt')])

random.shuffle(labeled_names)

# Extract features
featuresets = [(gender_features(name), gender) for (name, gender) in labeled_names]

# Split into training and testing sets
train_set, test_set = featuresets[500:], featuresets[:500]

# Train the Naive Bayes classifier
classifier = nltk.NaiveBayesClassifier.train(train_set)

# Evaluate the classifier
accuracy = nltk.classify.accuracy(classifier, test_set)
print(f"Naive Bayes Gender Classifier Accuracy: {accuracy * 100:.2f}%")
#

example_name = "John"  # Replace with your desired name
features = gender_features(example_name)
predicted_gender = classifier.classify(features)
print(f"The predicted gender for the name '{example_name}' is: {predicted_gender}")
classifier.show_most_informative_features(10)

''')
    elif(num == 7):
        print('''
#Q1.	Write a Python program using NLTK to extract named entities from the sentence: "Apple Inc. is looking at buying U.K. startup for $1 billion."
import spacy

# Load the spacy English model
nlp = spacy.load('en_core_web_sm')

# Input sentence
sentence = "Apple Inc. is looking at buying U.K. startup for $1 billion."

# Process the sentence with spaCy
doc = nlp(sentence)

# Extract named entities
for ent in doc.ents:
    print(f'{ent.label_}: {ent.text}')
###################################
# Q2., write a function that takes a list of sentences and returns a list of named entities found in each sentence.
import nltk
from nltk import word_tokenize, pos_tag, ne_chunk

# List of sentences
sentences = [
    "Apple Inc. is looking at buying U.K. startup for $1 billion.",
    "Barack Obama was the 44th president of the United States.",
    "Google is based in Mountain View, California."
]

# Extract named entities for each sentence
named_entities_per_sentence = []

for sentence in sentences:
    # Tokenize and POS tagging
    tokens = word_tokenize(sentence)
    tagged = pos_tag(tokens)

    # Named Entity Recognition
    tree = ne_chunk(tagged)

    # Extract named entities
    named_entities = [subtree for subtree in tree if isinstance(subtree, nltk.Tree)]
    named_entities_per_sentence.append(named_entities)

# Display extracted named entities for each sentence
for i, entities in enumerate(named_entities_per_sentence):
    print(f"Sentence {i+1}:")
    for entity in entities:
        print(f'  {" ".join(word for word, tag in entity)}')
######################################################################
#Q3.NLTK to extract and display all noun phrases from a given text.

import nltk

nltk.download('punkt')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('punkt_tab')
nltk.download('maxent_ne_chunker_tab')
nltk.download('averaged_perceptron_tagger_eng')

def extract_noun_phrases(text):
    tokens = nltk.word_tokenize(text)
    pos_tags = nltk.pos_tag(tokens)

    # Define noun phrase chunking grammar
    grammar = "NP: {<DT>?<JJ>*<NN>+}"  # Determiner (optional), Adjective (any), Noun (one or more)

    chunk_parser = nltk.RegexpParser(grammar)
    chunk_tree = chunk_parser.parse(pos_tags)

    # Extract noun phrases
    noun_phrases = [" ".join(word for word, tag in subtree.leaves())
                    for subtree in chunk_tree.subtrees() if subtree.label() == "NP"]

    return noun_phrases

# Example usage
text = "The quick brown fox jumps over the lazy dog."
print(extract_noun_phrases(text))
##########################################################################

#Q4.Using NLTK, write a program to perform chunking on the sentence
import nltk


nltk.download('punkt')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('punkt_tab')
nltk.download('maxent_ne_chunker_tab')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

sentence = "He reckons the current account deficit will narrow to only 8 billion."
tokens = nltk.word_tokenize(sentence)
pos_tags = nltk.pos_tag(tokens)

# Define a chunk grammar
grammar = "Chunk: {<DT>?<JJ>*<NN>+}"

chunk_parser = nltk.RegexpParser(grammar)
chunk_tree = chunk_parser.parse(pos_tags)

# Print chunk tree
chunk_tree.pretty_print()
#######################################################

#Q5. Python function using NLTK that takes a sentence as input and returns all verb phrases (VP) present in the sentence.

nltk.download('punkt')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('punkt_tab')
nltk.download('maxent_ne_chunker_tab')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
import nltk
def extract_verb_phrases(sentence):
    tokens = nltk.word_tokenize(sentence)
    pos_tags = nltk.pos_tag(tokens)

    # Define verb phrase grammar
    grammar = "VP: {<VB.*><RB>?<VB.*>*}"

    chunk_parser = nltk.RegexpParser(grammar)
    chunk_tree = chunk_parser.parse(pos_tags)

    # Extract verb phrases
    verb_phrases = [" ".join(word for word, tag in subtree.leaves())
                    for subtree in chunk_tree.subtrees() if subtree.label() == "VP"]

    return verb_phrases

# Example usage
sentence = "She is running quickly and will finish the race soon."
print(extract_verb_phrases(sentence))
''')
    elif(num == 8):
        print('''

#Q1. Write a Python program using NLTK to define a context-free grammar (CFG) that can parse simple sentences like "The cat sat on the mat." Use this grammar to generate the parse tree for the sentence.

import nltk
from nltk import CFG

# Define a context-free grammar (CFG) for simple sentences
grammar = CFG.fromstring("""
  S -> NP VP
  NP -> Det N
  VP -> V PP
  PP -> P NP
  Det -> 'The' | 'the'
  N -> 'cat' | 'mat'
  V -> 'sat'
  P -> 'on'
""")

# Sentence to parse
sentence = ['The', 'cat', 'sat', 'on', 'the', 'mat']

# Create a parser with the grammar
parser = nltk.ChartParser(grammar)

# Parse the sentence and visualize the parse tree
for tree in parser.parse(sentence):
    tree.pretty_print()  # Display the tree in a readable format

######################################################

#q2. Using NLTK, write a function that takes a sentence as input and returns all possible parse trees using a given CFG. Demonstrate this function with the sentence "I saw the man with the telescope."

import nltk
from nltk import CFG

# Define the context-free grammar (CFG)
grammar = CFG.fromstring("""
  S -> NP VP
  NP -> Pronoun | Det N | Det N PP
  VP -> V NP | V NP PP
  PP -> P NP
  Pronoun -> 'I'
  Det -> 'the'
  N -> 'man' | 'telescope'
  V -> 'saw'
  P -> 'with'
""")

# Function to generate all possible parse trees
def generate_parse_trees(sentence, grammar):
    parser = nltk.ChartParser(grammar)
    parse_trees = list(parser.parse(sentence))  # Generate all possible parse trees
    return parse_trees

# Input sentence
sentence = ['I', 'saw', 'the', 'man', 'with', 'the', 'telescope']

# Generate parse trees
parse_trees = generate_parse_trees(sentence, grammar)

# Display all parse trees
for tree in parse_trees:
    tree.pretty_print()  # Print the tree in a readable format

###########################################

#q3. 3.  Write a Python program using NLTK to create a recursive descent parser for a given CFG. Parse the sentence "She eats a sandwich." and display the parse tree.

import nltk
from nltk import CFG

# Define the context-free grammar (CFG)
grammar = CFG.fromstring("""
  S -> NP VP
  NP -> Pronoun | Det N
  VP -> V NP
  PP -> P NP
  Pronoun -> 'She'
  Det -> 'a'
  N -> 'sandwich'
  V -> 'eats'
  P -> 'with'
""")

# Recursive descent parser function
class RecursiveDescentParser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.parser = nltk.RecursiveDescentParser(self.grammar)

    def parse(self, sentence):
        return list(self.parser.parse(sentence))

# Sentence to parse
sentence = ['She', 'eats', 'a', 'sandwich']

# Create a parser with the given CFG
rd_parser = RecursiveDescentParser(grammar)

# Generate parse trees
parse_trees = rd_parser.parse(sentence)

# Display all parse trees
for tree in parse_trees:
    tree.pretty_print()  # Print the tree in a readable format


#q4. Using NLTK, write a program to extract noun phrases from a sentence using a chunk grammar. Apply it to the sentence "The quick brown fox jumps over the lazy dog."

import nltk
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger') # Download missing resource.
nltk.download('averaged_perceptron_tagger_eng')

from nltk import pos_tag, word_tokenize, RegexpParser

def extract_noun_phrases(sentence):


    # Tokenize the sentence
    tokens = word_tokenize(sentence)

    # Perform Part-of-Speech tagging
    tagged_tokens = pos_tag(tokens)

    # Define the chunk grammar for noun phrases (NP)
    chunk_grammar = r"""
        NP: {<DT>?<JJ>*<NN>}  # Noun phrase pattern: optional determiner, zero or more adjectives, and a noun
    """

    # Create a chunk parser
    chunk_parser = RegexpParser(chunk_grammar)

    # Parse the tagged tokens
    chunked_tree = chunk_parser.parse(tagged_tokens)

    # Extract noun phrases from the chunked tree
    noun_phrases = []
    for subtree in chunked_tree.subtrees():
        if subtree.label() == 'NP':
            noun_phrase = ' '.join(word for word, tag in subtree.leaves())
            noun_phrases.append(noun_phrase)

    return noun_phrases

# Example usage:
sentence = "The quick brown fox jumps over the lazy dog."
noun_phrases = extract_noun_phrases(sentence)

print("Noun phrases in the sentence:")
for phrase in noun_phrases:
    print(phrase)
#####################################################################

#Q5. Write a Python function using NLTK that takes a sentence as input and returns the verb phrases (VP) using a chunk grammar. Demonstrate this function with the sentence "The cat is sleeping on the mat."

import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

from nltk import pos_tag, word_tokenize, RegexpParser

def extract_verb_phrases(sentence):


    # Tokenize the sentence
    tokens = word_tokenize(sentence)

    # Perform Part-of-Speech tagging
    tagged_tokens = pos_tag(tokens)

    # Define the chunk grammar for verb phrases (VP)
    # This grammar is modified to capture complete verb phrases
    chunk_grammar = r"""
        VP: {<VB.?>+<RB.?>* <IN>? <DT>? <JJ>* <NN.?>+}  # Captures verb phrases
    """

    # Create a chunk parser
    chunk_parser = RegexpParser(chunk_grammar)

    # Parse the tagged tokens
    chunked_tree = chunk_parser.parse(tagged_tokens)

    # Extract verb phrases from the chunked tree
    verb_phrases = []
    for subtree in chunked_tree.subtrees():
        if subtree.label() == 'VP':
            verb_phrase = ' '.join(word for word, tag in subtree.leaves())
            verb_phrases.append(verb_phrase)

    return verb_phrases

# Example usage:
sentence = "The cat is sleeping on the mat."
verb_phrases = extract_verb_phrases(sentence)

print("Verb phrases in the sentence:")
for phrase in verb_phrases:
    print(phrase)

''')

