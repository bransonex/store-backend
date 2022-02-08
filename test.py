# dictionary

def print_name():
    print("Kvon Smith")
    

about_me = {
    "name": "Kvon",
    "last": "Smith",
    "age": "29",
    "hobbies": [],
    "address": {
        "street": "Windy Hill Rd",
        "number": "2377",
        "city": "Riverside", 
    }
}

print ( about_me["name"])

# using string formating, print the full name (first last)
print(f"{about_me['name']} {about_me['last']}")

