package vpokludova;

import java.util.List;
import java.util.Map;

public class DefaultKotlinFile {
    public int calculateSum(int a, int b) {
        return a + b;
    }

    public boolean checkEvenNumber(int number) {
        return number % 2 == 0;
    }

    public void printNumberRange(int max) {
        for (int i = 1; i <= max; i++) {
            System.out.println(i);
        }
    }

    public int findMaxValue(List<Integer> numbers) {
        int max = Integer.MIN_VALUE;
        for (int number : numbers) {
            if (number > max) {
                max = number;
            }
        }
        return max;
    }

    public int processData(Map<String, Integer> data) {
        int result = 0;
        for (Map.Entry<String, Integer> entry : data.entrySet()) {
            String key = entry.getKey();
            int value = entry.getValue();
            if (key.startsWith("data")) {
                result += value;
            }
        }
        return result;
    }

    public void InvalidMethodName() {
        System.out.println("This is an improperly named method according to camelCase.");
    }
}
