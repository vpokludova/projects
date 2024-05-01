package vpokludova

import java.io.File

/**
 * Manages the operation of an application that creates and utilizes an inverted index
 * from text files within a specified directory to facilitate efficient query processing.
 * <p>
 * The Application class initializes by building an inverted index from the directory provided
 * and then enters a loop where it continuously accepts user queries until a termination request
 * is received.
 * <p>
 * Usage:
 * To start the application, create an instance with a valid directory and call the {@code run} method.
 */
class Application(directory: File) {

    /**
     * The inverted index created from the text files within the specified directory.
     */
    private var invertedIndex: InvertedIndex = InvertedIndex(directory)

    /**
     * Initializes the inverted index and checks if it contains any entries.
     * Outputs a message based on whether the index has entries.
     *
     * @param directory the directory from which text files are indexed
     */
    init {
        if (invertedIndex.isNotEmpty()) {
            println("Text files indexed successfully.")
        }
    }

    /**
     * Starts the main loop of the application, processing queries until termination.
     * If the inverted index is empty, the application will print a termination message and exit.
     */
    fun run() {
        var looping = invertedIndex.isNotEmpty()

        if (looping) {
            println("Starting application for text file querying... Welcome!")
        }
        else {
            println("Created inverted index is empty... terminating application.")
            return
        }

        while (looping) {
            looping = applicationLoop()
        }

        println("Terminating application.")
    }

    /**
     * Processes a single user query or handles the termination command.
     * Prompts the user to input a query or 'QUIT' to exit. If a valid query is received,
     * it is processed against the inverted index. If 'QUIT' is entered, the loop is terminated.
     *
     * @return {@code true} to continue the loop, {@code false} to terminate it
     */
    private fun applicationLoop() : Boolean {
        println("Please enter a string query or 'QUIT' to terminate the application: ")
        val query = readlnOrNull()  // Read user input

        if (query != null){
            if (query == "QUIT"){
                return false        // Exit the loop on 'QUIT'
            }

            invertedIndex.processQuery(query)       // Process the user query

        } else {
            println("No query entered.")
        }

        return true     // Continue the loop
    }
}