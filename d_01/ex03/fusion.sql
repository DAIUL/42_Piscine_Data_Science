alter table customers
add column category_id bigint,
add column category_code text,
add column brand text;

update customers c
set
	category_id = i.category_id,
	category_code = i.category_code,
	brand = i.brand
from items i 
where c.product_id = i.product_id;