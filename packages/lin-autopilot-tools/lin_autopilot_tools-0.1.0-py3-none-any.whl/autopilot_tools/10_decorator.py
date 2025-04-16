def get_multiple_func(n):

    def multiple_func(x):
        return x * n
    return multiple_func

if __name__ == '__main__':
    double = get_multiple_func(2)
    triple = get_multiple_func(3)

    print(double(2))
    print(triple(3))
    pass