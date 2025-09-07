import copy

active_students = ["Naveed", "Waqas", "Asif"]


new_active_students = copy.copy(active_students)

new_active_students.append("Ali")
new_active_students.append("Kamran")

print("Original list:", active_students)
print("Newly Active copy of the list:", new_active_students)