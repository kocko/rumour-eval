import csv
from os import path

from utils import read, write, folders, files

DATA_LOCATION = ".\\resources\\dataset\\rumoureval-data"
TRAIN = DATA_LOCATION + "\\..\\traindev\\rumoureval-subtaskA-train.json"
DEV = DATA_LOCATION + "\\..\\traindev\\rumoureval-subtaskA-dev.json"


def tweet(location):
    keys = ['text', 'id_str', 'created_at', 'in_reply_to_status_id_str', 'retweet_count', 'entities']
    # user?
    data = read(location)
    return {key: data[key] for key in keys}


def load_data():
    # rumours = {k: {} for k in folders('.')}
    data = {}
    for rumour, r_location in folders(DATA_LOCATION):
        data[rumour] = {}
        for thread, t_location in folders(r_location):
            try:
                replies = files(path.join(t_location, 'replies'));
            except StopIteration:
                replies = []
            # print(rumour, thread, path.join(t_location, 'replies'))
            data[rumour][thread] = {
                "structure": read(path.join(t_location, 'structure.json')),
                "source": tweet(path.join(t_location, 'source-tweet', thread + '.json')),
                "replies": {id[:-5]: tweet(f) for id, f in replies}
            }

    write('data/data.json', data)
    return data


def walk(parent, node, result=None):
    if result is None:
        result = []
    for key, item in node.items():
        result.append({"from": parent, "to": key})
        if len(item):
            walk(key, item, result)
    return result


def create_table_json():
    data = read('data/data.json')
    all_tweets = {}
    for rumour, rumour_data in data.items():
        for x, thread in rumour_data.items():
            all_tweets[thread['source']['id_str']] = {
                'rumour': rumour,
                'text': thread['source']['text'],
                'id': thread['source']['id_str']
            }

            for key, tweet in thread['replies'].items():
                all_tweets[key] = {
                    'rumour': rumour,
                    'text': tweet['text'],
                    'id': key,
                    'reply_to': tweet['in_reply_to_status_id_str'],
                    'contains_original': compare_content(tweet['text'], thread['source']['text'])
                    # 'reply_to': all_tweets[tweet['in_reply_to_status_id_str']]['text']
                }

    for id, tweet in all_tweets.items():
        if 'reply_to' in tweet:
            tweet['reply_to'] = all_tweets[tweet['reply_to']]['text']

    write('data/tweets.json', list(all_tweets.values()))
    to_csv(list(all_tweets.values()))
    return all_tweets.values()


def compare_content(reply, original_tweet):
    count = 0
    split = original_tweet.split()
    total = len(split)
    for token in split:
        if token in reply:
            count += 1
    return (count / total) >= 0.4


def divide_train_dev(tweets):
    train_categories = read(TRAIN)
    dev_categories = read(DEV)
    train = []
    dev = []

    for tweet in tweets:
        if tweet.get('reply_to'):
            el = {
                'text': tweet['text'],
                'reply_to': tweet['reply_to']
            }

            if tweet['id'] in train_categories:
                el['group'] = train_categories[tweet['id']]
                train += [el]
                # train += [{
                #     'text': tweet['text'],
                #     'reply_to': tweet['reply_to'],
                #     'group': train_categories[tweet['id']]
                # }]
            else:
                el['group'] = dev_categories[tweet['id']]
                dev += [el]
                # dev += [{
                #     'text': tweet['text'],
                #     'reply_to': tweet['reply_to'],
                #     'group': dev_categories[tweet['id']]
                # }]
                # all += [el]

    write('data/train.json', train)
    write('data/dev.json', dev)
    write('data/groups.json', dict(train_categories.items() | dev_categories.items()))


def to_csv(data):
    keys = ['id', 'rumour', 'text', 'reply_to']

    with open('data/data.csv', 'w', encoding='utf-8') as file:
        csv_file = csv.writer(file)
        csv_file.writerow(keys)
        for item in data:
            if 'reply_to' in item:
                csv_file.writerow([item[key] for key in keys])


def main():
    load_data()
    tweets = create_table_json()
    divide_train_dev(tweets)


if __name__ == "__main__":
    main()