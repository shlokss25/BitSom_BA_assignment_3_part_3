import requests
from datetime import datetime

# -------------------------------
# TASK 1: FILE WRITE & READ
# -------------------------------

def file_operations():
    try:
        # Writing initial notes
        with open("python_notes.txt", "w", encoding="utf-8") as f:
            f.write("Topic 1: Variables store data. Python is dynamically typed.\n")
            f.write("Topic 2: Lists are ordered and mutable.\n")
            f.write("Topic 3: Dictionaries store key-value pairs.\n")
            f.write("Topic 4: Loops automate repetitive tasks.\n")
            f.write("Topic 5: Exception handling prevents crashes.\n")
        print("File written successfully.")

        # Appending extra lines
        with open("python_notes.txt", "a", encoding="utf-8") as f:
            f.write("Topic 6: Functions help reuse code.\n")
            f.write("Topic 7: APIs allow communication between systems.\n")
        print("Lines appended successfully.")

        # Reading file
        with open("python_notes.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()

        print("\nReading file:\n")
        for i, line in enumerate(lines, start=1):
            print(f"{i}. {line.strip()}")

        print(f"\nTotal lines: {len(lines)}")

        # Keyword search
        keyword = input("\nEnter keyword to search: ").lower()
        found = False

        for line in lines:
            if keyword in line.lower():
                print(line.strip())
                found = True

        if not found:
            print("No matching lines found.")

    except Exception as e:
        log_error("file_operations", str(e))


# -------------------------------
# LOGGER FUNCTION
# -------------------------------

def log_error(function_name, message):
    with open("error_log.txt", "a") as log:
        time = datetime.now()
        log.write(f"[{time}] ERROR in {function_name}: {message}\n")


# -------------------------------
# TASK 2: API FUNCTIONS
# -------------------------------

def fetch_products():
    url = "https://dummyjson.com/products?limit=20"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        print("\nProduct List:\n")
        print("ID | Title | Category | Price | Rating")
        print("-" * 60)

        for p in data["products"]:
            print(f"{p['id']} | {p['title']} | {p['category']} | ${p['price']} | {p['rating']}")

        return data["products"]

    except requests.exceptions.ConnectionError:
        print("Connection failed.")
        log_error("fetch_products", "ConnectionError")

    except requests.exceptions.Timeout:
        print("Request timed out.")
        log_error("fetch_products", "Timeout")

    except Exception as e:
        print(e)
        log_error("fetch_products", str(e))


def filter_products(products):
    try:
        filtered = [p for p in products if p["rating"] >= 4.5]
        filtered.sort(key=lambda x: x["price"], reverse=True)

        print("\nFiltered Products:\n")
        for p in filtered:
            print(f"{p['title']} - ${p['price']} (Rating: {p['rating']})")

    except Exception as e:
        log_error("filter_products", str(e))


def fetch_laptops():
    url = "https://dummyjson.com/products/category/laptops"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        print("\nLaptops:\n")
        for p in data["products"]:
            print(f"{p['title']} - ${p['price']}")

    except Exception as e:
        log_error("fetch_laptops", str(e))


def add_product():
    url = "https://dummyjson.com/products/add"
    product = {
        "title": "My Custom Product",
        "price": 999,
        "category": "electronics",
        "description": "A product I created via API"
    }

    try:
        response = requests.post(url, json=product, timeout=5)
        print("\nPOST Response:\n", response.json())

    except Exception as e:
        log_error("add_product", str(e))


# -------------------------------
# TASK 3: EXCEPTION HANDLING
# -------------------------------

def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except TypeError:
        return "Error: Invalid input types"


def read_file_safe(filename):
    try:
        with open(filename, "r") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    finally:
        print("File operation attempt complete.")


# -------------------------------
# INPUT LOOP
# -------------------------------

def product_lookup():
    while True:
        user_input = input("\nEnter product ID (1-100) or 'quit': ")

        if user_input.lower() == "quit":
            break

        if not user_input.isdigit():
            print("Invalid input. Enter a number.")
            continue

        pid = int(user_input)

        if pid < 1 or pid > 100:
            print("Out of range.")
            continue

        try:
            url = f"https://dummyjson.com/products/{pid}"
            res = requests.get(url, timeout=5)

            if res.status_code == 404:
                print("Product not found.")
                log_error("lookup_product", "404 Not Found")

            else:
                data = res.json()
                print(f"{data['title']} - ${data['price']}")

        except Exception as e:
            log_error("lookup_product", str(e))


# -------------------------------
# FORCE ERROR LOGGING
# -------------------------------

def trigger_errors():
    try:
        requests.get("https://this-host-does-not-exist-xyz.com/api", timeout=5)
    except Exception as e:
        log_error("forced_connection", str(e))

    try:
        res = requests.get("https://dummyjson.com/products/999", timeout=5)
        if res.status_code != 200:
            log_error("forced_404", "Product 999 not found")
    except Exception as e:
        log_error("forced_404", str(e))


def show_logs():
    try:
        with open("error_log.txt", "r") as f:
            print("\nError Logs:\n")
            print(f.read())
    except:
        print("No logs found.")


# ========================
#      MAIN
# ========================
if __name__ == "__main__":
    file_operations()

    products = fetch_products()
    if products:
        filter_products(products)

    fetch_laptops()
    add_product()

    print("\nSafe Divide Tests:")
    print(safe_divide(10, 2))
    print(safe_divide(10, 0))
    print(safe_divide("ten", 2))

    print("\nFile Read Test:")
    print(read_file_safe("python_notes.txt"))
    read_file_safe("ghost_file.txt")

    product_lookup()

    trigger_errors()
    show_logs()