# twitbot
A simple twitterbot experiment

This project consists of two Python scripts: twitbot.py and twitbot-gen.py.

The twitbot.py program takes in a csv file of timestamped tweets and Twitter bot credentials. 
If any of the timestamps within the tweet file are near the current time minus the fudge factor plus
the timewindow, then those tweets are tweeted. The idea is for this program to be run on a regular 
basis via something like crond/crontab.

The twitbot-gen.py is a simple program which will generate a csv file of timestamped tweets by parsing
a source files of tweets. The source file should contain one line per tweet. Arguments can be passed
to denote the startime and the timestride. 

Both programs offer simple explinations by executing them with the '--help' option.
