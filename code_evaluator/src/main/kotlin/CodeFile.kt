package vpokludova

import com.github.javaparser.StaticJavaParser
import com.github.javaparser.ast.CompilationUnit
import com.github.javaparser.ast.body.MethodDeclaration
import java.io.File

/**
 * Represents a file containing code that is to be analyzed for complexity and coding style.
 * It supports Java and Kotlin files and provides methods to find complex methods and check code style.
 *
 * @param file The file to be analyzed.
 */
class CodeFile (file : File) {
    /**
     * A list of methods extracted from the code file, represented as pairs of method names and their bodies.
     */
    private var methods: MutableList<Pair<String, String>> = mutableListOf()

    init {
        if (file.name.endsWith(".java")) {
            methods = getJavaMethods(file)
        } else if (file.name.endsWith(".kt")) {
            methods = getKotlinMethods(file)
        } else {
            println("The file ${file.name} is not a Java file, therefore can't be analyzed.")
        }
    }

    /**
     * Finds and prints the methods with the highest complexity in the file.
     * Complexity is determined based on the occurrence of certain keywords.
     */
    fun findComplexMethods() {
        // Define regex for splitting method body into relevant tokens
        val regex = "[\\s;{}()]".toRegex()

        // Initialize set of complexity counts and a mapping from complexity count to method(s)
        val counts : MutableSet<Int> = mutableSetOf()
        val countsMethodsMap: MutableMap<Int, MutableList<String>> = mutableMapOf()

        // Keywords whose occurrence in a method increase complexity
        val keywords = listOf("if", "while", "for", "switch", "return", "try", "catch", "finally", "continue", "break", "throw")

        // Calculate complexity score for each method/function
        for (method in methods) {
            val bodyTokens = method.second.split(regex).filter { it.isNotEmpty() }
            var count = 0

            for (token in bodyTokens) {
                if (token in keywords) {
                    count++
                }
            }

            counts.add(count)
            countsMethodsMap.getOrPut(count) { mutableListOf() }.add(method.first)
        }

        // Sort complexity score in decreasing order to then find the top 3 scores
        val counts1 = counts.toList().sortedDescending()
        var i = 0
        while (i < counts1.size && i < 3){
            val count = counts1[i]
            println("Methods/Functions with a complexity score $count are: ")
            val methodsWithHighestComplexity = countsMethodsMap[count]
            if (!methodsWithHighestComplexity.isNullOrEmpty()) {
                println(methodsWithHighestComplexity.joinToString(" "))
            } else {
                println("None")
            }
            i++
        }
        if (i < 3){
            println("There were only $i complexity scores, which is why only $i groups of methods were returned")
        }

    }

    /**
     * Checks and prints the percentage of method names that violate camelCase naming conventions.
     */
    fun checkCodeStyle() {
        // If methods list is empty, prematurely exit
        if (methods.isEmpty()){
            println("No functions/methods found therefore 0% of names violate camelCase conventions")
            return
        }

        // Count number of methods with syntactically incorrect names
        var countIncorrect = 0
        val strictCamelCaseRegex = """^[a-z]+(?:[A-Z][a-z0-9]*)*$""".toRegex()

        for (function in methods){
            val name = function.first

            if (!name.matches(strictCamelCaseRegex)){
                countIncorrect++
            }
        }

        // Calculate final percentage and print result
        val percentIncorrect = (countIncorrect * 1.0) / methods.size
        val percentFormatted = String.format("%.2f", percentIncorrect)
        println("$percentFormatted% of methods/functions have names which violate camelCase")

    }

    /**
     * Parses the Java file and extracts functions, storing them as pairs of names and bodies.
     *
     * @param file The Java file to be parsed.
     * @return A list of pairs representing the functions found in the file.
     */
    private fun getJavaMethods(file : File) : MutableList<Pair<String, String>> {
        // Read the code from the file
        val code = file.readText()

        val methods = mutableListOf<Pair<String,String>>()

        try {
            // Parse the code
            val cu: CompilationUnit = StaticJavaParser.parse(file)

            // Visit methods in the Java file
            cu.findAll(MethodDeclaration::class.java).forEach { method ->
                val methodName = method.name.toString()
                val methodBody = method.body.map { it.toString() }.orElse("")

                val pair = Pair(methodName, methodBody)

                methods.add(pair)
            }

            return methods

        } catch (e : Exception) {
            println("Failed to parse Java file.")
            println(e.message)
            return methods
        }
    }

    /**
     * Reads Kotlin source code from a file and extracts all methods as a list of name-body pairs.
     * @param file The Kotlin file to be parsed.
     * @return A mutable list of pairs, where each pair consists of a method name and its body.
     */
    private fun getKotlinMethods(file: File) : MutableList<Pair<String,String>> {
        val code = file.readText()
        val methodsList = mutableListOf<Pair<String,String>>()
        return extractKotlinMethods1(code, methodsList)
    }

    /**
     * Recursively extracts methods from the given string of code.
     * @param codeString The string containing Kotlin code.
     * @param methods1 A mutable list where extracted methods are added.
     * @return The list of methods extracted from the code.
     */
    private fun extractKotlinMethods1(codeString : String, methods1: MutableList<Pair<String,String>>) : MutableList<Pair<String,String>> {
        var index = 0
        var methods = methods1

        while (index < codeString.length) {
            val funIndex = findFunctionIndex(codeString, index)
            if (funIndex == -1) break // No more functions to process

            val firstOpenCurlyBrace = codeString.indexOf('{', funIndex)
            if (firstOpenCurlyBrace == -1) {
                println("Failed parse Kotlin file. Missing opening '{'.")
                return mutableListOf()
            }

            // Split the substring between function keyword and first curly brace into tokens to extract the function name
            val regex = "[\\s;{}()]".toRegex()
            val tokens = codeString.substring(funIndex + 4, firstOpenCurlyBrace).trim().split(regex).filter { it.isNotEmpty() }
            if (tokens.isEmpty()) {
                println("Failed to parse Kotlin file. Couldn't find method name.")
                return mutableListOf()
            }

            val methodName = tokens[0]
            var openBracesCount = 1 // Start counting braces from the first '{'
            val methodBody = StringBuilder("{")
            index = firstOpenCurlyBrace + 1

            while (index < codeString.length && openBracesCount > 0){
                val char = codeString[index]
                methodBody.append(char)
                when (char) {
                    '{' -> openBracesCount++
                    '}' -> openBracesCount--
                }
                index++
            }

            if (openBracesCount != 0) {
                println("Failed to parse Kotlin file. Unbalanced curly braces.")
                return mutableListOf()  // Early exit on failure
            }

            methods.add(Pair(methodName, methodBody.toString()))
            // Recursively process remaining method body code
            methods = extractKotlinMethods1(codeString.substring(firstOpenCurlyBrace, index), methods)
        }
        return methods
    }

    /**
     * Finds the index of the keyword "fun" that is used as a function declaration.
     * @param codeString The Kotlin source code.
     * @param startIndex The index to start the search from.
     * @return The index of "fun" keyword or -1 if not found.
     */
    private fun findFunctionIndex(codeString: String, startIndex: Int = 0): Int {
        val regex = """(?<=\s|^)fun(?=\s|\(|\{)""".toRegex() // Regex to locate 'fun' used as function declaration
        val matchResult = regex.find(codeString, startIndex)
        return matchResult?.range?.start ?: -1 // Return the start index of the match or -1 if not found
    }

}