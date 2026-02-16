from pathlib import Path
import psycopg2


def main():
	conn = psycopg2.connect(
    host="localhost",
    database="piscineds",
    user="qpuig",
    password="mysecretpassword"
	)
	cur = conn.cursor()
	# cur.execute(f"""create type if not exists event_type_enum as enum ('cart','view', 'purchase', 'remove_from_cart');""")
	# conn.commit()

	dir_path = '../../../42_subjects/piscine_data_science/d_00/subject/customer/'
	path = Path(dir_path)
	csv_files = list(path.glob('*.csv'))

	for file in csv_files:
		cur.execute(f"""create table if not exists {file.stem} (
			event_time TIMESTAMPTZ,
			event_type event_type_enum,
			product_id INTEGER,
			price NUMERIC,
			user_id INTEGER,
			user_session UUID,
			id SERIAL PRIMARY KEY
		);""")
		cur.execute(f"""copy {file.stem} (event_time, event_type, product_id, price, user_id, user_session)
		from '/subjects/d_00/subject/customer/{file.name}'
		csv header;""")
	conn.commit()
	cur.close()
	conn.close()

if __name__ == '__main__':
	main()