from tweepy import OAuthHandler
import twitter_credential as tc


def authenticate_twitter_app():
    """
    An authentication procedure of Twitter.
    :return: An token for accessing twitter
    :rtype: OAuthHandler
    """
    auth = OAuthHandler(tc.CONSUMER_KEY, tc.CONSUMER_SECRET)
    auth.set_access_token(tc.ACCESS_TOKEN, tc.ACCESS_TOKEN_SECRET)
    return auth

