# Countdown Word Solver
A basic python cli tool that will solve the letters games in the classic game show countdown.

The basic idea is you pass it a list of characters and the tool will find all the words hidden in that list of letters.

## Basic Usage
Make sure that `countdown.py` is executable by running `chmod +x countdown.py`

Then the basic usage of the tool is this:
```
./countdown.py <letters> [--word_list=<path_to_wordlist>] [--min=<word_length>]
```

Example:
```
./countdown.py asieduekp
```
Note that the letters are passed with no spaces. If you would like to use spaces, ensure you use quotes around the letters like so:
```
./countdown.py 'a s i e d u e k p'
```

### Optional Args
1. **Word List**

The word list argument is simply the path to the words list file (words.txt in this repo or any other file that contains a list of words). This is what will be used to find real english words, therefore the better this list is the better the results of the tool will be.
```
./countdown.py asieduekp --word_list=words.txt
```
Once you have run this once, it will create an anagram_dict file in the directory which it will use if you don't provide a `word_list` argument.

2. **Min Word Length To Include**

The final arg is the `--min` arg. This are is simply the minimum word length that should be calulated. For example, if you run the tool with the following args:
```
./countdown.py asieduekp --min=7
```
Then the tool will not even try to find words shorter than 7 letters. This options defaults to 5.
