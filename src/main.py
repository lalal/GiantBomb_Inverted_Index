import argparse
from PlatformDataRetriever import PlatformDataRetriever
from GameInvertedIndex import GameInvertedIndex
from threading import Thread


def load_game_data():
    """
    Retrieves data for the nes, snes and n64 systems via giant bomb api, creates an inverted index on them
    :return: The inverted index of combined games from nes, snes and n64
    """
    nes = PlatformDataRetriever(9, "Super Nintendo Entertainment System")
    snes = PlatformDataRetriever(21, "Nintendo Entertainment System")
    n64 = PlatformDataRetriever(43, "Nintendo 64")

    all_games = []
    my_threads = []
    my_threads.append(Thread(target=nes.retrieve_games_for_platform, args=()))
    my_threads.append(Thread(target=snes.retrieve_games_for_platform, args=()))
    my_threads.append(Thread(target=n64.retrieve_games_for_platform, args=()))

    for i in my_threads:
        i.start()

    for i in my_threads:
        i.join()

    all_games = nes.names + snes.names + n64.names

    print len(all_games)

    inverted = GameInvertedIndex(all_games)
    inverted.build_index()
    return inverted


def run_main():
    """
    Main function which will pull data,
    index it
    and then run a menu loop to get input from the user
    """

    parser = argparse.ArgumentParser(description='A simple process to search game titles on GiantBomb.com')
    parser.add_argument('--load', help='Load a corpus of game titles via a comma separated list of fully\
                                      qualified file paths instead of via the GiantBomb api')
    args = parser.parse_args()
    game_index = None
    if args.load:
        files = args.load.split(',')
        titles_from_files = []
        for i in files:
            a = open(i, 'r')
            titles_from_files += [{'name': i.strip(), 'platform': ''} for i in a.readlines()]
        game_index = GameInvertedIndex(titles_from_files)
        game_index.build_index()
    else:
        game_index = load_game_data()

    print
    print "All game data has now been loaded\n"
    choice = '1'
    while (choice != '0'):
        print "Please enter a number based on the Menu below: "
        print "0:  Exit the Program"
        print "1:  Search for a Game"
        print "2:  See all Game Titles"
        choice = raw_input().strip()
        if choice == '1':
            print "\nPlease enter the keywords, separated by spaces, you would like to search by:"
            query = raw_input().strip()

            game_titles = game_index.search(query)
            print "\nResults:"
            for i in game_titles:
                print '%s  (%s)' % (i['name'], i['platform'])
        elif choice == '2':
            for i in game_index.documents:
                print '%s  (%s)' % (i['name'], i['platform'])
            print "Total Games:  %s" % len(game_index.documents)
        elif choice == '0':
            pass
        else:
            print "I'm sorry, that's not an acceptable choice. Please enter either '0', '1' or '2'"
        print
    print "Thank you and Goodbye!"


if __name__ == '__main__':
    run_main()
