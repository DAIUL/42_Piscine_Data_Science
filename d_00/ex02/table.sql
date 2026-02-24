create table data_2022_oct (
	event_time timestamptz,
	event_type event_type_enum,
	product_id bigint,
	price numeric(10, 2),
	user_id int,
	user_session uuid,
	id serial primary key
);

\copy data_2022_oct(event_time, event_type, product_id, price, user_id, user_session) from '/Users/daiul/Documents/Code/42/piscine_data_science/d_00/ex02/data_2022_oct.csv' with (format csv, header true);