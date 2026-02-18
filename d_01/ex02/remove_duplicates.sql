delete from customers
where id in (
	select id
	from (
		select
			id,
			event_time,
			event_type,
			product_id,
			user_id,
			lag(event_time) over(
				partition by event_type, product_id, user_id, user_session order by event_time
			) as previous_time
			from customers
	) sub
	where previous_time is not null
		and event_time - previous_time <= interval '1 second'
);