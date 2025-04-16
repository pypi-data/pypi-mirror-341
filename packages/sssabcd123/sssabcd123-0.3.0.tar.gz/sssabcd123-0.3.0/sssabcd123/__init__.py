def p1a():
    return """Method 1: Using Standard Library
import math
num1 = int(input("Enter the first number: "))
num2 = int(input("Enter the second number: "))
print(f"The gcd of {num1} and {num2} is : {math.gcd(num1, num2)}")

Method 2: Using Recursion
def gcd(a, b):
 if b == 0:
 return a
 else:
 return gcd(b, a % b)
num1 = int(input("Enter the first number: "))
num2 = int(input("Enter the second number: "))
print(f"The gcd of {num1} and {num2} is: {gcd(num1, num2)}")

Method 3: Using Euclidean Algorithm
def gcd(a, b):
 if a == 0:
 return b
 if b == 0:
 return a
 if a == b:
 return a
 if a > b:
 return gcd(a - b, b)
 return gcd(a, b - a)
num1 = int(input("Enter the first number: "))
num2 = int(input("Enter the second number: "))
result = gcd(num1, num2)
if result:
 print(f'GCD of {num1} and {num2} is {result}')
else:
print('GCD not found')

Method 4: Using Lambda Function
gcd = lambda a, b: a if b == 0 else gcd(b, a % b)
num1 = int(input("Enter the first number: "))
num2 = int(input("Enter the second number: "))
print(f"The gcd of {num1} and {num2} is: {gcd(num1, num2)}")
)"""

def p1b():
    return """Method 1: Using Standard Library
import math
number = float(input("Enter a number to calculate its square root: "))
print(f"The square root of {number} is: {math.sqrt(number)}")

Method 2: Using the Exponentiation Operator
number = float(input("Enter a number to calculate its square root: "))
sqrt = number ** 0.5
print(f"The square root of {number} is {sqrt}")

Method 3: Using Newton-Raphson Method with Exception Handling
def newton_raphson_sqrt(number, iterations=10):
 if number < 0:
 raise ValueError("Cannot calculate the square root of a negative number.")
 approximation = number
 for _ in range(iterations):
 approximation = (approximation + number / approximation) / 2
 return approximation
try:
 number = float(input("Enter a number to calculate its square root: "))
 sqrt = newton_raphson_sqrt(number)
 print(f"The square root of {number} using Newton-Raphson is {sqrt}")
except ValueError as e:
 print(e)

 Method 4: Using Class & User-Defined Function Exception Handling
class CodesCracker:
 def sqrt(self, n):
 if n < 0:
 raise ValueError("Cannot calculate square root of a negative number.")
 return n ** 0.5
try:
 print("Enter a Number: ", end="")
 num = float(input().strip())
 obj = CodesCracker()
 result = obj.sqrt(num)
 print(f"\nSquare Root of {num} = {result:.2f}")
except ValueError as e:
 print(f"Error: {e}")
except Exception as e:
 print(f"Error: {e}")"""

def p2():
    return """Method 1: Using Standard Library
list1 = list(map(int, input("Enter numbers separated by spaces: ").split()))
max_number = max(list1)
print("The largest number is:", max_number)

Method 2: Using Brute Force Approach
def large(arr):
 max_ = arr[0]
 for ele in arr:
 if ele > max_:
 max_ = ele
 return max_
list1 = list(map(int, input("Enter numbers separated by spaces: ").split()))
result = large(list1)
print("The largest number is:", result)

Method 3: Using reduce() Function
from functools import reduce
list1 = list(map(int, input("Enter numbers separated by spaces: ").split()))
max_number = reduce(max, list1)
print("The largest number is:", max_number)

Method 4: Using sort() Function
list1 = list(map(int, input("Enter numbers separated by spaces: ").split()))
list1.sort()
print("Largest element is:", list1[-1])

Method 5: Using Tail RecursiveAlgorithm
def func(arr, max_=None):
 if max_ is None:
 max_ = arr.pop()
 current = arr.pop()
 if current > max_:
 max_ = current
 if arr:
 return func(arr, max_)
 return max_
list1 = list(map(int, input("Enter numbers separated by spaces: ").split()))
list_copy = list1.copy()
result = func(list_copy)
print("The largest number is:", result)"""

