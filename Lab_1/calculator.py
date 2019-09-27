def sum(m, n):
    """
    Must perform n increments (+1) to the value of m and return the result
    """
    sum_result = m
    if n < 0:
        for i in range(abs(n)):
            sum_result -= 1
    else:
        for i in range(n):
            sum_result += 1
    return sum_result


def divide(m,n):
    """
    Must substract n from m until it gets 0 and return the result
    """
    
    if n == 0:
        raise Exception("The value of n cannot be 0")

    divide_result = 0

    abs_current_m = abs(m)
    
    reached_zero = False
    result_has_minus_sign = False

    while not reached_zero:
        
        abs_current_m -= abs(n)
        if abs_current_m > 0:
            divide_result += 1
        elif abs_current_m == 0:
            divide_result += 1
            reached_zero = True
        else:
            reached_zero = True
    
    if m*n > 0:
        result_has_minus_sign = False
    else:
        result_has_minus_sign = True
    
    if result_has_minus_sign:
        return -divide_result
    else:
        return divide_result

    return divide_result


def subtract(m, n):
    return sum(m, -n)

def multiply(m, n):
    if n == 0:
        raise Exception("The value of n cannot be 0")
    return divide(m,1/n)

if __name__ == "__main__":

    m = -10
    n = -4
    print("m={} n={}".format(m,n))
    print("Sum = {}".format(sum(m,n)))
    print("Divide = {}".format(divide(m,n)))
    print("Subtract = {}".format(subtract(m,n)))
    print("Multiply = {}".format(multiply(m,n)))