# 序列化及反序列化

## 基础概念
序列化（Serialization）和反序列化（Deserialization）是数据处理中的两个重要概念。简单来说，序列化是将数据结构或对象转换成一种可以存储或传输的格式的过程，而反序列化则是将这种格式的数据恢复成原来的数据结构或对象的过程。

## python中实现
在Python中，常用的序列化和反序列化库有pickle、json和yaml等。下面分别介绍这些库的使用方法：
- pickle 模块
pickle 是Python内置的一个模块，可以实现Python对象的序列化和反序列化。它支持几乎所有的Python数据类型。
```python
import pickle
data = {'name': 'Alice', 'age': 30, 'is_student': True}
serialized_data = pickle.dumps(data)
deserialized_data = pickle.loads(serialized_data)
```
- json 模块
json 是一种轻量级的数据交换格式，易于人阅读和编写，同时也易于机器解析和生成。json 模块是Python内置的一个模块，主要用于字符串和字典之间的转换。
```python
import json
data = {'name': 'Alice', 'age': 30, 'is_student': True}
serialized_data = json.dumps(data)
deserialized_data = json.loads(serialized_data)
print(deserialized_data)
```
- yaml 模块
```python
import yaml
data = {'name': 'Alice', 'age': 30, 'is_student': True}
serialized_data = yaml.dump(data)
deserialized_data = yaml.safe_load(serialized_data)
print(deserialized_data)
```
## 比较
- pickle：适用于Python对象的序列化和反序列化，但生成的数据格式对其他编程语言不友好。
- json：跨语言的数据交换格式，适用于大多数场景，尤其是Web开发。
- yaml：适用于配置文件，结构清晰，易于阅读和编写。



