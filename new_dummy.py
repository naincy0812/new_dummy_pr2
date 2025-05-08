def calculate_average(numbers):
    total = sum(numbers)
    average = total / len(numbers)
    print("Average is: " + average)  # ❌ TypeError: Can't concatenate str and float
 if b == 0:
        print("Cannot divide by zero")
        return None
    return a / b
        print("Cannot divide by zero")
        return None
    return a / b

result = calculate_average([10, 20, 30, None])  # ❌ TypeError: unsupported operand type(s) for +: 'int' and 'NoneType'
print("Result:", result)
