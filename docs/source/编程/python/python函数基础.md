# python函数基础

## 1.函数的定义

在python中 ，函数是一个组织好的 ，可以重复使用的代码块 ，函数可以提高代码的重复利用率。

函数的特性：

1. 函数可以没有参数
2. 函数的参数可以是一个，也可以是多个
3. 当你使用def 定义了一个函数后，只有调用这个函数才能让这个函数运行
4. return的作用是退出函数并返回函数的返回值，任何时候，只要执行了return语句就一定会退出函数
5. 函数没有使用return语句，但仍然会有返回值，这种情况下，函数默认返回None
6. 函数一次返回多个结果时，是以元组的形式返回的

## 2.函数参数

python函数的参数可以分为位置参数，默认参数，关键字参数，可变参数，函数可以没有参数，也可以有多个参数，参数是传递给函数的命名变量。

- 形参和实参
  所谓形参，就是函数定义中的参数，形参在函数体内可以使用，而实参，则出现在调用过程中
- 必传参数(位置参数)
- 默认参数
  定义函数是时，如果有多个默认参数，他们必须放置在参数列表的最后，不允许在中间放置一个必传参数。
- 关键字参数
  关键字参数不是一个出现在函数定义时的概念，而是一个出现在函数调用时的概念。
  关键字参数允许你以任何顺序传递参数，只要必传参数都以key=value的形式传值即可
- 可变参数
  可变参数分为两种：

1. *args 接受任意多个实际参数
   所有传入的参数将被放入到一个元组中，因此args的类型是tuple元组
2. **kwargs接收任意多个以关键字参数赋值的实际参数
   在调用函数时，以关键字参数的形式进行参数传递，最终这些key-value对将组装成字典，kwargs的类型是dict。

## 3.函数名称

函数名称其实是一个变量名，def表示将保存在某块内存区域中的函数代码体赋值给函数名变量。

## 4.函数返回值

python的函数支持返回多个值。返回多个值时，默认以tuple的方式返回

## 5.函数作用域

作用域（scope）是指程序中变量的可见性和生命周期范围。
Python 中的作用域可以分为以下几类：

- 局部作用域（Local Scope）
- 嵌套作用域（Enclosing Scope）
- 全局作用域（Global Scope）
- 内置作用域（Built-in Scope）
  这些作用域遵循一个称为 LEGB（Local, Enclosing, Global, Built-in）的规则来解析标识符。

1. 局部作用域（Local Scope）
   局部作用域是指在函数内部定义的变量和参数，它们只在函数内部可见和生效。当函数执行完毕后，局部变量会被销毁。
2. 嵌套作用域（Enclosing Scope）
   嵌套作用域指的是嵌套函数（一个函数内部定义的另一个函数）中的变量。内层函数可以访问外层函数的局部变量，但不能修改它们，除非使用 nonlocal 关键字。

```python
def outer_function():
    outer_var = 20  # 外层函数的局部变量

    def inner_function():
        print(outer_var)  # 内层函数可以访问外层函数的变量

    inner_function()

outer_function()  # 输出: 20
```

如果需要在内层函数中修改外层函数的变量，可以使用 nonlocal 关键字：

```python
def outer_function() -> None:
    outer_var = 20  # 外层函数的局部变量

    def inner_function() -> None:
        nonlocal outer_var
        outer_var = 80
        print(outer_var)  # 内层函数可以访问外层函数的变量

    inner_function()
    print(outer_var)


outer_function()  # 输出: 80
```

3. 全局作用域（Global Scope）
   全局作用域指的是在模块级别定义的变量，它们在整个模块中都可以访问。全局变量在模块的生命周期内一直存在。

```python
global_var = 50  # 全局变量

def my_function():
    print(global_var)  # 函数内部可以访问全局变量

my_function()  # 输出: 50
print(global_var)  # 输出: 50
```

如果需要在函数内部修改全局变量，可以使用 global 关键字：

