#mypackage/calculator.py

__version__ = 0.1

#function
def add(num1, num2):
    return num1 + num2

def subtract(num1, num2):
    return num1 - num2

def multiply(num1, num2):
    return num1 * num2

def devide(num1, num2):
    return num1 / num2

#main module로 실행될 때만 실행되도록
if __name__ =="__main__":
    print(">>>name<<<", __name__)
    print("test")