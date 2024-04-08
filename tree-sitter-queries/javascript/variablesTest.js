import myDefaultFunction from './myModule';
import { myNamedFunction } from './myModule';
import { myNamedFunction, myNamedVariable } from './myModule';
import * as myModule from './myModule';
const myModule = await import('./myModule');

class Person {
  constructor(name, age) {
    this.name = name;
    this.age = age;
  }

  introduce() {
    console.log(`Hi, my name is ${this.name} and I am ${this.age} years old.`);
  }

  static sayHello() {
    console.log('Hello, world!');
  }
}

const person = new Person('Alice', 25);
person.introduce();
Person.sayHello(); 