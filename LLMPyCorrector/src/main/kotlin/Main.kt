package vpokludova

/**
 * The entry point for the Python Code Corrector Application.
 * This application uses the OpenAI API to help users correct errors in Python code.
 * It prompts the user for a Python file path, reads the file, and attempts to execute the Python code.
 * If errors are detected, it communicates with OpenAI's API to generate corrections until the code executes successfully.
 *
 * The application is initialized and run by creating an instance of the App class and invoking its runApplication method.
 */

fun main() {
    // Creates an instance of the App class
    val app = App()

    // Runs the main application logic, which handles user interactions and code correction processes
    app.runApplication()

}