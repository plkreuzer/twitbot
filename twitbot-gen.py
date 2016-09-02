'''
twitbot-gen.py

This file will either generate or append tweets to a twitbot compatible csv file.
'''

import argparse, csv, calendar, time, os.path, re
import twitter_bot_utils as tbu

def main():
    parser = argparse.ArgumentParser(description='my twitter bot source generator')
    parser.add_argument('-t', '--timestride', dest='timestride', help='Number in seconds to put between tweets.', type=int, default=3600)
    parser.add_argument('-s', '--srcfile', dest='srcfile', help='A source file to grab tweets from.', default='tweets.txt')
    parser.add_argument('-d', '--destfile', dest='destfile', help='The destination file to put timestampped tweets in.', default='tweets.csv')
    parser.add_argument('-n', '--now', dest='now', help='The /now/ time, i.e. the start time.', type=int, default=0)
    parser.add_argument('-m', '--mentions', dest='mentions', help='Any mentions you want to append.', default='')
    parser.add_argument('-r', '--replies', dest='replies', help='Any replies you want to prepend.', default='')
    
    args = parser.parse_args()
    now = args.now
    if now == 0:
        now = int(calendar.timegm(time.gmtime()))
    
    srcfile = open(os.path.abspath(args.srcfile), 'r')
    dstfile = open(os.path.abspath(args.destfile), 'a')
    
    curTime = now
    mentions = args.mentions.rstrip()
    replies = args.replies.rstrip()
    extraLineLen = len(mentions) + len(replies) + 3
    punctList = ['.', ',', ':', ';', '-']
    for line in srcfile:
        line = line.rstrip()
        if (len(line) + extraLineLen) > 141:
            '''
            Resultant line will be too big for one tweet, so break things up into sections like:
                <replies> <text> (X/Y) <mentions>
            First, split the text and put it into the tweetlist.
            Then, format and write the tweets to the file.
            '''
            tweetList = []
            maxLen = 140 - extraLineLen
            countLen = len('XX/YY')
            while len(line) > maxLen:
                '''
                    Thanks herminator: https://www.reddit.com/r/learnpython/comments/2fv6z2/help_splitting_strings_to_make_tweets_out_of_text/
                '''
                cutWhere, cutWhy = max((line.rfind(punc, 0, maxLen - countLen), punc) for punc in punctList)
                if cutWhere <= 0:
                    cutWhere = line.rfind(' ', 0, maxLen - countLen)
                    cutWhy = ' '
                elif line[cutWhere+1] == '"':
                    cutWhere += 1
                cutWhere += len(cutWhy)
                tweetList.append(line[:cutWhere].rstrip())
                line = line[cutWhere:].lstrip()
            
            if len(line) > 0:
                tweetList.append(line)
            
            totTweets = len(tweetList)
            curTweet = 1
            for tweet in tweetList:
                fTweet = "{twt} {X}/{Y} {mench}\n".format(rply = replies, 
                    twt = tweet, X = curTweet, Y = totTweets, mench = mentions)
                if len(replies) > 0:
                    fTweet = replies + " " + fTweet
                dstfile.write("{time}|{twt}".format(time=str(curTime),twt=fTweet))
                curTweet += 1
            curTime += args.timestride
        else:
            finalLine = replies + " " + line + " " + mentions + "\n"
            dstfile.write("{time}|{twt}".format(time=str(curTime),twt=finalLine))
            if not re.search("\.\.\.$", line):
                curTime += args.timestride
    dstfile.close()
    

if __name__ == '__main__':
    main()
