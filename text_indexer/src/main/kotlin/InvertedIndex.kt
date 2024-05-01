package vpokludova

import java.io.File

/**
 * Represents an inverted index for quick text retrieval. This class provides functionality to create an inverted index from
 * text files within a given directory and to process queries against this index.
 * <p>
 * An inverted index maps each unique word found in any document to the set of documents in which that word appears.
 * This allows for efficient querying of text data.
 */
class InvertedIndex (directory: File) {

    /**
     * Stores the inverted index where each key is a token and each value is a set of filenames (documents) where the token appears.
     */
    private var index: MutableMap<String, MutableSet<String>> = mutableMapOf()

    /**
     * The directory from which the text files are indexed.
     */
    private var directory: File

    /**
     * Initializes the InvertedIndex by creating the index from the specified directory.
     *
     * @param directory The directory containing the text files to be indexed.
     */
    init {
        this.index = createInvertedIndex(directory)
        this.directory = directory
    }

    /**
     * Checks if the index is not empty.
     *
     * @return {@code true} if the index contains one or more entries, {@code false} otherwise.
     */
    fun isNotEmpty(): Boolean {
        return index.isNotEmpty()
    }

    /**
     * Processes a user query against the inverted index and displays the results.
     * This method tokenizes the input query, searches for documents containing all tokens,
     * and manages query extensions by checking token prefixes and suffixes. It then evaluates
     * each document to find specific line numbers where the query appears.
     *
     * The search involves the following steps:
     * 1. Tokenization of the query based on whitespace and punctuation.
     * 2. For each token:
     *    - Retrieve and merge document lists for tokens that exactly match, are a suffix, or a prefix,
     *      depending on the token's position in the query.
     *    - Intersect these document lists to find common documents across all tokens.
     * 3. For each document, read through the lines to find exact matches or continuation of the query across lines.
     * 4. Print the file names and line numbers where the query or parts of it are found.
     *
     * If no documents contain the query, the process exits early.
     *
     * @param query The string query to process, which can include multiple words and punctuation.
     */
    fun processQuery(query: String) {
        // tokenize string
        val regex = "[\\s\\p{Punct}]+".toRegex()
        val tokens = query.split(regex).filter {it.isNotEmpty()}

        var postingsIntersection: MutableSet<String> = mutableSetOf()

        // Get the set of documents containing all tokens (or prefix / suffix if relevant) of query
        for (token in tokens) {
            // Add all postings for the entire token
            val tokenPostings = index[token.lowercase()] ?: mutableSetOf()

            // Extend postings with suffix or prefix matches if applicable
            if (tokens.indexOf(token) == 0){
                for (key in index.keys){
                    if (key.endsWith(token.lowercase())){
                        for (fileId in index[key]!!){
                            tokenPostings.add(fileId)
                        }
                    }
                }
            }

            if (tokens.indexOf(token) == tokens.size - 1) {
                for (key in index.keys) {
                    if (key.startsWith(token.lowercase())){
                        for (fileId in index[key]!!){
                            tokenPostings.add(fileId)
                        }
                    }
                }
            }

            if (tokenPostings.isNotEmpty()){
                if (postingsIntersection.isEmpty()) {
                    postingsIntersection = tokenPostings
                } else {
                    postingsIntersection.retainAll(tokenPostings)
                    if (postingsIntersection.isEmpty()) break // Early exit if no common documents are found
                }
            } else {
                postingsIntersection = mutableSetOf()
                break // No documents found for this token, clear postings
            }
        }

        // Process each document to find exact line matches
        postingsIntersection.let { validFiles ->
            if (validFiles.isNotEmpty()) {
                validFiles.forEach { fileName ->
                    val file = File(directory, fileName)
                    var results = mutableListOf<Pair<Int, Pair<Int, Int>>>()
                    var subquery = ""
                    var resultPair: Pair<MutableList<Pair<Int, Pair<Int, Int>>>, String>

                    // Read file lines, looking for full query matches
                    file.useLines { lines ->
                        lines.forEachIndexed { index, line ->
                            val lineNum = index + 1
                            val currentLine = line.trim().lowercase()

                            // Previous line found prefix of query, try to find remaining part
                            if (subquery.isNotEmpty()){
                                resultPair = findQuery(results, currentLine, lineNum, subquery, true)
                                results = resultPair.first
                                subquery = resultPair.second
                            }

                            // Look for entire query string
                            resultPair = findQuery(results, currentLine, lineNum, query, false)
                            results = resultPair.first
                            subquery = resultPair.second
                        }
                    }

                    // Display results for the current file
                    if (results.isNotEmpty()){
                        println("Query string found in file: $fileName")
                    }

                    for (pair in results){
                        val occurrence = pair.first
                        val range = pair.second
                        if (range.first == range.second){
                            if (occurrence == 0) {
                                println("Found on line ${range.first}.")
                            } else {
                                println("Found again on line ${range.first}")
                            }
                        } else {
                            println("Found spanning between lines ${range.first} and ${range.second}")
                        }
                    }
                }
            }
        }
    }