4. 内置作用域（Built-in Scope）
   内置作用域是 Python 语言内置的一些标识符和函数，这些标识符在所有作用域中都可以访问。它们由 Python 内置模块（如 builtins 模块）提供。
   LEGB 规则
   Python 解析变量名时，按照 LEGB 规则依次查找：

- Local（局部作用域）：首先在当前函数内部查找。
- Enclosing（嵌套作用域）：然后在外层函数的作用域中查找。
- Global（全局作用域）：再然后在模块的全局作用域中查找。
- Built-in（内置作用域）：最后在内置作用域中查找。

如果在所有这些作用域中都找不到变量名，就会抛出 NameError 异常。

```python
global_var = 'global'

def outer_function():
    outer_var = 'outer'

    def inner_function():
        inner_var = 'inner'
        print(inner_var)  # 内部局部作用域
        print(outer_var)  # 外层局部作用域
        print(global_var)  # 全局作用域
        print(len)  # 内置作用域

    inner_function()

outer_function()
```

## 6.函数类型

### 6.1 内置函数

[内置函数](https://docs.python.org/zh-cn/3/library/functions.html)

### 6.2 匿名函数

匿名函数是指没有名称的函数，任何编程语言中，匿名函数都扮演着重要角色，它的功能非常灵活，但是匿名函数中的逻辑一般很简单，否则直接使用命名函数更好，匿名函数常用于回调函数、闭包等等。

```python
lambda argl, arg2,... argN :expression statement
```

匿名函数的返回值是冒号后面的表达式计算得到的结果

### 6.3 嵌套函数

函数内部可以嵌套函数。一般来说，在函数嵌套时，内层函数会作为外层函数的返回值(当然，并非必须)。既然内层函数要作为返回值，这个嵌套的内层函数更可能会是lambda匿名函数

### 6.4 闭包函数

闭包（Closure）是指在一个函数内部定义的另一个函数，这个内部函数引用了外部函数的变量，并且外部函数返回了这个内部函数。这使得内部函数在外部函数执行完毕后，仍然能够访问和使用外部函数的变量。闭包是一个强大的编程工具，能够使得函数具有记忆功能和更高的抽象能力。
闭包包含以下几个要素：

1. 一个外部函数，它定义了一些局部变量。
2. 一个内部函数，它引用了外部函数的局部变量。
3. 外部函数返回内部函数，使得内部函数能够在外部函数执行完毕后继续使用外部函数的变量。

```python
def outer_function(x):
    def inner_function(y):
        return x + y
    return inner_function

closure = outer_function(10)
print(closure(5))  # 输出: 15
print(closure(20))  # 输出: 30
```

闭包的应用场景

- 数据隐藏：闭包可以用来隐藏数据，只暴露接口。
- 工厂函数：闭包可以用来创建带有特定参数的函数。
- 回调函数：闭包可以携带状态信息，用于回调函数中。

```python
# 数据隐藏
def make_counter():
    count = 0

    def counter():
        nonlocal count
        count += 1
        return count

    return counter

counter_a = make_counter()
print(counter_a())  # 输出: 1
print(counter_a())  # 输出: 2

counter_b = make_counter()
print(counter_b())  # 输出: 1
# 工厂函数
def power_factory(exponent):
    def power(base):
        return base ** exponent
    return power

square = power_factory(2)
print(square(3))  # 输出: 9

cube = power_factory(3)
print(cube(2))  # 输出: 8
```

闭包的优势
状态保持：闭包可以保持函数执行时的状态，使得函数在多次调用时能够维持状态。
代码简洁：闭包可以简化代码，避免使用全局变量和类。
提高抽象层次：闭包可以创建高阶函数，提升代码的抽象层次和可读性。
闭包的注意事项
变量生命周期：闭包依赖于外部函数的变量，这些变量在外部函数执行完毕后仍然存在。
内存使用：由于闭包会持有外部函数的变量，可能会导致内存占用增加，需要注意内存管理

### 6.5 回调函数

有一家旅馆提供叫醒服务，但是要求旅客自己决定叫醒的方法。可以是打客房电话，也可以是派服务员去敲门，睡得死怕耽误事的，还可以要求往自己头上浇盆水。这里，“叫醒”这个行为是旅馆提供的，相当于库函数，但是叫醒的方式是由旅客决定并告诉旅馆的，也就是回调函数。而旅客告诉旅馆怎么叫醒自己的动作，也就是把回调函数传入库函数的动作，称为登记回调函数（to register a callback function）
回调函数的定义
回调函数是指在某个操作完成后被调用的函数。通常，回调函数用于异步编程、事件处理、以及将逻辑解耦以提高代码的可维护性。
回调函数的应用场景
事件处理：在 GUI 或 Web 应用中，回调函数用于处理用户交互事件（如点击按钮）。
异步编程：在处理异步操作（如网络请求或定时器）时，回调函数用于处理操作完成后的结果。
策略模式：在设计模式中，回调函数用于实现策略模式，允许在运行时选择不同的算法。

## 7.函数属性
### 7.1 属性分析
python中的函数是一种对象，它有属于对象的属性。除此之外，函数还可以自定义自己的属性。注意，属性是和对象相关的，和作用域无关。

```python
import dis
from typing import Callable
x = 3
def f(a: int, b: int, *args: complex, c: int) -> Callable[[int], int]:
    a = 3
    y = 10
    print(a, b, c, x, y)

    def g(z: int) -> int:
        return a + b + c + x + z

    return g
# f()的show_code结果
dis.show_code(f)

# f()的co_XXX属性
for i in dir(f.__code__):
    if i.startswith("co"):
        print(i+":",eval("f.__code__."+i))

# 闭包函数，注意，传递了*args参数
f1=f(3,4,"arg1","arg2",c=5)

# f1()的show_code结果
dis.show_code(f1)

# f1()的co_XXX属性
for i in dir(f1.__code__):
    if i.startswith("co"):
        print(i+":",eval("f1.__code__."+i))
```
- co_name 函数的名称
- co_filename 函数定义在哪个文件名中
- co_firstlineno 函数声明语句在文件中的第几行。即def关键字所在的行号
- co_consts 该函数中使用的常量有哪些。python中并没有专门的常量概念，所有字面意义的数据都是常量
- co_kwonlyargcount keyword-only的参数个数
- co_argcount 除去*args之外的变量总数。实际上是除去*和\**所收集的参数以及keyword-only类的参数之后剩余的参数个数。换句话说，是*或**前面的位置参数个数。
- co_nlocals 本地变量个数
- co_varnames 本地变量名称,变量名称收集在元组中
- co_stacksize 本段函数需要在栈空间评估的记录个数。换句话说，就是栈空间个数。
- co_names 函数中保存的名称符号，一般除了本地变量外，其它需要查找的变量(如其它文件中的函数名，全局变量等)都需要保存起来
- co_cellvars co_freevars 这两个属性和嵌套函数(或者闭包有关)，它们是互相对应的，所以内容完全相同，它们以元组形式存在
- co_cellvars  是外层函数的哪些本地变量被内层函数所引用
- co_freevars  是内层函数引用了哪些外层函数的本地变量

### 7.2 属性和字节码对象PyCodeObject
对于python，通常都认为它是一种解释型语言。但实际上它在进行解释之前，会先进行编译，会将python源代码编译成python的字节码(bytecode)，然后在python virtual machine(PVM)中运行这段字节码，就像Java一样。但是PVM相比JVM而言，要更"高级"一些，这个高级的意思和高级语言的意思一样：离物理机(处理机器码)的距离更远，或者说要更加抽象。
源代码被python编译器编译的结果会保存在内存中一个名为PyCodeObject的对象中，当需要运行时，python解释器开始将其放进PVM中解释执行，执行完毕后解释器会"根据需要"将这个编译的结果对象持久化到二进制文件*.pyc中。下次如果再执行，将首先从文件中加载(如果存在的话)。
所谓"根据需要"是指该py文件是否只运行一次，如果不是，则写入pyc文件。至少，对于那些模块文件，都会生成pyc二进制文件。另外，使用compileall模块，可以强制让py文件编译后生成pyc文件。
但需要注意，pyc虽然是字节码文件，但并不意味着比py文件执行效率更高，它们是一样的，都是一行行地读取、解释、执行。pyc唯一比py快的地方在导入，因为它无需编译的过程，而是直接从文件中加载对象。
py文件中的每一个代码块(code block)都有一个属于自己的PyCodeObject对象。每个代码块除了被编译得到的字节码数据，还包含这个代码块中的常量、变量、栈空间等内容，也就是前面解释的各种co_XXX属性信息。
pyc文件包含3部分：
- 4字节的Magic int，表示pyc的版本信息
- 4字节的int，是pyc的产生时间，如果与py文件修改时间不同，则会重新生成
- PycodeObject对象序列化的内容

## 8.函数冻结
在functools模块中有一个工具partial()，可以用来"冻结"一个函数的参数，并返回"冻结"参数后的新函数。
```python
functools.partial(func, *args, **keywords)
```
partial()返回的其实是一个partial对象，这个对象包含了3个特殊的属性：

- func表示该对象所封装的原始函数
- args表示"冻结"的位置参数列表
- keywords表示"冻结"的关键字参数
另外需要注意的是，partial()不会保留封装函数的元数据，比如注释文档、注解等。

## 9.函数装饰器
### 9.1 基础
1. 谁可以作为装饰器(可以将谁编写成装饰器)：
- 函数
- 方法
- 实现了__call__的可调用类
2. 装饰器可以去装饰谁(谁可以被装饰)：
- 函数
- 方法
- 类
### 9.2 定义
```python
@funcA
def funcB():...

def funcB():...
funcB = funcA(funcB)
```
也就是说，将函数funcB作为函数funcA的参数，funcA会重新返回另一个可调用的对象(比如函数)并赋值给funcB。
所以，funcA要想作为函数装饰器，需要接收函数作为参数，并且返回另一个可调用对象(如函数)。
函数可以同时被多个装饰器装饰，后面的装饰器以前面的装饰器处理结果为基础进行处理：
装饰器函数可以用来扩展、增强另外一个函数。实际上，内置函数中staticmethod()、classmethod()和property()都是装饰器函数，可以用来装饰其它函数。

## 10.代码块

python 程序是由代码块构建的。块是作为一个单元执行的一段 Python 程序文本。

常见代码块的类型:

1. 模块文件是一个代码块
2. 函数体是一个代码块
3. class的定义是一个代码块
4. 交互式(python idle)的每一个命令行都是一个独立的代码块
5. 脚本文件是一个代码块
6. 脚本命令是一个代码块(python -c "xxx")
7. eval()和exec()中的内容也都有各自的代码块

代码块的作用是组织代码，同时意味着退出代码区块范围就退出了作用域范围.
同一个代码块内，虽然仍然是读一行解释一行，但在退出这个代码块之前，不会忘记这个代码块中的内容，而且会统筹安排这个代码块

## 11.思考

```python
x = 3
def f1():
    print(x)
    x=4
f1()
```

当执行到def语句的时候，因为def声明函数，函数体是一个代码块，所以按照代码块的方式读取属于这个代码块中的内容。首先读取print(x)，但并不会直接解释，而是会记住它，并继续向下读取，于是读取x=4，这意味着x是一个本地变量。然后统筹安排整个代码块，将print(x)的x认为是本地变量而非全局变量。注意，直到def退出的时候都还没有进行x的赋值，而是记录了本地变量x，赋值操作是在函数调用的时候进行的。当调用函数f()的时候，发现print(x)中的x是本地变量，但因为还没有赋值，所以报错.

```python
def f1():
    for i in range(5):
        def n():
            print(i)
    return n
f1()()

def f1():
    L = []
    for i in range(5):
        def n(i=i):
            print(i)
        L.append(n)
    return L
```
