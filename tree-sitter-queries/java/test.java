// 单独导入一个类
import java.util.Scanner;

// 导入整个包
import java.text.*;

// 使用静态导入
import static java.lang.Math.*;

public class Example {
    // 全局变量（未赋值）
    private static int globalVar;

    // 全局变量（已赋值）
    private static String globalStr = "这是一个全局变量";

    public static void main(String[] args) {
        // 局部变量（未赋值）
        int localVar;

        // 局部变量（已赋值）
        String localStr = "这是一个局部变量";

        // 调用有参数的函数
        printMessage("这是一个参数");

        // 调用无参数的函数
        printMessage();

        // 使用Scanner类读取用户输入
        Scanner scanner = new Scanner(System.in);
        System.out.print("请输入一个数字：");
        int num = scanner.nextInt();

        // 调用有返回值的函数
        int result = square(num);
        System.out.println("该数字的平方是：" + result);
    }

    // 有参数的函数
    public static void printMessage(String message, int msg2 = 20) {
        System.out.println(message);
    }

    // 无参数的函数
    public static void printMessage() {
        System.out.println("这是一个没有参数的函数");
    }

    // 有返回值的函数
    public static int square(int num) {
        return num * num;
    }

    // 使用静态导入的函数
    public static double calculateDistance(double x1, double y1, double x2, double y2) {
        double dx = x2 - x1;
        double dy = y2 - y1;
        return sqrt(dx * dx + dy * dy);
    }
}
