# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase


class TestPredictorController(BaseTestCase):
    """PredictorController integration test stubs"""

    def test_get_result_tweet_id(self):
        """Test case for get_result_tweet_id

        predict the salses
        """
        response = self.client.open(
            '/zaher88abd/DAta/1.0.0/tweetanalys/getresult/{itemid}'.format(itemid=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_set_tweet_id(self):
        """Test case for set_tweet_id

        predict the salses
        """
        response = self.client.open(
            '/zaher88abd/DAta/1.0.0/tweetanalys/{itemid}'.format(itemid=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