def p2b():
    return """Brute Force Approach
def nth_prime(n):
 if n <= 0:
 raise ValueError("N must be a positive integer greater than 0.")
 primes = []
 num = 2
 while len(primes) < n:
 is_prime = True
 for i in range(2, int(num ** 0.5) + 1):
 if num % i == 0:
 is_prime = False
 break
 if is_prime:
 primes.append(num)
 num += 1
 return primes[-1]
try:
 n = int(input("Enter the value of N to find the Nth prime number: "))
 nth_prime_number = nth_prime(n)
 print(f"The {n}th prime number is: {nth_prime_number}")
except ValueError as e:
 print(f"Error: {e}")
except Exception as e:
 print(f"Error: {e}")"""

def p3a():
    return """class StudentDetailsApp:
 def __init__(self):
 self.students = []
 def add_student(self):
 while True:
 name = input("Enter student's name (type 'exit' to stop adding): ")
 if name.lower() == 'exit':
 break
 roll_number = input("Enter roll number: ")
 marks = float(input("Enter marks: "))
 self.students.append({'name': name, 'roll_number': roll_number, 'marks': marks})
 def update_marks(self):
 roll_number = input("Enter roll number to update marks: ")
 for student in self.students:
 if student['roll_number'] == roll_number:
 new_marks = float(input("Enter new marks: "))
 student['marks'] = new_marks
 break
 def display_students(self):
 for student in self.students:
 print(f"Name: {student['name']}, Roll Number: {student['roll_number']}, Marks: {student['marks']}")
 def process(self):
 while True:
 print("1. Add a new student")
 print("2. Update student marks")
 print("3. Display all students")
 print("4. Exit")
 choice = input("Enter your choice: ")
 if choice == '1':
 self.add_student()
 elif choice == '2':
 self.update_marks()
 elif choice == '3':
 self.display_students()
 elif choice == '4':
 break
if name == " main ":
app = StudentDetailsApp()
app.process()"""

def p3b():
    return """class StringFunctionsDemo:
 def __init__(self, input_string):
 self.input_string = input_string
 def demonstrate_functions(self):
 print(f"Original String: {self.input_string}")
 print(f"capitalize(): {self.input_string.capitalize()}")
 print(f"casefold(): {self.input_string.casefold()}")
 print(f"center(30, '*'): {self.input_string.center(30, '*')}")
 substring = input("Enter substring to count occurrences: ")
 print(f"count('{substring}'): {self.input_string.count(substring)}")
 suffix = input("Enter suffix to check endswith: ")
 print(f"endswith('{suffix}'): {self.input_string.endswith(suffix)}")
 substring = input("Enter substring to find: ")
 print(f"find('{substring}'): {self.input_string.find(substring)}")
 print(f"isalnum(): {self.input_string.isalnum()}")
 print(f"isalpha(): {self.input_string.isalpha()}")
 print(f"isdigit(): {self.input_string.isdigit()}")
 print(f"islower(): {self.input_string.islower()}")
 print(f"isupper(): {self.input_string.isupper()}")
 delimiter = input("Enter delimiter for join: ")
 print(f"join(['a', 'b', 'c']): {delimiter.join(['a', 'b', 'c'])}")
 print(f"lower(): {self.input_string.lower()}")
 print(f"upper(): {self.input_string.upper()}")
 separator = input("Enter separator for split: ")
 print(f"split('{separator}'): {self.input_string.split(separator)}")
 print(f"strip(): {self.input_string.strip()}")
if __name__ == "__main__":
 input_string = input("Enter a string to demonstrate string functions: ")
 demo = StringFunctionsDemo(input_string)
demo.demonstrate_functions()
"""

