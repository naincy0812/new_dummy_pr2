def divide(a, b):
    if b == 0:
        print("Cannot divide by zero")
    return a / b  # ❌ Still tries to divide by zero even after warning

result = divide(10, 0)
print("Result is", result)
