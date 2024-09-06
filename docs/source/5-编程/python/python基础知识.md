# python基础知识
## 解释器执行流程
Python 解释器的工作流程可以分为几个阶段，每个阶段中 PVM 都起着重要作用：
1. 源代码编译为字节码：当 Python 解释器读取 .py 文件时，首先会通过编译器模块将 Python 源代码编译为字节码（这是一种中间语言，存储在 .pyc 文件中）。
2. 字节码解释执行：接下来，PVM 会从字节码中逐条读取指令，并执行这些指令。PVM 是解释字节码的核心，它依赖于栈操作和各种指令集来完成程序的逻辑。
3. 运行时支持：在执行过程中，Python 解释器的其他部分会协助 PVM 完成内存管理、垃圾回收、I/O 操作、模块加载等任务。
## 特点
动态类型：在Python中，变量在定义时不需要指定类型。Python在运行时根据变量的值自动推断类型。
尽管Python是动态类型语言，但它也是强类型语言。这意味着变量的类型不会被自动强制转换。
在Python中，变量只是引用对象的名称，实际的类型信息是存储在对象中的，而不是变量本身。
虽然Python作为高级语言在逻辑层面屏蔽了许多底层细节，但在 Python 解释器执行字节码时，依然需要依赖操作系统的内存分段布局。解释器会根据操作系统的内存管理机制在不同的内存段中创建和管理所需的内存资源。
## 与ELF文件的关系
尽管编写 Python 脚本时不直接处理 ELF 文件格式，但在 Python 的运行过程中，ELF 文件会间接发挥作用。以下是一些 Python 如何与 ELF 文件关联的情况：
- Python 解释器本身是一个 ELF 文件
在 Linux 系统上，Python 解释器（如 /usr/bin/python3）本身是一个 ELF 可执行文件。当你运行一个 Python 脚本时，实际上是通过操作系统加载并执行这个 ELF 文件，然后由该解释器来解释和运行 Python 代码。可以通过 file 命令查看 Python 解释器是否为 ELF 文件，
- 动态链接的共享库（Shared Libraries）
Python 解释器在运行时会依赖许多共享库（如标准 C 库 libc.so、数学库 libm.so 等），这些共享库在 Linux 系统上也是以 ELF 文件的形式存在的。
当 Python 执行时，这些 ELF 格式的共享库被动态加载并链接到 Python 解释器进程中，提供各种底层功能支持。
- 扩展模块：
Python 支持使用 C、C++ 等编写的扩展模块（如 .so 文件），这些模块通常也被编译为 ELF 格式的共享库。
Python 解释器本身、使用的共享库以及通过 C 扩展编写的模块都可能是 ELF 格式的文件。
## 变量
在程序设计中，变量是一种存储数据的载体。计算机中的变量实际是存储器中存储数据的一块内存空间，变量的值可以被读取和修改，这是所有计算和控制的基础。
python中的变量仅仅只是用来保存一个数据对象的地址。无论是什么数据对象，在内存中创建好数据对象之后，都只是把它的地址保存到变量名中。所以变量名是类型无关的，但它指向的值是类型相关的，可以是数值、字符串、列表、函数、类、对象等等。这些内存对象中都至少包含3部分：对象类型、对象的引用计数(用来判断改对象是否可被垃圾回收器回收)、对象的值。
python中的变量命名时只能包含数字、大小写字母、下划线这三种类型的字符，并且数字不能是首字符。
还有一些有特殊意义的变量命名方式
1. 单个下划线 _
   通常用作一个临时的占位符或者无关重要的变量名，表示一个不需要使用的值
2. 单个前导下划线 _var
   表示这个变量或者方法是“私有的”，不应该被直接访问。虽然 Python 并不会严格限制对这些变量的访问，但是开发者通常将它们视为内部实现的一部分，而不是公共 API 的一部分。
3. 单个后续下划线 var_
   通常用于避免与 Python 关键字或者内置函数命名冲突，或者避免与同名的 Python 标准库模块冲突。
4. 双前导下划线 __var（name mangling）
   在类定义中，双下划线开头的变量名会进行名称修饰（name mangling），Python 会在变量名前面加上 _ClassName 来防止子类中的命名冲突。
   例如，在类 A 中，__var 变量会被重命名为 _A__var，这样子类 B 中的同名变量不会与其冲突。
5. 双前后下划线 \__var__
   这种命名方式通常被 Python 保留用于特殊用途，例如魔术方法（magic methods）或者特殊变量，如 \__init__、\__repr__ 等。
   约定俗成的命名方式
6. 常量以全大写字符表示
7. 普通变量、函数名、方法名都以小写字母开头命名
8. 模块名、包名以全小写字母命名
9. 类名以大写字母开头
   python中变量赋值的几种形式。

```python
x = "long"                  # (1).基本形式
x, y = "long", "shuai"      # (2).元组对应赋值
[x, y] = ["long", "shuai"]  # (3).列表对应赋值
a, b, c, d = "long"         # (4).序列赋值
a, *b = 'long'              # (5).解包赋值
a = b = "long"              # (6).多目标赋值
a += 3                      # (7).二元赋值表达式
((a, b), c) = ('lo','ng')   # (8).嵌套赋值序列
```

在 Python 中，序列（sequence）是一种有序的数据结构，它包含了一系列的元素，每个元素都有一个唯一的索引。
python赋值时，总是先计算"="右边的结果，然后将结果按照赋值方式赋值给"="左边的变量
当使用一个*前缀变量的时候，表示将序列中对应的元素全部收集到一个列表中(注意，总是一个列表)，这个列表名为*开头的那个变量名。*号可以出现在任意位置处，只要赋值的时候能前后对应位置关系即可。不管如何，收集的结果总是列表，只不过可能是空列表或者只有一个元素的列表。
解包返回的一定是列表，但序列切片返回的内容则取决于序列的类型。
在python中的某些情况下，这种二元赋值表达式可能比普通的赋值方式效率更高些。原因有二：
1. 二元赋值表达式中，a可能会是一个表达式，它只需计算评估一次，而a = a + 3中，a要计算两次。
2. 对于可变对象，可以直接在原处修改得到修改后的值，而普通的一元赋值表达式必须在内存中新创建一个修改后的数据对象，并赋值给变量