    /**
     * Processes the search for a query within a single line of text, adjusting for possible continuation
     * in subsequent lines if the query does not fully match in the current line. This method is capable
     * of complex query processing, managing both complete and partial matches across multiple lines.
     *
     * @param results A mutable list of query results being accumulated. Each result includes an occurrence count
     *                and a pair indicating the range of lines where matches were found.
     * @param currentLine The text of the current line being examined.
     * @param lineIndex The index of the current line, used for tracking match locations.
     * @param query The query string being searched, which can be a complete query or a subquery continuing
     *              from the previous line.
     * @param isSubquery A boolean flag indicating whether the current processing involves a subquery,
     *                   i.e., a continuation from the end of the previous line.
     * @return A pair consisting of the updated results list and a potential remaining subquery string.
     *         The subquery string is used for continuing the search on the next line if the current line
     *         ends with a prefix of the query that could not be completely matched.
     */
    private fun findQuery(results: MutableList<Pair<Int, Pair<Int, Int>>>,
                          currentLine: String,
                          lineIndex: Int,
                          query: String, isSubquery: Boolean
    ): Pair<MutableList<Pair<Int, Pair<Int, Int>>>, String>{
        // Return immediately if the current line is empty
        if (currentLine.isEmpty())
            return Pair(results, "")

        // Handle non-subquery scenario: search for the query directly within the current line
        if (!isSubquery) {
            // Locate the first occurrence of the query within the current line
            val index = currentLine.indexOf(query)

            if (index != -1) {
                // Query found completely within the line, create a range marking this line
                val lineRange = Pair(lineIndex, lineIndex)
                val queryMatchesOnLine = results.filter { it.second == lineRange }
                val queryResultMax = queryMatchesOnLine.maxByOrNull { it.first }
                var queryCountLineIndex = 0

                if (queryResultMax != null) {
                    queryCountLineIndex = queryResultMax.first + 1
                }

                // Add the found query occurrence to the results
                results.add(Pair(queryCountLineIndex, lineRange))
                // Continue searching for the query in the remainder of the line if there's more to process
                val newCurrentLine = currentLine.substring(index + query.length)
                return findQuery(results, newCurrentLine, lineIndex, query, isSubquery)

            } else {
                // If the query was not found and the line could potentially hold the start of the query, check for overlap
                val overlap = queryLineOverlap(currentLine, query)
                if (overlap.isNotEmpty()) {
                    // The current line ends with a portion of the query; set up for continuation in the next line
                    results.add(Pair(0, Pair(lineIndex, -1)))
                    val subquery = query.substring(overlap.length).trim()
                    return Pair(results, subquery)
                }
            }
        } else {
            // Handle subquery that continues from a previous line
            if (query.length < currentLine.length && currentLine.startsWith(query)) {
                // The current line starts with the continuation of the subquery; find and update the corresponding result
                val result = results.find { it.second.second == -1 }
                var results1 = mutableListOf<Pair<Int, Pair<Int, Int>>>()

                if (result != null){
                    results1 = results.map {
                        if (it == result) {
                            it.first to (it.second.first to lineIndex)
                        } else {
                            it
                        }
                    }.toMutableList()
                }

                return Pair(results1, "")

            } else if(query.length >= currentLine.length && query.startsWith(currentLine)) {
                // The current line starts the query but may need further continuation
                val subquery = query.substring(currentLine.length)
                return Pair(results, subquery)

            } else {
                // No match found or the query does not continue appropriately; remove partial result from results
                val resultIndex = results.indexOfLast {it.second.second == -1}

                if (resultIndex != -1) {
                    results.removeAt(resultIndex)
                }

                return Pair(results, "")
            }
        }
        // Default return in case all conditions fail
        return Pair(results, "")
    }

