def gen(num):
    while num > 0:
        tmp = yield num
        if tmp is not None:
            num = tmp
        num -= 1

if __name__ == '__main__':
    g = gen(5)
    first = next(g) # 相当于 first = g.send(None)
    print(f"first: {first}")

    print(f"send: {g.send(10)}")

    for i in g:
        print(i)