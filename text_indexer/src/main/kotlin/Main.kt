package vpokludova

import java.io.File
/**
 * The entry point of the application, which initializes the indexing process and subsequently
 * engages the user in a query-response loop until termination is requested.
 * <p>
 * This application facilitates the creation of an inverted index based on text files located within a specified directory.
 * Once the index is created, users can continuously submit queries to the system. The application leverages this index
 * to efficiently search through the files, returning files along with all corresponding line numbers where the query string
 * appears.
 * <p>
 * By default, the application uses a pre-configured directory path, but this can be overridden by supplying an alternative
 * path as a command-line argument.
 *
 * @param args command-line arguments, optionally include the path to the directory to be indexed.
 *             If no arguments are provided, a default directory path is used.
 */
fun main(args: Array<String>) {
    // Set the default directory path unless overridden by command line arguments
    var directoryPath = "src/main/resources/default_directory"

    // Check for a directory path provided as a command-line argument and use it if present
    if (args.isEmpty()){
        println("Using the default directory for indexing. To index a specific directory, " +
                "please provide its path as an argument.")
    } else {
        directoryPath = args[0]
    }

    val directory = File(directoryPath)

    // Verify the existence and directory status of the provided path
    if (!directory.exists() || !directory.isDirectory){
        println("The provided path does not exist or is not a directory.")
        return
    }

    // Initialize and run the application with the specified or default directory
    val app = Application(directory)
    app.run()
}