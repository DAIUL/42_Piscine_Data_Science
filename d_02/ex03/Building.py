import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import pandas as pd


def main():
	engine = create_engine('postgresql+psycopg2://qpuig:mysecretpassword@localhost:5432/piscineds')

	query_frequency = """
		select
			user_id,
			count(*) as purchase_count
		from customers
		where event_type = 'purchase'
		group by user_id;
"""

	query_spent = """
	select
		user_id,
		sum(price) as total_spent
	from customers
	where event_type = 'purchase'
	group by user_id
	order by total_spent;
"""

	df_frequency = pd.read_sql(query_frequency, engine)
	df_spent = pd.read_sql(query_spent, engine)

	sns.set_theme(style='whitegrid')
	
	sns.histplot(data=df_frequency, x='purchase_count', bins=5, binrange=(1, 39))
	plt.xticks(range(0, 40, 10))
	plt.ylabel("customers")
	plt.xlabel("frequency")
	plt.show()

	sns.histplot(data=df_spent, x='total_spent', bins=5, binrange=(-25, 225))
	plt.xticks(range(0, 250, 50))
	plt.xlabel("monetary value")
	plt.ylabel("customers")
	plt.show()

if __name__ == '__main__':
	main()