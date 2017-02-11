# or maybe negative word count?
def opinion_words_percentage(text, lexicon):
    split = text.split()
    total = len(split)
    if total == 0:
        return 0.0
    count = 0
    for word in split:
        if word in lexicon:
            count += 1
    return count / total
