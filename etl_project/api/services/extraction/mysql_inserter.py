from .models.favorite_tweets import FavoriteTweet
from datetime import datetime
from django.conf import settings
import mysql.connector
import json
import logging

logger = logging.getLogger('myapp')

class MySQLInserter:
    def __init__(self, host, user, password, database):
        logger.info('Connecting to MySQL database')
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()

    def insert_tweet(self, tweet: FavoriteTweet):
        logger.info(f'Inserting tweet by {tweet.username}')
        query = """
        INSERT INTO favorite_tweets (Text, UserName, LinkToTweet, FirstLinkUrl, CreatedAt, TweetEmbedCode)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        self.cursor.execute(query, (
            tweet.text,
            tweet.username,
            tweet.link_to_tweet,
            tweet.first_link_url,
            current_time,
            tweet.tweet_embed_code
        ))
        self.connection.commit()
        logger.info(f'Tweet inserted successfully: {tweet.text}')

    def parse_jsonl_and_insert(self, file_path):
        logger.info(f'Starting to parse {file_path}')
        with open(file_path, 'r') as file:
            for line in file:
                tweet_data = json.loads(line.strip())
                tweet = FavoriteTweet(
                    tweet_data['Text'],
                    tweet_data['UserName'],
                    tweet_data['LinkToTweet'],
                    tweet_data['FirstLinkUrl'],
                    tweet_data['CreatedAt'],
                    tweet_data['TweetEmbedCode']
                )
                self.insert_tweet(tweet)
                logger.info(f'Tweet inserted from {file_path}')
        logger.info('Finished inserting all tweets')

    def close(self):
        logger.info('Closing MySQL connection')
        self.cursor.close()
        self.connection.close()