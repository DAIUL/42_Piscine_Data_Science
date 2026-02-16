drop table if exists items;	
create table items (
	product_id int,
	category_id bigint,
	category_code text,
	brand text
);

\copy items(product_id, category_id, category_code, brand) from '/Users/daiul/Documents/Code/42/piscine_data_science/d_00/ex04/item.csv' with (format csv, header true);

select count(*) from items;