```python
L = [1,2,3]
L = L + [4]     # (1)：慢
L += [4]        # (2)：快
L.append(4)     # (3)：快，等价于(2)

L = L + [5,6]   # (4)：慢
L += [5,6]      # (5)：快
L.extend([5,6]) # (6)：快，等价于(5)
```

按照理论上来说，确实二元赋值方式要效率高一些，但要注意的是，列表中保存的只是各元素的引用，所以拷贝列表也仅仅只是拷贝一点引用，这是微乎其微的开销。所以一元赋值和二元赋值的差距在这一点的性能上基本没差距，主要的差距还在于一元、二元赋值方式可能存在的表达式不同评估次数。
使用二元赋值表达式通常可以作为可变对象赋值的一种优化手段

## 基本数据类型

python中总共分为6种基本的数据类型

1. 不可变类型
   又叫静态数据类型，没有增删改操作，包括数字(number)、字符串(string)、元组(tuple)
2. 可变类型
   又叫动态数据类型，支持增删改操作，包括列表(list)、字典(dict)、集合(set)
   数字类型还可分为:整数(int)、浮点数(float)、复数(complex)、布尔(bool)
   字符串必须使用''或""括起来，对于特殊字符可以使用反斜杠\进行转义，用+拼接多个字符串， 用*复制字符串，字符串还支持索引截取(又叫切片)
   列表是一组可重复且有序的数据集合，任何类型的数据都可以存到列表中，会根据需要动态分配和回收内存，是Python中使用最频繁的数据类型，列表同样也支持索引截取(又叫切片)，列表中的元素是可变的，能够进行增删改操作
   元组也是一组可重复且有序的对象集合，任何类型的数据都可以存到元组中，但是元组中的元素是不可变的，元组同样也支持索引截取(又叫切片)
   字典是一组可变的无序的对象集合，字典中的元素是通过键(Key) : 值(Value)来保存的，一组键值对称为一个元素，其中键(Key)不可重复，必须唯一，而值(Value)是可重复的，字典会浪费较大内存，是一种使用空间换时间的数据类型
   集合是一组可变的、无序的且不可重复的元素序列，可以理解为是没有Key值得字典，基本功能是测试元素之间的关系和删除重复元素，比如：共同好友、你可能认识的人、关注TA的人还关注了…等
   注意点：
3. python 3.x中的整数不区分一般整数和长整型整数，3.x版本中的整数支持无穷精度
4. 任何时候浮点数都是不精确的。当带有小数点或科学计数的标记符号e或E，就表示这是浮点数

- 当浮点数参与表达式的运算时，会以浮点数的规则进行运算，也就是整数会转换成浮点数类型
- python中的浮点数精度和C语言的双精度浮点数精度相同

3. 整数除了十进制整数外，还可以写成二进制、八进制、十六进制甚至是其它进制的整数

- 当一个整数以0b或0B开头，其后都是0、1时，默认识别为二进制整数
- 当一个整数以0o或0O开头(数值零和大、小写的字母o)，其后都是0-7之间的数值时，默认识别为8进制整数
- 当一个整数以0x或0X开始，其后都是[0-9a-fA-F]之间的字符时，默认识别为十六进制

## 语句和表达式

表达式用于计算值，而语句用于执行操作。
语句是一组代码，它执行一些操作，但不会返回一个值。语句通常用于控制程序的流程，比如赋值、条件分支、循环等。
表达式是一段代码，它计算出一个值。这个值可以是数字、字符串、布尔值，也可以是任何其他数据类型。

## 运算符

Python 语言支持以下类型的运算符:

- 算术运算符
- 比较（关系）运算符
- 赋值运算符
- 逻辑运算符
- 位运算符
- 成员运算符
- 身份运算符
- 运算符优先级

### 数值基本运算

支持最基本的数学运算符号：+ - * / % **、取正负+x -x，地板除法//，除法和取模divmod(x, y):
注意事项：

1. python中的除法运算/得到的结果总是浮点数(例如9/3=3.0)，后面还有一种地板除法(floor)不一样
2. 当数值部分有小数时，会自动转换为浮点数类型进行运算，而且会自动忽略参与运算的小数尾部的0
3. 加号+和乘号*也能处理字符串

- +可以连接字符串，例如"abc" + "def"得到abcdef
- *可以重复字符串次数，例如"a"*3得到"aaa"，"ab"*3得到"ababab"

### 其它数学运算方法

```python
# 几个python的内置数学函数
pow():求幂，如pow(2,3)=8
abs():求绝对值，如abs(-3)=3
round():四舍五入，如round(3.5)=4
int():取整(截去小数部分)，如int(3.5)=3
float():转换成浮点数，如float(3)=3.0
oct():十进制整数转换成八进制
hex():十进制整数转换成十六进制整数
bin():十进制整数转换成二进制
...等等
```

还有专门的数学模块math、取随机数的模块random等。

### 浮点数

由于硬件的原因，使得计算机对于浮点数的处理总是不精确的。
例如，按照数学运算时，1.1-0.9=0.2，但实际得到的结果为：

```python
>>> 1.1-0.9
0.20000000000000007
```

它以高精度的极限趋近的值来显示。上面的趋近结果大于按照数学运算结果，但并不总是如此，例如下面的运算则是小于数学运算的结果：

```python
>>> 3.3-3.2
0.09999999999999964
```

由于浮点数不精确，所以尽量不要对两个浮点数数进行等值==和不等值!=比较.如果非要比较，应该通过它们的减法求绝对值，再与一个足够小(不会影响结果)的值做不等比较。

```python
>>> (3.2-2.8) == 0.4
False

>>> abs((3.2-2.8)-0.4) < 0.0002
True
```

最后，浮点数并非总是输出很长精度的值。正如前面的运算：
浮点数有两个特殊方法，一个是is_integer()，用来测试这个浮点数是否是整数，另一个是as_integer_ratio()，可以将浮点数转换成分子分母组成的元组，不过这个方法并非总是如你所想的那样友好。例如:

```python
>>> (3.0).is_integer()
True
>>> (3.2).is_integer()
False

>>> (2.5).as_integer_ratio()
(5, 2)
>>> (2.6).as_integer_ratio()
(5854679515581645, 2251799813685248)
```

浮点数总是不精确的，而且不能指定小数位数。但在python中，有一个专门的小数模块decimal，它可以提供精确的小数运算，还有一个分数模块fractions，也能提供精确的小数运算。

