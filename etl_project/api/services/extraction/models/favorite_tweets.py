class FavoriteTweet:
    def __init__(self, text, username, link_to_tweet, first_link_url, created_at, tweet_embed_code):
        self.text = text
        self.username = username
        self.link_to_tweet = link_to_tweet
        self.first_link_url = first_link_url
        self.created_at = created_at
        self.tweet_embed_code = tweet_embed_code

    def __str__(self):
        return f'Tweet by {self.username}: "{self.text}"'