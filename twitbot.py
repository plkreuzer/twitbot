'''
twitbot

A simple python-based twitter bot. 

The bot will read a CSV file which is formatted simply as:

<epoch timestamp>|<tweet>

If any of the timestamps are within time.now + timewindow in seconds, the associated
<tweets> are sent.
'''

import argparse, calendar, time
import twitter_bot_utils as tbu


def getTweets(api, timeWindow, tweetFile, fudge):
    tweetList = []
    
    now = int(calendar.timegm(time.gmtime())) - fudge
    api.logger.info("Now is %d", now)
    srcfile = open(tweetFile, 'r')
    for line in srcfile:
        row = line.split('|')
        rowtime = int(row[0])
        twt = row[1].rstrip()
        if (rowtime >= now) and (rowtime < (now + timeWindow)):
            tweetList.append(twt)
            api.logger.debug("Line : \"" + twt + "\" is within timeWindow")
        else:
            api.logger.debug("Line : \"%s\" is not within timeWindow, %d-%d",
                 twt, now, (now + timeWindow))

    api.logger.info("Found %d tweets." , len(tweetList))
    return tweetList

def main():
    parser = argparse.ArgumentParser(description='my twitter bot')
    parser.add_argument('-t', '--timewindow', dest='timewindow', help='Time window to use when determining which tweets to send.', type=int, default=3600)
    parser.add_argument('-f', '--fudge', dest='fudge', help='Fudge time in seconds to decrease the /now/ by.', type=int, default=300)
    parser.add_argument('-s', '--srcfile', dest='srcfile', help='CSV delimited source file for tweets to send.', default='tweets.csv')
    parser.add_argument('-p', '--pause', dest='pause', help='Time to wait, in seconds, between tweets.', type=int, default=30)
    tbu.args.add_default_args(parser, version='1.0')
    
    args = parser.parse_args()
    api = tbu.api.API(screen_name=args.screen_name,config_file=args.config_file)
    api.logger.info('Timewindow is %d', args.timewindow)
    tweets = getTweets(api, args.timewindow, args.srcfile, args.fudge)
    pause = args.pause
    
    if not args.dry_run:
        for tweet in tweets:
            api.update_status(tweet)
            api.logger.info('I just tweeted: \"%s\"', tweet)
            time.sleep(pause)

if __name__ == '__main__':
    main()
