# Analyze the numbers in trump's tweets using Benford's Law
# data source: http://www.trumptwitterarchive.com/archive json export

import json
import re
import collections
import string
import scipy
from scipy import stats


with open("tweets_2016_06_15-2019_01_30.json") as infile:
    data = json.load(infile)


regex_query = r' ([0-9][0-9{}]*)'.format(re.escape(string.punctuation))
tweets_with_numbers = [tweet for tweet in data if re.search(regex_query, tweet['text'])]

# extract multiset of leading digits from each tweet
tweet_to_numbers = {tweet['text']: re.findall(regex_query, tweet['text']) for tweet in tweets_with_numbers}
all_numbers = [y for (tweet, numbers) in tweet_to_numbers.items() for y in numbers]
print(list(sorted(all_numbers)))

# 5 of the numbers in his tweets start with a 0, so those are excluded and
# won't change much.
leading_digits = [int(y[0]) for y in all_numbers if y[0] != '0']
n = len(leading_digits)


digits_histogram = collections.Counter(leading_digits)
benfords_dist = {
    1: 0.301, 2: 0.176, 3: 0.125, 4: 0.097, 5: 0.079,
    6: 0.067, 7: 0.058, 8: 0.051, 9: 0.046,
}
expected_frequencies = [n * benfords_dist[i] for i in range(1, 10)]

actual_frequencies = [digits_histogram[i] for i in range(1, 10)]

print("Expected frequencies: %s" % expected_frequencies)
print("Actual frequencies: %s" % actual_frequencies)
# critical value is ~30
# actual statistic is ~115.50136030911078
print(scipy.stats.chisquare(actual_frequencies, f_exp=expected_frequencies))
