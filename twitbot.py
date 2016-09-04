'''
twitbot

A simple python-based twitter bot. 

The bot will read a CSV file which is formatted simply as:

<epoch timestamp>|<tweet>

If any of the timestamps are within time.now + timewindow in seconds, the associated
<tweets> are sent.
'''

import argparse, calendar, time, os, sys
import twitter_bot_utils as tbu

def getTweets(api, timeWindow, tweetFile, fudge, id=None):
    tweetList = []
    
    now = int(calendar.timegm(time.gmtime())) - fudge
    api.logger.info("Now is %d", now)
    srcfile = open(tweetFile, 'r')
    curId = -1
    for line in srcfile:
        row = line.split('|')
        rowtime = int(row[0])
        twt = row[1].rstrip()
        if (id == None) and (rowtime >= now) and (rowtime < (now + timeWindow)):
            tweetList.append(twt)
            api.logger.debug("Line : \"" + twt + "\" is within timeWindow")
        elif (id != None) and (rowtime > id):
            if curId == -1:
                curId = rowtime
                tweetList.append(twt)
                api.logger.debug("Line : \"" + twt + "\" is first line > " + str(id))
            elif curId != -1 and curId == rowtime:
                tweetList.append(twt)
                api.logger.debug("Line : \"" + twt + "\" matches curId " + str(id))
        else:
            api.logger.debug("Line : \"%s\" is not within timeWindow, %d-%d",
                 twt, now, (now + timeWindow))

    api.logger.info("Found %d tweets." , len(tweetList))
    return (curId, tweetList)

def main():
    parser = argparse.ArgumentParser(description='my twitter bot')
    parser.add_argument('-t', '--timewindow', dest='timewindow', help='Time window to use when determining which tweets to send.', type=int, default=3600)
    parser.add_argument('-f', '--fudge', dest='fudge', help='Fudge time in seconds to decrease the /now/ by.', type=int, default=300)
    parser.add_argument('-s', '--srcfile', dest='srcfile', help='CSV delimited source file for tweets to send.', default='tweets.csv')
    parser.add_argument('-i', '--idfile', dest='idfile', help='ID file to store the "ID" of the last sent tweet. With this defined the timestamps are no longer considered epoch seconds, but will be treated as unique, monotonix IDs. When the twitbot is run, it will find the lowest ID in the srcfile which is greater than the ID of the previously sent tweet. The ID of the currently sent tweet is then stored in this idfile.', default=None)
    parser.add_argument('-p', '--pause', dest='pause', help='Time to wait, in seconds, between tweets.', type=int, default=30)
    tbu.args.add_default_args(parser, version='1.0')
    
    args = parser.parse_args()
    api = tbu.api.API(screen_name=args.screen_name, config_file=args.config_file, 
        wait_on_rate_limit = True, wait_on_rate_limit_notify = True)
    api.logger.info('Timewindow is %d', args.timewindow)
    
    id = -1
    idfile = None
    if args.idfile != None:
        if os.access(args.idfile, os.W_OK | os.R_OK):
            idfile = open(args.idfile, 'r+')
            line = idfile.readline().strip()
            api.logger.info('idfile line is \"%s\"', line)
            if len(line) > 0:
                id = int(line)
                api.logger.info('Got ID %d from idfile.', id)
                if id < 0:
                    id = 0
            else:
                id = 0
        else:
            id = 0
            idfile = open(args.idfile, 'w+')
    
    (id, tweets) = getTweets(api, args.timewindow, args.srcfile, args.fudge, id)
    pause = args.pause
         
    if not args.dry_run:
        for tweet in tweets:
            try:
                api.update_status(tweet)
            except Exception, e:
                api.logger.error("Error tweating id %d. Error: %s", id, e)
                break
            api.logger.info('I just tweeted: \"%s\"', tweet)
            time.sleep(pause)
            
    if idfile != None and id != -1:
        api.logger.info('ID is now %d', id)
        idfile.seek(0)
        idfile.write(str(id) + "\n")
        idfile.close()
    elif idfile != None and id == -1:
        idfile.close()

if __name__ == '__main__':
    main()
