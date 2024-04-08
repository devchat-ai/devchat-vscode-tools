using System;  // 导入系统命名空间
using static System.Console;  // 导入Console类的静态成员
using System.Collections.Generic;  // 导入泛型集合命名空间

namespace Example  // 定义命名空间
{
    class Program  // 定义程序入口类
    {
        static int g_var, g_va2 = 10;  // 定义全局变量

        static void Main(string[] args)  // 定义主函数
        {
            int local_var;  // 定义未赋值的局部变量

            string local_str = "这是一个局部变量";  // 定义已赋值的局部变量

            PrintMessage("这是一个参数");  // 调用有参数的函数

            PrintMessage();  // 调用无参数的函数

            int random_num = new Random().Next(1, 101);  // 使用Random类生成随机数
            WriteLine($"生成的随机数是：{random_num}");

            Write("请输入一个字符串：");
            string input = ReadLine();  // 使用Console类读取用户输入
            WriteLine($"您输入的字符串是：{input}");

            int len = input.Length;  // 计算字符串长度
            WriteLine($"字符串长度是：{len}");

            string copy = input.Clone() as string;  // 复制字符串
            WriteLine($"复制后的字符串是：{copy}");

            List<int> nums = new List<int>() { 1, 2, 3 };  // 定义泛型列表
            WriteLine("泛型列表中的数据是：");
            foreach (int num in nums)  // 遍历泛型列表
            {
                Write($"{num} ");
            }
            WriteLine();
        }

        static void PrintMessage(string message = "这是一个没有参数的函数")  // 定义有默认参数值的函数
        {
            WriteLine(message);
        }

        static int Square(int num)  // 定义有返回值的函数
        {
            return num * num;
        }

        class Person  // 定义类
        {
            public string Name { get; set; }  // 定义属性
            public int Age { get; set; }  // 定义属性

            public void SayHello()  // 定义成员函数
            {
                WriteLine($"大家好，我是{Name}，今年{Age}岁了。");
            }
        }

        static void PrintPerson(Person person)  // 定义类函数
        {
            WriteLine($"姓名：{person.Name}，年龄：{person.Age}");
        }
    }
}
