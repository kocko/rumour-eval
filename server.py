import configparser
import json
import os

import tweepy
from flask import Flask, render_template, request

from search import search
from utils import read

app = Flask(__name__)
data = read('data/data.json')
rumours = list(data.keys())
threads = {k: v for rumour in data.values() for k, v in rumour.items()}
groups = read('data/groups.json')


def replies(thread):
    # log(thread_id)
    # log(len(threads[thread_id].get('replies', dict()).values()))
    # return [log(tweet['text']) for tweet in threads[thread_id].get('replies', dict()).values()]
    return [{
                'text': tweet['text'],
                'group': groups.get(tweet.get('id_str', 0), 'unknown')
            } for tweet in thread.get('replies', dict()).values()]


print(rumours)


@app.route("/")
def index():
    return render_template('index.html', rumours=rumours)


@app.route("/fetch")
def fetch_tweet_page():
    return render_template('fetch.html')


@app.route("/fetch-tweet", methods=['POST'])
def fetch_tweet_by_id():
    tweet_id = request.form['tweet_id']
    create_folders(tweet_id)
    api = authenticate()

    tweet = api.get_status(tweet_id)
    persist_tweet(tweet, "source-tweet")

    return render_template('success.html')


def create_folders(tweet_id):
    tweet_id_as_string = str(tweet_id)
    tweet_dir = "resources/dataset/rumoureval-data/random-rumours/" + tweet_id_as_string
    src_tweet_dir = tweet_dir + "/source-tweet"
    replies_tweet_dir = tweet_dir + "/replies"

    os.makedirs(tweet_dir)
    os.makedirs(src_tweet_dir)
    os.makedirs(replies_tweet_dir)


def authenticate():
    config = configparser.ConfigParser()
    config.read('config/twitter.ini')

    consumer_key = config.get('Twitter', 'consumer_key')
    consumer_secret = config.get('Twitter', 'consumer_secret')
    access_key = config.get('Twitter', 'access_key')
    access_secret = config.get('Twitter', 'access_secret')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    return tweepy.API(auth)


def persist_tweet(tweet, folder):
    tweet_id_as_string = str(tweet.id)
    tweet_dir = "resources/dataset/rumoureval-data/random-rumours/" + tweet_id_as_string + "/" + folder
    with open(tweet_dir + "/" + tweet_id_as_string + ".json", 'w') as outfile:
        json.dump(tweet._json, outfile)


@app.route("/style.css")
def style():
    return render_template('style.css')


@app.route('/text/<text>')
def search_text(text):
    print('searching for ', text.replace('%23', '#'))
    results = sorted(search(text).items(), key=lambda x: x[1], reverse=True)
    results = [{
                   "rating": rating,
                   "text": threads[id]['source']['text'],
                   "replies": replies(threads[id])
                   # [tweet['text'] for tweet in threads[id].get('replies', dict()).values()]
               } for id, rating in results]
    return json.dumps(results)


@app.route('/rumour/<rumour>')
def search_rumour(rumour):
    results = data[rumour].values()
    print('-----')
    print(len(results))
    print(len(list(results)))
    print(len(list(results)[0]))
    print(list(results)[0]['source']['text'])
    # print(json.dumps(list(results)[0]))
    print('-----')
    results = [{
                   "text": thread['source']['text'],
                   "replies": replies(thread)
               } for thread in results]
    print('dasdansuidnaskd')
    return json.dumps(results)


if __name__ == "__main__":
    app.run()
