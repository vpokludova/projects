package vpokludova

import java.io.File
import java.io.IOException
import java.nio.file.Files

import io.ktor.client.*
import io.ktor.client.engine.cio.*
import io.ktor.client.request.*
import io.ktor.client.statement.*
import io.ktor.http.*
import io.ktor.util.*

import kotlinx.coroutines.runBlocking

import com.google.gson.Gson

/**
 * Main application class that interacts with OpenAI's API to correct Python code.
 * It manages the conversation with the LLM, handles file operations, and executes Python code to validate fixes.
 */
class App {
    /** API key for OpenAI service, fetched from environment variables. */
    private val apiKey = System.getenv("OPENAI_API_KEY")

    /** List to keep track of the conversation history with the LLM. */
    private var conversationHistory: MutableList<Message> = mutableListOf()

    /** Data class to represent a request to the OpenAI chat completions API. */
    data class CompletionRequest(
        val model: String,
        val messages: List<Message>
    )

    /** Data class to represent a message within the conversation with the LLM. */
    data class Message(
        val role: String,
        val content: String
    )

    /** Data class for parsing the JSON response from the OpenAI API. */
    data class ChatCompletion(
        val id: String,
        val `object`: String,
        val created: Long,
        val model: String,
        val choices: List<Choice>,
        val usage: Usage,
        val systemFingerprint: String
    )

    /** Data class to represent a choice provided by the OpenAI API within a ChatCompletion. */
    data class Choice(
        val index: Int,
        val message: Message,
        val logProbs: Any?,
        val finishReason: String
    )

    /** Data class to encapsulate usage information about the tokens used in a chat completion request. */
    data class Usage(
        val promptTokens: Int,
        val completionTokens: Int,
        val totalTokens: Int
    )

    /**
     * Entry point for running the application.
     * It prompts the user for a Python file path and processes the file to attempt to fix any errors in the code.
     */
    fun runApplication(){
        println("Welcome to the LLM based Python Corrector Application!")
        println("Please provide a Python filepath: ")

        val filepath = readlnOrNull().toString()
        val file = File(filepath)

        // Validate file existence and check for correct file extension
        if (!file.exists() || !file.name.endsWith(".py")) {
            println("Must provide a valid Python file")
        }

        val pythonCodeOriginal = file.readText()
        var pythonCode = pythonCodeOriginal

        // Initialize conversation with system role instruction
        conversationHistory.add(
            Message(role="system", content="You will be fixing faulty Python code. Return the ENTIRE fixed VERSION of the CODE as a simple string but NO explanatory or extra TEXT.")
        )

        // Loop to correct the Python code using the LLM until no errors are found
        while(true) {
            val result = executePythonCode(pythonCode)
            if (result.first) {
                println("\n Python code executed successfully!")
                break
            } else {
                println(" \n Error found, consulting LLM for fixes...")
                conversationHistory.add(
                    Message(role="user", content="The code: \n$pythonCode\nthrew the following errors: ${result.second}.")
                )
                pythonCode = consultOpenAI()        // Update the Python code based on the LLM's suggestion
            }
        }
    }

    /**
     * Executes Python code in a temporary file to test for errors.
     * This method allows the application to dynamically execute Python code
     * while safely handling the code execution in isolation using a temporary file.
     * This method is crucial for validating Python code fixes suggested by the LLM.
     *
     * @param pythonCode The Python code to be tested. This code is assumed to be a complete,
     *                   executable Python script.
     * @return A Pair<Boolean, String> where the Boolean indicates if the code executed without errors (true) or not (false),
     *         and the String contains the error message if there was a failure, or is empty if the execution was successful.
     */
    private fun executePythonCode(pythonCode: String) : Pair<Boolean, String> {
        // Create a temporary file
        val tempFilePath = Files.createTempFile(null, ".py")
        val tempFile = tempFilePath.toFile()

        // Write the provided Python code to the temporary file
        tempFile.writeText(pythonCode)

        // Ensure the temporary file is deleted when the program exits
        tempFile.deleteOnExit()

        try {
            // Use a ProcessBuilder to start a Python process that executes the code in the temporary file
            val process = ProcessBuilder("python", tempFile.absolutePath).start()

            // Get all errors generated during the execution
            val errors = process.errorStream.bufferedReader().readText()

            // If there are no errors, return true indicating successful execution
            if (errors.isEmpty()) return Pair(true, "")

            // If errors were captured, return false and the error message
            return Pair(false, errors)
        } catch (e: IOException) {
            // Handle IOExceptions by logging them and returning an error message
            e.printStackTrace()
            return Pair(false, e.message ?: "Unknown error")
        }
    }

    /**
     * Consults the OpenAI API to generate fixes for provided Python code. This method utilizes a maintained
     * conversation context to ensure the language model understands the continuity of the interaction, improving the accuracy
     * and relevance of suggestions.
     *
     * @return A string containing the corrected Python code. Returns an empty string if no corrections are provided or if an error occurs.
     */
    @OptIn(InternalAPI::class)
    private fun consultOpenAI(): String = runBlocking {
        // Initialize the HTTP client with CIO engine, suitable for backend applications
        val client = HttpClient(CIO) { }

        // Endpoint URL for the OpenAI's chat completions API
        val url = "https://api.openai.com/v1/chat/completions"

        // Package the ongoing conversation history into the request payload
        val request = CompletionRequest(
            model = "gpt-3.5-turbo",
            messages = conversationHistory.toList()
        )

        // Convert the request object into a JSON string using Gson
        val gson = Gson()
        val jsonData = gson.toJson(request)

        try {
            // Execute the POST request to OpenAI's API with headers specifying JSON content type and authorization
            val response: HttpResponse = client.post(url) {
                header(HttpHeaders.ContentType, "application/json")
                header(HttpHeaders.Authorization, "Bearer $apiKey")
                body = jsonData
            }

            // Parse the response body text to a ChatCompletion object to process the result
            val stringResult = response.bodyAsText()
            val resultObject = gson.fromJson(stringResult, ChatCompletion::class.java)

            // Check if the response includes any choices and return the first one's message content
            if (resultObject.choices.isNotEmpty()) {
                val messageContent = resultObject.choices.first().message.content
                println("LLM Suggestion: \n$messageContent")
                return@runBlocking messageContent
            } else {
                // Handle cases where no choices are provided by the model
                println("No choices available")
                return@runBlocking ""
            }

        } catch (e: Exception) {
            // Log any exceptions during the HTTP request or processing to aid in debugging
            e.printStackTrace()
            return@runBlocking ""
        } finally {
            // Ensure the HTTP client is closed after the request to free resources
            client.close()
        }
    }
}
