package vpokludova

import java.io.File

/**
 * Represents a code evaluator that checks the quality of code in a specified directory.
 * It allows running a series of evaluations on code files within the directory.
 *
 * @param directoryPath The path to the directory containing code files to be evaluated.
 */
class CodeEvaluator (directoryPath: File){

    /**
     * The directory where code files are located for evaluation
     */
    private val directory: File = directoryPath

    /**
     * Initiates the code evaluation process. It checks if the directory is not empty,
     * prompts the user for a filename, and processes the code evaluation loop
     */
    fun runCodeEvaluator() {
        // Check that directory is not empty
        if (directory.listFiles()!!.isEmpty()){
            println("Specified directory is empty.")
        }

        var looping = true

        while (looping){
            looping = codeEvalLoop()
        }

    }

    /**
     * Executes a loop that continuously prompts the user for a filename until the user
     * decides to quit. It handles the logic for a default file selection and error handling
     * for file access.
     * @return Boolean indicating whether to continue the loop or not
     */
    private fun codeEvalLoop() : Boolean {
        println("Please provide a filename. Enter 'default' to use the default Kotlin file or 'QUIT' to quit.")
        val filename = readlnOrNull()

        if (filename != null){
            if (filename == "QUIT"){
                return false    // Exit the loop on "QUIT"
            }

            // Initialize file object based on specified filename or default path
            var file: File? = null

            if (filename == "default"){
                // Use a predefined default file path
                file = File("src/main/resources/default_directory/KotlinFile1.kt")
            } else {
                // Construct the file object using the specified directory path and filename
                file = File(directory.path, filename)

                if (!file.exists()) {
                    println("Error while trying to open file: $filename")
                    return true     // Prematurely exit the loop iteration due to invalid file
                }
            }

            // Perform evaluation on specified file
            performFileEvaluation(file)

        }
        return true
    }

    /**
     * Evaluates the specified file for code complexity and style issues. It
     * utilizes the CodeFile class to perform the evaluation.
     */
    private fun performFileEvaluation(file: File) {
        val codeFile = CodeFile(file)
        codeFile.findComplexMethods()
        codeFile.checkCodeStyle()

    }

}