def p4a():
    return """def display_students(students):
 print("\nCurrent Student List:")
 if not students:
 print("No students in the list.")
 else:
 for idx, student in enumerate(students, 1):
 print(f"{idx}. Name: {student['name']}, Age: {student['age']}, Grade: {student['grade']}")
def menu():
 print("\nStudent List Operations Menu:")
 print("1. Add a student (Append)")
 print("2. Add multiple students (Extend)")
 print("3. Insert a student at a specific position")
 print("4. Sort students by age")
 print("5. Remove a student by name")
 print("6. Pop the last student")
 print("7. Reverse the order of students")
 print("8. Copy the student list")
 print("9. Clear all students")
 print("0. Exit")
def main():
 students = []
 while True:
 menu()
 choice = input("Enter your choice: ")
 if choice == "1":
 name = input("Enter student's name: ")
 age = int(input("Enter student's age: "))
 grade = input("Enter student's grade: ")
 students.append({"name": name, "age": age, "grade": grade})
 display_students(students)
 elif choice == "2":
 num_students = int(input("Enter number of students to add: "))
 for _ in range(num_students):
 name = input("Enter student's name: ")
 age = int(input("Enter student's age: "))
 grade = input("Enter student's grade: ")
 students.append({"name": name, "age": age, "grade": grade})
 display_students(students)
 elif choice == "3":
 position = int(input("Enter the position to insert the student at (0-based index): "))
 name = input("Enter student's name: ")
 age = int(input("Enter student's age: "))
 grade = input("Enter student's grade: ")
 students.insert(position, {"name": name, "age": age, "grade": grade})
 display_students(students)
 elif choice == "4":
 students.sort(key=lambda student: student["age"])
 display_students(students)
 elif choice == "5":
 name_to_remove = input("Enter the name of the student to remove: ")
 student_found = False
 for student in students:
 if student["name"] == name_to_remove:
 students.remove(student)
 student_found = True
 break
 if student_found:
 print(f"Student {name_to_remove} removed.")
 else:
 print(f"Student {name_to_remove} not found.")
 display_students(students)
 elif choice == "6":
 if students:
 popped_student = students.pop()
 print(f"Popped student: {popped_student}")
 else:
 print("No students to pop.")
 display_students(students)
 elif choice == "7":
 students.reverse()
 display_students(students)
 elif choice == "8":
 copied_students = students.copy()
 print("Copied student list:")
 display_students(copied_students)
 elif choice == "9":
 students.clear()
 print("All students cleared.")
 display_students(students)
 elif choice == "0":
 break
 else:
 print("Invalid choice. Please try again.")
if __name__ == "__main__":
main()"""

def p4b():
    return """def display_catalog(catalog):
 if not catalog:
 print("The catalog is empty.")
 else:
 print("\nCurrent Book Catalog:")
 for title, details in catalog.items():
 print(f"Title: {title}, Author: {details['author']}, Year: {details['year']}")
def menu():
 print("\nBook Catalog Operations Menu:")
 print("1. Add a new book (Create)")
 print("2. Update an existing book (Update)")
 print("3. Sort books by title")
 print("4. Sort books by author")
 print("5. Remove a book by title")
 print("6. Copy the catalog")
 print("7. Clear all books from the catalog")
 print("0. Exit")
def main():
 book_catalog = {}
 while True:
 menu()
 choice = input("Enter your choice: ")
 if choice == "1":
 title = input("Enter book title: ")
 author = input("Enter author's name: ")
 year = input("Enter publication year: ")
 book_catalog[title] = {"author": author, "year": year}
 display_catalog(book_catalog)
 elif choice == "2":
 title = input("Enter the title of the book to update: ")
 if title in book_catalog:
 author = input("Enter new author's name: ")
 year = input("Enter new publication year: ")
 book_catalog[title] = {"author": author, "year": year}
 print(f"Book '{title}' has been updated.")
 else:
 print(f"Book '{title}' not found.")
 display_catalog(book_catalog)
 elif choice == "3":
 sorted_catalog = dict(sorted(book_catalog.items()))
 print("\nSorted Catalog by Title:")
 display_catalog(sorted_catalog)
 elif choice == "4":
 sorted_catalog = dict(sorted(book_catalog.items(), key=lambda item: item[1]["author"]))
 print("\nSorted Catalog by Author:")
 display_catalog(sorted_catalog)
 elif choice == "5":
 title = input("Enter the title of the book to remove: ")
 if title in book_catalog:
 book_catalog.pop(title)
 print(f"Book '{title}' has been removed.")
 else:
 print(f"Book '{title}' not found.")
 display_catalog(book_catalog)
 elif choice == "6":
 copied_catalog = book_catalog.copy()
 print("\nCopied Catalog:")
 display_catalog(copied_catalog)
 elif choice == "7":
 book_catalog.clear()
 print("All books have been cleared from the catalog.")
 display_catalog(book_catalog)
 elif choice == "0":
 break
 else:
 print("Invalid choice. Please try again.")
if __name__ == "__main__":
main()"""

