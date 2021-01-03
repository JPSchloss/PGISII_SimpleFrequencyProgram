# Jonathan Schlosser
# INLS 570
# Final Version of Project 1
# March 23, 2020

# The purpose of this program is to search the "grimms.txt" file for
#       - A single word's occurrence in a story.
#       - For the occurrences of any word ["word1 or word2 or... wordn"] in a story.
#       - For the co-occurrence of words within a story
#           - "word1 word2... wordn"
#           - "word1 and word2 and... wordn"]
#       - For the occurrence of a term more than a set value
#           - This can be a comparison to another term in that story
#               - Example: bird morethan owl
#           - Or to a specified value.
#               - Example: bird morethan 2

# Comments are included throughout to improve understanding and clarity.

#======== Beginning of Code ========#

# Importing needed packages.
import re
import string

# Defining a main function that controls the stopword generation, the working dictionary for the program,
# and the main query.
def main(filename):
    # Employing a function to process the stopwords.
    sw_list = process_stopwords('stopwords.txt')
    # Employing a function to process the file and generate the working dictionary.
    working_dict = process_file(filename, sw_list)

    print('\033[1m' + "Simple Word Frequency Program" + '\033[0m')

    print('\nThis program helps identify terms in the grimms.txt file. You can enter one search term, \n'
          'multiple terms, use and "or" term, or use an "and" term. This will help find single word \n'
          'occurrences, multiple word occurrences, and any word occurrences. You can also use the term \n'
          '"morethan" to identify texts where one term appears more than another. To quit the program \n'
          'enter the term "qquit" \n\n')

    # Running the main search functionality of the program.
    run_query(working_dict)


# Function to load in the stopwords and process them into an iterable form.
def process_stopwords(stopwordfilename):
    sw_file = open(stopwordfilename, "r")
    sw_list = []
    for sw_line in sw_file:
        sw_line = sw_line.strip(string.punctuation + string.whitespace)
        sw_line = sw_line.lower()
        sw_list.append(sw_line)
    sw_file.close()
    return sw_list

# Function to process the main file and create the working dictionary.
def process_file(filename, sw_list):
    # Creating an empty dictionary.
    working_dict = {}
    # Initiating a line count.
    line_count = 0
    # Opening the text file.
    text_file = open(filename, "r")
    # Initializing a title variable.
    title = ""
    # Iterating through the file, counting to line 124.
    for line in text_file:
        line_count += 1
        if 124 < line_count < 9209:
            # Cleaning up each line.
            line = line.replace('-', ' ')
            line = line.strip()
            # Identifying if the line is in all capitals - indicating a title.
            match = re.search(r'^[A-Z][A-Z ]+$', line)
            if match:
                # Setting the title.
                title = line
            else:
                # Calling a function to process the words.
                words = process_words(line)
                for word in words:
                    # Checking if the word is a stopword.
                    if word not in sw_list:
                        # Loading up the dict of dict of list for the working dictionary.
                        working_dict.setdefault(word, {}).setdefault(title, []).append((line_count, line))
    # Closing the text file.
    text_file.close()
    # Returning the working dictionary.
    return working_dict


# Function to process the words.
def process_words(line):
    # Initializing a list for the words.
    words = []
    # Splitting the line.
    for word in line.split():
        # Cleaning up the words.
        word = word.strip(string.punctuation + string.whitespace)
        word = word.lower()
        # Appending the word to the words list.
        words.append(word)
    # Returning the words.
    return words


# Main function aka search work-horse.
def run_query(working_dict):
    # Initializing a while loop control variable. When this is no longer true, the process will finish.
    qquit = None
    while qquit is None:
        # Requesting a query from the user.
        query = input("Please enter your query: ")

        # Identifying the type of request in the query.
        or_match = re.search("\\bor\\b", query)
        and_match = re.search("\\band\\b", query)
        morethan_match = re.search("\\b morethan \\b", query)
        qquit = re.search("\\bqquit\\b", query)
        multiple_match = re.search("\\b \\b", query)

        # Using a function to get a clean list of words to search for.
        words = process_query(query)

        # Depending on the search type identified in the query, one of these conditions will be met,
        # and the appropriate search function will be called.
        if or_match is not None:
            or_match_search(words, working_dict)

        elif and_match is not None:
            all_words_search(words, working_dict)

        elif morethan_match is not None:
            morethan_search(words, working_dict)

        elif multiple_match is not None:
            all_words_search(words, working_dict)

        # If the search is blank, this notice will inform the user and the loop will restart.
        elif words == []:
            print("\t \t \t - The entry was blank. -  \n"
                  "\t \t \t - Please try again. -")

        # This notifies the user that the program has quit, ends the loop,
        # and results in the program being finished.
        elif qquit is not None:
            print("\t \t \t - The program has been terminated. -  \n")
            continue

        # The last condition is true if all others are not met. In this case, if the query is a single word.
        else:
            single_word_search(words, working_dict)


