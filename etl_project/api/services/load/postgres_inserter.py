from datetime import datetime, timedelta
import psycopg2
import logging


logger = logging.getLogger('myapp')

class PostgresInserter:
    def __init__(self, host, user, password, database):
        logger.info('Connecting to PostgreSQL database')
        self.connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            dbname=database
        )
        self.cursor = self.connection.cursor()

    def insert_tweet(self, tweet):
        logger.info(f'Inserting tweet by {tweet["UserName"]} into PostgreSQL')
        query = """
        INSERT INTO favorite_tweets (Text, UserName, LinkToTweet, FirstLinkUrl, CreatedAt, TweetEmbedCode)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (
            tweet['Text'],
            tweet['UserName'],
            tweet['LinkToTweet'],
            tweet['FirstLinkUrl'],
            tweet['CreatedAt'],
            tweet['TweetEmbedCode']
        ))
        self.connection.commit()

    def get_latest_timestamp(self):
        # Query the latest CreatedAt timestamp in PostgreSQL
        query = "SELECT MAX(CreatedAt) FROM favorite_tweets"
        self.cursor.execute(query)
        latest_timestamp = self.cursor.fetchone()[0]

        # If latest_timestamp is None, set it to 3 years ago from today
        if latest_timestamp is None:
            latest_timestamp = datetime.now() - timedelta(days=3*365)

        return latest_timestamp

    def close(self):
        logger.info('Closing PostgreSQL connection')
        self.cursor.close()
        self.connection.close()