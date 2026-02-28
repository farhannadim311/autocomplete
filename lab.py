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
    """
    Stores a condensed mapping from word strings to values.
    """

    def __init__(self):
        self.value = None
        self.children = {}

    def __setitem__(self, word, value):
        """
        Mutates the tree so that the word is associated with the given value.
        Raises a TypeError if the given word is not a string.
        """
        if(type(word) != str):
            raise TypeError 
        for letters in word:
            if(letters not in self.children):
                self.children[letters] = PrefixTree()
                self = self.children[letters]
            else:
                self = self.children[letters]
        self.value = value

    def getKeys(self):
        return list(self.children.keys())

    def incrementTree(self, word):
        """
        Increment if valid word is given to tree
        """
        if(type(word) != str):
            raise TypeError 
        for letters in word:
            if(letters not in self.children):
                self.children[letters] = PrefixTree()
                self = self.children[letters]
            else:
                self = self.children[letters]
        self.value += 1
        

    def returnTree(self, word):
        """
        Returns a specific prefix tree
        """
        if(type(word) != str):
            raise TypeError
        for letters in word:
            if(letters not in self.children):
                return None
            else:
                self = self.children[letters]
        return self
    

    def __getitem__(self, word):
        """
        Returns the value for the specified word.
        Raises a KeyError if the given word is not in thve tree.
        Raises a TypeError if the given word is not a string.
        """
        tree = self.returnTree(word)
        if(tree == None):
            raise KeyError
        if(tree.value == None):
            raise KeyError
        else:
            return tree.value

    def __contains__(self, word):
        """
        Returns a boolean indicating whether the given word has a set value in the tree.
        Raises a TypeError if the given key is not a string.
        """
        tree = self.returnTree(word)
        if(tree == None):
            return False
        if(tree.value == None):
            return False
        else:
            return True

    
    def __iter__(self):
        """
        Generator that yields tuples of all the (word, value) pairs in the tree.
        """
        def builder(tree, s):
            if(tree.value is not None):
                yield (s, tree.value)
            for key,value in tree.children.items():
                t = value
                s = s + key
                yield from builder(t, s)
                s = s[:-1]

        return builder(self, "")
            
  
    def __delitem__(self, word):
        """
        Deletes the value of the given word from the tree.
        Raises a KeyError if the given word does not exist.
        Raises a TypeError if the given word is not a string.
        """
        if(type(word) != str):
            raise TypeError
        tree = self.returnTree(word)
        if(tree == None):
            raise KeyError
        if(tree.value == None):
            raise KeyError
        else:
            tree.value = None


def word_frequencies(text):
    """
    Given a piece of text as a single string, creates and returns a prefix tree whose
    keys are the words that appear in the text, and whose values are the number of times
    the associated word appears in the text.
    """
    sentence = tokenize_sentences(text)
    tree = PrefixTree()
    visited = set()
    for lines in sentence:
        words = lines.split()
        for w in words:
            if w in visited:
                tree.incrementTree(w)
            else:
                tree[w] = 1
                visited.add(w)
    return tree 

    


def autocomplete(tree, prefix, max_count=None):
    """
    Returns the set of the most-frequently occurring words that start with the given
    prefix string in the given tree. Includes only the top max_count most common words
    if max_count is specified, otherwise returns all auto-completions.
    """
    if(type(prefix) != str):
        raise TypeError
    res = []
    s = tree.returnTree(prefix)
    if(s == None):
        return set()
    for key, value in s:
        res.append((prefix + key, value))
    res.sort(key = lambda x: x[1], reverse= True)
    ans = set()
    if(max_count == 0):
        return ans
    if(max_count == None):
        for t in res:
            ans.add(t[0])
    else:
        for t in res:
            ans.add(t[0])
            if(len(ans) == max_count):
                break
    return ans
        
    

    


def generate_edits(word):
    """
    Generate all the possible ways to edit the given word string consisting
    entirely of lowercase letters in the range from "a" to "z".

    An edit for a word can be any one of the following:
    * A single insertion (add a single letter from "a" to "z" anywhere in the word)
    * A single deletion  (remove any one character from the word)
    * A single replacement (replace any one character in the word with a character in
      the range "a" to "z")
    * A two-character transpose (switch the positions of any two adjacent characters)

    Finding all valid edits may result in outputting duplicate edits or the
    original word. This function must be a generator function!
    """
    alphabets = "abcdefghijklmnopqrstuvwxyz"
    def single():
        for i  in range (len(word) + 1):
            for a in alphabets:
                yield word[:i] + a + word[i:]
        
    def other():
        for i in range(len(word)):
            for a in alphabets:
                yield word[:i] + a + word[i + 1:]
            s = word[0: i] + word[i + 1:]
            yield s
    def transpose():
        for i in range(len(word) - 1):
            adj = word[:i] + word[i + 1] + word[i] + word[i + 2:]
            yield adj
    yield from single()
    yield from other()
    yield from transpose()

def autocorrect(tree, prefix, max_count=None):
    """
    Returns the set of words that represent valid ways to autocorrect the given prefix
    string. Starts by including auto-completions. If there are fewer than max_count
    auto-completions (or if max_count is not specified), then includes the
    most-frequently occurring words that differ from prefix by a small edit, up to
    max_count total elements (or all elements if max_count is not specified).
    """
    autocmp = autocomplete(tree, prefix, max_count)
    res = set()
    edits = []
    visited = set()
    x = 0
    if(len(autocmp) == max_count):
        return autocmp
    for i in generate_edits(prefix):
        if(i in tree and i not in autocmp and i not in visited):
            edits.append((i, tree[i]))
            visited.add(i)
    
    edits.sort(key = lambda x: x[1], reverse= True)
    print(edits)
    for t in edits:
        if(max_count == None):
            res.add(t[0])
        else:
            res.add(t[0])
            if(len(res) + len(autocmp) ==  max_count):
                break
    print(res)
    return res | autocmp

    
     



    


def word_filter(tree, pattern):
    """
    Returns a set of all the words in the given tree that match the given
    pattern string. Each character in the pattern is one of:
        - '*' - matches any sequence of zero or more characters,
        - '?' - matches any single character,
        - otherwise the character must match the character in the word.
    """
    ans = set()
    def helper(t, pattern):
        a = set()
        if('?' not in pattern and '*' not in pattern):
            if(pattern in t):
                return {pattern}
            else:
                return set()
        else:
            for idx, char in enumerate(pattern):
                if(t == None):
                    break
                if(char == '?'):
                    keys = t.getKeys()
                    if(keys == []):
                        return set()
                    for k in keys:
                        #s = t.returnTree(k)
                        tmp = helper(t,  k + pattern[idx + 1:])
                        if(tmp != set()):
                            for items in tmp:
                                items = pattern[:idx] + items
                                a.add(items)
                    return a
                if(char == '*'):
                    keys = t.getKeys()
                    for k in keys:
                        tmp = helper(t, )
                else:
                    t = t.returnTree(char)

        return a
    return helper(tree, pattern)






    


if __name__ == "__main__":
    #_doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    #doctest.testmod(optionflags=_doctest_flags)  # runs ALL doctests
    # doctest.run_docstring_examples( # runs doctests for one function
    #    PrefixTree.__getitem__,
    #    globals(),
    #    optionflags=_doctest_flags,
    #    verbose=True
    # )
    pass