# This function processes the query, returns a cleaned up list of words,
# and removes the search operators ("or", "and", "morethan")
def process_query(query):
    words = []
    for word in query.split():
        word = word.strip(string.punctuation + string.whitespace)
        word = word.lower()
        words.append(word)
    while "or" in words:
        words.remove("or")
    while "and" in words:
        words.remove("and")
    while "morethan" in words:
        words.remove("morethan")
    return words


# This function works to identify all the titles associated with the search words.
def identify_all_titles(words, working_dict):
    titles = []
    for word in words:
        try:
            for title in working_dict[word].keys():
                if title not in titles:
                    titles.append(title)
        except KeyError:
            print("\t \t \t - One of your entries was not included in the set. -  \n"
                  "\t \t \t - Please try again. -")
    return titles


# This function works to change the presentation of the search terms in the results.
# It works to display the word as **WORD** in the search results.
def process_result_line(tmp_line, word):
    new_word = '**' + word.upper() + '**'
    tmp_line = tmp_line.replace(word.upper(), new_word)
    tmp_line = tmp_line.replace(word.capitalize(), new_word)
    tmp_line = tmp_line.replace(word, new_word)
    return tmp_line


# This function works to find the search and to present the results.
# If the search does not have a result, "--" is displayed.
def search_method(title, word, working_dict):
    if word in working_dict:
        if title in working_dict[word]:
            try:
                for line in working_dict[word][title]:
                    result_line = process_result_line(line[1], word)
                    print("\t \t \t", line[0], result_line)
            except KeyError:
                print("\t \t \t --")
        else:
            print("\t \t \t --")
    else:
        print("\t \t \t --")


# This function is called for an "or" condition.
def or_match_search(words, working_dict):
    # Identifies all the titles for all the words.
    titles = identify_all_titles(words, working_dict)
    # For the titles, it conducts a search and displays the results.
    for title in titles:
        print(title)
        for word in words:
            print("\t \t", word, sep="")
            search_method(title, word, working_dict)


# This is a function that identifies titles where all the words appear.
# If one of the words is not included, it will display an error message to the user.
def identify_only_titles(words, working_dict):
    titles = []
    duplicated_titles = []
    for word in words:
        try:
            for title in working_dict[word].keys():
                if title not in titles:
                    titles.append(title)
                else:
                    if title not in duplicated_titles:
                        duplicated_titles.append(title)
                        titles.append(title)
                    else:
                        continue
        except KeyError:
            print("\t \t \t - One of your entries was not included in the set. -  \n"
                  "\t \t \t - Please try again. -")
            continue
    return duplicated_titles


# This is the function for the "and" search and the multiple word search.
def all_words_search(words, working_dict):
    # Calls a function to identify only titles shared by the search terms.
    titles = identify_only_titles(words, working_dict)
    unique_titles = []

    for title in titles:
        try:
            if all(title in working_dict[word] for word in words):
                if title not in unique_titles:
                    unique_titles.append(title)
        except KeyError:
            continue

    # For each of the shared titles, it searches for the terms within those titles.
    for title in unique_titles:
        print(title)
        for word in words:
            print("\t \t", word, sep="")
            search_method(title, word, working_dict)


# This function is called to search for a single word within each title.
def single_word_search(words, working_dict):
    titles = identify_all_titles(words, working_dict)
    for title in titles:
        print(title)
        for word in words:
            print("\t \t", word, sep="")
            search_method(title, word, working_dict)


# This function controls the morethan search functionality in the program.
def morethan_search(words, working_dict):
    # Here it is identifying all the titles.
    titles = identify_all_titles(words, working_dict)

    # Looking to see if the second term is a word or a number.
    word_1 = words[0]
    word_2 = words[1]
    num_match = re.search("\\d+", word_2)

    # If it is a word, the function finds the number of word occurrences for each story
    # and presents the conditions where the first term is more than the second term.
    if num_match is None:
        for title in titles:
            try:
                if len(working_dict[word_1].get(title, "")) > len(working_dict[word_2].get(title, "")):
                    print(title)
                    for word in words:
                        print("\t \t", word, sep="")
                        search_method(title, word, working_dict)
                else:
                    continue
            except KeyError:
                continue

    # If it is a number, the function finds the number of word occurrences for each story
    # and presents the conditions where the first term is more than the number.
    else:
        for title in titles:
            try:
                if len(working_dict[word_1].get(title, "")) > int(word_2):
                    print(title)
                    print("\t \t", word_1, sep="")
                    search_method(title, word_1, working_dict)
                else:
                    continue
            except KeyError:
                continue


# This is the main function call.
main("grimms.txt")

