threshold = 0.4


def contains_original(reply, original_tweet):
    count = 0
    split = original_tweet.split()
    total = len(split)
    for token in split:
        if token in reply:
            count += 1
    return (count / total) >= threshold
