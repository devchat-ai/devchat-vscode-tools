<?php

// 导入外部文件
require_once 'config.php';

// 使用use关键字导入命名空间
use MyProject\Utils;

// 定义全局变量
$g_var = 10;

function printMessage($message = '这是一个没有参数的函数') {
    echo $message . '<br>';
}

function square($num) {
    return $num * $num;
}

class Person {
    public $name;
    public $age;

    public function sayHello() {
        echo "大家好，我是{$this->name}，今年{$this->age}岁了。<br>";
    }
}

function printPerson(Person $person) {
    echo "姓名：{$person->name}，年龄：{$person->age}<br>";
}

// 定义局部变量
$local_var;
$local_str = '这是一个局部变量';

// 调用有参数的函数
printMessage('这是一个参数');

// 调用无参数的函数
printMessage();

// 使用mt_rand函数生成随机数
$random_num = mt_rand(1, 100);
echo "生成的随机数是：{$random_num}<br>";

// 使用readline函数读取用户输入
echo '请输入一个字符串：';
$input = trim(fgets(STDIN));
echo "您输入的字符串是：{$input}<br>";

// 计算字符串长度
$len = strlen($input);
echo "字符串长度是：{$len}<br>";

// 复制字符串
$copy = strcpy($input);
echo "复制后的字符串是：{$copy}<br>";

// 定义数组
$nums = [1, 2, 3];
echo '数组中的数据是：';
foreach ($nums as $num) {
    echo "{$num} ";
}
echo '<br>';

// 使用Utils类中的静态方法
Utils\ArrayUtils::reverse($nums);
echo '反转后的数组中的数据是：';
foreach ($nums as $num) {
    echo "{$num} ";
}
echo '<br>';

// 创建Person对象
$person = new Person();
$person->name = '张三';
$person->age = 20;

// 调用成员函数
$person->sayHello();

// 调用类函数
printPerson($person);
