-- 1)	Список клиентов с общей суммой их покупок
SELECT c.user_name as `Клиент`, sum(p.price) as `Общая сумма покупок`
FROM orders o
    LEFT JOIN clients c on o.id_users = c.id_users
    LEFT JOIN products p on o.id_product = p.id_product
GROUP BY c.id_users;

-- 2)	Список клиентов, которые купили телефон
SELECT c.user_name as `Клиент`
FROM clients c, orders o, products p
    WHERE o.id_product = p.id_product
    AND o.id_users = c.id_users
    AND p.product_name = 'Телефон'
GROUP BY c.id_users;

-- 3)	Список товаров с количеством их заказов
SELECT p.product_name as `Товар`, count(o.id_product) as `Количество заказов`
FROM products p, orders o
WHERE p.id_product = o.id_product
GROUP BY o.id_product

