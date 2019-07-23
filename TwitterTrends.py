import time
import tweepy
import json


def printTopTenElements(allItemsDict, freqAtIndex):
    allItemsDictValues = list(allItemsDict.values())
    # heapq.heapify(allItemsDictValues)
    sortedList = sortList(allItemsDictValues, freqAtIndex)

    if (len(sortedList) >= 10):
        for i in range(10):
            print('Value at index ' + str(i) + ' ' + sortedList[i].toString())
    else:
        for i in range(len(sortedList)):
            print('Value at index ' + str(i) + ' ' + sortedList[i].toString())

def sortList(list, freqAtIndex):
    if (freqAtIndex == 0):
        return sorted(list, key=compareGetFreq0, reverse=True)
    if (freqAtIndex == 1):
        return sorted(list, key=compareGetFreq1, reverse=True)
    if (freqAtIndex == -1):
        return sorted(list, key=compareGetPredictedFreq, reverse=True)

def compareGetFreq0(tweetFreq):
    if (len(tweetFreq.freq) == 0):
        return 0
    return tweetFreq.freq[0]

def compareGetFreq1(tweetFreq):
    if (len(tweetFreq.freq) < 2):
        return 0
    return tweetFreq.freq[1]

def compareGetPredictedFreq(tweetFreq):
    return tweetFreq.predictedFreq

class TweetFreq:
    name=''
    # freq[0] = 4, freq[1] = 5
    freq = []
    rateOfChange=''
    predictedFreq=0

    def calculatePredictedValue(self):
        if self.freq[0]==0:
            self.predictedFreq = self.freq[1]
        elif (len(self.freq) >= 2):
            rateFactor = ((self.freq[1] - self.freq[0]) / self.freq[0])
            self.predictedFreq = self.freq[1]*rateFactor + self.freq[1]

    def print(self):
        print(self.toString())

    def toString(self):
        frequencies = str(self.freq)
        return ' Name ' + self.name + ', freq: ' + frequencies + ', PredictedFreq: ' + str(self.predictedFreq)


class CollectTrends:
    # Which topic is likely to become trend

    # Put trends in files
    def getTrends(self):
        CONSUMER_KEY = 'mid4jiNnnpRS2XuuRbvMfpoQF'
        CONSUMER_SECRET = 'WQLAGiTHIOWEvlvAft9XY3krX4y3Kqs6edFu7csrX0JlsEtr2N'
        ACCESS_TOKEN = '235982811-O7n7LNkbksk0XnyNU4eA1O2f2X9HDRORSMShXUZJ'
        ACCESS_TOKEN_SECRET = 'WlEXOdYRlapHwHvDezUWJgqf5g0uqiY2cyWTHGY21OkDx'

        oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        oauth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(oauth, parser=tweepy.parsers.JSONParser())

        # All seen trends in twitter
        # [Name] : {object of class TweetFreq}
        allItemsDict = {}

        for iteration in range(2):
            # Get Trends for all globe
            currentTrendsResultList = api.trends_place(1)
            trendsPlaceResult = currentTrendsResultList[0]
            currentTrendsDict = trendsPlaceResult['trends']
            print('iteration ' + str(iteration))
            print(trendsPlaceResult)

            for trend in currentTrendsDict:
                # Only add new trends to the list
                name = trend['name']
                currentFreq = trend['tweet_volume']
                if currentFreq == None:
                    currentFreq = 0

                if name in allItemsDict:
                    allItemsDict[name].freq.append(currentFreq)
                else:
                    newTrend = TweetFreq()
                    newTrend.name = name
                    newTrend.freq = [currentFreq]
                    allItemsDict[name] = newTrend

            print('iteration ' + str(iteration) + ' length of map of trends ' + str(len(allItemsDict)))
            if (iteration == 0):
                time.sleep(3600)

        for trend in allItemsDict.values():
            trend.print()

        # trendDoc = open('trends.txt', "w")
        # allItemsDictJson = json.dumps(allItemsDict)
        # trendDoc.write(allItemsDictJson)
        # trendDoc.close()

        return allItemsDict


if __name__ == '__main__':
    object = CollectTrends()
    testTweetsDict = object.getTrends()

    # testTweetsDict = {}
    #
    # amrita = TweetFreq()
    # amrita.name = 'amrita'
    # amrita.freq = [5, 2]
    # testTweetsDict['Amrita'] = amrita
    #
    # bob = TweetFreq()
    # bob.name = 'bob'
    # bob.freq = [3, 4]
    # testTweetsDict['bob'] = bob

    print('sorting by frequency for iteration 0')
    printTopTenElements(testTweetsDict, 0)

    print('sorting by frequency for iteration 1')
    printTopTenElements(testTweetsDict, 1)

    for tweetFreq in testTweetsDict.values():
        tweetFreq.calculatePredictedValue()

    print('sorting by predictedFreq')
    printTopTenElements(testTweetsDict, -1)
