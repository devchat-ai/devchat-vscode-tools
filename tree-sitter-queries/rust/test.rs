// 导入标准库中的io模块
use std::io;

// 导入第三方库中的rand模块
extern crate rand;
use rand::Rng;

// 全局变量
static GLOBAL_VAR: i32 = 10;

fn main() {
    // 局部变量（未赋值）
    let mut local_var: i32;

    // 局部变量（已赋值）
    let local_str = "这是一个局部变量";

    // 调用有参数的函数
    print_message("这是一个参数");

    // 调用无参数的函数
    print_message();

    // 使用rand模块生成随机数
    let mut rng = rand::thread_rng();
    let random_num = rng.gen_range(1, 101);
    println!("生成的随机数是：{}", random_num);

    // 使用io模块读取用户输入
    println!("请输入一个数字：");
    let mut input = String::new();
    io::stdin().read_line(&mut input).expect("读取用户输入失败");
    let num: i32 = input.trim().parse().expect("转换成数字失败");
    println!("您输入的数字是：{}", num);
}

// 有参数的函数
fn print_message(message: &str) {
    println!("{}", message);
}

// 无参数的函数
fn print_message() {
    println!("这是一个没有参数的函数");
}

// 有返回值的函数
fn square(num: i32) -> i32 {
    num * num
}

// 结构体定义
struct Person {
    name: String,
    age: i32,
}

// 结构体实现方法
impl Person {
    fn say_hello(&self) {
        println!("大家好，我是{}，今年{}岁了。", self.name, self.age);
    }
}
