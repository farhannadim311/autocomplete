# Autocomplete Lab

This project is an implementation of an Autocomplete and Autocorrect system using a **Prefix Tree (Trie)** data structure. 

## Features

- **Prefix Tree (Trie)**: A custom data structure to store words and their frequencies efficiently.
- **Autocomplete**: Given a prefix, suggests the most frequently occurring valid words that start with that prefix.
- **Autocorrect**: Suggests valid corrections for a given prefix based on small edits (insertions, deletions, replacements, and transpositions).
- **Word Filter**: Advanced pattern matching supporting wildcards (`*` for any sequence of zero or more characters, `?` for any single character).
- **Word Frequencies**: Tokenizes large text files and builds a comprehensive frequency map inside the prefix tree.

## Project Structure

- `lab.py`: Core logic for the Autocomplete and Autocorrect functions, including the PrefixTree class.
- `test.py`: Unit tests to verify the correctness and performance of the tree and algorithms.
- `text_tokenize.py`: Utility functions to parse text into readable tokens.

## Running Tests

You can verify the implementation by running the provided test suite using `pytest`:

```bash
pytest test.py
```
