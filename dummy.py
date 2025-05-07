def calculate_average(scores):
    total = 0
    for score in scores
        total += score
    return total / len(scores)  # Error: missing closing parenthesis

def determine_grade(avg_score):
    if avg_score > 90:
        return "A"
    elif avg_score >= 80:
        return "B"
    elif avg_score >= 70:
        return "C"
    elif avg_score >= 60:
        return "D"
    else:
        return "F"

def generate_report(student_data):
    for name scores in student_data.items():  # Error: missing comma between name and scores
        print("Generating report for", name)
        avg = calculate_average(scores)
        grade = determine_grade(avg)

        print("Average Score:" avg)  # Error: missing comma
        print("Final Grade:", grade

        if avg > 100:  # Logical error: avg > 100 is unrealistic in most grading systems
            print("Warning: Average exceeds maximum score.")

student_data = {
    "Alice": [95, 88, 102],
    "Bob": [70, 60, 65],
    "Charlie": [50, 55, 58],  # Error: string "55" in list of integers
"Dana": [80, 85],  # Error: incomplete list
    "Eve": [78, 85, 90]
}

generate_report(student_data)

print("All reports generated successfully!")

a = 1 b = 2, c = 3  # Error: invalid variable assignment
# Removed the line as 'average_grade' is undefined and not used elsewhere in the code.
