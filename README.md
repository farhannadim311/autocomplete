# 🔤 Autocomplete and Word Filter with Prefix Tree

This project implements a fast and memory-efficient **autocomplete system** using a custom `PrefixTree` (trie) data structure. It supports:

- ✅ **Prefix-based autocompletion** of words sorted by frequency  
- ✅ **Autocorrect** using single-edit suggestions (insert, delete, replace, transpose)  
- ✅ **Wildcard-based word filtering** using:
  - `?` to match any single character  
  - `*` to match zero or more characters  

---

## 📁 Features

- **PrefixTree class**  
  Efficiently stores and retrieves words using trie nodes.

- **`autocomplete(tree, prefix)`**  
  Returns a list of the most frequent words starting with a given prefix.

- **`autocorrect(tree, prefix)`**  
  Returns suggestions for misspelled words using valid edits.

- **`word_filter(tree, pattern)`**  
  Supports wildcard patterns with `*` and `?` to match flexible word forms.

---

## 🧪 Example

```python
tree = PrefixTree()
tree["bat"] = 5
tree["bar"] = 3
tree["bark"] = 2
tree["beast"] = 4
tree["best"] = 7

word_filter(tree, "b*?t")
# Output: {('bat', 5), ('best', 7), ('beast', 4)}
