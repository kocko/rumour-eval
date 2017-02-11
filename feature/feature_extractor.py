from feature.contains_original import contains_original
from feature.opinion_words import opinion_words_percentage
from feature.questionmark import contains_question_mark
from utils import read, write

REPLIES = "..\\data\\tweets.json"
OUTFILE = "..\\data\\vector.json"
NEGATIVE_LEXICON = "..\\resources\\lexicon\\negative.txt"
POSITIVE_LEXICON = "..\\resources\\lexicon\\positive.txt"

# vector explained:
# [contains_original, positive_words_percentage, negative_words_percentage, reversed_word_order, contains_question_mark]
# more possible features: contains_only_usernames

def main():
    data = read(REPLIES)
    negative = [line.rstrip('\n') for line in open(NEGATIVE_LEXICON)]
    positive = [line.rstrip('\n') for line in open(POSITIVE_LEXICON)]
    result = {}
    for tweet in data:
        tweet_id = tweet['id']
        text = tweet['text']
        vector = list()
        if "reply_to" in tweet:
            in_reply_to = tweet['reply_to']
            vector.append(contains_original(text, in_reply_to))
        vector.append(opinion_words_percentage(text, positive))
        vector.append(opinion_words_percentage(text, negative))
        # todo: implement reversed_word_order feature
        vector.append(contains_question_mark(text))
        result[tweet_id] = {
            'rumour': tweet['rumour'],
            'vector': vector
        }
    write(OUTFILE, result)


if __name__ == "__main__":
    main()
