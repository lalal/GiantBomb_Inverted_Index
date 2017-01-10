# GiantBomb_Inverted_Index

---

## Background

GiantBomb API
---
http://www.giantbomb.com/api/

This code challenge uses python2.7 as a command line tool which can be invoked by the following command(s):
```
cd src
python main.py
```
---
## Code Description

The code is broken up into 3 main modules

1.  main.py
  * Responsible for running the actual program.  It first pulls the data from the Giant Bomb API, builds an inverted index on it and then presents the user with a menu from which they can choose to search, quit or see a listing of all the games and their corresponding platforms.  Threading is used to pull for the 3 platforms.
  
2.  PlatformDataRetriever.py
  * This class performs the retrieval of data for a given platform.  It uses threads to expedite the process of making concurrent calls to the api.  An initial api call is made to get the total number of games which is then used to figure out how many batches of api calls to make.  Batch size is set to 100 (based on Giant Bomb's limit).  The total number of batches are also used to initialize a 'results' list where each index in the result represents of the batched data for that thread.
  
3.  GameInvertedIndex.py
  * This class stores all the game data returned by the api, builds an index on it and allows that index to be searched.  It assumes the document data is formatted in a certain way and if that format is not met, a runtime error is raised.
  
---
## Algorithm Design

The algorithmic approach to resolving this code challenge was to use an inverted index.  For each game title, the individual words were first tokenized (ie, split by space ' '), normalized (ie, removed certain punctuation and lower-cased), and then added to a hash map.  The values of the hashmap were represented as a set containing the indices of the game titles taken from an arraylist of all the game titles.  

The reason for using a set was because it ensures uniqueness of the indices, ie, no duplicates or repetitions, and when making compound queries it is relatively easy and efficient to find the intersection of the sets to return the game titles which contained all the keywords.  

Given the relatively small size of the game titles, this was relatively easy to fit all into memory.  However, if there was a need to scale this out, one might potentially have to think of more sophisticated ways of storing and accessing the data provided it can't all fit into memory.  

Some possible solutions, assuming memory is left at a constant, might be to order the data and then partition it with different chunks being stored to disk and loaded into memory as needed.  Thus, depending on the kind of query being made, one can dynamically pull data into memory as needed.

---
## Error Handling

The general approach was to capture and raise major exceptions as runtime errors.  Error handling is captured around the api calls, missing data returned via the api and/or missing/incorrect data while building the index.

---
## Unit Tests

Unit tests are captured in the 'test' directory and are focused around the two major classes, ie, PlatformDataRetriever and GameInvertedIndex.  Each function is unit tested and, in the case of the api, calls to the API are made.  Generally speaking, the unit tests for the API could be improved without having to invoke the API potentially through some dependency injection or mock api factory method.  That way, some of the error conditions could also be adequately tested to make sure they are handled properly.  

The test cases for both modules are consolidated into a single file 'test.py' and can be invoked by the running the 'run_test.sh' script while in the 'test' directory.  The script will automagically set the relative python path so that the modules are in scope. Below are the commands one would need to invoke in order to run all the tests:
```
cd test
./run_test.sh
```
