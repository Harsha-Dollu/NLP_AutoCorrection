import string
import re
from collections import Counter
import editdistance
import numpy as np

class Autocorrection(object):

    def __init__(self, filename):
        with open(filename, "r", encoding="utf-8") as file:
            word = []
            lines = file.readlines()
            for line in lines:
                word += re.findall(r'\w+', line.lower())

        self.vocabulary = set(word)
        self.counts_of_word = Counter(word)
        self.total_words = float(sum(self.counts_of_word.values()))
        self.smoothing_factor = 1.0
        self.prob_of_word = {w: (self.counts_of_word[w] + self.smoothing_factor) / 
                            (self.total_words + self.smoothing_factor * len(self.vocabulary)) 
                            for w in self.vocabulary}

    def edit1(self, word):
        letter = string.ascii_lowercase
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        insert = [l + c + r for l, r in splits for c in letter]
        delete = [l + r[1:] for l,r in splits if r]
        replace = [l + c + r[1:] for l, r in splits if r for c in letter]
        swap = [l + r[1] + r[0] + r[2:] for l, r in splits if len(r) > 1]

        return set(replace + insert + delete + swap)
  
    def edit2(self, word):
        return [e2 for e1 in self.edit1(word) for e2 in self.edit1(e1)]

    def common_prefix_length(self, word1, word2):
        common_len = 0
        for i, (c1, c2) in enumerate(zip(word1, word2)):
            if c1 == c2:
                common_len += 1
            else:
                break
        return common_len

    def custom_score(self, suggestion, original_word):
        replace_weight = 1
        insert_weight = 2
        delete_weight = 3
        swap_weight = 4

        distance = editdistance.eval(suggestion, original_word)
        
        if len(suggestion) == len(original_word):  # Replace
            common_prefix_len = self.common_prefix_length(suggestion, original_word)
            score = distance * replace_weight + (len(original_word) - common_prefix_len)
        elif len(suggestion) == len(original_word) + 1:  # Insert
            common_prefix_len = self.common_prefix_length(suggestion, original_word)
            score = distance * insert_weight + (len(original_word) - common_prefix_len)
        elif len(suggestion) == len(original_word) - 1:  # Delete
            score = distance * delete_weight
        else:  # Swap
            score = distance * swap_weight

        return score
  
    def correct_spelling(self, word):
        if word in self.vocabulary:
            print(f"{word} is already correctly spelt")
            return

        suggestions = self.edit1(word) or self.edit2(word) or [word]
        best_guesses = [w for w in suggestions if w in self.vocabulary]

        if not best_guesses:
            return []

        best_guesses.sort(key=lambda w: self.custom_score(w, word))

        suggestion_probs = []
        for w in best_guesses:
            prob = self.prob_of_word.get(w, self.smoothing_factor / 
                                       (self.total_words + self.smoothing_factor * len(self.vocabulary)))
            suggestion_probs.append((w, prob))

        total_prob = sum(prob for _, prob in suggestion_probs)
        if total_prob > 0:
            suggestion_probs = [(w, p/total_prob) for w, p in suggestion_probs]

        return suggestion_probs
