import psycopg2
import random
import datetime
import uuid

def random_datetime():
    start = datetime.datetime.strptime('2025-09-29 00:00', '%Y-%m-%d %H:%M')
    end = datetime.datetime.strptime('2025-11-02 23:59', '%Y-%m-%d %H:%M')
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return str(start + datetime.timedelta(seconds=random_second))

def gen_uuid():
    return uuid.uuid1()

db_config_west = {
    "dbname": "west_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5446"
}

db_config_east = {
    "dbname": "east_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5447"
}

conn_west = psycopg2.connect(**db_config_west)
cur_west = conn_west.cursor()
conn_east = psycopg2.connect(**db_config_east)
cur_east = conn_east.cursor()

categories = ["fruits", "beverages", "electronics", "vegetables", "dairy"]
for ID in range(len(categories)):
    cur_west.execute("INSERT INTO Category (ROWguid, CategoryID, CategoryName) "
                     "VALUES (%s, %s, %s)",
                     (str(gen_uuid()), ID, categories[ID]))
    cur_east.execute("INSERT INTO Category (ROWguid, CategoryID, CategoryName) "
                     "VALUES (%s, %s, %s)",
                     (str(gen_uuid()), ID, categories[ID]))

customers = ["Adam", "Boris", "Charlie", "David", "Ethan",
             "Florian", "Gerald", "Hilbert", "Ian", "John",
             "Kevin", "Lucas", "Martin", "Noah", "Opal",
             "Peter", "Quinsy", "Roger", "Samuel", "Thomas",
             "Uriel", "Victor", "Wesley", "Xavier", "Yvonne",
             "Zachary"]
for ID in range(len(customers)):
    cur_west.execute("INSERT INTO Customer (ROWguid, CustomerID, CustomerFirstName, CustomerLastName) "
                     "VALUES (%s, %s, %s, %s)",
                     (str(gen_uuid()), ID, customers[ID], "West"))
    cur_east.execute("INSERT INTO Customer (ROWguid, CustomerID, CustomerFirstName, CustomerLastName) "
                     "VALUES (%s, %s, %s, %s)",
                     (str(gen_uuid()), ID, customers[ID], "East"))

products = [["apple", "banana", "kiwi", "mango", "pear"],
            ["coffee", "cola", "pepsi", "tea", "water"],
            ["camera", "gaming console", "fryer", "TV", "vacuum cleaner"],
            ["cucumber", "garlic", "onion", "pumpkin", "tomato"],
            ["cheese", "cream", "milk", "milkshake", "yoghurt"]]
product_prices = [[10, 7, 25, 20, 15],
                  [30, 10, 12, 20, 5],
                  [300, 450, 200, 700, 450],
                  [5, 8, 7, 32, 10],
                  [35, 45, 18, 42, 24]]
for categoryID in range(len(categories)):
    for productIDinCaterogy in range(len(products[categoryID])):
        ID = categoryID * 5 + productIDinCaterogy
        cur_west.execute("INSERT INTO Product (ROWguid, ProductID, ProductName, ProductPrice) "
                         "VALUES (%s, %s, %s, %s)",
                         (str(gen_uuid()), ID, products[categoryID][productIDinCaterogy],
                          product_prices[categoryID][productIDinCaterogy]))
        cur_west.execute("INSERT INTO ProductCategory (ROWguid, ProductCategoryID, CategoryID, ProductID) "
                         "VALUES (%s, %s, %s, %s)",
                         (str(gen_uuid()), ID, categoryID, ID))
        cur_east.execute("INSERT INTO Product (ROWguid, ProductID, ProductName, ProductPrice) "
                         "VALUES (%s, %s, %s, %s)",
                         (str(gen_uuid()), ID, products[categoryID][productIDinCaterogy],
                          product_prices[categoryID][productIDinCaterogy]))
        cur_east.execute("INSERT INTO ProductCategory (ROWguid, ProductCategoryID, CategoryID, ProductID) "
                         "VALUES (%s, %s, %s, %s)",
                         (str(gen_uuid()), ID, categoryID, ID))

customerIDs = [i for i in range(len(customers))]
random.shuffle(customerIDs)
receiptIDWest = 0
receiptItemIDWest = 0
receiptIDEast = 0
receiptItemIDEast = 0
parity = 0
for customerID in customerIDs:
    for receipt in range(random.randint(2, 8)):
        products_count = random.randint(1, 3)
        items = []
        total_price = 0
        completed_datetime = random_datetime()
        for _ in range(products_count):
            categoryID = random.randint(0, 4)
            productIDinCaterogy = random.randint(0, 4)
            productID = categoryID * 5 + productIDinCaterogy
            price = product_prices[categoryID][productIDinCaterogy]
            discount = random.randint(0, 20) # in %
            actual_price = price * (100 - discount) // 100
            if categoryID != 2:
                amount = random.randint(1, 12)
            else:
                amount = 1
            items.append([productID, actual_price, amount])
            total_price += actual_price * amount
        if parity == 0:
            cur_west.execute("INSERT INTO Receipt (ROWguid, ReceiptID, CustomerID, TotalPrice, CompletedDate) "
                             "VALUES (%s, %s, %s, %s, %s)",
                             (str(gen_uuid()), receiptIDWest, customerID, total_price, completed_datetime))
            for item in items:
                cur_west.execute("INSERT INTO ReceiptItem (ROWguid, ReceiptItemID, ReceiptID, ProductID, ActualPrice, Amount)"
                                 "VALUES (%s, %s, %s, %s, %s, %s)",
                                 (str(gen_uuid()), receiptItemIDWest, receiptIDWest, item[0], item[1], item[2]))
                receiptItemIDWest += 1
            receiptIDWest += 1
            parity = 1
        else:
            cur_east.execute("INSERT INTO Receipt (ROWguid, ReceiptID, CustomerID, TotalPrice, CompletedDate) "
                             "VALUES (%s, %s, %s, %s, %s)",
                             (str(gen_uuid()), receiptIDEast, customerID, total_price, completed_datetime))
            for item in items:
                cur_east.execute("INSERT INTO ReceiptItem (ROWguid, ReceiptItemID, ReceiptID, ProductID, ActualPrice, Amount)"
                                 "VALUES (%s, %s, %s, %s, %s, %s)",
                                 (str(gen_uuid()), receiptItemIDEast, receiptIDEast, item[0], item[1], item[2]))
                receiptItemIDEast += 1
            receiptIDEast += 1
            parity = 0

conn_west.commit()
conn_east.commit()
cur_west.close()
cur_east.close()
conn_west.close()
conn_east.close()
print("All done!")