### 真除法、Floor除法和小数位截断

- /：实现的是真除法。在python中，它总是返回浮点数值。
- //：实现的是floor地板除法，它会去掉除法运算后的小数位，以便得到小于运算结果的最大整数。如果参与运算的有小数，则返回浮点数，否则返回整数
- 在math模块中，有地板函数math.floor()和天花板函数math.ceil()。它们的意义可以根据现实中地板、空气、天花板的高低位置来考虑。地板位于空气之下，地板运算的返回值是比空气小的最大整数，天花板位于空气之上，天花板运算的的返回值是比空气大的最小整数
- round(x, N)是四舍五入，可以指定四舍五入到哪个小数位
- math.trunc()是直接截断小数
- 实际上int()函数自身就是字节截断小数的

### 数值类型的转换

- int()可以将字符串或浮点数转换成整数，也可以用于进制数转换
- float()可以将字符串或整数转换成浮点数
  实际上它们表示根据给定参数在内存中构造一个整数、浮点数对象，所以可以用来作为类型转换工具。而且，前面已经说过，int()可以用来截断小数位。
  int()还可用于进制数转换，

```python
int(x, base=10)
```

base指定要将x解释成哪个进制位的数，然后转换成十进制数，也就是前面说的构造一个整数对象。不指定base时，默认解释成10进制。
base的值可以是0或2-36之间的任意一个数，base=0也表示解释成10进制。

### 小数类型(Decimal)

小数模块decimal，它有一个函数Decimal()，它是精确的，是可以指定小数位数的。

```python
import decimal
decimal.Decimal('0.1') * 3 - decimal.Decimal('0.3')
```

注意，Decimal()的参数都是字符串，如果不加引号，它还是会解释成浮点数。

### 分数(Fraction)

分数模块fractions，它有一个函数Fraction()，它可以构建分数。有了分数之后，可以参与运算。分数和浮点数不同，分数是精确的。

```python
# 分数加、减、乘、除分数
fractions.Fraction(1,3) + fractions.Fraction(2,3)
fractions.Fraction(1,3) - fractions.Fraction(2,3)
fractions.Fraction(1,3) * fractions.Fraction(2,3)
fractions.Fraction(1,3) / fractions.Fraction(2,3)
```

## 布尔类型

python中True表示真，False表示假，它们是布尔类型：

```python
type(True)
<class 'bool'>
```

在python中，bool的True和False是数值1和0的数值表示格式，实际上bool类型是int类型的一个子类。
因为True/False是数值1和0的另一种表示方式，它们可以直接参与数值运算。

```python
True + 2
```

### True/False的各种形式

虽然True代表1，False代表0。但实际上，python中的任何一个数据对象要么是True，要么是False，所以可以直接在布尔测试的表达式中使用，而并非一定要去大小比较、通过函数测试等等。比如：
那么，哪些类型的数据是True，哪些类型的数据是False？

- 整数值0、浮点数值0.0等、空字符串都为假
- None为假
- 空数据对象都是假，比如[]、{}、()等
  - 注意，元组的括号和逗号的特殊性。例如(None)、(1)这些都不是元组，而是单个数据对象，加上逗号才算是元组。所以，使用括号包围但却不是元组的数据，如果它们是假，则整个返回假，而不是元组看上去不为空而返回真
  - 注意(())表示一个空元组，使用 () 包裹另一对括号时，Python 将解释为一个空元组
    **实际上，一个数据对象是真还是假，是根据这个类型的__bool__()的返回值(为False则为假)以及__len__()的返回值(为0则为假)来决定的。**

## None

python中的None有以下几种特性：

1. None在python中是一个特殊的对象，它表示空值，其类型为NoneType
2. None只存在一个，python解释器启动时创建，解释器退出时销毁
3. None不支持任何运算，也没有内建方法，除了表示空以外，什么都做不了。
4. 如果要判断一个对象是否为None,使用is身份运算符
5. 如果一个函数，没有显式return任何数据，则默认返回None
6. 在判断语句中，None等价于False

## 逻辑运算：and、or、not

python中只支持字符形式的and、or、not逻辑运算，不支持符号类型的&&、||、!
not优先级很低，所以not a == b等价于not (a == b)
需要注意，and和or会短路运算(即只要能确定真假关系，就立即停止运算)，并返回运算的结果(不是返回True/False，而是返回表达式的运算结果)。而not运算是返回True/False的。

```python
2 and 3, 3 and 2
[] and {}
3 and []
```

上面第一行and测试，因为and左边的都是True，所以必须得评估and右边的值，那么不管and右边是True还是False，都会返回and右边的值，比如第一行and测试，第三行and测试。第二行and测试中，因为and左边为False，所以直接能确定为False，所以直接短路返回[]。
再次说明，and、or返回的不是True/False的布尔值，而是逻辑表达式的运算结果。但因为python中只要是数据，要么是True，要么是False，所以and/or/not都可以用于真假测试，只不过and/or还可以在布尔测试的基础上进行赋值操作。

## 空、非空测试的建议

经常会遇到要测试数据是否为空。这里的空可能是None、""、[]、{}、()中的一种，建议不要使用len() == 0去测试,而是直接将数据作为真、假值进行判断：

```python
if x:
if not x:
```

## 等值、大小比较

在python中，只要两个对象的类型相同，且它们是内置类型(字典除外)，那么这两个对象就能进行比较。关键词：内置类型、同类型。所以，两个对象如果类型不同，就没法比较，比如数值类型的数值不能和字符串类型的数值或字母比较。
比较操作符有：

```python
==  !=  <  <=  >  >=
```

python中同类型的内置类型对象(字典除外)，都是从左开始，一个一个元素向后比较，就算中间遇到嵌套的容器结构(如list/tuple/Set)，也会递归到嵌套的结构中去一个个比较。
注意，**None对象只能参与等值和不等值比较，不能参与大小比较**。
python支持连续比较，连续比较时等价于使用and运算。
连续比较是一种比较语法，它不仅限于数值的连续比较，还支持其它类型。比如：

```python
"ac" > "ab" < "ad"
```

### is 和 ==

有两种比较数据对象是否相等的方式："=="和"is"，它们的否定形式分别为"!="和"is not"。
它们都是比较表达式，但却是完全不同的比较方式：

