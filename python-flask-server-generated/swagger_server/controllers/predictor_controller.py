import connexion
import six
from swagger_server.controllers.EtractTweets import extractTweets
from swagger_server.models.byte_array import ByteArray  # noqa: E501
from swagger_server import util


def get_result_tweet_id(itemid):  # noqa: E501
    """predict the salses

    Returns a single number for the salse # noqa: E501

    :param itemid: ID of item to return
    :type itemid: int

    :rtype: None
    """
    return 'do some magic!'


def get_result_tweet_id_status(itemid, outputstate):  # noqa: E501
    """predict the salses

    Returns a single number for the salse # noqa: E501

    :param itemid: ID of item to return
    :type itemid: int
    :param outputstate: ID of item to return
    :type outputstate: int

    :rtype: None
    """
    extractTweets(itemid, 2, 5)

    """
    End of test
    """

    html = "<html>" \
           "<head><title>Tweet Analyzer</title></head>" \
           "<body><h1>Tweet Analyzer</h1>" \
           "<h3>Coming Soon</h3>" \
           "<h3>"   "</h3>" \
           "</body>" \
           "</html>"

    return html


def set_tweet_id(itemid, times, seconds):  # noqa: E501
    """predict the salses

    Returns a single number for the salse # noqa: E501

    :param itemid: ID of item to return
    :type itemid: str
    :param times: ID of item to return
    :type times: int
    :param seconds: ID of item to return
    :type seconds: int

    :rtype: None
    """
    print(itemid, times, seconds)
    extractTweets(itemid, times, seconds)

    """
    End of test
    """

    html = "<html>" \
           "<head><title>Tweet Analyzer</title></head>" \
           "<body><h1>Tweet Analyzer</h1>" \
           "<h3>Coming Soon</h3>" \
           "<h3>"   "</h3>" \
           "</body>" \
           "</html>"

    return html
