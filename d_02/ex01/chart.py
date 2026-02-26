import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from sqlalchemy import create_engine
import pandas as pd


def average_spend(df):
	daily_customer = df.groupby(df['event_time'].dt.date)['user_id'].nunique().reset_index()
	average_spend = df.groupby(df['event_time'].dt.date)['price'].sum().reset_index()
	daily_stats = pd.merge(daily_customer, average_spend, on='event_time')
	daily_stats['daily_spend'] = daily_stats['price'] / daily_stats['user_id']
	plt.fill_between(daily_stats['event_time'], daily_stats['daily_spend'])
	sns.lineplot(data=daily_stats, x='event_time', y='daily_spend')
	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b'))
	plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
	plt.xticks(rotation=45)
	plt.ylabel('average spend/customers')
	plt.show()

def total_sales(df):
	monthly_revenue = df.groupby(df['event_time'].dt.to_period('M'))['price'].sum().reset_index()
	monthly_revenue['month'] = monthly_revenue['event_time'].dt.strftime('%b')
	monthly_revenue['revenue_M'] = monthly_revenue['price'] / 1_000_000
	sns.barplot(data=monthly_revenue, x='month', y='revenue_M')
	plt.ylabel('Total sales in million')
	plt.show()

def number_customers(df):
	daily_customers = df.groupby(df['event_time'].dt.date)['user_id'].nunique().reset_index()
	sns.lineplot(data=daily_customers, x='event_time', y='user_id')
	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b'))
	plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
	plt.xticks(rotation=45)
	plt.ylabel('number of customers')
	plt.show()


def main():
	engine = create_engine('postgresql+psycopg2://qpuig:mysecretpassword@localhost:5432/piscineds')

	query = """
		select
			event_time,
			event_type,
			user_id,
			price
		from customers
		where event_type = 'purchase';
	"""

	df = pd.read_sql(query, engine)

	number_customers(df)
	total_sales(df)
	average_spend(df)

if __name__ == '__main__':
	main()