- "=="和"!="符号比较的是数据的值是否相等、相同
- "is"比较的是两个数据对象在内存中是否是同一个数据对象。换句话说，比较的是内存地址

## python中的字符串

在python 3.x中，字符串的类型str是Unicode的。除此之外还有byte类型、bytearray类型。
python中可以使用单引号、双引号、三引号包围字符串，并可以使用反斜线转义特殊字符：

- 单、双引号是完全一致的，不像其他语言一样有强、弱引用之分
- 三引号('''xxx'''或"""xxx""")包围的字符完全是字面符号，包围什么就得到什么，包括换行，且不会进行任何转义、替换等
  - 使用这种块字符串的方式，在输入需要换行的字符串时非常方便
  - 而且可以作为块注释符注释一段代码。这表示这段被包围的代码解释为字符串，但因为没有赋值给变量，所以直接丢弃了
- 反斜线\可以转义特殊字符，例如在字符串中保留单引号"a\'b"

### raw字符串

虽然可以通过反斜线\转义去调整字符串，但带上反斜线有时候会严重影响可读性。如果不想使用反斜线转义，可以考虑使用三引号包围，也可以使用r来声明后面的字符串是raw字符串，这里面的所有字符都是字面意义的，不会进行任何转义。
注意，raw字符串不能以反斜线结尾，除非对其转义。例如r'abc\ndef\'是错误语法，但r'abc\ndef\\'是正确的语法，它表示后面有两个反斜线字符

### 字符串转换

数值和字符串类型不能直接放在一起操作，例如9 + "9"是错误的。要将一个数值类型转换成字符串类型，可以使用str()方法或repr()方法。

### 操作字符串

1. 在python中，操作字符串的方式有多种，大概概括有：
   字符串是一个序列，且是不可变序列，所以序列的通用操作和不可变序列的操作都能应用在str上
2. string对象自身实现了很多方法，比如大小写转换、子串搜索、截断等等
3. 字符串连接，如"abc" "def"或"abc" + "def"是等价的，都是"abcdef"，"a" * 3得到"aaa"
4. 字符串格式化
   因为python中的字符串是一种序列类型，所以可以使用in来测试字符串中是否包含某个字符或子串。

### 字符串的索引和分片操作

字符串是一种序列，可以应用序列的一种非常方便的分片操作。
必须注意，因为字符串是不可变对象，无法原处修改，所以无论是索引取值还是分片操作，都会创建新字符串对象。

### 索引取单个元素

索引位可以是负数，表示从尾部开始取元素，-1表示倒数第一个元素，-2表示倒数第二个元素。

### 分片取多个元素

分片的方式是使用[i:j]或[i:j:k]的方式，表示从索引位i开始取到索引位j(不包含j)，i或j都可以省略。如果指定了k，则表示每隔k个元素取一次，也就是取一次元素之后跳过(k-1)一个元素。i、j、k都可以使用负数。

## 异常和错误处理

在shell脚本中，常用if来判断程序的某个部分是否可能会出错，并在if的分支中做出对应的处理，从而让程序更具健壮性。if判断是异常处理的一种方式，所有语言都通用。对于特性完整的编程语言来说，都有专门的异常处理机制，有些语言用起来可能会很复杂，要求一堆堆的，有些语言则非常简洁，用起来非常通畅。

### 异常处理：try/except

```python
try:
    statement1
    ...
    statementN
except <ERRORTYPE>:
    ...statementS..
```

例如，try中是要监视正确执行与否的语句，ERRORTYPE是要监视的错误类型。

- 只要try中的任何一条语句抛出了错误，try中该异常语句后面的语句都不会再执行；
- 如果抛出的错误正好是except所监视的错误类型，就会执行statementS部分的语句；
- 如果异常正好被except捕获(匹配)到了，程序在执行完statementS后会继续执行下去，如果没有捕获到，程序将终止
  - 换句话说，except捕获到错误后，相当于处理了这个错误，程序不会因为已经被处理过的错误而停止

### 异常处理：try/finally

finally是try之后一定会执行的语句段落。可以结合except一起使用。

```python
try:
    statement1
    ...
    statementN
finally:
    ...statementF...
try:
    statement1
    ...
    statementN
except <ERRORTYPE>:
    ...statementS...
finally:
    ...statementF...
```

不论try中的语句是否出现异常，不论except是否捕获到对应的异常，finally都会执行：

- 如果异常没有被捕获，则在执行finally之后程序退出
- 如果异常被except捕获，则执行完except的语句之后执行finally的语句，然后程序继续运行下去
  一般来说，finally中都会用来做程序善后清理工作。

### 产生异常：raise和assert

使用raise或assert可以主动生成异常情况。其中raise可以直接抛出某个异常，assert需要通过布尔值来判断，然后再抛出给定的错误。
assert是一种断言，在计算机语言中表示：如果断言条件为真就跳过，如果为假就抛出异常信息。它可以自定义异常信息。

### 自定义异常

python中的异常是通过类来定义的，而且所有的异常类都继承自Exception类，而Exception又继承自BaseException(这个类不能直接作为其它异常类的父类)。所以自定义异常的时候，也要继承Exception，当然，继承某个中间异常类也可以。
需要注意，因为异常类都继承字Exception，except监视Exception异常的时候，也会匹配其它的异常。更标准地说，监视异常父类，也会捕获到这个类的子类异常。

### 如何看抛出的异常

看异常信息是最基本的能力。例如，下面的这段代码会报除0错误：

```python
def a(x, y):
    return x/y

def b(x):
    print(a(x, 0))

b(1)
```

执行时，报错信息如下：

```python
Traceback (most recent call last):
  File "g:/pycode/list.py", line 7, in <module>
    b(1)
  File "g:/pycode/list.py", line 5, in b
    print(a(x, 0))
  File "g:/pycode/list.py", line 2, in a
    return x/y
ZeroDivisionError: division by zero
```

这个堆栈跟踪信息中已经明确说明了(most recent call last)，说明最近产生异常的调用在最上面，也就是第7行。上面的整个过程是这样的：第7行出错，它是因为第5行的代码引起的，而第5行之所以错是第2行的源代码引起的。
所以，从最底部可以看到最终是因为什么而抛出异常，从最顶部可以看到是执行到哪一句出错。

### 深入异常处理

try/except/else/finally

