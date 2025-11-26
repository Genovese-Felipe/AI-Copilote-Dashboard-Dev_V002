import pandas as pd
import numpy as np

def generate_data():
    """
    Generates a synthetic dataset of incident records.

    This function creates a pandas DataFrame with randomly generated data
    simulating incident reports across various categories, causes, sites,
    and time periods.

    Returns:
        pandas.DataFrame: A DataFrame containing the synthetic incident data.
    """
    print("🔄 Generating synthetic incident data...")

    categories = ['Security', 'Equipment', 'Customer', 'Transport', 'Complaint', 'Spill', 'Injury', 'Divergence']
    causes = ['Procedure', 'Design', 'Training', 'External', 'Management', 'Equipment', 'Personnel', 'Material']
    sites = ['Weston', 'Shirley', 'Lincoln', 'Hudson', 'Concord', 'Bolton', 'Maynard', 'Acton']
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    years = [2007, 2008, 2009]
    severities = ['Critical', 'Major', 'Medium', 'Near Miss']
    status = ['Open', 'Closed']

    np.random.seed(42)
    records = []

    for year in years:
        for month in months:
            for site in sites:
                for category in categories:
                    for cause in np.random.choice(causes, size=2, replace=False):
                        severity = np.random.choice(severities, p=[0.05, 0.15, 0.35, 0.45])
                        stat = np.random.choice(status, p=[0.3, 0.7])
                        count = np.random.poisson(lam=6) + 1
                        records.append({
                            'Category': category,
                            'Cause': cause,
                            'Site': site,
                            'Month': month,
                            'Year': year,
                            'Severity': severity,
                            'Status': stat,
                            'Count': count
                        })

    df = pd.DataFrame(records)
    print(f"✅ Generated {len(df)} records with {df['Count'].sum()} total incidents")
    return df