CREATE TABLE IF NOT EXISTS Category (
    ROWguid UUID DEFAULT gen_random_uuid(),
    ModifiedDate TIMESTAMP DEFAULT now(),

    CategoryID INTEGER PRIMARY KEY,
    CategoryName VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS Customer (
    ROWguid UUID DEFAULT gen_random_uuid(),
    ModifiedDate TIMESTAMP DEFAULT now(),

    CustomerID INTEGER PRIMARY KEY,
    CustomerFirstName VARCHAR(50) NOT NULL,
    CustomerLastName VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS Product (
    ROWguid UUID DEFAULT gen_random_uuid(),
    ModifiedDate TIMESTAMP DEFAULT now(),

    ProductID INTEGER PRIMARY KEY,
    ProductName VARCHAR(50) NOT NULL,
    ProductPrice INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS ProductCategory (
    ROWguid UUID DEFAULT gen_random_uuid(),
    ModifiedDate TIMESTAMP DEFAULT now(),

    ProductCategoryID INTEGER PRIMARY KEY,
    CategoryID INTEGER NOT NULL,
    ProductID INTEGER NOT NULL,

    FOREIGN KEY (CategoryID) REFERENCES Category(CategoryID),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);

CREATE TABLE IF NOT EXISTS Receipt (
    ROWguid UUID DEFAULT gen_random_uuid(),
    ModifiedDate TIMESTAMP DEFAULT now(),

    ReceiptID INTEGER PRIMARY KEY,
    CustomerID INTEGER NOT NULL,
    TotalPrice INTEGER NOT NULL,
    CompletedDate TIMESTAMP NOT NULL,

    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
);

CREATE TABLE IF NOT EXISTS ReceiptItem (
    ROWguid UUID DEFAULT gen_random_uuid(),
    ModifiedDate TIMESTAMP DEFAULT now(),

    ReceiptItemID INTEGER PRIMARY KEY,
    ReceiptID INTEGER NOT NULL,
    ProductID INTEGER NOT NULL,
    ActualPrice INTEGER NOT NULL,
    Amount INTEGER NOT NULL,

    FOREIGN KEY (ReceiptID) REFERENCES Receipt(ReceiptID),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);