```python
try:
    <statements>
except <name1>:           # 捕获到名为name1的异常
    <statements>
except (name2, name3):    # 捕获到name2或name3任一异常
    <statements>
except <name4> as <data>: # 捕获name4异常，并获取异常的示例
    <statements>
except:                   # 以上异常都不匹配时
    <statements>
else:                     # 没有产生异常时
    <statements>
finally:                  # 一定会执行的
    <statements>
```

注意，当抛出的异常无法被匹配时，将归类于空的except:，但这是很危险的行为，因为很多时候的异常是必然的，比如某些退出操作、内存不足、Ctrl+C等等，而这些都会被捕获。与之大致等价的是捕获异常类的"伪"祖先类Exception，即except Exception:，它和空异常匹配类似，但能解决不少不应该匹配的异常。但使用Exception依然是危险的，能不用尽量不用。
如果一个异常既能被name1匹配，又能被name2匹配，则先匹配到的处理这个异常。
通过as关键字可以将except捕获到的异常对象赋值给data变量。用法稍后会解释，现在需要知道的是，在python 3.x中，变量data只在当前的except块范围内有效，出了范围就会被回收。如果想要保留异常对象，可以将data赋值给一个变量。例如下面的b在出了try范围都有效，但是a在这个except之后就无效了。

### raise

raise用于手动触发一个异常。而每一种异常都是一个异常类，所以触发实际上是触发一个异常类的实例对象。

```python
raise <instance>  # 直接触发一个异常类的对象
raise <class>     # 构建此处所给类的一个异常对象并触发
raise             # 触发最近触发的异常
raise <2> from <1>  # 将<1>的异常附加在<2>上
```

其中第二种形式，raise会根据给定类不传递任何参数地自动构建一个异常对象，并触发这个异常对象。第三种直接触发最近触发的异常对象，这在传播异常的时候很有用。

例如，下面两种方式实际上是等价的，只不过第一种方式传递的是类，raise会隐式地自动创建这个异常类的实例对象。

```python
raise IndexError
raise IndexError()
```

可以为异常类构建实例时指定点参数信息，这些参数会保存到名为args的元组。例如：

```python
try:
    raise IndexError("something wrong")
except Exception as E:
    print(E.args)
```

不仅如此，只要是异常类或异常对象，不管它们的存在形式如何，都可以放在raise中。例如：

```python
err = IndexErro()
raise err

errs = [IndexError, TypeError]
raise errs[0]
```

对于第三种raise形式，它主要用来传播异常，一般用在except代码段中。例如：

```python
try:
    raise IndexError("aaaaa")
except IndexError:
    print("something wrong")
    raise
```

因为异常被except捕获后，就表示这个异常已经处理过了，程序会跳转到finally或整个try块的尾部继续执行下去。但是如果不想让程序继续执行，而是仅仅只是想知道发生了这个异常，并做一番处理，然后继续向上触发异常。这就是异常传播。
因为实际触发的异常都是类的实例对象，所以它有属性。而且，可以通过在except中使用as来将对象赋值给变量：

```python
try:
    1/0
except Exception as a:
    print(a)
```

变量a在出了except的范围就失效，所以可以将它保留给一个不会失效的变量：

```python
try:
    1/0
except Exception as a:
    print(a)
    b=a

print(b)
```

如果在一个except中触发了另一个异常，会造成异常链：

```python
try:
    1/0
except Exception as E:
    raise TypeError('Bad')
```

将会报告两个异常，并提示处理异常E的时候，触发了另一个异常TypeError。

使用from关键字，可以让关系更加明确。

```python
try:
    1/0
except Exception as E:
    raise TypeError('Bad') from E
```

实际上，使用from关键字的时候，会将E的异常对象附加到TypeError的__cause__属性上。
但无论如何，这里都触发了多个异常。在python 3.3版本，可以使用from None的方式来掩盖异常的来源，也就是禁止输出异常E，停止异常链：

### sys.exc_info()

该函数用来收集正在处理的异常的信息。

它返回一个包含3个值的元组(type, value, traceback)，它们是当前正在处理的异常的信息。如果没有正在处理的异常，则返回3个None组成的元组。

- type表示正在处理的异常类
- value表示正在处理的异常实例
- traceback表示一个栈空间的回调对象
  什么时候要获取异常类的信息？当except所监视的异常类比较大范围，同时又想知道具体的异常类。比如，except:或except Exception:这两种监视的异常范围都非常大，前者会监视BaseException，也就是python的所有异常，后者监视的是Exception，也就是python的所有普通的异常。正因为监视范围太大，导致不知道具体是抛出的是哪个异常。

### 区分异常和错误

错误都是异常，但异常并不一定都是错误。

很常见的，文件结尾的EOF在各种语言中它都定义为异常，是异常就能被触发捕获，但在逻辑上却不认为它是错误。

除此之外，还有操作系统的异常，比如sys.exit()引发的SystemeExit异常，ctrl+c引发的的中断异常KeyboardInterrupt都属于异常，但它们和普通的异常不一样。而且python中的普通异常都继承字Exception类，但SystemExit却并非它的子类，而是BaseException的子类。所以能通过空的except:捕获到它，却不能通过except Exception:来捕获。

### 异常类的继承

所有异常类都继承自Exception，要编写自定义的异常时，要么直接继承该类，要么继承该类的某个子类。

例如，下面定义三个异常类，General类继承Exception，另外两个继承General类，表示这两个是特定的、更具体的异常类。

```python
class General(Exception):pass
class Specific1(General): pass
class Specific2(General): pass

def raise0():
    x = General()
    raise x

def raise1():
    x = Specific1()
    raise x

def raise2():
    x = Specific2()
    raise x

for func in (raise0, raise1, raise2):
    try:
        func()
    except General as E:
        import sys
        print("caught: ", E.__class__)
```

except监视父类异常的时候，也会捕获该类的子类异常。正如这里监视的是Gereral类，但触发了Specific子类异常也会被捕获

### 异常类的嵌套

这是非常常见的陷阱。有两种异常嵌套的方式：try的嵌套；代码块的异常嵌套(比如函数嵌套)。无论是哪种嵌套模式，异常都只在最近(或者说是最内层)的代码块中被处理，但是finally块是所有try都会执行的。
第一种try的嵌套模式：

```python
try:
    try:
        (1)
    except xxx:
        (2)
    finally:
        (3)
except yyy:
    ...
finally:
    (4)
```

