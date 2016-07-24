import requests
import json
from threading import Thread
import math

class PlatformDataRetriever:
    """
    Retrieves data from GiantBoy api by platform id and returns the data
    """

    url = 'http://www.giantbomb.com/api/games/'
    format='json'
    field_list='name'
    batch_size = 100

    def __init__(self, platform, p_name):
        """
        Constructor class sets up the basic details about the platform and initializes the names list
        :param platform:  the id of the platform which will be used to retrieve data via the api
        :param p_name:    the stringified name of the platform which will be used for display purposes
        :return:          None
        """
        self.platform = platform
        self.platform_name = p_name
        self.names = []

    def get_from_api(self, offset, limit):
        """
        Setup and retrieve data from the Giant Bomb API using the requests library
        :param offset: the position within the total titles we want to retrieve data for from the api
        :param limit:  The total number of results you want returned back, max limit at present is 100
        :return:  the data returned via the api after being json loaded
        """
        params = dict(api_key='84e4fdf8957ddf84247c3ea012a4773ffead8156',
                      format=self.format,
                      offset=offset,
                      limit=limit,
                      platforms='%s' % self.platform,
                      field_list=self.field_list)
        resp = requests.get(url=self.url, params=params)

        data = []
        if resp.status_code == 200:
            data = json.loads(resp.text)
            if data['status_code'] != 1:
                raise RuntimeError('Got back the following error from the api: %s' % data['error'])
        else:
            resp.raise_for_status()

        return data


    def get_total_games_for_platform(self):
        """
        We make an api call to get the total titles for a given platform
        Redundant because we set the limit as 1, technically, we should be able to use it

        :return: the total game titles in the platform assuming it is returned
        """
        # limit to 1 because all we need are the total results
        data = self.get_from_api('0', 1)
        my_total = 0
        if 'number_of_total_results' in data:
            my_total = data['number_of_total_results']
        else:
            raise RuntimeError('Total games was not returned by api. Potential error: %s' % data['error'])

        return my_total

    def get_and_store_names(self, results, offset):
        """
        wrapper function on api call to support threading and result storing
        :param results: pass by reference list which will be used to store results for a given offset
        :param offset: the position within the total titles we want to retrieve data for from the api
        :return: None
        """
        my_names = []

        data = self.get_from_api(offset, 100)

        if 'results' in data:
            my_results = data['results']
        else:
            raise RuntimeError('There were no game titles returned by api for offset: %s. \
                                Potential error: %s' % (offset, data['error']))

        # Consolidate the name and platform in a map
        # The map allows for more metadata to be collected as we iterate through the results
        for i in my_results:
            my_names.append({'name': i['name'],
                             'platform': self.platform_name})

        # Results for this thread go in their proper index of the results list
        results[offset/self.batch_size] = my_names


    def retrieve_games_for_platform(self):
        """
        Threads the retrieval of data via the giant bomb api
        We first make a call to the api to get the total titles for the platform
        This allows us to break up the data retrieval into (total / 100) threads
        since we can pull batches of 100 at a time
        :return: The collected names or titles of the games for the platform (also accessible via the object)
        """
        total = self.get_total_games_for_platform()
        print "Now retrieving %s total game titles for platform %r....." % (total, self.platform_name)

        my_threads = []

        # We can create ceiling(total / 100) threads
        results = self.setup_results_list(total)

        # Create the threads and add them to a list
        for i in range(0, total, self.batch_size):
            t = Thread(target=self.get_and_store_names,
                       args=(results, i,))
            my_threads.append(t)

        # Start all threads
        for i in my_threads:
            i.start()

        # Wait for threads to finish
        for i in my_threads:
            i.join()

        # Consolidate all the results, ie, game titles, together
        for i in results:
            self.names += i
        print "All game titles for %r have been retrieved!" % self.platform_name
        return self.names

    def setup_results_list(self, total):

        if total > 0:
            results = [None] * int(math.ceil((total / float(self.batch_size))))
        else:
            results = [None]

        return results

