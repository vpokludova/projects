package vpokludova

import kotlinx.cli.*
import java.io.File

/**
 * This is the entry point for the command-line code evaluator application.
 * It parses the command-line arguments and sets up the environment for code evaluation.
 */
fun main(args: Array<String>) {
    // Create an instance of ArgParser
    val parser = ArgParser("code_evaluator")

    // Define a directory option with a default value
    val directory by parser.option(ArgType.String, shortName = "d", description = "Path to the directory")
        .default("src/main/resources/default_directory")

    // Parse command-line arguments
    parser.parse(args)

    // Check that provided or default directory path is valid
    val directoryFile = File(directory)
    if(!directoryFile.exists() || !directoryFile.isDirectory){
        println("Invalid directory.")
        return
    }

    println("Directory set to: $directory")

    // Instantiate and run codeEvaluator
    val codeEvaluator = CodeEvaluator(directoryFile)
    codeEvaluator.runCodeEvaluator()

}