如果在(1)处抛出了异常，无论yyy是否匹配这个异常，只要xxx能匹配这个异常，就会执行(2)。但(3)、(4)这两个finally都会执行。

第二种代码块嵌套，常见的是函数调用的嵌套，这种情况可能会比较隐式。例如：

```python
def action2():
    print(1 + [])

def action1():
    try:
        action2()
    except TypeError:
        print('inner try')

try:
    action1()
except TypeError:
    print('outer try')
```

上面的action2()会抛出一个TypeError的异常。在action1()中用了try包围action2()的调用，于是action2()的异常汇报给action1()层，然后被捕获。

但是在最外面，使用try包围action1()的调用，看上去异常也会被捕获，但实际上并不会，因为在action2()中就已经通过except处理好了异常，而处理过的异常将不再是异常，不会再触发外层的异常，所以上面不会输出"outer try"。

### except应该捕获哪些异常

在考虑异常捕获的时候，需要注意几点：

- except监视的范围别太大了
- except监视的范围别太小了
- 有些异常本就该让它中断程序的运行，不要去捕获它
  第三点很容易理解，有些异常会导致程序无法进行后续的运行，改中断还是得中断。
  对于第一点，可能常用的大范围异常监视就是下面两种方式：

```python
except:
except Exception:
```

这两种方式监视的范围都太大了，比如有些不想处理的异常也会被它们监视到。更糟糕的可能是本该汇报给上层的异常，结果却被这种大范围捕获了。例如：

```python
def func():
    try:
        ...
    except:
        ...

try:
    func()
except IndexErro:
    ...
```

本来是想在外层的try中明确捕获func触发的IndexError异常的，但是func()内却使用了空的except:，使得异常直接在这里被处理，外层的try永远也捕获不到任何该函数的异常。

关于第二点，不应该监视范围太小的异常。范围小，意味着监视的异常太过具体，太过细致，这种监视方式虽然精确，但却不利于维护。例如E1异常类有2个子异常类E2、E3，在代码中监视了E2、E3，但如果未来又添加了一个E1的子异常类E4，那么又得去改代码让它监视E4。如果代码是写给自己用的倒无所谓，但如果像通用模块一样交给别人用的，这意味着让别的模块使用者也去改代码。

### 自定义异常类

在前面设计异常类的时候，总是使用pass跳过类代码体。但却仍然能使用这个类作为异常类，因为它继承了Exception，在Exception中有相关代码可以输出异常信息。

前面说过，在构造异常类的时候可以传递参数，它们会放进异常实例对象的args属性中：

### 自定义异常输出

自定义异常类的时候，也可以重写这两个中的一个，从而可以定制属于自己的异常类的输出信息。一般来说只重写__str__，因为Exception中也是重写该类，且它的优先级高于__repr__

```python
class MyError(Exception):
    def __str__(self):
        return 'output this message for something wrong'

try:
    raise MyError("hahhaha")
except MyError as E:
    print(E)
```

### 提供构造方法

自定义异常类的时候，可以重写构造方法__init__()，这样raise异常的时候，可以指定构造的数据。而且更进一步的，还可以重写__str__来自定义异常输出。
例如，格式化文件的程序中定义一个异常类，用来提示解析到哪个文件的哪一行出错。

```python
class MyError(Exception):
    def __init__(self,line,file):
        self.line = line
        self.file = file
    def __str__(self):
        return "format failed: %s at %s" % (self.file, self.line)

def format():
    ...
    raise MyError(42, "a.json")
    ...

try:
    format()
except MyError as E:
    print(E)
```

### 提供异常类的其它方法

异常类既然是类，说明它可以像普通类一样拿来应用。比如添加其它类方法。

例如，可以将异常信息写入到文件中。只需提供一个向文件写入的方法，并在except的语句块中调用这个方法即可。

```python
class MyError(Exception):
    def __init__(self, line, file):
        self.line = line
        self.file = file

    def logerr(self):
        with open('Error.log', 'a') as logfile:
            print(self, file=logfile)

    def __str__(self):
        return "format failed: %s at %s" % (self.file, self.line)

def format():
    raise MyError(42, "a.json")

try:
    format()
except MyError as E:
    E.logerr()
```

## with/as和contextlib上下文管理使用说明

### with/as

使用open打开过文件的对with/as都已经非常熟悉，其实with/as是对try/finally的一种替代方案。
当某个对象支持一种称为"环境管理协议"的协议时，就会通过环境管理器来自动执行某些善后清理工作，就像finally一样：不管中途是否发生异常，最终都会执行某些清理操作。
用法：

```python
with expression [as var]:
    with_block_code
```

当expression返回的对象是支持环境管理协议的时候，就可以使用with。as var是可选的，如果不使用as var，expression返回对象将被丢弃，如果使用as var，就会将expression的返回对象赋值给变量var。
整个流程大致如下：先评估expression，如果支持环境管理协议，然后开始with/as语句块结构，当准备退出with语句块的时候，将执行对象中定义的善后操作。工作机制的细节见下文。

例如，open()返回的文件对象是支持环境管理协议的，所以可以用with/as来安全地打开文件：

```python
with open(r'd:\a\b\c\a.log') as logfile:
    for line in logfile:
        print(line)
        ...more code here...
```

整个过程是先open()，然后with/as，输出每一行后将要退出with语句块的时候，环境管理器根据文件对象中定义的操作关闭文件。
它实际上等价于：

```python
myfile = open(r'd:\a\b\c\a.log')
try:
    for line in myfile:
        print(line)
        ...more code here...
finally:
    myfile.close()
```

虽然在文件不被引用之后，垃圾回收器会自动回收这个文件对象，但是垃圾回收器的回收操作是有等待时间的。换句话说，如果不使用with/as打开文件，也不显示close()关闭文件，那么这个文件很可能会在用完之后保持空闲一段时间，然后才被垃圾回收器回收。
with/as不仅用于文件打开/关闭，锁操作也支持环境管理协议，也就是说，在有需要的时候会自动释放锁资源。

### 嵌套多个环境管理器

在python 3.1之后，with as支持多个环境管理器，使用逗号隔开即可。

```python
with A() as a, B() as b:
      ...statements...
```

它等价于嵌套的with：

```python
with A() as a:
    with B() as b:
        ...statements...
```

多环境管理器管理的多个对象会在with语句块中出现异常的时候，或者执行完with语句块的时候全部自动被清理(例如文件关闭操作)。

