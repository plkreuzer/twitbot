'''
twitbot

A simple python-based twitter bot.
'''

import argparse
import twitter_bot_utils as tbu

def main():
    parser = argparse.ArgumentParser(description='my twitter bot')
    tbu.args.add_default_args(parser, version='1.0')
    
    args = parser.parse_args()
    api = tbu.api.API(screen_name=args.screen_name,config_file=args.config_file)

    if not args.dry_run:
        api.update_status('Hello World!')
        api.logger.info('I just tweeted!')

if __name__ == '__main__':
    main()