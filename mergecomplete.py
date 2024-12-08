import pandas as pd

# Load the data
file1_path = 'new_lon_lat.csv'
file2_path = 'LonLATs.csv'

df1 = pd.read_csv(file1_path)
df2 = pd.read_csv(file2_path)

# Merge the data on common columns
common_columns = ['State', 'LGA', 'Ward', 'PU-Code', 'PU-Name']
merged_df = pd.merge(df1, df2, on=common_columns, suffixes=('_file1', '_file2'))

# Fill missing values in file1's Latitude and Longitude using file2's values
merged_df['Latitude_file1'].fillna(merged_df['Latitude_file2'], inplace=True)
merged_df['Longitude_file1'].fillna(merged_df['Longitude_file2'], inplace=True)

# Drop the extra columns
merged_df = merged_df[[col for col in merged_df.columns if not col.endswith('_file2')]]

# Rename columns to original names
merged_df.rename(columns={'Latitude_file1': 'Latitude', 'Longitude_file1': 'Longitude'}, inplace=True)

# Save the result to a new CSV file
merged_df.to_csv(r'C:\Users\TECH 23\PycharmProjects\HNG_Project\Real_lon_lat.csv', index=False)
