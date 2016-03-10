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
    for line in srcfile:
        line = line.rstrip()
        finalLine = replies + " " + line + " " + mentions + "\n"
        
        # If the line is > 140 + \n then issue warning
        if len(finalLine) > 141:
            print "Warning: \'" + finalLine + "\' is over 140char"
        
        dstfile.write("{time}|{twt}".format(time=str(curTime),twt=finalLine))
        if not re.search("\.\.\.$", line):
            curTime += args.timestride
        
    dstfile.close()
    

if __name__ == '__main__':
    main()
