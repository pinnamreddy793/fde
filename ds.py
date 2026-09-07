#Data Structures
import pandas as pd

#Print the data
def display_items(x):
    if isinstance(x, dict):
        for i in x:
            print(f"{i}: {x[i]}")
        print("\n")
    else:
        for i in x:
            print(i)
        print("\n")
    return None;

# Lists
print("\nLists\n")

sl = ["apple", "mango", "plum", "grape", "apple", "pineapple"]
print(f"Shopping List: {sl}\n")
sorted_sl = sorted(sl)
reverse_sl = sorted(sl, reverse=True)

todo = ["buy milk", "buy eggs", "buy bread", "clean sheets", "water plants"]
completed = ["buy milk", "buy eggs"]

print(f"Todo: {todo}")
print(f"Completed: {completed}\n")

todo.append("buy fruits")
completed.append("buy fruits")
print(f"Todo added: {todo}")
print(f"Completed added: {completed}")

completed.remove("buy milk")
print(f"Completed removed: {completed}")
completed[1] = "buy oranges"
print(f"Completed updated: {completed}\n")

print("Data Frames\n")
df = pd.DataFrame(sl, columns=["Shopping List"])
df.rename(columns={"Shopping List": "Items"}, inplace=True)
df["sorted"] = sorted_sl
df["reverse"] = reverse_sl
print(f"{df} \n")
print(df.transpose())

# Dictonaries

print("\nDictionaries\n")

grades = {"John": 90, "Alice": 85, "Bob": 92, "Eve": 88}
print(f"Grades: {grades}\n")

print(f"John's grade: {grades['John']}")
print(f"Eve's grade: {grades['Eve']}\n")

grades["Alex"] = 95
print(f"Grades added  : {grades}")

grades["Alice"] = 89
print(f"Grades updated: {grades}\n")

phonebook = {"John": "123-456-7890", "Alice": "987-654-3210", "Bob": "555-555-5555"}
print(f"Phonebook: {phonebook}")

phonebook["Eve"] = "111-222-3333"
phonebook["Charlie"] = "987-654-3210"  
print(f"Phonebook updated: {phonebook}\n")

print(f"John's phone number: {phonebook['John']}")
print(f"Alice's phone number: {phonebook['Alice']}")
print(f"Charlie's phone number: {phonebook['Charlie']}\n")

phonebook["John"] = "234-567-8901"
phonebook["Alice"] = phonebook["Alice"].replace("987", "999")
phonebook["Charlie"] = phonebook["Bob"]

print(f"Phonebook after updates:")
display_items(phonebook)

phonebook.pop("Bob")
print("Updated Phonebook after removing Bob:")
display_items(phonebook)

# Sets
print("\nSets\n")
visitors = {"John": 5, "Alice": 3, "Bob": 8, "Eve": 2, "David": 6, "John": 5}
print(f"Visitors: {visitors}\n")
visitors["Alice"] += 2
print(f"Visitors updated: {visitors}\n")
visitors["Charlie"] = 4
visitors["Eve"] = 0
visitors.pop("Bob")
print("Visitors after adding Charlie and updating Eve and removing Bob:") 
display_items(visitors)

print(f"Length of visitors: {len(visitors)}")

# Tuples
print("\nTuples\n")

tupleA = (1, 2, 3, 4, 5)
print(f"TupleA: {tupleA}")

coordinates = (10, 20)
print(f"Coordinates: {coordinates}")
print(f"X coordinate: {coordinates[0]}, Y coordinate: {coordinates[1]}\n")

updated_coordinates = coordinates + (30, 40)
print(f"Updated Coordinates with Reassignment: {updated_coordinates}\n")