def p5():
    return """def print_pascals_triangle(n):
 triangle = []
 for i in range(n):
 row = [1] * (i + 1)
 for j in range(1, i):
 row[j] = triangle[i - 1][j - 1] + triangle[i - 1][j]
 triangle.append(row)
 for row in triangle:
 print(" ".join(map(str, row)).center(n * 2))
def main():
 n = int(input("Enter the number of rows for Pascal's Triangle: "))
 print_pascals_triangle(n)
if __name__ == "__main__":
 main()"""

def p6a():
    return """def greet(name):
 print(f"Hello, {name}!")
def calculate_area(length, width=1):
 area = length * width
 return area
def average(*args):
 if len(args) == 0:
 return 0
 return sum(args) / len(args)
def factorial(n):
 if n == 0 or n == 1:
 return 1
 else:
 return n * factorial(n - 1)
def calculate_circle(radius):
 circumference = 2 * 3.14 * radius
 area = 3.14 * radius ** 2
 return circumference, area
def print_order(item, quantity, price):
 print(f"Order: {quantity} {item}(s) at ${price} each.")
def greet_with_title(name: str, title: str = "Mr."):
 print(f"Hello, {title} {name}!")
square = lambda x: x ** 2
def display_menu():
 print("\nMenu:")
 print("1. Greet")
 print("2. Calculate Area")
 print("3. Calculate Average")
 print("4. Calculate Factorial")
 print("5. Calculate Circle")
 print("6. Print Order")
 print("7. Greet with Title")
 print("8. Square a Number")
 print("0. Exit")
if __name__ == "__main__":
 while True:
 display_menu()
 choice = input("Enter your choice (0-8): ")
 if choice == '1':
 name = input("Enter your name: ")
 greet(name)
 elif choice == '2':
 length = float(input("Enter length: "))
 width = float(input("Enter width (default is 1 if not provided): ") or 1)
 area = calculate_area(length, width)
 print(f"Area of Rectangle is: {area}")
 elif choice == '3':
 nums = input("Enter numbers separated by space: ").split()
 nums = list(map(float, nums))
 avg = average(*nums)
 print(f"Average is: {avg}")
 elif choice == '4':
 n = int(input("Enter a number to calculate factorial: "))
 fact = factorial(n)
 print(f"Factorial of {n} is: {fact}")
 elif choice == '5':
 radius = float(input("Enter radius of the circle: "))
 circ, area = calculate_circle(radius)
 print(f"Circle with radius {radius} has circumference: {circ} and area: {area}")
 elif choice == '6':
 item = input("Enter item name: ")
 quantity = int(input("Enter quantity: "))
 price = float(input("Enter price per item: "))
 print_order(item=item, quantity=quantity, price=price)
 elif choice == '7':
 name = input("Enter your name: ")
 title = input("Enter your title (default is 'Mr.'): ") or "Mr."
 greet_with_title(name, title)
 elif choice == '8':
 num = float(input("Enter a number to square: "))
 print(f"Square of {num} is: {square(num)}")
 elif choice == '0':
 print("Exiting program. Goodbye!")
 break
 else:
 print("Invalid choice. Please enter a number from 0 to 8.")"""

