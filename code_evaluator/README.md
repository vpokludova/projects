# Code Evaluator

## Overview

The Kotlin Code Evaluator is a command-line application designed to analyze Kotlin and Java source files in a specified 
directory. The application evaluates the complexity of methods within the source files and checks if the method names 
adhere to camelCase naming conventions.

## Features 

- Analyze Kotlin and Java files for code complexity.
- Check for camelCase naming convention adherence in method names. 
- Report the groups of methods with the top 3 highest complexity scores. 
- Calculate the percentage of method names that do not follow camelCase.

## Usage 

The application can be run with the following command-line arguments:
- `-d <directory>`: Specify the path to the directory containing the source files to be evaluated. If omitted, the default directory 'src/main/resources/default_directory' will be used.

Once the application is running, follow the on-screen prompts to analyze specific files or to use default settings.

## Example Input and Output

This section illustrates a typical interaction with the Kotlin Code Evaluator when it is run with a specified directory containing Kotlin or Java files. The process demonstrates how users can input commands, and it displays the corresponding outputs based on the complexity analysis and style checking of the provided code files.

    Directory set to: src/main/resources/default_directory
    Please provide a filename. Enter 'default' to use the default Kotlin file or 'QUIT' to quit.
    default
    Methods/Functions with a complexity score 3 are:
    checkEvenNumber findMaxValue ProcessData
    Methods/Functions with a complexity score 1 are:
    calculateSum printNumberRange
    Methods/Functions with a complexity score 0 are:
    _invalidMethodName
    0.33% of methods/functions have names which violate camelCase
    Please provide a filename. Enter 'default' to use the default Kotlin file or 'QUIT' to quit.
    QUIT



## Technical Approach 

**Parsing Strategy**

The Kotlin Code Evaluator utilizes different strategies for parsing Java and Kotlin files to analyze code complexity and style adherence:

- **Java Files**: For Java, the application leverages the powerful `JavaParser library`, which provides robust parsing capabilities that can efficiently handle Java syntax and abstract syntax trees (AST). This library allows us to extract method declarations and bodies easily and accurately.
- **Kotlin Files**: Due to the lack of readily available and mature Kotlin parsing libraries, the project implements a custom parsing solution for Kotlin files. This parser is designed to identify functions by searching for the `fun` keyword and carefully managing nested structures such as blocks and expressions. It handles typical Kotlin function declarations, including those with default parameters, inline functions, and extension functions.

**Custom Kotlin Parser**

The custom Kotlin parser operates by:
- **Identifying function declarations**: It searches for the `fun` keyword that signifies the start of a function declaration. This is accomplished using regular expressions that account for possible leading spaces or line beginnings, ensuring that only actual function declarations are matched.
- **Extracting function bodies**: Once a function declaration is identified, the parser locates the corresponding opening and closing braces to extract the complete function body. This process involves counting nested braces to correctly identify the end of the function, even when multiple nested scopes are present.
- **Handling nested bodies**: The parser is recursive, allowing it to handle functions nested within other functions. Each discovered function is processed in the same manner, ensuring that all levels of nesting are evaluated.

**Complexity Calculation**

To assess the complexity of the methods, the evaluator counts the occurrences of specific keywords that typically increase the logical complexity of the code. These keywords include:

- Control flow statements: `if`, `else`, `while`, `for`, `switch`
- Exception handling: `try`, `catch`, `finally`
- Branching and looping: `continue`, `break`
- Other keywords that might affect flow: `return`, `throw`

Each occurrence of these keywords in a method increments its complexity score. After evaluating all methods, instead of selecting the top three methods with the highest complexity, the evaluator groups methods by their complexity scores. This approach ensures that all methods with high complexity are highlighted, even if more than three methods share the same top scores. This method of reporting provides a more comprehensive overview of potential areas within the code that might require refactoring or further inspection.


 