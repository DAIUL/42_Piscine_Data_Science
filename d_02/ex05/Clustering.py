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
        user_id,
        sum(price) as total_spent,
        count(*) as frequency,
        avg(price) as average_spent,
        extract(day from (timestamp '2023-03-01' - max(event_time))) as recency
    from customers
    where event_type = 'purchase'
    group by user_id;
"""
    df = pd.read_sql(query, engine)
    X = df[['total_spent', 'frequency', 'average_spent', 'recency']]

    cluster_names = {
        0 : 'Gold',
        1 : 'Silver',
        2 : 'New customer',
        3 : 'inactive'
    }

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=4, random_state=42)
    kmeans.fit(X_scaled)
    df['cluster'] = kmeans.labels_

    df_count = df['cluster'].value_counts().reset_index()
    df_count.columns = ['cluster', 'count']
    df_count['cluster_names'] = df_count['cluster'].map(cluster_names)
    df_count['median_recency'] = df.groupby('cluster')['recency'].median()
    df_count['median_frequency'] = df.groupby('cluster')['frequency'].median()
    df_count['average_spent'] = df.groupby('cluster')['average_spent'].mean()

    sns.set_theme(style='whitegrid')
    
    sns.barplot(data=df_count, x='count', y='cluster_names', orient='h', hue='cluster_names')
    plt.xlabel("number of customers")
    plt.show()

    sns.scatterplot(data=df_count, x='median_recency', y='median_frequency', size='average_spent', hue='cluster', sizes=(500, 1000), alpha=0.7, legend=False)
    plt.show()


if __name__ == '__main__':
    main()