from sklearn import svm

from utils import read


def tweet_to_binary_array(tweet, index):
    words = tweet['text'].split(' ')
    index = index['words']
    array = [index[word] for word in words if index.get(word)]
    array2 = [False] * len(index)
    for e in array:
        array2[e] = True

    return (array2, tweet['group'])


def divide_data_and_target(tweets):
    # tweets = [tweet for tweet in tweets if tweet[1] != 'comment']
    data = [tweet[0] for tweet in tweets]
    target = [tweet[1] for tweet in tweets]
    return (data, target)


def create_classifier(train_tweets):
    clf = svm.SVC(gamma=0.1, C=20)
    data, target = divide_data_and_target(train_tweets)
    clf.fit(data, target)
    return clf


def test_classifier(clf, test_tweets):
    # data, target = divide_data_and_target(test_tweets)
    correct = 0
    for tweet, group in test_tweets:
        prediction = clf.predict(tweet)
        print(prediction, group)
        if prediction == group:
            correct += 1
    print('correct: ', correct)
    print('all: ', len(test_tweets))
    print('success: ', correct / len(test_tweets))


def count_groups(tweets):
    groups = {}
    for tweet in tweets:
        group = tweet['group']
        groups[group] = groups.get(group, 0) + 1
    print(groups)


def main():
    print('reading index')
    index = read('data/index.json')
    print('reading train')
    train = [tweet_to_binary_array(tweet, index) for tweet in read('data/train.json')]
    count_groups(read('data/train.json'))
    print('reading dev')
    dev = [tweet_to_binary_array(tweet, index) for tweet in read('data/dev.json')]
    # dev = [tweet for tweet in dev if tweet[1] != 'comment']
    print('creating classifier')
    clf = create_classifier(train)
    return clf
    # print('testing classifier')
    # test_classifier(clf, dev)


if __name__ == '__main__':
    clf = main()
    print('testing classifier')
    test_classifier(clf, dev)

# print(tweet_to_binary_array(train[0], index))
