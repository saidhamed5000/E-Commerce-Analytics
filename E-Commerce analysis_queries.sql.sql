select * from customers;
select * from products;
select * from orders;
select * from items;
select * from payments;
select * from sellers;
select * from reviews;
select * from geo;
select * from translation;

-- counting total unique orders and unique customers
select COUNT(distinct order_id ) as total_orders 
from orders


--distribution of unique orders by status
select 
order_status,
count(distinct order_id)as count_status
from Orders 
group by order_status
order by count_status desc


--calculating total and average payment values
select 
round(SUM(payment_value),0) as total_paymens,
round(AVG (payment_value),0) as average_order_value
from payments

--top 5 states by number of unique customers
select top 5
customer_state,
count(distinct customer_id) as customer_count
from customers
group by customer_state
order by customer_count desc


--top 10 product categories by total revenue
select top 10 
product_category_name_english,
round(sum(price),0)as total_revenue
from items i
join products p on i.product_id=p.product_id
join translation t on p.product_category_name=t.product_category_name
group by product_category_name_english
order by total_revenue desc


-- payment methods by unique order count and total value
select
 payment_type,
 count( order_id)as order_count,
 round(SUM(payment_value),0) as total_paymens
 from payments
 group by payment_type
 order by  total_paymens desc


 --average review score for  orders
 select 
 order_status,
 avg(review_score) as average_score,
 count(review_id) as total_reviews
 from Orders o
 join reviews r on o.order_id=r.order_id
 group by order_status
 order by average_score desc


 --count of  sellers in each state
 select 
 seller_state,
 count(seller_id) as sellers_count
 from sellers
 group by seller_state
 order by sellers_count desc

 -- top 10 customers by revenue
select top 10
customer_id,
sum(payment_value)as total_paymens
from Orders o
join payments p on o.order_id=p.order_id
group by customer_id
order by total_paymens desc



-- full order details
select 
o.order_id,
o.order_status,
c.customer_state,
i.price,
p.payment_value,
r.review_score
from Orders o
join customers c on o.customer_id=c.customer_id
join items i on o.order_id=i.order_id
join payments p on o.order_id=p.order_id
join reviews r on o.order_id=r.order_id

-- Time Analysis
-- orders per year
select 
YEAR(order_purchase_timestamp) as year,
count(order_id) as total_orders
from Orders
group by YEAR(order_purchase_timestamp)
order by total_orders desc


-- orders per month(1)
select 
month(order_purchase_timestamp) as month,
count(order_id) as total_orders
from Orders
group by month(order_purchase_timestamp)
order by total_orders desc


-- orders per month every year(2)
select 
format(order_purchase_timestamp,'MM-yyy') as month,
count(order_id) as total_orders
from Orders
group by format(order_purchase_timestamp,'MM-yyy')
order by month


-- orders by hour of day
select 
datepart(HOUR,order_purchase_timestamp) as hour,
count(order_id) as total_orders
from Orders
group by datepart(HOUR,order_purchase_timestamp)
order by hour

--orders with payments higher than 4000
select 
    order_id, 
    sum(payment_value) as total_order_value
from payments
group by order_id
having sum(payment_value) > 4000
order by total_order_value desc


--analyzing orders with low review scores
select 
    review_score, 
    avg(freight_value) as avg_freight_cost,
    count(o.order_id) as total_orders
from orders o
join reviews r on o.order_id = r.order_id
join items i on o.order_id = i.order_id
where r.review_score <= 3
group by r.review_score
