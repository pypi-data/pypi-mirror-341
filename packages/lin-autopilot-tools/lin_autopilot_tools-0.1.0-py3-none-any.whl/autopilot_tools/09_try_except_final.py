def try_except_final():
    try:
        a = 5
        result = a+b
    except ZeroDivisionError:
        print("catch ZeroDivisionError")
    except:
        print("catch Unexpected error")
    else:
        print("no error")
    finally:
        print("finally")
    pass

if __name__ == '__main__':
    try_except_final()