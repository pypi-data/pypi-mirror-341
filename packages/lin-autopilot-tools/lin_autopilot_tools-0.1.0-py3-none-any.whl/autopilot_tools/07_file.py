

if __name__ == "__main__":
    file = "06_object.py"
    f = open(file, "r", encoding="utf-8")
    print(f.read(10))
    print("======")
    print(f.readline())
    print("--=-=-=-=-=")
    print(f.readline(5))
    print("xxxxxxx")
    print(f.read())
    pass