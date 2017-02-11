from utils import read, write, folders, files

from feature.contains_original import contains_original
from feature.questionmark import contains_question_mark


REPLIES = "..\\data\\tweets.json"
OUTFILE = "..\\data\\vector.json"


def main():
    data = read(REPLIES)
    result = {}
    for tweet in data:
        tweet_id = tweet['id']
        text = tweet['text']
        if "reply_to" in tweet:
            in_reply_to = tweet['reply_to']
            vector = list()
            vector.append(contains_original(text, in_reply_to))
            vector.append(contains_question_mark(text))
            result[tweet_id] = {
                'rumour': tweet['rumour'],
                'vector': vector
            }

    write(OUTFILE, result)


if __name__ == "__main__":
    main()