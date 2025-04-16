
class Mamma:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        print("call mamma's init function")

class CuteCat(Mamma):
    def __init__(self, name, age, hobby):
        super().__init__(name, age)
        self.hobby = hobby
        print("call cutecat's init function")

    def __str__(self):
        return f'{self.name} is {self.age} years old'



if __name__ == '__main__':
    cat1 = CuteCat('cat1', 20,"play ball")
    print(cat1)