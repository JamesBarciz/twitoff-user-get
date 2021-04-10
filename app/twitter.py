import tweepy
from decouple import config


TWITTER_AUTH = tweepy.OAuthHandler(
  config('TWITTER_API_KEY'),
  config('TWITTER_API_SECRET')
)

TWITTER = tweepy.API(TWITTER_AUTH)


def get_user(username):
  final_JSON = {}

  try:
    twitter_user = TWITTER.get_user(username)
    final_JSON['twitter_handle'] = {'username': username, 'id': twitter_user.id}

    tweets = twitter_user.timeline(
      count=200, exclude_replies=True, include_rts=False, tweet_mode='extended'
      )

    final_JSON['tweets'] = []

    for tweet in tweets:
      text = tweet.full_text
      tweet_id = tweet.id
      final_JSON['tweets'].append({'id': tweet_id, 'full_text': text})

    return final_JSON

  except Exception as e:
    print(f'Error processing {username}: {e}')
    raise e


if __name__ == '__main__':
  JSON_elon = get_user('elonmusk')