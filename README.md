# mini-ir-system
A basic Information Retrieval system that indexes PDF documents, supports keyword search, fuzzy matching, auto-suggestions, and voice search. Enables document viewing and downloading.
Aim of the Project:
This project aims to develop a fun yet functional Information Retrieval system that efficiently indexes PDF documents, performs keyword searches, handles typos and synonyms using fuzzy matching, provides auto-suggestions, and supports voice search. 🗂️🔍 The goal is to enhance search relevance and simplify document management for users. 📄📁

# Requirements:
To get started, you'll need to install the following dependencies:

Python (version >=3.7)
PyPDF2: For extracting text from PDF files. 📝
Command: pip install PyPDF2
SpeechRecognition: For voice search functionality. 🎤
Command: pip install SpeechRecognition
nltk: For natural language processing tasks like fetching synonyms. 🌟
Command: pip install nltk
trie: A simple Trie data structure for auto-suggestions. 🔍
Command: pip install trie
# Components Used:
PDF Document Indexing: To read and index text from PDF files using PyPDF2. 📄
Trie Data Structure: For fast auto-suggestions based on user input. 🏃‍♂️
Fuzzy Matching: Using difflib.get_close_matches to find similar words in indexed documents. 🔄
WordNet: To fetch synonyms for query expansion using NLTK. 🌐
Speech Recognition: For capturing voice input and converting it to text for search. 🎧
# Purpose:
Improve the search experience by capturing similar word matches. 📈
Enable document management functionalities (view and download). 📥📧
Support voice-based search for improved accessibility. 🎙️
# Working Model:
You can view a working model of this project here. 🌐✨
