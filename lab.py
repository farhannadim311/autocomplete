"""
6.101 Lab:
Autocomplete
"""

# NO ADDITIONAL IMPORTS!

# import string # optional import
# import pprint # optional import
# import typing # optional import
import doctest
from text_tokenize import tokenize_sentences


class PrefixTree:
    def __init__(self):
        self.value = None
        self.children = {}

    def __setitem__(self, key, value):
        """
        Add a key with the given value to the prefix tree,
        or reassign the associated value if it is already present.
        Raise a TypeError if the given key is not a string.
        """
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
        node = self
        for char in key:
            if char not in node.children:
                node.children[char] = PrefixTree()
            node = node.children[char]
        node.value = value



    def __getitem__(self, key):
        """
        Return the value for the specified prefix.
        Raise a KeyError if the given key is not in the prefix tree.
        Raise a TypeError if the given key is not a string.
        """
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
        node = self
        for char in key:
            if char not in node.children:
                raise KeyError("Key is not in the Tree")
            node = node.children[char]
        if(node.value == None):
            raise KeyError("Key is not in the Tree")
        return node.value
    def __contains__(self, key):
        """
        Is key a key in the prefix tree?  Return True or False.
        Raise a TypeError if the given key is not a string.
        """
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
        node = self
        for char in key:
            if char not in node.children:
                return False
            node = node.children[char]
        if(node.value == None):
            return False
        return True

    def __iter__(self):
        """
        Generator of (key, value) pairs for all keys/values in this prefix tree
        and its children.  Must be a generator!
        """
        def helper (node, path):
            if(node.value != None):
                yield (path, node.value)
            for char, n in node.children.items():
                yield from helper(n, path + char)
            
        yield from helper (self, "")





    def __delitem__(self, key):
        """
        Delete the given key from the prefix tree if it exists.
        Raise a KeyError if the given key is not in the prefix tree.
        Raise a TypeError if the given key is not a string.
        """
        if(not isinstance(key,str)):
            raise TypeError("Key must be a string")
        node = self
        for char in key:
            if char not in node.children:
                raise KeyError("Key is not in the prefix tree")
            node = node.children[char]
        if(node.value == None):
            raise KeyError("Key not found") 
        node.value = None


    def find_node(self, key):
        """
        Traverse the tree and return the node corresponding to the key,
        or None if the key is not present.
        """
        node = self
        for char in key:
            if char not in node.children:
                return None
            node = node.children[char]
        return node
    

def word_frequencies(text):
    """
    Given a piece of text as a single string, create a prefix tree whose keys
    are the words in the text, and whose values are the number of times the
    associated word appears in the text.
    """
    sentences = tokenize_sentences(text)
    tree = PrefixTree()
    for sentence in sentences:
        words = sentence.split()
        for word in words:
            node = tree.find_node(word)
            if node is not None and node.value is not None:
                node.value += 1
            else:
                tree[word] = 1
    return tree



def autocomplete(tree, prefix, max_count=None):
    """
    Return the list of the most-frequently occurring elements that start with
    the given prefix.  Include only the top max_count elements if max_count is
    specified, otherwise return all.

    Raise a TypeError if the given prefix is not a string.
    """
    lst = []
    if(not isinstance(prefix, str)):
        raise TypeError("Given prefix is not a string")
    node = tree.find_node(prefix)
    if node is None:
        return []
    for key, value in node:
        lst.append((prefix + key,value))
    lst.sort(key = lambda x: x[1], reverse = True)
    if(max_count == None):
        return [key for key, val in lst]
    elif (max_count > len(lst)):
        return [key for key, val in lst]
    else:
        return [key for key, val in lst[:max_count]]
            




def autocorrect(tree, prefix, max_count=None):
    """
    Return the list of the most-frequent words that start with prefix or that
    are valid words that differ from prefix by a small edit.  Include up to
    max_count elements from the autocompletion.  If autocompletion produces
    fewer than max_count elements, include the most-frequently-occurring valid
    edits of the given word as well, up to max_count total elements.
    """
    correct = autocomplete(tree, prefix, max_count)
    if max_count is not None and len(correct) >= max_count:
        return correct[:max_count]

    # Set to keep track of suggestions
    suggestions = {}
    letters = [chr(i) for i in range(ord('a'), ord('z') + 1)]

    # Valid edit: insertion
    for i in range(len(prefix) + 1):
        for ch in letters:
            edited = prefix[:i] + ch + prefix[i:]
            if edited in tree and edited not in correct:
                suggestions[edited] = tree[edited]

    # Valid edit: deletion
    for i in range(len(prefix)):
        edited = prefix[:i] + prefix[i+1:]
        if edited in tree and edited not in correct:
            suggestions[edited] = tree[edited]

    # Valid edit: replacement
    for i in range(len(prefix)):
        for ch in letters:
            if prefix[i] != ch:
                edited = prefix[:i] + ch + prefix[i+1:]
                if edited in tree and edited not in correct:
                    suggestions[edited] = tree[edited]

    # Valid edit: transposition
    for i in range(len(prefix) - 1):
        if prefix[i] != prefix[i+1]:  # skip if swapping identical chars
            edited = (prefix[:i] + prefix[i+1] + prefix[i] + prefix[i+2:])
            if edited in tree and edited not in correct:
                suggestions[edited] = tree[edited]

    # Sort suggestions by frequency descending
    sorted_suggestions = sorted(suggestions.items(), key=lambda x: x[1], reverse=True)
    edited_words = [word for word, _ in sorted_suggestions]

    # Determine how many additional edits we can take
    if max_count is None:
        return correct + edited_words
    else:
        remaining = max_count - len(correct)
        return correct + edited_words[:remaining]






def word_filter(tree, pattern):
    result = set()

    if pattern in tree:
        result.add((pattern, tree[pattern]))
        return result

    if "*" not in pattern and "?" not in pattern:
        return set()

    stack = [(tree, 0, "")]  # start with root, index 0, empty word

    while stack:
        node, i, word = stack.pop()

        if i == len(pattern):
            if node.value is not None:
                result.add((word, node.value))
            continue

        char = pattern[i]

        if char == "?":
            for c, child in node.children.items():
                stack.append((child, i + 1, word + c))

        elif char == "*":
            # Case 1: match 0 characters → move to next pattern char
            stack.append((node, i + 1, word))
            # Case 2: match 1 or more characters → try each child
            for c, child in node.children.items():
                stack.append((child, i, word + c))

        else:
            if char in node.children:
                stack.append((node.children[char], i + 1, word + char))

    return result
if __name__ == "__main__":
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)  # runs ALL doctests
    # doctest.run_docstring_examples( # runs doctests for one function
    #    PrefixTree.__getitem__,
    #    globals(),
    #    optionflags=_doctest_flags,
    #    verbose=True
    # )
