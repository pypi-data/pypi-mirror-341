# Mysql and Pandas random data generation

This is an auxiliary package for learning Mysql and Pandas, 
and the I feel that inserting some test data is too 
cumbersome to enter manually, 
so I write a method that generates this 
data **randomly** and can **automatically** write it 
in Mysql language and save it to a text file.
Currently, only insert into generation is supported.


Only Chinese is supported(Mysql).

0.2.1 更多信息通过get_help()与get_demo()查看

pandas的帮助信息：
```python
import DataMakeCN.pd_datamaker as pdk
print(pdk.get_demo()) # 查看如何使用 pandas随机生成的案例
```
mysql的帮助信息
```python
import DataMakeCN.datamaker as dm
print(dm.get_demo()) # 获取 mysql 相关的案例
print(dm.get_help()) # 获取 mysql 相关的帮助
```
使用案例(mysql) 1：
实例1，生成单一数据
姓名，性别，年龄，城市
```python
import DataMakeCN.datamaker as dm
one = dm.DataMaker(20, ("姓名", "性别", "年龄", "城市"))
one.get_data()
```

使用案例(mysql) 2：
示例2，员工信息
姓名，性别，生日，年龄，身份证，部门，手机，100人
```python
import DataMakeCN.datamaker as dm
one = dm.DataMaker(50, ("姓名", "性别", "工号", "分数语文", "分数数学", "分数英语"),
                work_head="2024.三班", work_numwidth=2)
one.get_data("insert_into")
```

使用案例(mysql) 3：
示例3，员工信息
姓名，性别，生日，年龄，身份证，部门，手机，100人
```python
import DataMakeCN.datamaker as dm
one = dm.DataMaker(100, ("姓名", "性别", "生日", "年龄", "身份证", "部门", "手机"))
one.get_data("insert_into")
```

使用案例(pandas.DataFrame) 4：
实例4，单纯的获取数据，并非写入数据，便于大家做数据分析时的使用
```python
import DataMakeCN.datamaker as dm
one = dm.DataMaker(20, ("姓名", "性别",  "年龄", "城市"))
api = one.API()
print(list(api['name']))
```

使用案例(pandas.DataFrame) 5：
示例5，DataFrame对象，该对象的随机成绩
列名：科目
行名：姓名
```python
from DataMakeCN.pd_datamaker import to_DataFrame_maker
index = ["Tom",
         "Bob",
         "Jerry",
         "Lucy",
         "Lily",
         "Mike",
         "Tony",
         "Amber",
         "Kevin",
         "Peter"]

r = to_DataFrame_maker(n=20, low=80, high=150,
                       seed=10, write=True,
                       display='flatten', index=index,
                       items=('a',))

r2 = to_DataFrame_maker(5,low=9, high=0.)
print(r)
```