# Text File Indexing and Query Application

## Contents
1. [Overview](#overview)
2. [Basic Approach Explanation](#basic-approach-explanation)
3. [How to Use](#how-to-use)
4. [Example Input and Output](#example-input-and-output)
5. [Improvements](#improvements)

## Overview

This application builds an inverted index from text files within a specified directory and allows users to query 
this index to find and display files that contain specific search terms along with the line numbers where these terms appear.

## Basic Approach Explanation
The application reads all text files from a given directory and processes each file to tokenize the text into words. 
Each word is indexed along with the file names where it appears. When a user enters a query, the application tokenizes 
this query and uses the inverted index to quickly find all documents containing the words in the query. It displays the 
results along with the line numbers of each occurrence.

## How to Use
1. Place all your text files in a directory.
2. Run the application and provide the path to that directory as an input argument. If no path is provided, a 
   default directory will be used.
3. The application will start and prompt you to enter search queries. Enter your queries when prompted and receive 
   results in real-time.
4. Enter "QUIT" when you would like to terminate the application.

## Example Input and Output

The following examples demonstrate interactions with the application using the default directory. You will see responses
to a variety of query types, including a (1) straightforward single-word query, a (2) query that is found on multiple lines, and a
(3) query involving a prefix match within the tokens of a file.

    Using the default directory for indexing. To index a specific directory, please provide its path as an argument.
    Text files indexed successfully.
    Starting application for text file querying... Welcome!
    Please enter a string query or 'QUIT' to terminate the application:
    they        // (1) straightforward single-word query
    Query string found in file: file2.txt
    Found on line 14.
    Found on line 15.
    Found on line 18.
    Query string found in file: file3.txt
    Found on line 9.
    Found again on line 9
    Found on line 11.
    Query string found in file: file5.txt
    Found on line 11.
    Please enter a string query or 'QUIT' to terminate the application:
    sun had     // (2) query that is found on multiple lines
    Query string found in file: file2.txt
    Found spanning between lines 5 and 6
    Please enter a string query or 'QUIT' to terminate the application:
    he d        // (3) Query where one of the tokens is a prefix of a token in the file
    Query string found in file: file2.txt
    Found on line 2.
    Found on line 6.
    Query string found in file: file3.txt
    Found on line 3.
    Found on line 7.
    Query string found in file: file4.txt
    Found on line 3.
    Found on line 5.
    Query string found in file: file5.txt
    Found on line 3.
    Found on line 5.
    Found on line 7.
    Found again on line 7
    Found again on line 7
    Found on line 9.
    Please enter a string query or 'QUIT' to terminate the application:
    QUIT
    Terminating application.

## Improvements

- **Case Sensitivity**: The first point is refined to directly state the current behavior (case-insensitive matching) 
  and suggests the potential for optional case-sensitive matching, explaining its usefulness clearly.

- **Advanced Text Analysis**: Depending on the specific requirements and the nature of the text files, this tool could 
  be enhanced with more sophisticated text analysis features. For English text files, integrating stemming and morphological 
  analysis could allow the application not only to find exact matches but also to support partial matches and perform 
  proximity queries, thereby broadening the scope and utility of the search functionality.