def p6b():
    return """def binary_search(arr, target):
 left, right = 0, len(arr) - 1
 while left <= right:
 mid = (left + right) // 2
 if arr[mid] == target:
 return mid
 elif arr[mid] < target:
 left = mid + 1
 else:
 right = mid - 1
 return -1
if __name__ == "__main__":
 arr = list(map(int, input("Enter sorted array elements separated by space: ").split()))
 target = int(input("Enter the target value to search: "))
 arr.sort()
 result = binary_search(arr, target)
 if result != -1:
 print(f"Element {target} is present at index {result}.")
 else:
 print(f"Element {target} is not present in the array.")"""

def p7():
    return """def is_palindrome(num):
 return str(num) == str(num)[::-1]
def find_odd_palindromes(start, end):
 results = []
 for num in range(start, end + 1):
 if num % 2 != 0 and is_palindrome(num):
 results.append(num)
 return results
if __name__ == "__main__":
 start = int(input("Enter the starting number of the range: "))
 end = int(input("Enter the ending number of the range: "))
 odd_palindromes = find_odd_palindromes(start, end)
 if odd_palindromes:
 print(f"Odd palindromes between {start} and {end}:")
 print(odd_palindromes)
 else:
 print(f"No odd palindromes found between {start} and {end}.")"""

def p8():
    return """import numpy as np
arr = np.array([[1, 2, 3], [4, 5, 6]])
print("Array:")
print(arr)
print("\nType of Array:")
print(type(arr))
print("\nAxes of Array:")
print(arr.ndim)
print("\nShape of Array:")
print(arr.shape)
print("\nType of Elements in Array:")
print(arr.dtype)
print("\nTotal Number of Elements in Array:")
print(arr.size)
print("\nItemsize (Bytes per Element):")
print(arr.itemsize)
print("\nTotal Bytes Consumed by the Array:")
print(arr.nbytes)
print("\nStrides of the Array:")
print(arr.strides)"""

def p9():
    return """import pandas as pd
data = {
 'Name': ['Steve', 'Lia', 'Vin', 'Katie', 'John', 'Anna', 'Mike'],
 'Age': [32, 28, 45, 38, 41, 29, 35],
 'Gender': ['Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male'],
 'Rating': [3.45, 4.6, 3.9, 2.78, 4.1, 3.8, 3.95],
 'Department': ['IT', 'Finance', 'HR', 'Marketing', 'IT', 'Finance', 'IT']
}
df = pd.DataFrame(data)
print("Original DataFrame:")
print(df)
print("\n.head(): Returns the first 3 rows:")
print(df.head(3))
print("\n.tail(): Returns the last 2 rows:")
print(df.tail(2))
print("\n.info(): Provides DataFrame summary:")
print(df.info())
print("\n.describe(): Generates descriptive statistics:")
print(df.describe())
print("\n.sort_values(): Sorts by 'Age' in ascending order:")
print(df.sort_values(by='Age'))
print("\n.groupby(): Groups by 'Department' and calculates mean age:")
print(df.groupby('Department')['Age'].mean())
print("\n.apply(): Applies lambda function to double 'Rating':")
df['Double_Rating'] = df['Rating'].apply(lambda x: x * 2)
print(df)
print("\n.drop(): Drops 'Double_Rating' column:")
df = df.drop(columns=['Double_Rating'])
print(df)
print("\n.pivot_table(): Creates a pivot table of average age by 'Gender':")
pivot_table = pd.pivot_table(df, values='Age', index='Gender', aggfunc='mean')
print(pivot_table)
print("\n.concat(): Concatenates two DataFrames along rows:")
df1 = df.head(3)
df2 = df.tail(4)
concatenated_df = pd.concat([df1, df2])
print(concatenated_df)"""

def p10():
    return """import matplotlib.pyplot as plt
import pandas as pd
import datetime
data = {
 'Date': pd.date_range(start='2025-01-01', periods=10),
 'Temperature': [20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
}
df = pd.DataFrame(data)
plt.figure(figsize=(10, 6))
plt.plot(df['Date'], df['Temperature'], marker='o', linestyle='-', color='b', label='Temperature')
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.title('Date vs Temperature')
plt.grid(True)
plt.gcf().autofmt_xdate()
plt.legend()
plt.show()"""

