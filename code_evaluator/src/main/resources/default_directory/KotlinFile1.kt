package vpokludova

class KotlinFile1 {
    fun calculateSum(a: Int, b: Int): Int {
        return a + b
    }

    fun checkEvenNumber(number: Int): Boolean {
        if (number % 2 == 0) {
            return true
        }
        return false
    }

    fun printNumberRange(max: Int) {
        for (i in 1..max) {
            println(i)
        }
    }

    fun findMaxValue(numbers: List<Int>): Int {
        var max = Int.MIN_VALUE
        for (number in numbers) {
            if (number > max) {
                max = number
            }
        }
        return max
    }

    fun ProcessData(data: Map<String, Int>): Int {
        var result = 0
        for ((key, value) in data) {
            if (key.startsWith("data")) {
                result += value
            }
        }
        return result
    }

    fun _invalidMethodName() {
        println("This is an improperly named method according to camelCase.")
    }
}