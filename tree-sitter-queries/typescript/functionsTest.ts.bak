function greeter(person: string) {
  return "Hello, " + person;
}

function foo<T>(x: T): T {

}

function foo<T, U>(a: T[], f: (x: T) => U): U[] {

}

function foo<T, U>(this: T[]): U[] {
  return []
}

function foo<const T, const U extends string>(x: T, y: U) {

}

function* foo<A>(amount, interestRate, duration): number {
	yield amount * interestRate * duration / 12
}

class A extends B {
    constructor(x: number, y: number) {
        super(x);
    }
    public toString() {
        return super.toString() + " y=" + this.y;
    }
}