def write():
    with open('test.txt', 'w') as f:
        f.write('hello\n')
        f.write('world')
    pass

if __name__ == '__main__':
    write()