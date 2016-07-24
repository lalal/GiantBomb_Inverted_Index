import unittest
from GameInvertedIndex import GameInvertedIndex

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