### 自定义环境管理器

无论是文件还是锁，都是别人已经写好了环境管理器的对象。我们自己也可以写环境管理器，让它可以使用with/as，这实际上属于运算符重载的范畴。

要写自己的环境管理器，先了解with/as的工作机制的细节：

1. 先评估expression，评估的返回结果是一个对象，这个对象要具有__enter__和__exit__方法，返回的对象称为"环境管理器"
2. 然后调用环境管理器的__enter__方法。__enter__方法的返回值赋值给 as 指定的变量，或者直接丢弃(没有使用as)
3. 然后执行with语句块中的内容
4. 如果执行with语句块中的内容时抛出了异常，将调用__exit__(type,value,traceback)方法，其中这3个和异常相关的参数来源于sys.exc_info。如果__exit__返回值为False，则会自动重新抛异常以便传播异常，否则异常被认为合理处理
5. 如果with语句块中的内容没有抛异常，则直接调用__exit__(None,None,None)，即这三个参数都传递为None值

```python
class TraceBlock:
    def message(self, arg):
        print('running ' + arg)

    def __enter__(self):
        print('starting with block')
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type is None:
            print('exited normally\n')
        else:
            print('raise an exception! ' + str(exc_type))
            return False
```

上面的__enter__方法返回的对象会赋值给as关键字指定的变量，在这个示例中即将对象自身返回。如果有需求，可以返回其它对象。

上面的__exit__中，如果异常的类型为None，说明with语句块中的语句执行过程没有抛异常，正常结束即可。但是如果有异常，则要求返回False，实际上上面的return False可以去掉，因为函数没有return时默认返回None，它的布尔值代表的就时False。
定义环境管理器不是件简单的事。一般来说，如果不是很复杂的需求，直接使用try/finally来定义相关操作即可。

### contextlib模块

在自定义上下文管理器的时候，可以通过contextlib模块的contextmanager装饰器来简化，这样不需要自己去写__enter__和__exit__。

使用contextlib.contextmanager装饰的时候，所装饰的对象必须是一个生成器函数，且该生成器函数必须只yield一个值，这个值将会被绑定到with/as的as子句的变量上。

```python
from contextlib import contextmanager

@contextmanager
def managed_resource(*args, **kwds):
    # Code to acquire resource, e.g.:
    resource = acquire_resource(*args, **kwds)
    try:
        yield resource
    finally:
        # Code to release resource, e.g.:
        release_resource(resource)

>>> with managed_resource(timeout=3600) as resource:
...     # Resource is released at the end of this block,
...     # even if code in the block raises an exception
```

它的执行流程是这样的：

1. 当执行到with语句的时候，首先评估managed_resource(timeout=3600)，它是一个生成器函数，它会返回一个生成器
2. 然后执行resource = acquire_resource，并在yield的地方状态被挂起这个生成器函数
3. 在yield挂起的时候，with语句块中的语句开始执行
4. 当with语句块退出的时候，yield被恢复，于是继续执行生成器函数中后面的语句
   如果在with语句块中发生了异常且未处理，则会在生成器yield被恢复的时候再次抛出这个异常。因此，可以使用try...except...finally语句来捕获可能存在的错误，以便保证yield后面的语句(通常是资源释放类的善后工作)可以正常执行。

## f-string

Python 中的字符串通常被括在双引号（""）或单引号（''）内。要创建 f-string，你只需要在字符串的开头引号前添加一个 f 或 F。
当使用 f-string 来显示变量时，你只需要在一组大括号 {} 内指定变量的名字。而在运行时，所有的变量名都会被替换成它们各自的值。

### 基本语法

f"{value[:specifier]}" -> str	# f大小写都可以
"""
f-string 允许将 Python语句 直接嵌入到目标语句中，使用花括号包裹
同时还可以指定该变量的格式说明符
"""

### 用 Python f-string 来评估表达式

由于 f-string 是在运行时评估的，所以你也可以在运行时评估有效的 Python 表达式。
在下面的例子中，num1 和 num2 是两个变量。为了计算它们的乘积，你可以在一组大括号内插入表达式 num1*num2

```python
num1 = 83
num2 = 9
print(f"The product of {num1} and {num2} is {num1 * num2}.")
```

在任何 f-string 中，{var_name}, {expression} 作为变量和表达式的占位符，并在运行时被替换成相应的值。

```python
from datetime import datetime
day = datetime(2012, 12, 12)
str(day)
repr(day)
f"{day = }"
```

可以看出，= 号前的表达式会自动求结果值，并调用结果值的 repr 形式值作为 = 号后的内容

### 如何在 Python f-string 中使用条件语句

if...else 块，有更简洁的等价的代码，其语法如下

```python
<true_block> if <condition> else <false_block>
```

这在 Python 中通常被称为三元运算符，因为它在某种意义上需要 3 个操作数——true 代码块、被测条件 condition 和 false 代码块。

```python
num = 87;
print(f"Is num even? {True if num%2==0 else False}")
```

### 用 Python f-string 调用方法

```python
author = "jane smith"
print(f"This is a book by {author.title()}.")
```

### 在 Python f-string 中调用函数

就像变量名被值所替代，表达式被评估结果所替代一样，函数调用被函数的返回值所替代。

```python
print(f"Hello Python, tell me what I should learn. {random(3)}")
```

### 使用f-string进行格式化

格式说明符即 specifier ，f-string 和 format 的格式说明符遵循一致的规则！

- 输出内容对齐 & 补全

```python
word = "python"

>>> f"|{word:<10}|"
'|python    |'

>>> f"|{word:>10}|"
'|    python|'

>>> f"|{word:^10}|"
'|  python  |'
```

带有补全的对齐效果：

```python
# 本例用小数点来补全空余内容
>>> f"|{word:.<10}|"
'|python....|'

>>> f"|{word:.>10}|"
'|....python|'

>>> f"|{word:.^10}|"
'|..python..|'
```

