import pandas as pd

# Load the dataset with grouped neighbors
grouped_df = pd.read_csv(r"C:\Users\TECH 23\PycharmProjects\HNG_Project\grouped_rad.csv")

# Check the shape of the original dataset
print(f"Original dataset shape: {grouped_df.shape}")


# Function to calculate the average votes of neighboring units
def calculate_neighbor_averages(grouped_df, party):
    avg_votes = []
    for i, row in grouped_df.iterrows():
        group = row['Group']
        if pd.notna(group):
            group = str(group)  # Convert to string in case it's not
            group_indices = [int(idx) for idx in group.split(',')]
            neighbor_votes = grouped_df.iloc[group_indices][party].mean()
        else:
            neighbor_votes = None  # Handle no neighbors case
        avg_votes.append(neighbor_votes)
    return avg_votes


# Calculate average neighbor votes for each party
grouped_df['APC_Avg_Neighbor_Votes'] = calculate_neighbor_averages(grouped_df, 'APC')
grouped_df['PDP_Avg_Neighbor_Votes'] = calculate_neighbor_averages(grouped_df, 'PDP')
grouped_df['LP_Avg_Neighbor_Votes'] = calculate_neighbor_averages(grouped_df, 'LP')
grouped_df['NNPP_Avg_Neighbor_Votes'] = calculate_neighbor_averages(grouped_df, 'NNPP')

# Calculate outlier scores for each party
grouped_df['APC_Outlier_Score'] = abs(grouped_df['APC'] - grouped_df['APC_Avg_Neighbor_Votes'])
grouped_df['PDP_Outlier_Score'] = abs(grouped_df['PDP'] - grouped_df['PDP_Avg_Neighbor_Votes'])
grouped_df['LP_Outlier_Score'] = abs(grouped_df['LP'] - grouped_df['LP_Avg_Neighbor_Votes'])
grouped_df['NNPP_Outlier_Score'] = abs(grouped_df['NNPP'] - grouped_df['NNPP_Avg_Neighbor_Votes'])

# Check the shape of the dataset after calculations
print(f"Dataset shape after calculations: {grouped_df.shape}")

# Drop any duplicates if they exist
grouped_df.drop_duplicates(inplace=True)

# Check the shape after dropping duplicates
print(f"Dataset shape after dropping duplicates: {grouped_df.shape}")

# Sort by outlier scores (example: sorting by APC outlier score)
grouped_df.sort_values(by='APC_Outlier_Score', ascending=False, inplace=True)

# Export cleaned dataset with outlier scores
grouped_df.to_csv(r'C:\Users\TECH 23\PycharmProjects\HNG_Project\cleaned_grouped_dataset_with_outlier_score.csv',
                  index=False)

# Generate report
with open(r'C:\Users\TECH 23\PycharmProjects\HNG_Project\outlier_reports.txt', 'w') as f:
    f.write('Outlier Detection Report\n')
    f.write('=======================\n\n')

    # Top 3 Outliers for APC
    f.write('Top 3 Outliers for APC:\n')
    f.write(grouped_df.nlargest(3, 'APC_Outlier_Score')[
                ['PU-Name', 'APC', 'APC_Avg_Neighbor_Votes', 'APC_Outlier_Score']].to_string(index=False))
    f.write('\n\n')

    # Top 3 Outliers for PDP
    f.write('Top 3 Outliers for PDP:\n')
    f.write(grouped_df.nlargest(3, 'PDP_Outlier_Score')[
                ['PU-Name', 'PDP', 'PDP_Avg_Neighbor_Votes', 'PDP_Outlier_Score']].to_string(index=False))
    f.write('\n\n')

    # Top 3 Outliers for LP
    f.write('Top 3 Outliers for LP:\n')
    f.write(grouped_df.nlargest(3, 'LP_Outlier_Score')[
                ['PU-Name', 'LP', 'LP_Avg_Neighbor_Votes', 'LP_Outlier_Score']].to_string(index=False))
    f.write('\n\n')

    # Top 3 Outliers for NNPP
    f.write('Top 3 Outliers for NNPP:\n')
    f.write(grouped_df.nlargest(3, 'NNPP_Outlier_Score')[
                ['PU-Name', 'NNPP', 'NNPP_Avg_Neighbor_Votes', 'NNPP_Outlier_Score']].to_string(index=False))
    f.write('\n\n')

print("Outlier detection and reporting complete.")
