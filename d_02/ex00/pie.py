import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns


def main():
	engine = create_engine('postgresql+psycopg2://qpuig:mysecretpassword@localhost:5432/piscineds')

	query = """
		select event_type, count(*) as count
		from customers
		group by event_type
		order by count desc;
	"""

	df = pd.read_sql(query, engine)

	sns.set_theme(style='whitegrid')

	plt.pie(
		df['count'],
		labels=df['event_type'],
		autopct='%1.1f%%'
	)

	plt.show()


if __name__ == '__main__':
	main()