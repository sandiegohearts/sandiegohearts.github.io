
"""
Yelp API v2.0 code sample.

This program demonstrates the capability of the Yelp API version 2.0
by using the Search API to query for businesses by a search term and location,
and the Business API to query additional information about the top result
from the search query.

Please refer to http://www.yelp.com/developers/documentation for the API documentation.

This program requires the Python oauth2 library, which you can install via:
`pip install -r requirements.txt`.

Sample usage of the program:
`python sample.py --term="bars" --location="San Francisco, CA"`
"""
from __future__ import division
import argparse
import json
import pprint
import sys
import urllib
import urllib2
import pandas as pd

#import json
import csv
from collections import Counter

import numpy as np
import requests

import oauth2


API_HOST = 'api.yelp.com'
DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = 'San Francisco, CA'
SEARCH_LIMIT = 10
SEARCH_PATH = '/v2/search/'
BUSINESS_PATH = '/v2/business/'

# OAuth credential placeholders that must be filled in by users.
CONSUMER_KEY = CONSUMER_KEY
CONSUMER_SECRET = CONSUMER_SECRET
TOKEN = TOKEN
TOKEN_SECRET =TOKEN_SECRET

#import sys
#sys.path.append('/Users/yoavfreund/VaultDSE/')
#import yelpCreds
#CONSUMER_KEY,CONSUMER_SECRET,TOKEN,TOKEN_SECRET=yelpCreds.getKeys()

def request(host, path, url_params=None):
    """Prepares OAuth authentication and sends the request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        dict: The JSON response from the request.

    Raises:
        urllib2.HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = 'http://{0}{1}?'.format(host, path)
    #print 1
    consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    oauth_request = oauth2.Request(method="GET", url=url,parameters=url_params)
    #print 1.5
    oauth_request.update(
        {
            'oauth_nonce': oauth2.generate_nonce(),
            'oauth_timestamp': oauth2.generate_timestamp(),
            'oauth_token': TOKEN,
            'oauth_consumer_key': CONSUMER_KEY
        }
    )
    token = oauth2.Token(TOKEN, TOKEN_SECRET)
    oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url = oauth_request.to_url()
    #print 2
    print 'Querying {0} ...'.format(url)
    #print 3
    #conn = urllib2.urlopen(signed_url, None)
    #try:
     #   response = json.loads(conn.read())
    #  print 4
    #finally:
    #    conn.close()
    resp = requests.get(url=signed_url)
    response = resp.json()
    #print response
    #return response
    return response

def search(term, location):
    """Query the Search API by a search term and location.

    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.

    Returns:
        dict: The JSON response from the request.
    """
    
    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    return request(API_HOST, SEARCH_PATH, url_params=url_params)

def get_business(business_id):
    """Query the Business API by a business ID.

    Args:
        business_id (str): The ID of the business to query.

    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path)

def query_api(term, location):
    """Queries the API by the input values from the user.

    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    response = search(term, location)

    businesses = response.get('businesses')
        
    
    if not businesses:
        print 'No businesses for {0} in {1} found.'.format(term, location)
        return

    business_id = businesses[0]['id']
    
    print '{0} businesses found, querying business info for the top result "{1}" ...'.format(
        len(businesses),
        business_id
    )
    df = pd.DataFrame(columns=['id','name','categories','address','city','postal_code','state','latitude','longitude'])

    i=0
    for res in businesses:
        df.loc[i]=([res['id'],res['name'],term,res['location']['address'][0],res['location']['city'],res['location']['postal_code'],res['location']['state_code'],res['location']['coordinate']['latitude'],res['location']['coordinate']['longitude']])
        i+=1
    
    print df.iloc[0].values
    
    if len(pd.read_csv('data.csv')) == 0:
        df.to_csv('data.csv',index=False,encoding='utf8')
    else:
        with open('data.csv', 'a') as f:
            df.to_csv(f, header=False,index=False,encoding='utf8')
    
    response = get_business(business_id)
    
    #for res in businesses:
        
    
    print 'Result for business "{0}" found:'.format(business_id)
    pprint.pprint(response, indent=2)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM, type=str, help='Search term (default: %(default)s)')
    parser.add_argument('-l', '--location', dest='location', default=DEFAULT_LOCATION, type=str, help='Search location (default: %(default)s)')

    input_values = parser.parse_args()

    try:
        query_api(input_values.term, input_values.location)
    except urllib2.HTTPError as error:
        sys.exit('Encountered HTTP error {0}. Abort program.'.format(error.code))


if __name__ == '__main__':
    main()