- 数字格式化

  - 浮点数 ：指定精度显示

  ```python
    pi = 3.141592654
    print(f"PI = {pi:.2f}")
    # PI = 3.14

    print(f"PI = {pi:.3f}")
    # PI = 3.142
  ```

  - 科学计数

  ```python
    print(f"{pi:e}")	# 不指定精度，默认6位小数，和format一致
    # 3.141593e+00
    print(f"{pi:.2e}")
    # 3.14e+00
  ```

  - 百分比格式化

  ```python
    # 兼顾小数位保留和百分号格式化功能
    print(f"PI = {pi:.3%}")
    # PI = 314.159%
    print(f"PI = {pi:.2%}")
    # PI = 314.16%
  ```

  - 千位分隔符

  ```python
    # 使用 , 格式化数字展示（常用于金额），易于阅读
    >>> f"{234234234:,}"
    '234,234,234'

    >>> f"{234234234.1314:,.2f}"
    '234,234,234.13'

    >>> f"{234234234.1314:_.2f}"
    '234_234_234.13'
  ```
- 进制转换
  在f-string中，b、o、x分别代表二进制、八进制、十六进制

```python
    f"{num:b}"	# '10111'
    f"{num:o}"	# '27'
    f"{num:x}"	# '17'
```

要想实现常用用法的效果，进制规则代码前需要加#号：

```python
    f"{num:#b}"	# '0b10111'
    f"{num:#o}"	# '0o27'
    f"{num:#x}"	# '0x17'
    f"{num:#X}" # '0X17
```

日期格式化
适用于 date、datetime 和 time 对象

```python
    today = datetime.datetime.today()
    f"{today:%Y}"			# '2022'
    f"{today:%Y-%m}"		# '2022-12'
    f"{today:%Y-%m-%d}"		# '2022-12-16'

    f"{today:%F}"			# '2022-12-16'
    f"{today:%D}"			# '12/16/22'
    f"{today:%X}"			# '21:01:27'
    f"{today:%F %X}"		# '2022-12-16 21:01:27'
```

### 使用建议

1. 如果格式化的字符串是由用户输入的，那么基于安全性考虑，推荐使用Template
2. 如果使用的python3.6+版本的解释器，推荐使用F-Strings
3. 如果要兼容python2.x版本的python解释器，推荐使用format形式
4. 一般不推荐使用%，尤其是生产环境

| 限定符 | 说明                                                                                                    |
| ------ | ------------------------------------------------------------------------------------------------------- |
| :<     | Left aligns the result (within the available space)                                                     |
| :>     | Right aligns the result (within the available space)                                                    |
| :^     | Center aligns the result (within the available space)                                                   |
| :=     | Places the sign to the left most position                                                               |
| :+     | Use a plus sign to indicate if the result is positive or negative                                       |
| :-     | Use a minus sign for negative values only                                                               |
| :      | Use a space to insert an extra space before positive numbers (and a minus sign before negative numbers) |
| :,     | Use a comma as a thousand separator                                                                     |
| :_     | Use a underscore as a thousand separator                                                                |
| :b     | Binary format                                                                                           |
| :c     | Converts the value into the corresponding unicode character                                             |
| :d     | Decimal format                                                                                          |
| :e     | Scientific format, with a lower case e                                                                  |
| :E     | Scientific format, with an upper case E                                                                 |
| :f     | Fix point number format                                                                                 |
| :F     | Fix point number format, in uppercase format (show inf and nan as INF and NAN)                          |
| :g     | General format                                                                                          |
| :G     | General format (using a upper case E for scientific notations)                                          |
| :o     | Octal format                                                                                            |
| :x     | Hex format, lower case                                                                                  |
| :X     | Hex format, upper case                                                                                  |
| :n     | Number format                                                                                           |
| :%     | Percentage format                                                                                       |

## 深拷贝与浅拷贝

浅拷贝创建一个新的对象，但不拷贝对象内部的子对象。新对象中的元素实际上是对原对象中元素的引用。因此，如果子对象发生变化，浅拷贝的对象也会受到影响。

想象你有一本笔记本（相当于一个对象），里面有很多贴纸（相当于子对象）。浅拷贝就像是你创建了一本新的笔记本，但贴纸并没有复制过去，而是把原本贴纸的链接放到了新笔记本上。所以，任何一个笔记本上的贴纸变化，另一个也会变化。

深拷贝创建一个新的对象，并且递归地拷贝所有子对象。因此，新对象和原对象完全独立，修改一个对象不会影响另一个对象。

想象你有一本笔记本，里面有很多贴纸。深拷贝就像是你创建了一本新的笔记本，并且把每一个贴纸都复制了一份放到新的笔记本上。所以，两个笔记本互不影响，一个上的贴纸变化不会影响另一个。

## for迭代的陷阱

```python
L = ['a','b','c','d','e']

## 原处修改列表，新元素f、g也会被迭代
for i in L:
    if i in "de":
        L += ["f", "g"]
    print(i)

## 创建新列表，新元素f、g不会被迭代
for i in L:
    if i in "de":
        L = L + ["f", "g"]
    print(i)

for i in L:
    if i in "bc":
        L.remove(i)
        print(i)

print(L)
```

比较以下三种赋值方式
L1 += ['X']
L1 = L1 + ['X']
L1.extend(['X'])

如果迭代并修改的是集合或字典呢？将会报错。虽然它们是可变序列，但是它们是以hash key作为迭代依据的，只要增、删元素，就会导致整个对象的顺序hash key发生改变，这显然是编写这两种类型的迭代器时所需要避免的问题。

在 Python 中迭代一个字典时，Python 内部会进行一些检查以确保迭代过程的安全性。如果在迭代过程中修改了字典的结构（例如添加或删除元素），Python 会检测到这种变化，并抛出一个异常。这种机制被称为并发修改检测。
并发修改检测
为了防止在迭代过程中修改字典（或其他类似的数据结构）导致未定义行为，Python 引入了一种机制来检测和处理这种情况。这种机制的工作原理如下：

1. 迭代器状态捕获：当你开始迭代一个字典时，会创建一个迭代器对象。这个迭代器对象会捕获字典的当前状态，包括字典的大小和内部结构。
2. 修改计数器：字典内部维护了一个修改计数器，每当字典的结构发生变化（例如添加或删除元素）时，这个计数器就会增加。
3. 迭代过程中的检查：在每次迭代时，迭代器会检查当前字典的修改计数器是否与迭代开始时的计数器一致。如果不一致，就意味着字典在迭代过程中发生了修改，此时会抛出 RuntimeError 异常。

## 验证小整数常量池

```python
for i, j in zip(range(-10, 260), range(-10, 260)):
    if id(i) != id(j):
        print(i)
```
