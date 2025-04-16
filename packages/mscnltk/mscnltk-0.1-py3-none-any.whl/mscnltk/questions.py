
questions = [
        "Q1. using nltk to tokenize sentence 'natural language processing with python is fun'",
        "Q2. Word frequency in 'Moby Dick' most common",
        "Q3. Bigrams in 'Sense and Sensibility' and list top 5 bigrams",
        "Q4. Total and distinct words in 'Sense and Sensibility'",
        "Q5. Calculate lexical diversity for text5 (humour) and text2 (romance)",
        "Q6. Using the Gutenberg corpus in nltk, list all available file identifiers",
        "Q7. Calculate the average word length, average sentence length (in words) and lexical diversity for 'Moby Dick' by Herman Melville using Gutenberg corpus",
        "Q8. Using the brown corpus find the most frequent words in the news category",
        "Q9. Use the inaugural address corpus to find the total number of words and the total number of unique words in the inaugural addresses delivered in the 21st century",
        "Q10. Write a Python program to find the frequency distribution of the words 'democracy', 'freedom', 'liberty', and 'equality' in all inaugural addresses using NLTK",
        "Q11. Write a Python program to display the 5 most common words in the text of 'Sense and Sensibility' by Jane Austen using the Gutenberg Corpus",
        "Q12. Write a Python program to download the text of 'Pride and Prejudice' by Jane Austen from Project Gutenberg, tokenize the text, and display the first 10 tokens",
        "Q13. Using NLTK, write a function that takes a URL as input, fetches the raw text from the webpage, and returns the number of words in the text",
        "Q14. Explain how to remove HTML tags from a web page's content using Python and NLTK. Provide a code example that fetches a web page, removes HTML tags, and prints the cleaned text",
        "Q15. Write a Python program that reads a text file, tokenizes its content into sentences, and prints the number of sentences in the file",
        "Q16. Using regular expressions in Python, write a function that takes a list of words and returns a list of words that end with 'ing'",
        "Q17. Difference between assigning a list to a new variable using direct assignment (=) and using the copy() method",
        "Q18. Function extract_nouns(text) using NLTK's part-of-speech tagging",
        "Q19. List comprehension to create a list of the lengths of each word in a sentence",
        "Q20. Function word_frequency(text) to return a dictionary of word frequencies",
        "Q21. Write a Python program using NLTK to perform part-of-speech tagging on the sentence: 'The quick brown fox jumps over the lazy dog.'",
        "Q22. Using NLTK, write a function that takes a list of sentences and returns a list of part-of-speech tagged sentences",
        "Q23. Explain how to map the Penn Treebank POS tags to the Universal POS tags using NLTK. Provide a code example that tags a sentence and maps the tags accordingly",
        "Q24. Write a Python function using NLTK that takes a sentence as input and returns a list of all nouns in the sentence",
        "Q25. Using the Brown Corpus in NLTK, write a program to find the most common part-of-speech tag in the news category",
        "Q26. Write a Python program to calculate the frequency of each part-of-speech tag in a given text",
        "Q27. Using NLTK, write a program that tags words in a sentence and prints only the verbs",
        "Q28. Using the names corpus in NLTK, build a gender classifier that predicts whether a name is male or female based on the last letter of the name. Evaluate its accuracy",
        "Q29. Enhance the gender classifier by including features such as the first letter and the length of the name. Evaluate if these features improve the classifier's accuracy",
        "Q30. Using the movie_reviews corpus in NLTK, build a document classifier to categorize movie reviews as positive or negative. Evaluate its performance",
        "Q31. Write a Python program using NLTK to extract named entities from the sentence: 'Apple Inc. is looking at buying U.K. startup for $1 billion'",
        "Q32. Using NLTK, write a function that takes a list of sentences and returns a list of named entities found in each sentence",
        "Q33. Write a Python program that uses NLTK to extract and display all noun phrases from a given text",
        "Q34. Using NLTK, write a program to perform chunking on the sentence: 'He reckons the current account deficit will narrow to only 8 billion.' and display the chunked tree",
        "Q35. Write a Python program using NLTK to define a context-free grammar (CFG) that can parse simple sentences like 'The cat sat on the mat.' Use this grammar to generate the parse tree for the sentence",
        "Q36. Using NLTK, write a function that takes a sentence as input and returns all possible parse trees using given CFG. Demonstrate this function with the sentence 'I saw the man with the telescope.'",
        "Q37. Write a Python program using NLTK to create a recursive descent parser for a given CFG. Parse the sentence 'She eats a sandwich.' and display the parse tree"
]


