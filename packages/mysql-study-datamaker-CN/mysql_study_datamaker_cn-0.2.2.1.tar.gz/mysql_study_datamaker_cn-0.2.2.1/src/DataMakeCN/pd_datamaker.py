from os import write

import numpy as np
import pandas as pd
import random as rd
from itertools import tee


def __set_seed(seed=None):
    if not isinstance(seed, int) and seed != None:
        raise ValueError('seed must be an integer or None')

    if seed != None:
        np.random.seed(seed)
        rd.seed(seed)

def get_name(__N, __seed=None):
    """
    返回随机生成的姓名系统，总共有 300个姓氏，3579个名字；
    如果超过 1,073,700 个姓名，就一定会有重复的名字出现；
    因为没有做去重处理，所以就算生成 2 个随机姓名也有重复出现的概率！
    :param __N: 生成名字的个数；
    :return: 返回一个迭代器；
    """
    __set_seed(__seed)
    with open(__file__[:__file__.rfind("\\")] + r'\new_names.txt', encoding="utf-8") as f:
        names = f.read().splitlines()

    with open(__file__[:__file__.rfind("\\")] + r'\new_family.txt', encoding="utf-8") as f:
        family = f.read().splitlines()

    return (rd.choice(family) + rd.choice(names) for _ in range(__N))


def to_DataFrame_maker(n: int,
                       types: str = "subject",
                       low: int | float = 80,
                       high: int | float = 150,
                       seed: int | None = None,
                       index: tuple | list | int = 10,
                       items: tuple | None = None,
                       display: str = 'short',
                       write: bool = False,
                       filename: str = "dataFrame_maker.csv") -> pd.DataFrame | None:
    """
    这只是一个为了方便生成一个随机访问的 DataFrame 数据而做的方法；
    现在只是实现了一些比较基础的功能，不要对这个方法报有过多的想法；
    目前的版本只能生成一个随机的成绩和姓名相关的 DataFrame对象；
    你可以扩大学科的种类或者更改学科的种类，在items参数中；
    下面的参数说明：
    :param n: 要生成的 column的数量，如果生成的数量多于items所提供的（默认9个）数量，则用默认命名法处理，Sub_0, Sub_1 ...
    :param types: 现在只有 subject 一种类型，想正常运行它，不要去更改这个参数！
    :param low: 目前是随机的最高分和最低分中的最低分，默认为 80，不支持非int类型
    :param high: 最高分，不支持小于low，默认值为 150
    :param index: index的索引项，可以不给，默认10
    :param items: column的值，默认是学科，并放置了 9 个学科（语数外物化生史地政）
    :param display: 默认值是 short，默认情况下，DataFrame的列数过长，【打印时】无法显示全部内容；
                    参数值为 all，则显示所有的列的内容，但是长度为默认值，这样显示出来的效果会带换行；
                    参数值为 flatten，则不会换行，会显示一个特别长的长行，但是需要注意，数据量过多可能会出现异常；
    :param write: 默认为False，如果是True，则写一个csv文件（Pandas 的 to_csv）
    :param filename: 文件的名称，默认 ‘dataFrame_maker.csv’
    :return: pd.DataFrame 或 None
    """

    assert isinstance(n, int) and n > 0

    if type(high) not in (int, float) or type(low) not in (int, float):
        raise ValueError('<low> and <high> must be an integer or float or complex')
    assert high > low, "high value must be greater than low"

    __set_seed(seed)
    if types == "subject":
        assert isinstance(index, tuple) or isinstance(index, list) or isinstance(index, int)
        if items is None:
            items: tuple = ("Chinese",
                            "Math",
                            "English",
                            "Physics",
                            "Chemistry",
                            "Biology",
                            "History",
                            "Geography",
                            "Polity")


        if len(items) >= n:
            subjects = items[0:n]
            flatten_length = 0
            for s in subjects:
                flatten_length += len(s) * 2

        else:
            subjects, flatten = tee((f'Sub_{i}' for i in range(n)), 2)
            flatten_length = 0
            for sub in flatten:
                flatten_length += len(sub) * 2

        flatten_length += 10

        if display == 'short':
            pd.reset_option("display.max_columns")
            pd.reset_option('display.width')
        elif display == 'all':
            pd.set_option("display.max_columns", None)
        elif display == 'flatten':
            pd.set_option("display.max_columns", None)
            pd.set_option('display.width', flatten_length)
        else:
            raise ValueError('display must be "short" or "all" or "flatten"')

        dic = {}
        for subject in subjects:
            if isinstance(low, int) and isinstance(high, int):
                score = np.random.randint(low=low, high=high, size=index if isinstance(index, int) else len(index))
            else:
                score = np.random.uniform(low=low, high=high, size=index if isinstance(index, int) else len(index))
            dic[subject] = score
        result = pd.DataFrame(dic, index=range(index) if isinstance(index, int) else index)

        if write:
            result.to_csv(filename, encoding='utf-8')
        return result
    return None


def get_demo():
    content = """if __name__ == '__main__':
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

    names = tuple(get_name(10))

    r1 = to_DataFrame_maker(n=200,
                            seed=10, write=False,
                            display='flatten', index=index,
                            items=('a',))
    print(r1)
    r2 = to_DataFrame_maker(n=9,
                            seed=10, write='w',
                            index=names)
    print(r2)
    """
    print(content)


if __name__ == '__main__':
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

    names = tuple(get_name(10))

    r1 = to_DataFrame_maker(n=200,
                            seed=10, write=True,
                            display='flatten', index=index,
                            items=('a',))
    print(r1)