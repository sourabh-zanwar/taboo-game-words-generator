import pandas as pd


def draw_word(keys):
    curr_word = keys.pop()
    return curr_word, keys


def game_play(curr_word, action, completed_words):
    past_words = completed_words[action]
    past_words.append(curr_word)
    completed_words[action] = list(set(past_words))
    return completed_words


def complete_round(remaining_keys, completed_words):
    keys = remaining_keys + completed_words["skipped"]
    keys = list(set(keys))
    return keys, completed_words