    /**
     * Analyzes overlap between the end of a line and the beginning of a query. This method checks if any prefix of the
     * query matches a suffix of the line. If such a match is found, it returns the overlapped part of the query.
     *
     * The method splits both the line and the query into tokens and compares segments of these tokens to find
     * the maximum overlap. If an overlap is found, it calculates the length of this overlap from the start of the
     * query string and returns the substring.
     *
     * @param line The line of text to compare against the query.
     * @param query The query string whose prefixes are checked against the suffixes of the line.
     * @return A substring of the query that overlaps with the end of the line. Returns an empty string if no overlap is found.
     */
    private fun queryLineOverlap(line: String, query: String) : String {
        val regex = "\\s+".toRegex()
        val queryTokens = query.split(regex).filter {it.isNotEmpty()}
        val lineTokens = line.split(regex).filter {it.isNotEmpty()}

        var i = queryTokens.size - 1

        while (i > 0 && i <= lineTokens.size){
            val queryTokens1 = queryTokens.take(i)
            val lineTokens1 = lineTokens.takeLast(i)

            if (queryTokens1 == lineTokens1){
                val lastSubQueryToken = queryTokens1.last()
                val lastTokenOccurrences = queryTokens1.count { it == lastSubQueryToken }
                val queryEndIndex = indexOfNth(query, lastSubQueryToken, lastTokenOccurrences) + lastSubQueryToken.length
                return query.substring(0, queryEndIndex)
            }

            i++
        }
        return ""
    }

    /**
     * Finds the index of the nth occurrence of a substring in a given string. If the nth occurrence does not exist,
     * the method returns -1.
     *
     * This method iterates through the given string, searching for the substring and counting its occurrences until
     * it reaches the desired count (nth occurrence). The search continues from the end of the last found occurrence
     * to handle overlapping cases effectively.
     *
     * @param str The string in which to search for the substring.
     * @param substring The substring to search for within the main string.
     * @param n The occurrence number to find (e.g., 1st, 2nd, 3rd occurrence).
     * @return The index position of the start of the nth occurrence of the substring within the string, or -1 if
     *         the nth occurrence does not exist.
     */
    private fun indexOfNth(str: String, substring: String, n: Int): Int {
        var count = 0
        var index = str.indexOf(substring)
        while (index != -1) {
            count++
            if (count == n) {
                return index
            }
            index = str.indexOf(substring, index + substring.length)
        }
        return -1
    }

    /**
     * Creates the inverted index from all text files within the specified directory.
     *
     * @param directory The directory from which to load text files.
     * @return A mutable map representing the inverted index.
     */
    private fun createInvertedIndex(directory: File): MutableMap<String, MutableSet<String>> {
        val textFiles = directory.listFiles { file -> file.extension == "txt"}

        // check that the directory contains at least one text file
        if (textFiles == null || textFiles.isEmpty()) {
            println("No text files found in ${directory.absolutePath}")
            return index
        }

        textFiles.forEach { file ->
            // tokenize file contents
            val fileContent = file.readText(Charsets.UTF_8)
            // Split on whitespace and punctuations, but not within words
            val regex = "[\\s\\p{Punct}]+".toRegex()
            val tokens = fileContent.split(regex).filter {it.isNotEmpty()}

            // update inverted index using tokens from file
            tokens.forEach { token ->
                val normalizedToken = token.lowercase()

                if (normalizedToken in index){
                    // get existing postings for normalized token
                    val postingsSet = index[normalizedToken]!!

                    // add current file to the postings set
                    postingsSet.add(file.name)
                } else {
                    index[normalizedToken] = mutableSetOf(file.name)
                }
            }
        }
        return index
    }
}