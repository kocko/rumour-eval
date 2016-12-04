import os, re, json
from os import path
from pprint import pprint

def read(file):
    with open(file) as data_file:
        return json.load(data_file)

def write(file, data):
    with open(file, 'w') as outfile:
        json.dump(data, outfile)

def folders(dirname):
    return ((f, os.path.join(dirname, f)) for f in next(os.walk(dirname))[1])

def files(dirname):
    return ((f, os.path.join(dirname, f)) for f in next(os.walk(dirname))[2])

def tweet(location):
    keys = ['text', 'id_str', 'created_at', 'in_reply_to_status_id_str', 'retweet_count',
        'entities'] #user?
    data = read(location)
    return { key: data[key] for key in keys }

def load_data():
    # rumours = {k: {} for k in folders('.')}
    data = {}
    for rumour, r_location in folders('.'):
        data[rumour] = {}
        for thread, t_location in folders(r_location):
            replies = files(path.join(t_location, 'replies'));
            data[rumour][thread] = {
                "structure": read(path.join(t_location, 'structure.json')),
                "source": tweet(path.join(t_location, 'source-tweet', thread + '.json')),
                "replies": {id[:-5]: tweet(f) for id, f in replies}
            }

    write('data.json', data);
    return data

def walk(parent, node, result=[]):
    for key, item in node.items():
        result.append({"from": parent, "to": key})
        if len(item):
            walk(key, item, result)
    return result

def log(sth):
    print(sth)
    return sth

def to_table_json():
    data = read('data.json')
    result = []
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
                    'reply_to': tweet['in_reply_to_status_id_str']
                    # 'reply_to': all_tweets[tweet['in_reply_to_status_id_str']]['text']
                }

    for id, tweet in all_tweets.items():
        if 'reply_to' in tweet:
            tweet['reply_to'] = all_tweets[tweet['reply_to']]['text']

    write('tweets.json', list(all_tweets.values()))
    to_csv(list(all_tweets.values()))

import csv
def to_csv(data):
    keys = ['id', 'rumour', 'text', 'reply_to']

    with open('data.csv', 'w', encoding='utf-8') as file:
        csv_file = csv.writer(file)
        csv_file.writerow(keys)
        for item in data:
            if 'reply_to' in item:
                csv_file.writerow([item[key] for key in keys])

if __name__ == "__main__":
    load_data()
    to_table_json()

