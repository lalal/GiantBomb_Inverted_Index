import unittest
from PlatformDataRetriever import PlatformDataRetriever
from GameInvertedIndex import GameInvertedIndex

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

class GameInvertedIndexTest(unittest.TestCase):

    def test_instantiation(self):
        self.assertRaises(RuntimeError, GameInvertedIndex, 'foo')
        self.assertRaises(RuntimeError, GameInvertedIndex, [])

    def test_normalize(self):
        a = GameInvertedIndex(['foo'])
        self.assertEqual(a.normalize('Mario!'), 'mario')
        self.assertEqual(a.normalize('MARIO'), 'mario')
        self.assertEqual(a.normalize('All-Stars'), 'allstars')
        self.assertEqual(a.normalize('#1'), '1')
        self.assertEqual(a.normalize('Game:'), 'game')

    def test_build_index(self):
        data = [{'name': 'Mario Tennis'},
                {'name': 'Mario Party 4'},
                {'name': 'Dr. Mario'},
                {'name': 'Big Party: Super Mario Fun Time'},
                 {'name': 'Tetris Party'}]
        a = GameInvertedIndex(data)
        a.build_index()
        self.assertTrue('mario' in a.inv_index.keys())
        self.assertTrue('tennis' in a.inv_index.keys())
        self.assertTrue('dr' in a.inv_index.keys())
        self.assertTrue('super' in a.inv_index.keys())
        self.assertFalse('party:' in a.inv_index.keys())
        self.assertEqual(len(a.inv_index.keys()), 10)
        self.assertEqual(a.inv_index['4'], set([1]))
        self.assertEqual(a.inv_index['mario'], set([0, 1, 2, 3]))
        print a.inv_index

    def test_search(self):
        data = [{'name': 'Mario Tennis'},
                {'name': 'Mario Party 4'},
                {'name': 'Dr. Mario'},
                {'name': 'Big Party: Super Mario Fun Time'},
                {'name': 'Tetris Party'}]

        a = GameInvertedIndex(data)

        self.assertRaises(RuntimeError, a.search, 'Mario')

        a.build_index()
        res = a.search('Mario')

        self.assertEqual(len(res), 4)
        for i in range(4):
            self.assertTrue(data[i] in res)

        res = a.search('PARTY')
        self.assertEqual(len(res), 3)
        self.assertTrue(data[1] in res)
        self.assertTrue(data[3] in res)
        self.assertTrue(data[4] in res)

        res = a.search('mArIo PaRTY')
        self.assertEqual(len(res), 2)
        self.assertTrue(data[1] in res)
        self.assertTrue(data[3] in res)


if __name__ == '__main__':
    unittest.main()