def question():
    for q in questions:
        print(q)


def code(question_number):
    code_dict = {
        1: '''import nltk
nltk.download("all")
from nltk.tokenize import word_tokenize
sentence = "natural language processing with python is fun"
tokens = word_tokenize(sentence)
tokens''',
        
        2: '''from nltk.corpus import gutenberg
from nltk import FreqDist
moby_text = gutenberg.words('melville-moby_dick.txt')
fdist = FreqDist(moby_text)
print("Most common words in Moby Dick:", fdist.most_common(20))''',
        
        3: '''import nltk
from nltk.book import text2
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
bigram_finder = BigramCollocationFinder.from_words(text2)
bigram_finder.apply_freq_filter(3)
top_bigrams = bigram_finder.ngram_fd.most_common(5)
for bigram, frequency in top_bigrams:
    print(f"{bigram}: {frequency} occurrences")''',
        
        4: '''import nltk
from nltk.book import text2
total_words = len(text2)
distinct_words = len(set(text2))
print(f"Total number of words: {total_words}")
print(f"Number of distinct words: {distinct_words}")''',
        
        5: '''import nltk
from nltk.book import text5, text2

def lexical_diversity(text):
    unique_words = len(set(text))  # Number of unique words
    total_words = len(text)        # Total number of words
    return unique_words / total_words

humour_diversity = lexical_diversity(text5)
romance_diversity = lexical_diversity(text2)
print(f"Lexical diversity of humour (text5): {humour_diversity:.4f}")
print(f"Lexical diversity of romance (text2): {romance_diversity:.4f}")
if humour_diversity > romance_diversity:
    print("Humour genre is more lexically diverse.")
elif romance_diversity > humour_diversity:
    print("Romance genre is more lexically diverse.")
else:
    print("Both genres have the same lexical diversity.")''',
        
        6: '''import nltk
nltk.download('gutenberg')
from nltk.corpus import gutenberg
file_ids = gutenberg.fileids()
print(len(file_ids))
print(file_ids)''',
        
        7: '''import nltk
nltk.download('punkt')
from nltk.corpus import gutenberg
nltk.download('punkt')
moby_dick = gutenberg.raw('melville-moby_dick.txt')
words = nltk.word_tokenize(moby_dick)
sentences = nltk.sent_tokenize(moby_dick)
total_characters = sum(len(word) for word in words)
total_words = len(words)
average_word_length = total_characters / total_words
total_sentences = len(sentences)
average_sentence_length = total_words / total_sentences
unique_words = len(set(words))
lexical_diversity = unique_words / total_words
print(f"Average Word Length: {average_word_length:.2f}")
print(f"Average Sentence Length: {average_sentence_length:.2f}")
print(f"Lexical Diversity: {lexical_diversity:.2f}")''',
        
        8: '''import nltk
from nltk.corpus import brown
from collections import Counter
nltk.download('brown')
news_words = brown.words(categories='news')
word_freq = Counter(news_words)
most_common_words = word_freq.most_common(10)
print("Most frequent words in the news category:", most_common_words)
categories = brown.categories()
print("Categories in the Brown corpus:", categories)''',
        
        9: '''from nltk.corpus import inaugural
nltk.download('inaugural')
fileids = [fileid for fileid in inaugural.fileids() if int(fileid[:4]) >= 2001]
words = [word.lower() for fileid in fileids for word in inaugural.words(fileid)]
total_words = len(words)
unique_words = len(set(words))
print("Total words in 21st-century inaugural addresses:", total_words)
print("Total unique words in 21st-century inaugural addresses:", unique_words)''',
        
        10: '''from nltk.corpus import inaugural
nltk.download('inaugural')
target_words = ["democracy", "freedom", "liberty", "equality"]
freq_dist = {word: 0 for word in target_words}
for fileid in inaugural.fileids():
    words = [word.lower() for word in inaugural.words(fileid)]
    for word in target_words:
        freq_dist[word] += words.count(word)
print("Frequency distribution of words in inaugural addresses:")
for word, freq in freq_dist.items():
    print(f"{word}: {freq}")''',
        
        11: '''from nltk.corpus import gutenberg
from collections import Counter
nltk.download('gutenberg')
sense_text = gutenberg.words('austen-sense.txt')
words = [word.lower() for word in sense_text if word.isalpha()]
word_freq = Counter(words)
most_common_words = word_freq.most_common(5)
print("5 most common words in 'Sense and Sensibility':", most_common_words)''',
        
        12: '''import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
import requests
nltk.download('punkt')
url = "https://www.gutenberg.org/files/1342/1342-0.txt"
response = requests.get(url)
text = response.text
tokens = word_tokenize(text)
print("First 10 tokens:", tokens[:10])''',
        
        13: '''import requests
from nltk.tokenize import word_tokenize

def count_words_in_webpage(url):
    response = requests.get(url)
    text = response.text
    print(text)
    tokens = word_tokenize(text)
    return len(tokens)

url = "https://example.com"
word_count = count_words_in_webpage(url)
print("Number of words:", word_count)''',
        
        14: '''import requests
from bs4 import BeautifulSoup

def remove_html_tags(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    cleaned_text = soup.get_text()
    return cleaned_text

url = "https://example.com"
cleaned_text = remove_html_tags(url)
print("Cleaned text:", cleaned_text)

tokens = word_tokenize(cleaned_text)
print("Number of words:", len(tokens))''',
        
        15: '''from nltk.tokenize import sent_tokenize
!wget https://raw.githubusercontent.com/itsfoss/text-script-files/refs/heads/master/agatha.txt

def count_sentences(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    sentences = sent_tokenize(text)
    return len(sentences)

file_path = "agatha.txt"
sentence_count = count_sentences(file_path)
print("Number of sentences:", sentence_count)''',
        
        16: '''import re

def find_ing_words(words):
    return [word for word in words if re.search(r'ing$', word)]

words = ["running", "jumping", "swim", "singing"]
ing_words = find_ing_words(words)
print("Words ending with 'ing':", ing_words)''',
        
        17: '''list1 = [1, 2, 3]
list2 = list1
list2.append(4)
print(f"Using Direct Assigment Operator\nList 1 : {list1}")
print(f"List 2: {list2}")

list3 = [1, 2, 3]
list4 = list3.copy()
list4.append(4)
print(f"Using Copy\nList 3 : {list3}")
print(f"List 4: {list4}")''',
        
        18: '''import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger_eng')

def extract_nouns(text):
    words = word_tokenize(text)
    tagged_words = pos_tag(words)
    nouns = [word for word, pos in tagged_words if pos.startswith('NN')]
    return nouns

text = "The cat sat on the mat and the dog barked."
print(f"Text > {text}")
print(f"Nouns are >\n{extract_nouns(text)}\n\n")''',
        
        19: '''sentence = "This is a sample sentence"
word_lengths = [len(word) for word in sentence.split()]
for word in sentence.split():
    print(f"{word}: {len(word)}")''',
        
        20: '''from collections import Counter

def word_frequency(text):
    words = text.split()
    return dict(Counter(words))

text = "hello world hello"
print(word_frequency(text))''',
        
        21: '''import nltk
from nltk import pos_tag, word_tokenize
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger_eng')

sentence = "The quick brown fox jumps over the lazy dog."
tokens = word_tokenize(sentence)
tagged = pos_tag(tokens)

print(tagged)''',
        
        22: '''def tag_sentences(sentences):
    tagged_sentences = [pos_tag(word_tokenize(sentence)) for sentence in sentences]
    return tagged_sentences

sentences = ["The quick brown fox jumps.", "The lazy dog sleeps."]
print(tag_sentences(sentences))''',
        
        23: '''from nltk import pos_tag, word_tokenize
from nltk.corpus import wordnet
from nltk import pos_tag
from nltk.corpus import wordnet as wn
nltk.download('universal_tagset')

sentence = "The quick brown fox jumps over the lazy dog."
tokens = word_tokenize(sentence)
tagged = pos_tag(tokens, tagset='universal')
print(tagged)''',
        
        24: '''def extract_nouns(sentence):
    tokens = word_tokenize(sentence)
    tagged = pos_tag(tokens)
    nouns = [word for word, pos in tagged if pos.startswith('NN')]
    return nouns

sentence = "The quick brown fox jumps over the lazy dog."
print(extract_nouns(sentence))''',
        
        25: '''from nltk.corpus import brown
from collections import Counter
nltk.download('brown')

news_words = brown.tagged_words(categories='news', tagset='universal')
pos_tags = [tag for word, tag in news_words]
most_common_tag = Counter(pos_tags).most_common(1)[0]

print(most_common_tag)''',
        
        26: '''from nltk import pos_tag, word_tokenize

def pos_tag_frequency(text):
    tokens = word_tokenize(text)
    tagged = pos_tag(tokens)
    pos_tags = [pos for word, pos in tagged]
    frequency = Counter(pos_tags)
    return frequency

text = "The quick brown fox jumps over the lazy dog."
print(pos_tag_frequency(text))''',
        
        27: '''def extract_verbs(sentence):
    tokens = word_tokenize(sentence)
    tagged = pos_tag(tokens)
    verbs = [word for word, pos in tagged if pos.startswith('VB')]
    return verbs

sentence = "The quick brown fox jumps over the lazy dog."
print(extract_verbs(sentence))''',
        
        28: '''import nltk
from nltk.corpus import names
from collections import defaultdict
import random
nltk.download('names')

names = [(name, 'male') for name in names.words('male.txt')] + \
        [(name, 'female') for name in names.words('female.txt')]
random.shuffle(names)

def gender_features(word):
    return {'last_letter': word[-1]}

featuresets = [(gender_features(n), gender) for (n, gender) in names]
train_set, test_set = featuresets[500:], featuresets[:500]
classifier = nltk.NaiveBayesClassifier.train(train_set)
accuracy = nltk.classify.accuracy(classifier, test_set)
print(f"Accuracy: {accuracy:.2f}")''',
        
        29: '''import nltk
from nltk.corpus import names
from collections import defaultdict
import random
nltk.download('names')

def gender_features_enhanced(word):
    return {
        'last_letter': word[-1],
        'first_letter': word[0],
        'length': len(word)
    }

featuresets_enhanced = [(gender_features_enhanced(n), gender) for (n, gender) in names]
train_set_enhanced, test_set_enhanced = featuresets_enhanced[500:], featuresets_enhanced[:500]

classifier_enhanced = nltk.NaiveBayesClassifier.train(train_set_enhanced)
accuracy_enhanced = nltk.classify.accuracy(classifier_enhanced, test_set_enhanced)
print(f"Enhanced Accuracy: {accuracy_enhanced:.2f}")''',
        
        30: '''from nltk.corpus import movie_reviews
from nltk import FreqDist
from nltk.classify import NaiveBayesClassifier
nltk.download('movie_reviews')

documents = [(list(movie_reviews.words(fileid)), category)
             for category in movie_reviews.categories()
             for fileid in movie_reviews.fileids(category)]
random.shuffle(documents)

def document_features(document):
    document_words = set(document)
    features = {}
    for word in document_words:
        features[f'contains({word})'] = (word in document_words)
    return features

featuresets = [(document_features(d), c) for (d, c) in documents]
train_set, test_set = featuresets[:1500], featuresets[1500:]
classifier = NaiveBayesClassifier.train(train_set)
accuracy = nltk.classify.accuracy(classifier, test_set)
print(f"Movie Review Classifier Accuracy: {accuracy:.2f}")''',
        
        31: '''import nltk
nltk.download('all')
from nltk import word_tokenize, pos_tag, ne_chunk

sentence = "Microsoft Inc. is looking at buying U.K. startup for $1 billion."
words = word_tokenize(sentence)
tagged = pos_tag(words)
entities = ne_chunk(tagged)
print(entities)''',
        
        32: '''import nltk
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.tree import Tree
nltk.download('all')

def extract_named_entities(sentences):
    named_entities_list = []

    for sentence in sentences:
        tokens = word_tokenize(sentence)
        pos_tags = pos_tag(tokens)
        chunked_tree = ne_chunk(pos_tags)

        named_entities = []

        for subtree in chunked_tree:
            if isinstance(subtree, Tree):
                entity_name = " ".join(token for token, pos in subtree.leaves())
                named_entities.append(entity_name)

        named_entities_list.append(named_entities)

    return named_entities_list

sentences = ["AppleInc. is looking at buying U.K. startup for $1 billion."]
print(extract_named_entities(sentences))''',
        
        33: '''import nltk
from nltk import word_tokenize, pos_tag, RegexpParser

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def extract_noun_phrases(text):
    tokens = word_tokenize(text)
    pos_tags = pos_tag(tokens)
    grammar = "NP: {<DT>?<JJ>*<NN.*>+}"
    chunk_parser = RegexpParser(grammar)
    tree = chunk_parser.parse(pos_tags)

    noun_phrases = []
    for subtree in tree:
        if hasattr(subtree, 'label') and subtree.label() == 'NP':
            phrase = " ".join(word for word, tag in subtree.leaves())
            noun_phrases.append(phrase)

    return noun_phrases

text = "The quick brown fox jumps over the lazy dog near the tall building."
noun_phrases = extract_noun_phrases(text)
print("Noun Phrases:", noun_phrases)''',
        
        34: '''import nltk
from nltk import word_tokenize, pos_tag, RegexpParser

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

sentence = "He reckons the current account deficit will narrow to only 8 billion."
words = word_tokenize(sentence)
tagged = pos_tag(words)

grammar = r"""
    NP: {<DT>?<JJ>*<NN>}  # Noun phrase
    VP: {<VB.*><NP|PP>}    # Verb phrase
"""
cp = RegexpParser(grammar)
result = cp.parse(tagged)
print(result)''',
        
        35: '''import nltk
from nltk import CFG

grammar = CFG.fromstring("""
    S -> NP VP
    NP -> Det N
    VP -> V PP | V
    PP -> P NP
    Det -> 'The' | 'the'
    N -> 'cat' | 'mat' | 'dog'
    V -> 'sat' | 'jumps'
    P -> 'on' | 'over'
""")

sentence = "The cat sat on the mat"
words = sentence.split()
parser = nltk.ChartParser(grammar)
for tree in parser.parse(words):
    print(tree)
    tree.pretty_print()''',
        
        36: '''import nltk
from nltk import CFG

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

def get_parse_trees(sentence, grammar):
    parser = nltk.ChartParser(grammar)
    return list(parser.parse(sentence))

sentence = ['I', 'saw', 'the', 'man', 'with', 'the', 'telescope']
parse_trees = get_parse_trees(sentence, grammar)
for tree in parse_trees:
    print(tree)
    tree.pretty_print()''',
        
        37: '''from nltk import RecursiveDescentParser
from nltk import CFG
grammar = CFG.fromstring("""
    S -> NP VP
    NP -> Det N | 'She'
    VP -> V NP
    Det -> 'a'
    N -> 'sandwich'
    V -> 'eats'
""")
parser = RecursiveDescentParser(grammar)
sentence = "She eats a sandwich"
for tree in parser.parse(sentence.split()):
    print(tree)
    tree.pretty_print()'''
    }
    return code_dict.get(question_number, "Sorry, question not found.")
