
# generate_sample_data.py

import pandas as pd
import random

# Make the generated data repeatable for practice.
random.seed(42)

students = []

# Generate 300 fictional student records.
for i in range(300):

    # Generate fictional academic information.
    attendance = random.randint(30, 100)
    internal_marks = random.randint(10, 100)
    assignment_completion = random.randint(20, 100)
    previous_performance = random.randint(10, 100)

    # Create a simulated outcome for this exercise.
    # This is an artificial rule, NOT a real dropout label.
    concern_count = 0

    if attendance < 75:
        concern_count += 1

    if internal_marks < 40:
        concern_count += 1

    if assignment_completion < 60:
        concern_count += 1

    if previous_performance < 40:
        concern_count += 1

    # Simulate a binary outcome:
    # 1 = simulated dropout
    # 0 = simulated continued study
    dropped_out = 1 if concern_count >= 3 else 0

    students.append({
        "Attendance": attendance,
        "Internal_Marks": internal_marks,
        "Assignment_Completion": assignment_completion,
        "Previous_Performance": previous_performance,
        "Dropped_Out": dropped_out
    })

# Convert the list of records into a table.
df = pd.DataFrame(students)

# Save the dataset to a CSV file.
df.to_csv("sample_students.csv", index=False)

print("Sample dataset created successfully!")
print(df.head())
print("\nOutcome counts:")
print(df["Dropped_Out"].value_counts())
