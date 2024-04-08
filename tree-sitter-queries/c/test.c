#include <stdio.h>  // 导入标准库中的输入输出模块
#include <stdlib.h>  // 导入标准库中的随机数模块
#include <string.h>  // 导入标准库中的字符串模块

// 全局变量
int g_var, g_var3 = 10;
int g_var2, g_var4;

int main() {
    // 局部变量（未赋值）
    int local_var;

    // 局部变量（已赋值）
    char *local_str = "这是一个局部变量";

    // 调用有参数的函数
    print_message("这是一个参数");

    // 调用无参数的函数
    print_message();

    // 使用rand函数生成随机数
    srand(time(NULL));
    int random_num = rand() % 100 + 1;
    printf("生成的随机数是：%d\n", random_num);

    // 使用gets函数读取用户输入
    printf("请输入一个字符串：");
    char input[100];
    gets(input);
    printf("您输入的字符串是：%s\n", input);

    // 使用strlen函数计算字符串长度
    int len = strlen(input);
    printf("字符串长度是：%d\n", len);

    // 使用strcpy函数复制字符串
    char copy[100];
    strcpy(copy, input);
    printf("复制后的字符串是：%s\n", copy);
}

// 有参数的函数
void print_message(char *message) {
    printf("%s\n", message);
}

// 无参数的函数
void print_message() {
    printf("这是一个没有参数的函数\n");
}

// 有返回值的函数
int square(int num, int num2[], int* num3) {
    return num * num;
}

// 结构体定义
struct Person {
    char name[20];
    int age;
};

// 结构体实现函数
void say_hello(struct Person *person) {
    printf("大家好，我是%s，今年%d岁了。\n", person->name, person->age);
}
