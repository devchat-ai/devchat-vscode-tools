package main

import (
    "fmt"
    "math"

    "github.com/go-ego/riot/riotcore"
)

// 全局变量（未赋值）
var globalVar int

// 全局变量（已赋值）
var globalStr = "这是一个全局变量"

func main() {
    // 局部变量（未赋值）
    var localVar int

    // 局部变量（已赋值）
    localStr := "这是一个局部变量"

    // 调用有参数的函数
    printMessage("这是一个参数")

    // 调用无参数的函数
    printMessage()

    // 使用math包中的Sqrt函数计算平方根
    num := 4.0
    result := math.Sqrt(num)
    fmt.Printf("该数字的平方根是：%.2f\n", result)

    // 使用riotcore包中的NewClient函数创建一个HTTP客户端
    client := riotcore.NewClient()
    resp, err := client.Get("https://www.baidu.com")
    if err != nil {
        fmt.Println("请求失败：", err)
        return
    }
    defer resp.Body.Close()
    body, err := ioutil.ReadAll(resp.Body)
    if err != nil {
        fmt.Println("读取响应体失败：", err)
        return
    }
    fmt.Println(string(body))
}

// 有参数的函数
func printMessage(message string) {
    fmt.Println(message)
}

// 无参数的函数
func printMessage() {
    fmt.Println("这是一个没有参数的函数")
}

// 有返回值的函数
func square(num int, num2 int) int {
    return num * num
}

// 结构体定义
type Person struct {
    Name string
    Age  int
}

// 结构体方法
func (p Person) sayHello() {
    fmt.Printf("大家好，我是%s，今年%d岁了。\n", p.Name, p.Age)
}
