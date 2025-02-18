---Створення таблиці Products
CREATE TABLE Products (
    product_id INTEGER PRIMARY KEY,
    name TEXT,
    category TEXT,
    price NUMERIC(10,2)
	);

----Заповнення таблиці Products
INSERT INTO Products (product_id, name, category, price) VALUES
(1, 'Laptop', 'Electronics', 999.99),
(2, 'Smartphone', 'Electronics', 799.99),
(3, 'Headphones', 'Electronics', 199.99),
(4, 'Mouse', 'Accessories', 49.99),
(5, 'Keyboard', 'Accessories', 89.99);

---Створення таблиці Customers
CREATE TABLE Customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT,
    city TEXT
);

----Заповнення таблиці Customers
INSERT INTO Customers (customer_id, name, city) VALUES
(1, 'John Doe', 'Kyiv'),
(2, 'Jane Smith', 'Lviv'),
(3, 'Bob Johnson', 'Kyiv');

---Створення таблиці Orders
CREATE TABLE Orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

----Заповнення таблиці Orders
INSERT INTO Orders (order_id, customer_id, product_id, quantity) VALUES
(1, 1, 1, 2),
(2, 1, 2, 1),
(3, 2, 1, 1),
(4, 3, 3, 3),
(5, 2, 2, 2);


----Запит 1
SELECT 
    p.category,
    COUNT(o.order_id) as total_orders,
    SUM(o.quantity) as total_quantity,
    ROUND(AVG(p.price * o.quantity), 2) as avg_order_value
FROM Products p
JOIN Orders o ON p.product_id = o.product_id
GROUP BY p.category;

---- Запит 2
SELECT 
    c1.name as customer1,
    c2.name as customer2,
    c1.city
FROM Customers c1
JOIN Customers c2 ON c1.city = c2.city AND c1.customer_id < c2.customer_id;

---- Запит 3
SELECT 
    p.name as product_name,
    COALESCE(COUNT(o.order_id), 0) as orders_count,
    COALESCE(SUM(o.quantity), 0) as total_quantity
FROM Products p
LEFT JOIN Orders o ON p.product_id = o.product_id
GROUP BY p.name;

---- Запит 4
SELECT 
    c.name,
    o.order_id,
    p.name as product_name,
    o.quantity
FROM Customers c
LEFT JOIN Orders o ON c.customer_id = o.customer_id
LEFT JOIN Products p ON o.product_id = p.product_id
UNION ALL
SELECT 
    c.name,
    o.order_id,
    p.name as product_name,
    o.quantity
FROM Orders o
RIGHT JOIN Customers c ON c.customer_id = o.customer_id
RIGHT JOIN Products p ON o.product_id = p.product_id
WHERE c.customer_id IS NULL;



