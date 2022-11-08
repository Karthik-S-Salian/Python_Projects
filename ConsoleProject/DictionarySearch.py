from math import factorial
from collections import Counter
from functools import reduce


def dictionary_search(word, search_word):
    def _validate_input(word, search_word):
        try:
            word = word.lower()
            search_word = search_word.lower()
        except:
            raise "PARAMETER_IS_NOT_STRING"

        if not Counter(word) == Counter(search_word):
            raise "word don't match"

    def search(word, search_word):
        word = word.lower()
        search_word = search_word.lower()
        word_dict = Counter(word)
        length = len(word)
        sum = 0
        for i, letter in enumerate(search_word, start=1):
            for current_letter in word_dict:
                if letter == current_letter:
                    if word_dict[current_letter] > 1:
                        word_dict[current_letter] -= 1
                    else:
                        word_dict.pop(current_letter)
                    break

                x = reduce(lambda x, y: x / factorial(y), word_dict.values(), factorial(length - i))

                sum = sum + x * factorial(word_dict[current_letter]) / factorial(word_dict[current_letter] - 1)

        return sum + 1

    _validate_input(word, search_word)
    return search(word, search_word)


def dictionary_search_old(main_word, search_word):
    counts = dict()
    letters = list()
    s_letters = list()
    r_letters = list()

    def _list_letters(word):
        for letter in word:
            r_letters.append(letter)
            if letter in letters:
                counts[letter] += 1
            else:
                letters.append(letter)
                counts[letter] = counts.get(letter, 1)
        letters.sort()
        for l in search_word:
            s_letters.append(l)

    def _error_check(search_word):
        try:
            word = main_word.lower()
            search_word = search_word.lower()
        except:
            return "PARAMETER_IS_NOT_STRING"
        _list_letters(word)
        if not len(search_word) == len(word):
            return "WORD_LENGTH_ERROR"

        for letter in search_word:
            if not letter in word:
                r_letters.remove(letter)
            else:
                return "LETTERS_NOT_IN_RANGE"

    def search(current_letter, Aletters, Acounts, l):
        sum = 0
        for letter in Aletters:
            if letter == current_letter:
                break
            product = 1
            for key, val in Acounts.items():
                if key == letter:
                    continue
                if val > 1:
                    product *= factorial(val)
            sum += factorial(l - 1) / product
        return sum

    def main_search():
        test_array = letters.copy()
        test_dict = counts.copy()
        total = 0
        for _ in search_word:
            break_letter = s_letters[0]

            total += search(break_letter, test_array, test_dict, len(s_letters))
            s_letters.remove(break_letter)
            test_array.remove(break_letter)
            if test_dict[break_letter] > 1:
                test_dict[break_letter] -= 1
                test_array.append(break_letter)
                test_array.sort()
            else:
                del test_dict[break_letter]
        total += 1
        return total

    _error_check(search_word)
    return main_search()


if __name__ == "__main__":
    print(dictionary_search(input("main word: "), input("search word: ")))
