import calculator as c

class FooCalculator:

    def __init__(self):
        pass

    def sum(self,m,n):
        return c.sum(m,n)
    
    def divide(self,m,n):
        return c.divide(m,n)
    
    def subtract(self,m,n):
        return c.subtract(m,n)

    def multiply(self,m,n):
        return c.multiply(m,n)


if __name__ == "__main__":
    fooCalc = FooCalculator()
    m = -10
    n = 1
    print("m={} n={}".format(m,n))
    print("Sum = {}".format(fooCalc.sum(m,n)))
    print("Divide = {}".format(fooCalc.divide(m,n)))
    print("Subtract = {}".format(fooCalc.subtract(m,n)))
    print("Multiply = {}".format(fooCalc.multiply(m,n)))