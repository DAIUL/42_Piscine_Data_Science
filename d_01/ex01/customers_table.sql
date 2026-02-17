drop table if exists customers;
create table customers (
	event_time timestamptz,
	event_type event_type_enum,
	product_id int,
	price numeric(10,2),
	user_id int,
	user_session uuid,
	id serial primary key
);

insert into customers (event_time, event_type, product_id, price, user_id, user_session)
select event_time, event_type, product_id, price, user_id, user_session
from data_2022_dec
union all
select event_time, event_type, product_id, price, user_id, user_session
from data_2022_nov
union all
select event_time, event_type, product_id, price, user_id, user_session
from data_2022_oct
union all
select event_time, event_type, product_id, price, user_id, user_session
from data_2023_jan
union all
select event_time, event_type, product_id, price, user_id, user_session
from data_2023_feb;

select count(*) from customers;