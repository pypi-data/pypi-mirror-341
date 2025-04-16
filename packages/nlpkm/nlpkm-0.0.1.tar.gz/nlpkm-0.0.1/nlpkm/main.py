def nlp():
    num = int(input())
    if(num==1):
        print("""
1.Write a python program using nltk to tokenize the sentence: "Natural Langauge Processing with Python is fun" into words.
from nltk.tokenize import sent_tokenize, word_tokenize 
text = "Natural Langauge Processing with Python is fun!"
print(word_tokenize(text))
              

2.Using NLTK write a program to find the frequency distribution of words in the text of "Moby Dick" by Herman Melville
from nltk.book import *
fdist1 = FreqDist(text1)
print(fdist1)

fdist1.most_common(50)
###########################################################              
import nltk
from nltk.corpus import gutenberg 

# Download necessary NLTK data if not already downloaded
nltk.download('gutenberg') 

# Access the text of Moby Dick from the Gutenberg corpus
text = gutenberg.words('melville-moby_dick.txt') 

# Create a frequency distribution
word_freq = nltk.FreqDist(text) 

# Print the most common words and their frequencies
print("Most common words in Moby Dick:")
for word, count in word_freq.most_common():
    print(f"{word}: {count}") 
###########################################################               
import nltk
from nltk.corpus import gutenberg

# Download necessary NLTK data if not already downloaded
nltk.download('gutenberg')

# Access Moby Dick text from Gutenberg corpus
moby_dick = gutenberg.raw('melville-moby_dick.txt')

# Tokenize the text into words
words = nltk.word_tokenize(moby_dick.lower()) 

# Remove punctuation and non-alphanumeric characters
words = [word for word in words if word.isalnum()] 

# Create a frequency distribution
fdist = nltk.FreqDist(words) 

# Print the most common words and their frequencies
print("Most frequent words in Moby Dick:")
for word, count in fdist.most_common()[:10]:
    print(f"{word}: {count}"


3.Create a bi-gram collocation finder using NLKT for the text of "Sense and Sensibility" by Jnae Austen and list the top 5 Bi-gram
from nltk.book import *
text2.collocations(5)

import nltk
from nltk.corpus import gutenberg
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures

# Download the dataset if not already downloaded
nltk.download('gutenberg')
nltk.download('punkt')

# Load 'Sense and Sensibility' by Jane Austen
text = gutenberg.raw('austen-sense.txt')


# Tokenize words
tokens = nltk.word_tokenize(text)

tokens = [word.lower() for word in tokens if word.isalpha()]

# Find bigrams using BigramCollocationFinder
bigram_finder = BigramCollocationFinder.from_words(tokens)

# Rank bi-grams by Pointwise Mutual Information (PMI)
bigram_scores = bigram_finder.nbest(BigramAssocMeasures.likelihood_ratio,5)

print(bigram_scores)


4.Using NLTK's Text2 , calculate the total number of words and number of distinct words
import nltk
from nltk.book import text2

# Total number of words
total_words = len(text2)

# Number of distinct words (unique words)
distinct_words = len(set(text2))

# Output the results
print("Total number of words:", total_words)
print("Number of distinct words:", distinct_words)
              

5.Compare the lexical diversity of humor and romance fiction in nltks text5 and text2.which genre is more lexically diverse?
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
######################################################################################################
import nltk
from nltk.book import text2, text5 

# Compute lexical diversity
def lexical_diversity(text):
    return len(set(text)) / len(text)

diversity_text5 = lexical_diversity(text5)
diversity_text2 = lexical_diversity(text2)

print(f"Lexical Diversity of Humor Fiction (text5): {diversity_text5:.4f}")
print(f"Lexical Diversity of Romance Fiction (text2): {diversity_text2:.4f}")

# Compare results
if diversity_text5 > diversity_text2:
    print("Humor fiction (chat corpus) is more lexically diverse.")
else:
    print("Romance fiction (Sense and Sensibility) is more lexically diverse.") 


6.Produce a dispersion plot of the four main protagonist in "Sense and sensibility" : Elinor, Marianne, Edward, and Willoughby. What observations can you make about their appearances  in the text?
import nltk
from nltk.corpus import gutenberg
from nltk import FreqDist
from nltk import Text
from nltk.draw import dispersion_plot

# Download required NLTK datasets
nltk.download('gutenberg')
nltk.download('punkt')

# Load the 'Sense and Sensibility' text
sense_sensibility_text = gutenberg.words('austen-sense.txt')

# Create a Text object to use with NLTK's dispersion_plot
sense_sensibility_text = Text(sense_sensibility_text)

# Define the list of character names to plot
characters = ['Elinor', 'Marianne', 'Edward', 'Willoughby']

# Plot the dispersion plot for the characters
sense_sensibility_text.dispersion_plot(characters)
#########################################################################################
import nltk
import matplotlib.pyplot as plt
from nltk.corpus import gutenberg

# Download required dataset
nltk.download('gutenberg')
nltk.download('punkt')

# Load the text of "Sense and Sensibility"
text = nltk.Text(nltk.word_tokenize(gutenberg.raw('austen-sense.txt')))

# List of characters to analyze
characters = ["Elinor", "Marianne", "Edward", "Willoughby"]

# Generate dispersion plot
plt.figure(figsize=(12, 6))
text.dispersion_plot(characters)
            
7.Find the collections in NLTK's text5(the chat corpus). List the top 5 collections.
import nltk
from nltk.book import text5
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures

# Tokenize the text5 into words
words = text5

# Find bigrams in the text using BigramCollocationFinder
bigram_finder = BigramCollocationFinder.from_words(words)

# Apply association measures to find the top 5 collocations using likelihood ratio or pointwise mutual information (PMI)
top_5_collocations = bigram_finder.nbest(BigramAssocMeasures.likelihood_ratio, 5)

# Output the top 5 collocations
print(top_5_collocations)
#############################################################
import nltk
nltk.download('webtext')

from nltk.book import text5  # Chat corpus

# Find collocations in text5
text5.collocations(5)
              

8.Define two lists, phrase1 and phrase2, each containing a few words. join them together to form a sentence.
# Define two lists (Phrase 1 and Phrase 2)
phrase_1 = ["I", "have", "a", "pet", "cat"]
phrase_2 = ["her", "name", "is", "Kaju"]

# Join the lists together to form a sentence
sentence = ' '.join(phrase_1 + phrase_2)

# Output the sentence
print(sentence)
            
""")
    elif (num==2):
        print("""
1.	Use the inaugural address corpus to find the total number of words and the total number of unique words in the inaugural addresses delivered in the 21st century.
import nltk
from nltk.corpus import inaugural

# Download necessary NLTK resources
nltk.download('inaugural')

# List of files for 21st-century inaugural addresses
addresses_21st_century = [
    '2001-Bush.txt',
    '2005-Bush.txt',
    '2009-Obama.txt',
    '2013-Obama.txt',
    '2017-Trump.txt',
    '2021-Biden.txt'
]

# Initialize an empty list to store all the words
all_words = []

# Iterate through the 21st-century addresses
for address in addresses_21st_century:
    # Tokenize the words in each address
    words = nltk.word_tokenize(inaugural.raw(address))
    all_words.extend(words)

# Total number of words (including duplicates)
total_words = len(all_words)

# Total number of unique words (no duplicates)
unique_words = len(set(all_words))

# Print the results
print(f"Total number of words: {total_words}")
print(f"Total number of unique words: {unique_words}")

##############################################################################################################################################################################             
     
2.	Write a Python program to find the frequency distribution of the words "democracy", "freedom", "liberty", and "equality" in all inaugural addresses using NLTK.
import nltk
from nltk.corpus import inaugural
from collections import Counter

# Download necessary NLTK resources
nltk.download('inaugural')
nltk.download('punkt')

# List of target words
target_words = ["democracy", "freedom", "liberty", "equality"]

# Initialize a Counter to keep track of word frequencies
word_frequencies = Counter()

# Iterate over all the inaugural addresses
for file_id in inaugural.fileids():
    # Get the raw text of the address
    text = inaugural.raw(file_id)
    
    # Tokenize the text into words
    words = nltk.word_tokenize(text.lower())  # Convert to lowercase to make it case-insensitive
    
    # Count occurrences of each target word
    for word in target_words:
        word_frequencies[word] += words.count(word.lower())  # Count the occurrences of each word

# Print the frequency distribution of the target words
print("Frequency distribution of target words in all inaugural addresses:")
for word in target_words:
    print(f"{word.capitalize()}: {word_frequencies[word]}")

##############################################################################################################################################################################             
              
3.	Write a Python program to display the 5 most common words in the text of "Sense and Sensibility" by Jane Austen using the Gutenberg Corpus.
import nltk
from nltk.corpus import gutenberg
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
import string

# Download necessary NLTK resources
nltk.download('gutenberg')
nltk.download('punkt')

# Load the text of "Sense and Sensibility" by Jane Austen
sense_and_sensibility = gutenberg.raw('austen-sense.txt')

# Tokenize the text into words
words = word_tokenize(sense_and_sensibility)

# Remove punctuation and convert words to lowercase
cleaned_words = [word.lower() for word in words if word.isalpha()]

# Calculate the frequency distribution of words
fdist = FreqDist(cleaned_words)

# Display the 5 most common words
print("5 most common words in Sense and Sensibility:")
print(fdist.most_common(5))
              
##############################################################################################################################################################################                    

4.	Generate a conditional frequency distribution of modal verbs ('can', 'could', 'may', 'might', 'must', 'will') across the categories of the Brown Corpus.
import nltk
from nltk.corpus import brown
import pandas as pd

# Download necessary NLTK resources
nltk.download('brown')

# List of modal verbs
modal_verbs = ['can', 'could', 'may', 'might', 'must', 'will']

# Initialize a dictionary to hold frequencies
frequency_matrix = {verb: [] for verb in modal_verbs}

# Iterate over all categories in the Brown Corpus
for category in brown.categories():
    # Get all the words (tagged as (word, POS)) in the current category
    tagged_words = brown.tagged_words(categories=category)
    
    # Initialize a frequency counter for modal verbs in this category
    counts = {verb: 0 for verb in modal_verbs}
    
    # Iterate through the tagged words
    for word, tag in tagged_words:
        # Check if the word is a modal verb
        if word.lower() in modal_verbs:
            counts[word.lower()] += 1
    
    # Append the count for each modal verb in the current category
    for verb in modal_verbs:
        frequency_matrix[verb].append(counts[verb])

# Convert the frequency matrix into a pandas DataFrame for easier readability
df = pd.DataFrame(frequency_matrix, index=brown.categories())

# Display the matrix
print("Frequency Distribution of Modal Verbs across Categories:")
print(df)


##############################################################################################################################################################################                     

5.	Write a Python program to identify the longest word in "Moby Dick" from the Gutenberg Corpus.
import nltk
from nltk.corpus import gutenberg
import string

# Download necessary NLTK resources
nltk.download('gutenberg')
nltk.download('punkt')

# Load the text of "Moby Dick" from the Gutenberg Corpus
moby_dick = gutenberg.raw('melville-moby_dick.txt')

# Tokenize the text into words
words = nltk.word_tokenize(moby_dick)

# Preprocess: remove punctuation and non-alphabetic words, and convert to lowercase
cleaned_words = [word.lower() for word in words if word.isalpha()]

# Find the longest word
longest_word = max(cleaned_words, key=len)

print(f"The longest word in 'Moby Dick' is: {longest_word}")
              

##############################################################################################################################################################################             

6.	Using the Brown Corpus, calculate the frequency of the word "government" across all categories.
import nltk
from nltk.corpus import brown

# Download necessary NLTK resources
nltk.download('brown')

# Initialize a dictionary to store the frequency of the word "government" in each category
government_freq = {}

# Iterate through the categories of the Brown Corpus
for category in brown.categories():
    # Tokenize the words in the category
    words = brown.words(categories=category)
    
    # Count occurrences of the word "government" in the current category
    freq = words.count('government')
    
    # Store the frequency in the dictionary
    government_freq[category] = freq

# Display the frequency of the word "government" across all categories
print("Frequency of the word 'government' across all categories:")
for category, freq in government_freq.items():
    print(f"Category: {category} - Frequency: {freq}")
##############################################################################################################################################################################             

7.	Write a Python program using the Reuters Corpus to find the number of documents categorized under "crude".
import nltk
from nltk.corpus import reuters

# Download necessary NLTK resources
nltk.download('reuters')

# Get a list of all document IDs in the Reuters Corpus
document_ids = reuters.fileids()

# Initialize a counter for the number of documents in the "crude" category
crude_count = 0

# Iterate over all documents and check if they belong to the "crude" category
for doc_id in document_ids:
    if 'crude' in reuters.categories(doc_id):
        crude_count += 1

# Display the number of documents categorized under "crude"
print(f"Number of documents categorized under 'crude': {crude_count}")
##############################################################################################################################################################################             
""")
    elif (num==3):
        print("""
1.	Write a Python program to download the text of "Pride and Prejudice" by Jane Austen from Project Gutenberg, tokenize the text, and display the first 10 tokens.
import requests
import nltk
nltk.download('punkt')

# Download the text of "Pride and Prejudice" from Project Gutenberg
url = "https://www.gutenberg.org/files/1342/1342-0.txt"
response = requests.get(url)
text = response.text

# Tokenize the text
tokens = nltk.word_tokenize(text)

# Display the first 10 tokens
print(tokens[:10])
              
                          
2.	Using NLTK, write a function that takes a URL as input, fetches the raw text from the webpage, and returns the number of words in the text.
import nltk
import requests
from bs4 import BeautifulSoup

nltk.download('punkt')

def word_count_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract text from the page
    text = soup.get_text()
    
    # Tokenize the text into words
    words = nltk.word_tokenize(text)
    
    # Return the number of words
    return len(words)

# Example usage
url = "https://www.geeksforgeeks.org/static-websites/"
print(word_count_from_url(url))

              
3.	Explain how to remove HTML tags from a web page's content using Python and NLTK. Provide a code example that fetches a web page, removes HTML tags, and prints the cleaned text.
import requests
from bs4 import BeautifulSoup

def remove_html_tags(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract text without HTML tags
    text = soup.get_text()
    
    return text

# Example usage
url = "https://www.gutenberg.org/files/1342/1342-0.txt"
clean_text = remove_html_tags(url)
print(clean_text[:200])  # Print first 200 characters of cleaned text


4.	Write a Python program that reads a text file, tokenizes its content into sentences, and prints the number of sentences in the file.
import nltk

# Read the text file
with open('D:/C045/Text.txt', 'r') as file:
    text = file.read()

# Tokenize the text into sentences
sentences = nltk.sent_tokenize(text)

# Print the number of sentences
print(f"Number of sentences: {len(sentences)}")


5.	Using regular expressions in Python, write a function that takes a list of words and returns a list of words that end with 'ing'.
import re

def words_ending_with_ing(word_list):
    return [word for word in word_list if re.search(r'ing$', word)]

# Example usage
words = ["running", "playing", "jump", "singing", "cat"]
print(words_ending_with_ing(words))
           
              
6.	Describe how to normalize text by converting it to lowercase and removing punctuation using NLTK. Provide a code example that processes a given sentence.
import nltk
import string

nltk.download('punkt')

def normalize_text(sentence):
    # Tokenize the sentence
    tokens = nltk.word_tokenize(sentence)
    
    # Remove punctuation and convert to lowercase
    normalized = [word.lower() for word in tokens if word not in string.punctuation]
    
    return normalized

# Example usage
sentence = "Hello, World! It's a great day."
print(normalize_text(sentence))


7.	Using NLTK's PorterStemmer, write a function that takes a list of words and returns a list of their stemmed forms.
from nltk.stem import PorterStemmer

def stem_words(word_list):
    stemmer = PorterStemmer()
    return [stemmer.stem(word) for word in word_list]

# Example usage
words = ["running", "played", "playing", "happier", "happiness", "happy"]
print(stem_words(words))
                          
              
8.	Explain the difference between stemming and lemmatization in text processing. Provide code examples using NLTK to demonstrate both processes on the word 'running'.
from nltk.stem import PorterStemmer, WordNetLemmatizer
nltk.download('wordnet')

def stem_and_lemma(word):
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    
    stemmed = stemmer.stem(word)
    lemmatized = lemmatizer.lemmatize(word, pos='v')  # Lemmatize as verb
    
    return stemmed, lemmatized

# Example usage
word = "running"
stemmed, lemmatized = stem_and_lemma(word)
print(f"Stemmed: {stemmed}, Lemmatized: {lemmatized}")


9.	Write a Python program to count the number of vowels (a, e, i, o, u) in a given text.
def count_vowels(text):
    vowels = "aeiou"
    count = sum(1 for char in text.lower() if char in vowels)
    return count

# Example usage
text = "Hello, how many vowels are here?"
print(count_vowels(text))


10.	Write a Python program to tokenize the text into words and filter out words that contain digits.
import nltk

nltk.download('punkt')

def filter_words_with_digits(text):
    tokens = nltk.word_tokenize(text)
    return [word for word in tokens if not any(char.isdigit() for char in word)]

# Example usage
text = "I have 2 apples and 3 oranges."
print(filter_words_with_digits(text))

            
11.	Write a program to read text from a file and display all the words starting with a capital letter.
import nltk

nltk.download('punkt')

def words_starting_with_capital(text):
    tokens = nltk.word_tokenize(text)
    return [word for word in tokens if word[0].isupper()]

# Example usage
text = "This is a Sample Text with Some Capitalized Words."
print(words_starting_with_capital(text))


12.	Write a Python program to identify and display all the email addresses from a given text.
import re

def extract_emails(text):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(email_pattern, text)

# Example usage
text = "Here are some emails: test@example.com, hello@world.org."
print(extract_emails(text))


13.	Write a program to tokenize a text into sentences and display only those sentences containing more than 10 words.
import nltk

nltk.download('punkt')

def sentences_with_more_than_10_words(text):
    sentences = nltk.sent_tokenize(text)
    return [sentence for sentence in sentences if len(nltk.word_tokenize(sentence)) > 10]

# Example usage
text = "This is a short sentence. This one has a lot of words and is definitely much longer than the other one."
print(sentences_with_more_than_10_words(text))


14.	Write a Python program that takes a sentence as input and returns all words that are at least 5 characters long.
import nltk

nltk.download('punkt')

def words_at_least_5_characters(text):
    tokens = nltk.word_tokenize(text)
    return [word for word in tokens if len(word) >= 5]

# Example usage
sentence = "I like programming with Python and learning new things."
print(words_at_least_5_characters(sentence))


15.	Write a Python program using regular expressions to find all words starting with 'un' in a given text.
import re

def words_starting_with_un(text):
    return re.findall(r'\bun\w*', text)

# Example usage
text = "The unexpected turn of events was unfortunate."
print(words_starting_with_un(text))

""")
    elif (num==4):
        print("""
1.	Explain the difference between assigning a list to a new variable using direct assignment (=) and using the copy() method. Provide code examples to illustrate the difference.
original_list = [1, 2, 3]
new_list = original_list  # Direct assignment
new_list[0] = 99
print(original_list)  # Output: [99, 2, 3] (Both refer to the same list)
print(new_list)       # Output: [99, 2, 3]
original_list = [1, 2, 3]
new_list = original_list.copy()  # Using copy() method
new_list[0] = 99
print(original_list)  # Output: [1, 2, 3] (Original list is unchanged)
print(new_list)       # Output: [99, 2, 3]


2.	Write a function extract_nouns(text) that takes a text string as input and returns a list of all nouns in the text. Use NLTK's part-of-speech tagging for this task.
import nltk
from nltk import pos_tag
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def extract_nouns(text):
    words = word_tokenize(text)
    tagged = pos_tag(words)
    nouns = [word for word, pos in tagged if pos in ['NN', 'NNS', 'NNP', 'NNPS']]
    return nouns

# Example usage
text = "The cat and the dog are playing in the park."
print(extract_nouns(text))

                          
3.	Demonstrate how to use list comprehension to create a list of the lengths of each word in a given sentence.
sentence = "This is an example sentence"
word_lengths = [len(word) for word in sentence.split()]
print(word_lengths)  # Output: [4, 2, 2, 7, 8]

            
4.	Write a function word_frequency(text) that takes a text string and returns a dictionary with words as keys and their frequencies as values.
from collections import Counter

def word_frequency(text):
    words = text.split()
    return dict(Counter(words))

# Example usage
text = "apple orange apple banana apple orange"
print(word_frequency(text))  # Output: {'apple': 3, 'orange': 2, 'banana': 1}


5.	Explain the concept of variable scope in Python with an example demonstrating the difference between local and global variables.
x = 10  # Global variable

def my_function():
    y = 5  # Local variable
    print("Local variable y:", y)
    print("Global variable x:", x)

my_function()
print("Global variable x outside function:", x)
# print(y)  # This would raise an error as 'y' is local to the function



6.	Write a Python program that reads a text file and counts the number of lines, words, and characters in the file.
def count_file_details(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        num_lines = len(lines)
        num_words = sum(len(line.split()) for line in lines)
        num_chars = sum(len(line) for line in lines)
    
    return num_lines, num_words, num_chars

# Example usage (assuming "sample.txt" exists)
file_path = 'D:/C045/Text.txt'
lines, words, chars = count_file_details(file_path)
print(f"Lines: {lines}, Words: {words}, Characters: {chars}")



7.	Describe how to handle exceptions in Python with a try-except block. Provide an example that handles a division by zero error.
def division(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        return "Error: Division by zero is not allowed"
    return result

# Example usage
print(division(10, 2))  # Output: 5.0
print(division(10, 0))  # Output: Error: Division by zero is not allowed



8.	Write a function remove_stopwords(text) that removes common English stopwords from a given text using NLTK's stopwords corpus.
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
nltk.download('punkt')

def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return filtered_words

# Example usage
text = "This is a sample sentence with stopwords."
print(remove_stopwords(text))


9.	Write a Python program to extract and print all words from a text that start with a capital letter using regular expressions.
import re

def extract_capitalized_words(text):
    return re.findall(r'\b[A-Z][a-z]*\b', text)

# Example usage
text = "Alice and Bob are working together."
print(extract_capitalized_words(text))  # Output: ['Alice', 'Bob']



10.	Write a Python program to tokenize a given text into words and count how many words are exactly 5 characters long.
import nltk
nltk.download('punkt')

def count_five_letter_words(text):
    words = nltk.word_tokenize(text)
    return len([word for word in words if len(word) == 5])

# Example usage
text = "This is a simple example text."
print(count_five_letter_words(text))  # Output: 2 (simple, text)



11.	Write a Python program to use regular expressions to find all email addresses in a given string.
import re

def extract_emails(text):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(email_pattern, text)

# Example usage
text = "Here are two emails: test@example.com and hello@world.org"
print(extract_emails(text))  # Output: ['test@example.com', 'hello@world.org']

                          
12.	Write a Python program to tokenize a sentence into words and then sort the words alphabetically.
import nltk
nltk.download('punkt')

def sort_words_alphabetically(text):
    words = nltk.word_tokenize(text)
    return sorted(words)

# Example usage
text = "This is a simple sentence"
print(sort_words_alphabetically(text))  # Output: ['a', 'is', 'sentence', 'simple', 'This']


13.	Write a Python program to calculate and print the lexical diversity of a given text.
import nltk
nltk.download('punkt')

def lexical_diversity(text):
    words = nltk.word_tokenize(text)
    return len(set(words)) / len(words) if len(words) > 0 else 0

# Example usage
text = "This is a simple sentence with some repetition repetition."
print(lexical_diversity(text))  # Output: 0.833 (or similar)


14.	Write a Python program that takes a sentence as input and prints the words in reverse order.
def reverse_words(sentence):
    words = sentence.split()
    return ' '.join(reversed(words))

# Example usage
sentence = "Hello World, how are you?"
print(reverse_words(sentence))  # Output: "you? are how World, Hello"


15.	Write a Python program to find and print all words in a text that contain at least one digit.
import re

def find_words_with_digits(text):
    return re.findall(r'\b\w*\d\w*\b', text)

# Example usage
text = "I have 2 apples and 3 oranges."
print(find_words_with_digits(text))  # Output: ['2', '3']
              
        """)
    elif (num==5):
        print("""
1.	Write a Python program using NLTK to perform part-of-speech tagging on the sentence: "The quick brown fox jumps over the lazy dog."
sentence = "The quick brown fox jumps over the lazy dog."
words = nltk.word_tokenize(sentence)
pos_tags = nltk.pos_tag(words)

print("POS Tags:", pos_tags)
              

2.	Using NLTK, write a function that takes a list of sentences and returns a list of part-of-speech tagged sentences.
def pos_tag_sentences(sentences):
    return [nltk.pos_tag(nltk.word_tokenize(sentence)) for sentence in sentences]

sentences = ["The sun is shining.", "The birds are chirping."]
print(pos_tag_sentences(sentences))



3.	Explain how to map the Penn Treebank POS tags to the Universal POS tags using NLTK. Provide a code example that tags a sentence and maps the tags accordingly.
nltk.download('universal_tagset')

sentence = "The quick brown fox jumps over the lazy dog."
words = nltk.word_tokenize(sentence)
pos_tags = nltk.pos_tag(words)
universal_tags = [(word, nltk.map_tag('en-ptb', 'universal', tag)) for word, tag in pos_tags]

print("Mapped Tags:", universal_tags)


4.	Write a Python function using NLTK that takes a sentence as input and returns a list of all nouns in the sentence.
def extract_nouns(sentence):
    words = nltk.word_tokenize(sentence)
    pos_tags = nltk.pos_tag(words)
    return [word for word, tag in pos_tags if tag.startswith('NN')]

sentence = "The quick brown fox jumps over the lazy dog."
print("Nouns:", extract_nouns(sentence))


5.	Using the Brown Corpus in NLTK, write a program to find the most common part-of-speech tag in the news category.
nltk.download('brown')

from nltk.corpus import brown
from collections import Counter

news_tags = brown.tagged_words(categories='news')
tag_counts = Counter(tag for _, tag in news_tags)

print("Most Common POS Tag:", tag_counts.most_common(1))


6.	Write a Python program using NLTK to train a unigram part-of-speech tagger on the Brown Corpus and evaluate its accuracy.
import nltk
from nltk.tag import UnigramTagger
from nltk.corpus import brown
from collections import Counter

# Updated code:
# Load the tagged sentences from the 'news' category
all_news_tagged_sents = brown.tagged_sents(categories='news')

# Define the training size and test size
train_size = len(all_news_tagged_sents) - 500
test_size = 500

# Split the data into training and testing sets
train_data = all_news_tagged_sents[:train_size]
test_data = all_news_tagged_sents[train_size:]

# Train the UnigramTagger
unigram_tagger = UnigramTagger(train_data)

# Evaluate the tagger and print the accuracy
print("Unigram Tagger Accuracy:", unigram_tagger.evaluate(test_data))

# Example use of other functions to verify they work:
def extract_nouns(sentence):
    words = nltk.word_tokenize(sentence)
    pos_tags = nltk.pos_tag(words)
    return [word for word, tag in pos_tags if tag.startswith('NN')]

sentence = "The quick brown fox jumps over the lazy dog."
print("Nouns:", extract_nouns(sentence))

news_tags = brown.tagged_words(categories='news')
tag_counts = Counter(tag for _, tag in news_tags)

print("Most Common POS Tag:", tag_counts.most_common(1))


7.	Explain the concept of backoff tagging in NLTK. Write a Python program that combines a bigram tagger with a unigram tagger as a backoff, and evaluate its performance on the Brown Corpus.
import nltk
nltk.download('brown')
nltk.download('punkt')
from nltk.tag import UnigramTagger, BigramTagger
from nltk.corpus import brown
from collections import Counter

# Load the tagged sentences from the 'news' category
all_news_tagged_sents = brown.tagged_sents(categories='news')

# Determine the number of sentences in the 'news' category
num_sentences = len(all_news_tagged_sents)
print(f"Number of sentences in the 'news' category: {num_sentences}")

# Define the training size and test size
# Make sure the train size will be large enough that the test size is positive
train_size = num_sentences - 500
test_size = num_sentences - train_size

# Split the data into training and testing sets
train_data = all_news_tagged_sents[:train_size]
test_data = all_news_tagged_sents[train_size:]

# Train the UnigramTagger
unigram_tagger = UnigramTagger(train_data)

# Evaluate the tagger and print the accuracy
print("Unigram Tagger Accuracy:", unigram_tagger.evaluate(test_data))

# Example use of other functions to verify they work:
def extract_nouns(sentence):
    words = nltk.word_tokenize(sentence)
    pos_tags = nltk.pos_tag(words)
    return [word for word, tag in pos_tags if tag.startswith('NN')]

sentence = "The quick brown fox jumps over the lazy dog."
print("Nouns:", extract_nouns(sentence))

news_tags = brown.tagged_words(categories='news')
tag_counts = Counter(tag for _, tag in news_tags)

print("Most Common POS Tag:", tag_counts.most_common(1))

# Create a bigram tagger
bigram_tagger = BigramTagger(train_data, backoff=unigram_tagger)

# Determine an appropriate slice for evaluation
# Find out how many sentences remain after train_size
remaining_sentences = num_sentences - train_size

# If there are remaining sentences, use them for the test
if remaining_sentences > 0:
    # Use remaining sentences
    print("Bigram + Unigram Tagger Accuracy:", bigram_tagger.evaluate(all_news_tagged_sents[train_size:]))
else:
    print("Not enough data to evaluate BigramTagger")


8.	Write a Python program to tag words with part-of-speech using NLTK and then extract all adjectives from the sentence: "The beautiful sunset painted the sky with vibrant colors."
def extract_adjectives(sentence):
    words = nltk.word_tokenize(sentence)
    pos_tags = nltk.pos_tag(words)
    return [word for word, tag in pos_tags if tag.startswith('JJ')]

sentence = "The beautiful sunset painted the sky with vibrant colors."
print("Adjectives:", extract_adjectives(sentence))


9.	Write a Python program to calculate the frequency of each part-of-speech tag in a given text.
def pos_frequency(text):
    words = nltk.word_tokenize(text)
    pos_tags = nltk.pos_tag(words)
    return Counter(tag for _, tag in pos_tags)

text = "The quick brown fox jumps over the lazy dog."
print("POS Frequency:", pos_frequency(text))


10.	Using NLTK, write a program that tags words in a sentence and prints only the verbs.
def extract_verbs(sentence):
    words = nltk.word_tokenize(sentence)
    pos_tags = nltk.pos_tag(words)
    return [word for word, tag in pos_tags if tag.startswith('VB')]

sentence = "The quick brown fox jumps over the lazy dog."
print("Verbs:", extract_verbs(sentence))


11.	Write a Python program using NLTK to identify and print all proper nouns from a given sentence.
 def extract_proper_nouns(sentence):
    words = nltk.word_tokenize(sentence)
    pos_tags = nltk.pos_tag(words)
    return [word for word, tag in pos_tags if tag == 'NNP']

sentence = "Alice and Bob went to New York."
print("Proper Nouns:", extract_proper_nouns(sentence))


12.	Write a Python program to train a trigram part-of-speech tagger with a unigram backoff on the Brown corpus and evaluate its performance.
import nltk
nltk.download('brown')
nltk.download('punkt')
from nltk.tag import UnigramTagger, BigramTagger, TrigramTagger
from nltk.corpus import brown
from collections import Counter

# Load the tagged sentences from the 'news' category
all_news_tagged_sents = brown.tagged_sents(categories='news')

# Determine the number of sentences in the 'news' category
num_sentences = len(all_news_tagged_sents)
print(f"Number of sentences in the 'news' category: {num_sentences}")

# Define the training size and test size
# Make sure the train size will be large enough that the test size is positive
train_size = num_sentences - 500
test_size = 500

# Split the data into training and testing sets
train_data = all_news_tagged_sents[:train_size]
test_data = all_news_tagged_sents[train_size:]

# Train the UnigramTagger
unigram_tagger = UnigramTagger(train_data)

# Create a trigram tagger
trigram_tagger = TrigramTagger(train_data, backoff=unigram_tagger)

# Determine an appropriate slice for evaluation
# Find out how many sentences remain after train_size
remaining_sentences = num_sentences - train_size

# If there are remaining sentences, use them for the test
if remaining_sentences > 0:
    # Use remaining sentences
    print("Trigram + Unigram Tagger Accuracy:", trigram_tagger.evaluate(all_news_tagged_sents[train_size:]))
else:
    print("Not enough data to evaluate TrigramTagger")


13.	Write a Python program using NLTK to tag a sentence and count how many words belong to each part-of-speech category.
def count_pos_categories(sentence):
    words = nltk.word_tokenize(sentence)
    pos_tags = nltk.pos_tag(words)
    return Counter(tag for _, tag in pos_tags)

sentence = "The little dog barked at the big cat."
print("POS Category Counts:", count_pos_categories(sentence))


14.	Write a Python program to tag a given text with part-of-speech tags and then filter out only determiners (DT) using NLTK.
def filter_determiners(sentence):
    words = nltk.word_tokenize(sentence)
    pos_tags = nltk.pos_tag(words)
    return [word for word, tag in pos_tags if tag == 'DT']

sentence = "The boy found a book on the table."
print("Determiners:", filter_determiners(sentence))


15.	Write a Python program to calculate and print the lexical diversity of nouns, verbs, adjectives, and adverbs in a given text.
def lexical_diversity(text):
    words = nltk.word_tokenize(text)
    pos_tags = nltk.pos_tag(words)

    pos_categories = {
        'nouns': [word for word, tag in pos_tags if tag.startswith('NN')],
        'verbs': [word for word, tag in pos_tags if tag.startswith('VB')],
        'adjectives': [word for word, tag in pos_tags if tag.startswith('JJ')],
        'adverbs': [word for word, tag in pos_tags if tag.startswith('RB')],
    }

    diversity_scores = {key: len(set(words)) / len(words) if words else 0 for key, words in pos_categories.items()}
    return diversity_scores

text = "The quick brown fox jumps swiftly over the lazy dog. The dog barked loudly."
print("Lexical Diversity:", lexical_diversity(text))
              
        """)
    elif (num==6):
        print("""

import nltk
import random
from nltk.corpus import names
from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy
              

1.	Using the names corpus in NLTK, build a gender classifier that predicts whether a name is male or female based on the last letter of the name. Evaluate its accuracy.
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


2.	Enhance the gender classifier by including features such as the first letter and the length of the name. Evaluate if these features improve the classifier's accuracy.
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


3.	Using the movie_reviews corpus in NLTK, build a document classifier to categorize movie reviews as positive or negative. Evaluate its performance.
import nltk
import random
from nltk.corpus import movie_reviews
from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy

nltk.download('movie_reviews')

# Load movie review data
documents = [(list(movie_reviews.words(fileid)), category)
             for category in movie_reviews.categories()
             for fileid in movie_reviews.fileids(category)]

# Shuffle data
random.shuffle(documents)

# Feature extractor (unigrams)
def document_features(words):
    return {word.lower(): True for word in words}

# Prepare dataset
featuresets = [(document_features(words), category) for words, category in documents]

# Train classifier
classifier = NaiveBayesClassifier.train(featuresets)

# Evaluate
print("Movie Review Classifier Accuracy:", accuracy(classifier, featuresets))
classifier.show_most_informative_features(10)

                          
4.	Implement a custom feature extractor for the movie review classifier that considers bigrams (pairs of consecutive words) in addition to unigrams (single words). Evaluate its impact on classification accuracy.
from nltk import bigrams

# Feature extractor with unigrams and bigrams
def bigram_features(words):
    words = [w.lower() for w in words]
    word_features = {word: True for word in words}  # Unigrams
    bigram_features = {f"{w1}_{w2}": True for w1, w2 in bigrams(words)}  # Bigrams
    return {**word_features, **bigram_features}

# Prepare dataset
bigram_featuresets = [(bigram_features(words), category) for words, category in documents]

# Train classifier
bigram_classifier = NaiveBayesClassifier.train(bigram_featuresets)

# Evaluate
print("Bigram Movie Review Classifier Accuracy:", accuracy(bigram_classifier, bigram_featuresets))
bigram_classifier.show_most_informative_features(10)


5.	Build a Naive Bayes classifier using the names corpus to predict gender based on both the first and last letters of a name. Evaluate the model's accuracy.
from nltk.corpus import names

nltk.download('names')

# Extract names
male_names = [(name, 'male') for name in names.words('male.txt')]
female_names = [(name, 'female') for name in names.words('female.txt')]

# Combine and shuffle data
data = male_names + female_names
random.shuffle(data)

# Feature extractor (first and last letter)
def name_features(name):
    return {
        'first_letter': name[0].lower(),
        'last_letter': name[-1].lower(),
    }

# Prepare dataset
name_featuresets = [(name_features(name), gender) for name, gender in data]

# Train classifier
name_classifier = NaiveBayesClassifier.train(name_featuresets)

# Evaluate
print("Name Classifier Accuracy:", accuracy(name_classifier, name_featuresets))
name_classifier.show_most_informative_features(5)


6.	Write a Python program using the movie_reviews corpus to identify the 10 most common words in positive reviews.
import nltk
from nltk.corpus import movie_reviews
from collections import Counter

nltk.download('movie_reviews')

# Get words from positive reviews
positive_words = [word.lower() for fileid in movie_reviews.fileids('pos')
                  for word in movie_reviews.words(fileid)]

# Count frequency
word_freq = Counter(positive_words)

# Display top 10 words (excluding stopwords)
common_words = word_freq.most_common(10)
print("Top 10 Most Common Words in Positive Reviews:", common_words)


7.	Implement a Naive Bayes classifier to classify movie reviews using only adjectives as features.
import random
import nltk
from nltk.corpus import movie_reviews
from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy
from nltk import pos_tag
nltk.download('averaged_perceptron_tagger_eng')

nltk.download('movie_reviews')
nltk.download('averaged_perceptron_tagger')

# Load and shuffle data
documents = [(list(movie_reviews.words(fileid)), category)
             for category in movie_reviews.categories()
             for fileid in movie_reviews.fileids(category)]
random.shuffle(documents)

# Feature extractor: Use only adjectives
def adjective_features(words):
    words = [word.lower() for word in words]
    tagged_words = pos_tag(words)  # Part-of-speech tagging
    return {word: True for word, tag in tagged_words if tag.startswith('JJ')}  # JJ = adjective

# Prepare dataset
featuresets = [(adjective_features(words), category) for words, category in documents]

# Train classifier
classifier = NaiveBayesClassifier.train(featuresets)

# Evaluate
print("Adjective-Based Classifier Accuracy:", accuracy(classifier, featuresets))
classifier.show_most_informative_features(10)


8.	Write a Python program that uses the names corpus to build a gender classifier using Decision Tree Classifier from NLTK
import random
import nltk
from nltk.corpus import names
from nltk.classify import DecisionTreeClassifier

nltk.download('names')

# Load names dataset
male_names = [(name, 'male') for name in names.words('male.txt')]
female_names = [(name, 'female') for name in names.words('female.txt')]

# Combine and shuffle data
data = male_names + female_names
random.shuffle(data)

# Feature extractor
def name_features(name):
    return {'first_letter': name[0].lower(), 'last_letter': name[-1].lower()}

# Prepare dataset
feature_sets = [(name_features(name), gender) for name, gender in data]

# Train classifier
classifier = DecisionTreeClassifier.train(feature_sets)

# Evaluate
print("Decision Tree Name Classifier Accuracy:", nltk.classify.accuracy(classifier, feature_sets))


9.	Write a Python program using NLTK to identify bigrams that are frequently used together in movie reviews.
import nltk
from nltk.corpus import movie_reviews
from collections import Counter
from nltk import bigrams

nltk.download('movie_reviews')

# Get words from all reviews
all_words = [word.lower() for word in movie_reviews.words()]

# Extract bigrams
bigram_list = list(bigrams(all_words))

# Count bigram frequency
bigram_freq = Counter(bigram_list)

# Display top 10 bigrams
print("Top 10 Most Frequent Bigrams:", bigram_freq.most_common(10))


10.	Write a Python program to train a Naive Bayes classifier on the movie_reviews corpus with features based on word lengths.
import random
import nltk
from nltk.corpus import movie_reviews
from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy

nltk.download('movie_reviews')

# Load and shuffle data
documents = [(list(movie_reviews.words(fileid)), category)
             for category in movie_reviews.categories()
             for fileid in movie_reviews.fileids(category)]
random.shuffle(documents)

# Feature extractor: Word lengths
def word_length_features(words):
    return {'avg_word_length': sum(len(word) for word in words) / len(words)}

# Prepare dataset
featuresets = [(word_length_features(words), category) for words, category in documents]

# Train classifier
classifier = NaiveBayesClassifier.train(featuresets)

# Evaluate
print("Word Length-Based Classifier Accuracy:", accuracy(classifier, featuresets))


11.	Write a Python program using NLTK to create a frequency distribution of word lengths from movie reviews.
import nltk
import matplotlib.pyplot as plt
from nltk.corpus import movie_reviews
from collections import Counter

nltk.download('movie_reviews')

# Get word lengths
word_lengths = [len(word) for word in movie_reviews.words()]

# Compute frequency distribution
length_freq = Counter(word_lengths)

# Plot
plt.bar(length_freq.keys(), length_freq.values())
plt.xlabel("Word Length")
plt.ylabel("Frequency")
plt.title("Word Length Frequency Distribution in Movie Reviews")
plt.show()


12.	Write a Python program to extract all named entities from a given text using NLTK's ne_chunk functionality.
import nltk

nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('punkt_tab')
nltk.download('maxent_ne_chunker_tab')

# Sample text
text = "Elon Musk is the CEO of Tesla and was born in Pretoria, South Africa."

# Tokenize and tag
words = nltk.word_tokenize(text)
tagged_words = nltk.pos_tag(words)

# Named Entity Recognition (NER)
ner_tree = nltk.ne_chunk(tagged_words)

# Print named entities
print("Named Entities:", ner_tree)

        """)
    elif (num==7):
        print("""
1.	Write a Python program using NLTK to extract named entities from the sentence: "Apple Inc. is looking at buying U.K. startup for $1 billion."
import nltk

nltk.download('punkt')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('punkt_tab')
nltk.download('maxent_ne_chunker_tab')
nltk.download('averaged_perceptron_tagger_eng')

# Sample sentence
sentence = "Apple Inc. is looking at buying U.K. startup for $1 billion."

# Tokenization & POS tagging
tokens = nltk.word_tokenize(sentence)
pos_tags = nltk.pos_tag(tokens)

# Named Entity Recognition (NER)
ner_tree = nltk.ne_chunk(pos_tags)

# Print the named entity tree
print(ner_tree)
#####################################3
import spacy

# Load English NLP model
nlp = spacy.load("en_core_web_sm")

# Process the text
sentence = "Apple Inc. is looking at buying U.K. startup for $1 billion."
doc = nlp(sentence)

# Print Named Entities
for ent in doc.ents:
    print(ent.text, ent.label_)              

2.	Using NLTK, write a function that takes a list of sentences and returns a list of named entities found in each sentence.
def extract_named_entities(sentences):
    named_entities = []

    for sentence in sentences:
        tokens = nltk.word_tokenize(sentence)
        pos_tags = nltk.pos_tag(tokens)
        ner_tree = nltk.ne_chunk(pos_tags)

        # Extract named entities
        entities = []
        for subtree in ner_tree:
            if isinstance(subtree, nltk.Tree):  # If it's a named entity
                entity_name = " ".join([token for token, pos in subtree.leaves()])
                entity_type = subtree.label()
                entities.append((entity_name, entity_type))

        named_entities.append(entities)

    return named_entities

# Example usage
sentences = ["Microsoft Corporation is headquartered in Redmond.",
             "Barack Obama was the 44th President of the USA."]
print(extract_named_entities(sentences))


3.	Write a Python program that uses NLTK to extract and display all noun phrases from a given text.
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


4.	Using NLTK, write a program to perform chunking on the sentence: "He reckons the current account deficit will narrow to only 8 billion." and display the chunked tree.
import nltk

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


5.	Write a Python function using NLTK that takes a sentence as input and returns all verb phrases (VP) present in the sentence.
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


6.	Write a Python program using NLTK to perform named entity recognition (NER) on a paragraph containing multiple sentences. Display the extracted named entities.
paragraph = Elon Musk founded SpaceX and Tesla.
Google was started in California.
Apple Inc. is one of the biggest tech companies. 
sentences = nltk.sent_tokenize(paragraph)

for sentence in sentences:
    tokens = nltk.word_tokenize(sentence)
    pos_tags = nltk.pos_tag(tokens)
    ner_tree = nltk.ne_chunk(pos_tags)
    print(ner_tree)


7.	Write a Python program to count the number of named entities of type GPE (Geopolitical Entity) in a given text.
nltk.download('words')

text = "Barack Obama was born in Hawaii and later moved to Washington, D.C."

tokens = nltk.word_tokenize(text)
pos_tags = nltk.pos_tag(tokens)
ner_tree = nltk.ne_chunk(pos_tags)

gpe_count = sum(1 for subtree in ner_tree if isinstance(subtree, nltk.Tree) and subtree.label() == "GPE")
print("Number of GPEs:", gpe_count)


8.	Write a Python program to extract all organization names from a given text using NLTK's Named Entity Recognition (NER).
text = "Microsoft company is developing artificial intelligence."

tokens = nltk.word_tokenize(text)
pos_tags = nltk.pos_tag(tokens)
ner_tree = nltk.ne_chunk(pos_tags)

organizations = [subtree[0][0] for subtree in ner_tree if isinstance(subtree, nltk.Tree) and subtree.label() == "ORGANIZATION"]
print("Organizations:", organizations)


9.	Write a Python program using NLTK to extract proper nouns (NNP) from a given sentence.
text = "Alice went to Paris and met Bob."

tokens = nltk.word_tokenize(text)
pos_tags = nltk.pos_tag(tokens)

proper_nouns = [word for word, tag in pos_tags if tag == "NNP"]
print("Proper Nouns:", proper_nouns)


10.	Write a Python program to extract noun phrases from a given text using a custom chunking grammar.
text = "The smart student wrote an excellent essay."

tokens = nltk.word_tokenize(text)
pos_tags = nltk.pos_tag(tokens)

# Define custom grammar for noun phrases
grammar = "NP: {<DT>?<JJ>*<NN>+}"

chunk_parser = nltk.RegexpParser(grammar)
chunk_tree = chunk_parser.parse(pos_tags)

chunk_tree.pretty_print()


11.	Write a Python program to extract verb phrases (VP) from a given sentence using a custom chunking grammar.
sentence = "She has been reading a novel."

tokens = nltk.word_tokenize(sentence)
pos_tags = nltk.pos_tag(tokens)

grammar = "VP: {<VB.*><RB>?<VB.*>*}"

chunk_parser = nltk.RegexpParser(grammar)
chunk_tree = chunk_parser.parse(pos_tags)

chunk_tree.pretty_print()


13.	Write a Python program to visualize named entities using ne_chunk from NLTK.
              sentence = "Jeff Bezos founded Amazon in Seattle."

tokens = nltk.word_tokenize(sentence)
pos_tags = nltk.pos_tag(tokens)
ner_tree = nltk.ne_chunk(pos_tags)

ner_tree.pretty_print()

        """)
    elif (num==8):
        print("""
1.	Write a Python program using NLTK to define a context-free grammar (CFG) that can parse simple sentences like "The cat sat on the mat." Use this grammar to generate the parse tree for the sentence.
import nltk
from nltk import CFG

# Define a context-free grammar (CFG) for simple sentences
grammar = CFG.fromstring(
  S -> NP VP
  NP -> Det N
  VP -> V PP
  PP -> P NP
  Det -> 'The' | 'the'
  N -> 'cat' | 'mat'
  V -> 'sat'
  P -> 'on'
)

# Sentence to parse
sentence = ['The', 'cat', 'sat', 'on', 'the', 'mat']

# Create a parser with the grammar
parser = nltk.ChartParser(grammar)

# Parse the sentence and visualize the parse tree
for tree in parser.parse(sentence):
    tree.pretty_print()  # Display the tree in a readable format

2.	Using NLTK, write a function that takes a sentence as input and returns all possible parse trees using a given CFG. Demonstrate this function with the sentence "I saw the man with the telescope."
import nltk
from nltk import CFG

# Define the context-free grammar (CFG)
grammar = CFG.fromstring(
  S -> NP VP
  NP -> Pronoun | Det N | Det N PP
  VP -> V NP | V NP PP
  PP -> P NP
  Pronoun -> 'I'
  Det -> 'the'
  N -> 'man' | 'telescope'
  V -> 'saw'
  P -> 'with'
)

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



3.	Write a Python program using NLTK to create a recursive descent parser for a given CFG. Parse the sentence "She eats a sandwich." and display the parse tree.
import nltk
from nltk import CFG

# Define the context-free grammar (CFG)
grammar = CFG.fromstring(
  S -> NP VP
  NP -> Pronoun | Det N
  VP -> V NP
  PP -> P NP
  Pronoun -> 'She'
  Det -> 'a'
  N -> 'sandwich'
  V -> 'eats'
  P -> 'with'
)

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


4.	Using NLTK, write a program to extract noun phrases from a sentence using a chunk grammar. Apply it to the sentence "The quick brown fox jumps over the lazy dog."
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger') # Download missing resource.
nltk.download('averaged_perceptron_tagger_eng')

from nltk import pos_tag, word_tokenize, RegexpParser

def extract_noun_phrases(sentence):
    
    #Extracts noun phrases from a sentence using a chunk grammar.

    #Args:
        #sentence (str): The input sentence.

    #Returns:
        #list: A list of noun phrases found in the sentence.
    

    # Tokenize the sentence
    tokens = word_tokenize(sentence)

    # Perform Part-of-Speech tagging
    tagged_tokens = pos_tag(tokens)

    # Define the chunk grammar for noun phrases (NP)
    chunk_grammar = r
        NP: {<DT>?<JJ>*<NN>}  # Noun phrase pattern: optional determiner, zero or more adjectives, and a noun
    

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


5.	Write a Python function using NLTK that takes a sentence as input and returns the verb phrases (VP) using a chunk grammar. Demonstrate this function with the sentence "The cat is sleeping on the mat."
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

from nltk import pos_tag, word_tokenize, RegexpParser

def extract_verb_phrases(sentence):
    
    #Extracts verb phrases (VP) from a sentence using a chunk grammar.

    #Args:
        #sentence (str): The input sentence.

    #Returns:
        #list: A list of verb phrases found in the sentence.
    

    # Tokenize the sentence
    tokens = word_tokenize(sentence)

    # Perform Part-of-Speech tagging
    tagged_tokens = pos_tag(tokens)

    # Define the chunk grammar for verb phrases (VP)
    # This grammar is modified to capture complete verb phrases
    chunk_grammar = r
        VP: {<VB.?>+<RB.?>* <IN>? <DT>? <JJ>* <NN.?>+}  # Captures verb phrases
    

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


6.	Write a Python program using NLTK to define a probabilistic context-free grammar (PCFG) and generate a parse tree for the sentence "The cat sleeps."
import nltk
from nltk import PCFG

# Define the probabilistic context-free grammar (PCFG)
grammar = PCFG.fromstring(
    S -> NP VP [1.0]
    NP -> Det N [0.8] | Pronoun [0.2]
    VP -> V [0.7] | V PP [0.3]
    PP -> P NP [1.0]
    Det -> 'The' [0.6] | 'the' [0.4]
    N -> 'cat' [0.7] | 'mat' [0.3]
    V -> 'sleeps' [1.0]
    Pronoun -> 'He' [0.5] | 'She' [0.5]
    P -> 'on' [1.0]
)

# Sentence to parse
sentence = "The cat sleeps".split()

# Create a parser with the PCFG
viterbi_parser = nltk.ViterbiParser(grammar)

# Parse the sentence and get the most likely parse tree
for tree in viterbi_parser.parse(sentence):
    print(tree)
    tree.pretty_print()  # Display the tree in a readable format


7.	Write a Python program to visualize the chunk tree for a given sentence using a noun phrase chunking grammar.
import nltk
from nltk.chunk import RegexpParser
from nltk.tokenize import word_tokenize
from nltk import pos_tag

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Define a simple noun phrase (NP) chunking grammar
grammar = 
  NP: {<DT>?<JJ>*<NN>}  # Noun Phrase (optional Determiner, adjectives, and a noun)


# Function to chunk and visualize the chunk tree
def visualize_chunk_tree(sentence):
    # Tokenize and tag the sentence
    tokens = word_tokenize(sentence)
    tagged = pos_tag(tokens)

    # Create the chunk parser with the defined grammar
    chunk_parser = RegexpParser(grammar)

    # Parse the sentence to identify noun phrases
    chunk_tree = chunk_parser.parse(tagged)

    # Visualize the chunk tree (text-based output)
    chunk_tree.pretty_print()  # Pretty print the tree

# Example sentence
sentence = "The quick brown fox jumped over the lazy dog."

# Visualize the chunk tree for the sentence
visualize_chunk_tree(sentence)
            
8.	Write a Python program that extracts prepositional phrases (PP) from a given text using a chunking grammar.
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.chunk import RegexpParser

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Define a chunking grammar for extracting prepositional phrases (PP)
grammar = 
  PP: {<IN><DT>?<JJ>*<NN.*>+}  # Prepositional Phrase (Preposition followed by a Noun Phrase)
  NP: {<DT>?<JJ>*<NN.*>+}       # Noun Phrase (optional Determiner, adjectives, and one or more nouns)


# Function to extract prepositional phrases from text
def extract_prepositional_phrases(text):
    # Tokenize and tag the sentence
    tokens = word_tokenize(text)
    tagged = pos_tag(tokens)

    # Create the chunk parser with the defined grammar
    chunk_parser = RegexpParser(grammar)

    # Parse the tagged sentence to extract PPs
    chunk_tree = chunk_parser.parse(tagged)

    # Extract and return the prepositional phrases
    pp_phrases = []
    for subtree in chunk_tree.subtrees(filter=lambda t: t.label() == 'PP'):
        pp_phrases.append(" ".join(word for word, tag in subtree.leaves()))  # Join words in PP

    return pp_phrases

# Example sentence
sentence = "The cat sat on the mat with a toy."

# Extract prepositional phrases
prepositional_phrases = extract_prepositional_phrases(sentence)

# Print the extracted prepositional phrases
print("Prepositional Phrases:", prepositional_phrases)



9.	Write a Python program that extracts all adjective phrases (ADJP) from a given sentence using a chunking grammar.
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

from nltk import pos_tag, word_tokenize, RegexpParser

def extract_adjective_phrases(sentence):
    
    #Extracts all adjective phrases (ADJP) from a given sentence using a chunking grammar.

    #Args:
        #sentence (str): The input sentence.

    #Returns:
        #list: A list of adjective phrases found in the sentence.
    

    # Tokenize the sentence
    tokens = word_tokenize(sentence)

    # Perform Part-of-Speech tagging
    tagged_tokens = pos_tag(tokens)

    # Define the chunk grammar for adjective phrases (ADJP)
    chunk_grammar = r
        ADJP: {<JJ.*>+}   # Adjective Phrase: one or more adjectives (including comparative/superlative)
                           # You can extend this to include adverbs modifying adjectives if needed
    

    # Create a chunk parser
    chunk_parser = RegexpParser(chunk_grammar)

    # Parse the tagged tokens
    chunked_tree = chunk_parser.parse(tagged_tokens)

    # Extract adjective phrases from the chunked tree
    adjective_phrases = []
    for subtree in chunked_tree.subtrees():
        if subtree.label() == 'ADJP':
            adjective_phrase = ' '.join(word for word, tag in subtree.leaves())
            adjective_phrases.append(adjective_phrase)

    return adjective_phrases

# Example usage:
sentence = "The quick brown fox jumps over the very lazy dog."
adjective_phrases = extract_adjective_phrases(sentence)

print("Adjective phrases in the sentence:")
for phrase in adjective_phrases:
    print(phrase) 


10.	Write a Python program that extracts all verb phrases (VP) from a given sentence using a chunking grammar.
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.chunk import RegexpParser

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Define a chunking grammar for extracting verb phrases (VP)
grammar = 
  VP: {<VB.*><RB.*>*<NP|PP>*}  # Verb Phrase (Verb followed by optional adverb or noun/PP)
  NP: {<DT>?<JJ>*<NN.*>+}      # Noun Phrase (optional Determiner, adjectives, and one or more nouns)
  PP: {<IN><NP>}               # Prepositional Phrase (Preposition followed by a Noun Phrase)


# Function to extract verb phrases from a sentence
def extract_verb_phrases(text):
    # Tokenize and tag the sentence
    tokens = word_tokenize(text)
    tagged = pos_tag(tokens)

    # Create the chunk parser with the defined grammar
    chunk_parser = RegexpParser(grammar)

    # Parse the tagged sentence to extract VPs
    chunk_tree = chunk_parser.parse(tagged)

    # Extract and return the verb phrases
    vp_phrases = []
    for subtree in chunk_tree.subtrees(filter=lambda t: t.label() == 'VP'):
        vp_phrases.append(" ".join(word for word, tag in subtree.leaves()))  # Join words in VP

    return vp_phrases

# Example sentence
sentence = "She is eating a sandwich with enthusiasm."

# Extract verb phrases
verb_phrases = extract_verb_phrases(sentence)

# Print the extracted verb phrases
print("Verb Phrases:", verb_phrases)


11.	Write a Python program to extract complex noun phrases (NP) containing nested structures using chunking grammar.
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.chunk import RegexpParser

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Define a chunking grammar for complex noun phrases (NP) with nested structures
grammar = 
  NP: {<DT|JJ>*<NN.*>+<PP>*}            # Basic Noun Phrase (Determiner, Adjective, Noun)
  PP: {<IN><NP>}                         # Prepositional Phrase (Preposition followed by Noun Phrase)


# Function to extract complex noun phrases from a sentence
def extract_complex_noun_phrases(text):
    # Tokenize and tag the sentence
    tokens = word_tokenize(text)
    tagged = pos_tag(tokens)

    # Create the chunk parser with the defined grammar
    chunk_parser = RegexpParser(grammar)

    # Parse the tagged sentence to extract NPs
    chunk_tree = chunk_parser.parse(tagged)

    # Extract and return the noun phrases with nested structures
    np_phrases = []
    for subtree in chunk_tree.subtrees(filter=lambda t: t.label() == 'NP'):
        np_phrases.append(" ".join(word for word, tag in subtree.leaves()))  # Join words in NP

    return np_phrases

# Example sentence
sentence = "The big black cat on the mat looked at the man with a telescope."

# Extract complex noun phrases
complex_noun_phrases = extract_complex_noun_phrases(sentence)

# Print the extracted complex noun phrases
print("Complex Noun Phrases:", complex_noun_phrases)

                          
12.	Write a Python program using NLTK to define and apply a probabilistic grammar to generate a parse tree for a given sentence.
import nltk
from nltk import PCFG
from nltk.parse import ChartParser

# Download necessary NLTK resources
nltk.download('punkt')

# Define a probabilistic context-free grammar (PCFG)
# Format for PCFG: (non-terminal -> [rule, probability])

probabilistic_grammar = PCFG.fromstring(
  S -> NP VP [1.0]
  NP -> Det N [0.5] | Det Adj N [0.5]
  VP -> V NP [0.7] | V NP PP [0.3]
  PP -> P NP [1.0]
  Det -> 'the' [0.6] | 'a' [0.4]
  N -> 'cat' [0.3] | 'dog' [0.3] | 'man' [0.4]
  V -> 'chased' [0.5] | 'saw' [0.5]
  Adj -> 'big' [1.0]
  P -> 'with' [1.0]
)

# Define a function to generate the parse tree for a given sentence
def generate_parse_tree(sentence):
    # Tokenize the sentence
    tokens = nltk.word_tokenize(sentence)

    # Create the ChartParser with the given PCFG
    parser = ChartParser(probabilistic_grammar)

    # Parse the sentence and generate all possible parse trees
    for tree in parser.parse(tokens):
        tree.pretty_print()  # Print the tree in a readable format

# Example sentence
sentence = "the big cat chased a dog with the man"

# Generate and display the parse tree
generate_parse_tree(sentence)


        """)
    else:
        print("""
              1:
            1.Write a python program using nltk to tokenize the sentence: "Natural Langauge Processing with Python is fun" into words.
            2.Using NLTK write a program to find the frequency distribution of words in the text of "Moby Dick" by Herman Melville
            3.Create a bi-gram collocation finder using NLKT for the text of "Sense and Sensibility" by Jnae Austen and list the top 5 Bi-gram
            4.Using NLTK's Text2 , calculate the total number of words and number of distinct words
            5.Compare the lexical diversity of humor and romance fiction in nltks text5 and text2.which genre is more lexically diverse?
            6.Produce a dispersion plot of the four main protagonist in "Sense and sensibility" : Elinor, Marianne, Edward, and Willoughby. What observations can you make about their appearances  in the text?
            7.Find the collections in NLTK's text5(the chat corpus). List the top 5 collections.
            8.Define two lists, phrase1 and phrase2, each containing a few words. join them together to form a sentence.
            

              2:
            1.	Use the inaugural address corpus to find the total number of words and the total number of unique words in the inaugural addresses delivered in the 21st century.
            2.	Write a Python program to find the frequency distribution of the words "democracy", "freedom", "liberty", and "equality" in all inaugural addresses using NLTK.
            3.	Write a Python program to display the 5 most common words in the text of "Sense and Sensibility" by Jane Austen using the Gutenberg Corpus.
            4.	Generate a conditional frequency distribution of modal verbs ('can', 'could', 'may', 'might', 'must', 'will') across the categories of the Brown Corpus.
            5.	Write a Python program to identify the longest word in "Moby Dick" from the Gutenberg Corpus.
            6.	Using the Brown Corpus, calculate the frequency of the word "government" across all categories.
            7.	Write a Python program using the Reuters Corpus to find the number of documents categorized under "crude".
              
 ##############################################################################################################################################################################             

              3:
            1.	Write a Python program to download the text of "Pride and Prejudice" by Jane Austen from Project Gutenberg, tokenize the text, and display the first 10 tokens.
            2.	Using NLTK, write a function that takes a URL as input, fetches the raw text from the webpage, and returns the number of words in the text.
            3.	Explain how to remove HTML tags from a web page's content using Python and NLTK. Provide a code example that fetches a web page, removes HTML tags, and prints the cleaned text.
            4.	Write a Python program that reads a text file, tokenizes its content into sentences, and prints the number of sentences in the file.
            5.	Using regular expressions in Python, write a function that takes a list of words and returns a list of words that end with 'ing'.
            6.	Describe how to normalize text by converting it to lowercase and removing punctuation using NLTK. Provide a code example that processes a given sentence.
            7.	Using NLTK's PorterStemmer, write a function that takes a list of words and returns a list of their stemmed forms.
            8.	Explain the difference between stemming and lemmatization in text processing. Provide code examples using NLTK to demonstrate both processes on the word 'running'.
            9.	Write a Python program to count the number of vowels (a, e, i, o, u) in a given text.
            10.	Write a Python program to tokenize the text into words and filter out words that contain digits.
            11.	Write a program to read text from a file and display all the words starting with a capital letter.
            12.	Write a Python program to identify and display all the email addresses from a given text.
            13.	Write a program to tokenize a text into sentences and display only those sentences containing more than 10 words.
            14.	Write a Python program that takes a sentence as input and returns all words that are at least 5 characters long.
            15.	Write a Python program using regular expressions to find all words starting with 'un' in a given text.
              
############################################################################################################################################################################## 

              4:
            1.	Explain the difference between assigning a list to a new variable using direct assignment (=) and using the copy() method. Provide code examples to illustrate the difference.
            2.	Write a function extract_nouns(text) that takes a text string as input and returns a list of all nouns in the text. Use NLTK's part-of-speech tagging for this task.
            3.	Demonstrate how to use list comprehension to create a list of the lengths of each word in a given sentence.
            4.	Write a function word_frequency(text) that takes a text string and returns a dictionary with words as keys and their frequencies as values.
            5.	Explain the concept of variable scope in Python with an example demonstrating the difference between local and global variables.
            6.	Write a Python program that reads a text file and counts the number of lines, words, and characters in the file.
            7.	Describe how to handle exceptions in Python with a try-except block. Provide an example that handles a division by zero error.
            8.	Write a function remove_stopwords(text) that removes common English stopwords from a given text using NLTK's stopwords corpus.
            9.	Write a Python program to extract and print all words from a text that start with a capital letter using regular expressions.
            10.	Write a Python program to tokenize a given text into words and count how many words are exactly 5 characters long.
            11.	Write a Python program to use regular expressions to find all email addresses in a given string.
            12.	Write a Python program to tokenize a sentence into words and then sort the words alphabetically.
            13.	Write a Python program to calculate and print the lexical diversity of a given text.
            14.	Write a Python program that takes a sentence as input and prints the words in reverse order.
            15.	Write a Python program to find and print all words in a text that contain at least one digit.

############################################################################################################################################################################## 
             
               5:
            1.	Write a Python program using NLTK to perform part-of-speech tagging on the sentence: "The quick brown fox jumps over the lazy dog."
            2.	Using NLTK, write a function that takes a list of sentences and returns a list of part-of-speech tagged sentences.
            3.	Explain how to map the Penn Treebank POS tags to the Universal POS tags using NLTK. Provide a code example that tags a sentence and maps the tags accordingly.
            4.	Write a Python function using NLTK that takes a sentence as input and returns a list of all nouns in the sentence.
            5.	Using the Brown Corpus in NLTK, write a program to find the most common part-of-speech tag in the news category.
            6.	Write a Python program using NLTK to train a unigram part-of-speech tagger on the Brown Corpus and evaluate its accuracy.
            7.	Explain the concept of backoff tagging in NLTK. Write a Python program that combines a bigram tagger with a unigram tagger as a backoff, and evaluate its performance on the Brown Corpus.
            8.	Write a Python program to tag words with part-of-speech using NLTK and then extract all adjectives from the sentence: "The beautiful sunset painted the sky with vibrant colors."
            9.	Write a Python program to calculate the frequency of each part-of-speech tag in a given text.
            10.	Using NLTK, write a program that tags words in a sentence and prints only the verbs.
            11.	Write a Python program using NLTK to identify and print all proper nouns from a given sentence.
            12.	Write a Python program to train a trigram part-of-speech tagger with a unigram backoff on the Brown corpus and evaluate its performance.
            13.	Write a Python program using NLTK to tag a sentence and count how many words belong to each part-of-speech category.
            14.	Write a Python program to tag a given text with part-of-speech tags and then filter out only determiners (DT) using NLTK.
            15.	Write a Python program to calculate and print the lexical diversity of nouns, verbs, adjectives, and adverbs in a given text.

              
############################################################################################################################################################################## 
              
              6:
            1.	Using the names corpus in NLTK, build a gender classifier that predicts whether a name is male or female based on the last letter of the name. Evaluate its accuracy.
            2.	Enhance the gender classifier by including features such as the first letter and the length of the name. Evaluate if these features improve the classifier's accuracy.
            3.	Using the movie_reviews corpus in NLTK, build a document classifier to categorize movie reviews as positive or negative. Evaluate its performance.
            4.	Implement a custom feature extractor for the movie review classifier that considers bigrams (pairs of consecutive words) in addition to unigrams (single words). Evaluate its impact on classification accuracy.
            5.	Build a Naive Bayes classifier using the names corpus to predict gender based on both the first and last letters of a name. Evaluate the model's accuracy.
            6.	Write a Python program using the movie_reviews corpus to identify the 10 most common words in positive reviews.
            7.	Implement a Naive Bayes classifier to classify movie reviews using only adjectives as features.
            8.	Write a Python program that uses the names corpus to build a gender classifier using Decision Tree Classifier from NLTK
            9.	Write a Python program using NLTK to identify bigrams that are frequently used together in movie reviews.
            10.	Write a Python program to train a Naive Bayes classifier on the movie_reviews corpus with features based on word lengths.
            11.	Write a Python program using NLTK to create a frequency distribution of word lengths from movie reviews.
            12.	Write a Python program to extract all named entities from a given text using NLTK's ne_chunk functionality.


 ############################################################################################################################################################################## 
              
              7:
            1.	Write a Python program using NLTK to extract named entities from the sentence: "Apple Inc. is looking at buying U.K. startup for $1 billion."
            2.	Using NLTK, write a function that takes a list of sentences and returns a list of named entities found in each sentence.
            3.	Write a Python program that uses NLTK to extract and display all noun phrases from a given text.
            4.	Using NLTK, write a program to perform chunking on the sentence: "He reckons the current account deficit will narrow to only 8 billion." and display the chunked tree.
            5.	Write a Python function using NLTK that takes a sentence as input and returns all verb phrases (VP) present in the sentence.
            6.	Write a Python program using NLTK to perform named entity recognition (NER) on a paragraph containing multiple sentences. Display the extracted named entities.
            7.	Write a Python program to count the number of named entities of type GPE (Geopolitical Entity) in a given text.
            8.	Write a Python program to extract all organization names from a given text using NLTK's Named Entity Recognition (NER).
            9.	Write a Python program using NLTK to extract proper nouns (NNP) from a given sentence.
            10.	Write a Python program to extract noun phrases from a given text using a custom chunking grammar.
            11.	Write a Python program to extract verb phrases (VP) from a given sentence using a custom chunking grammar.
            12.	Write a Python program that extracts all named entities and classifies them into their respective categories (PERSON, ORGANIZATION, GPE, etc.).
            13.	Write a Python program to visualize named entities using ne_chunk from NLTK.

 ############################################################################################################################################################################## 
             
               8:
            1.	Write a Python program using NLTK to define a context-free grammar (CFG) that can parse simple sentences like "The cat sat on the mat." Use this grammar to generate the parse tree for the sentence.
            2.	Using NLTK, write a function that takes a sentence as input and returns all possible parse trees using a given CFG. Demonstrate this function with the sentence "I saw the man with the telescope."
            3.	Write a Python program using NLTK to create a recursive descent parser for a given CFG. Parse the sentence "She eats a sandwich." and display the parse tree.
            4.	Using NLTK, write a program to extract noun phrases from a sentence using a chunk grammar. Apply it to the sentence "The quick brown fox jumps over the lazy dog."
            5.	Write a Python function using NLTK that takes a sentence as input and returns the verb phrases (VP) using a chunk grammar. Demonstrate this function with the sentence "The cat is sleeping on the mat."
            6.	Write a Python program using NLTK to define a probabilistic context-free grammar (PCFG) and generate a parse tree for the sentence "The cat sleeps."
            7.	Write a Python program to visualize the chunk tree for a given sentence using a noun phrase chunking grammar.
            8.	Write a Python program that extracts prepositional phrases (PP) from a given text using a chunking grammar.
            9.	Write a Python program that extracts all adjective phrases (ADJP) from a given sentence using a chunking grammar.
            10.	Write a Python program that extracts all verb phrases (VP) from a given sentence using a chunking grammar.
            11.	Write a Python program to extract complex noun phrases (NP) containing nested structures using chunking grammar.
            12.	Write a Python program using NLTK to define and apply a probabilistic grammar to generate a parse tree for a given sentence.


              """)

# Call the function with the condition
