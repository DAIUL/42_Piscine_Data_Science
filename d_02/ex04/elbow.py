import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sqlalchemy import create_engine
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


def main():
	engine = create_engine('postgresql+psycopg2://qpuig:mysecretpassword@localhost:5432/piscineds')

	query = """
	select 
		spend.user_id,
		spend.total_spent,
		freq.frequency,
		avg_spent.average_spent
	from (
		select
			user_id,
			sum(price) as total_spent
		from customers
		where event_type = 'purchase'
		group by user_id
	) as spend
	join (
		select
			user_id,
			count(*) as frequency
		from customers
		where event_type = 'purchase'
		group by user_id
	) as freq
	on spend.user_id = freq.user_id
	join (
		select
			user_id,
			avg(price) as average_spent
		from customers
		where event_type = 'purchase'
		group by user_id
	) as avg_spent
	on spend.user_id = avg_spent.user_id;
"""

	df = pd.read_sql(query, engine)
	X = df[['total_spent', 'frequency', 'average_spent']]

	scaler = StandardScaler()
	X_scaler = scaler.fit_transform(X)

	inertias = []
	K_range = range(1, 11)

	for k in K_range:
		kmeans = KMeans(n_clusters=k, random_state=42)
		kmeans.fit(X_scaler)
		inertias.append(kmeans.inertia_)

	sns.set_theme(style='whitegrid')

	sns.lineplot(x=K_range, y=inertias)
	plt.show()



if __name__ == '__main__':
	main()