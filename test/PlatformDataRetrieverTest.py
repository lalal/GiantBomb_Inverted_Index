import unittest
from PlatformDataRetriever import PlatformDataRetriever

class PlatformDataRetrieverTest(unittest.TestCase):

    def test_get_from_api(self):
        b = PlatformDataRetriever(43, 'N64')  # Nintendo 64

        # offset 0, limit 1
        data = b.get_from_api(0, 1)
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['status_code'], 1)
        self.assertTrue('number_of_total_results' in data)


    def test_retrieve_games_for_platform(self):

        b = PlatformDataRetriever(43, 'N64')  # Nintendo 64
        total = b.get_total_games_for_platform()

        games = b.retrieve_games_for_platform()
        self.assertEquals(len(games), total)


    def test_get_total_games_for_platform(self):
        b = PlatformDataRetriever(43, 'N64')  # Nintendo 64
        total = b.get_total_games_for_platform()
        self.assertEquals(total, 375)

    def test_get_and_store_names(self):
        b = PlatformDataRetriever(43, 'N64')  # Nintendo 64
        results = [None] * 4

        b.get_and_store_names(results, 200)

        self.assertEqual(results[0], None)
        self.assertEqual(results[1], None)
        self.assertEqual(results[3], None)

        self.assertTrue(isinstance(results[2], list))
        self.assertEqual(len(results[2]), 100)

    def test_setup_results_list(self):
        b = PlatformDataRetriever(43, 'N64')  # Nintendo 64
        total = 2211
        results = b.setup_results_list(total)
        self.assertEqual(len(results), 23)
        total = 112
        results = b.setup_results_list(total)
        self.assertEqual(len(results), 2)
        total = -221
        results = b.setup_results_list(total)
        self.assertEqual(len(results), 1)



if __name__ == '__main__':
    unittest.main()
