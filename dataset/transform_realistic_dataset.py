import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv('dataset/cleaned_dataset.csv')

# Print available columns to check what's actually in the dataset
print("Available columns:")
print(df.columns.tolist())

# 1. Remove some of the less common roles
roles_to_remove = ['API Specialist', 'Graphics Designer', 'Technical Writer', 
                  'Helpdesk Engineer', 'Customer Service Executive']
df = df[~df['Role'].isin(roles_to_remove)]

# 2. Remove some columns that might be redundant or less relevant
columns_to_remove = [
    'Project Management',
    'Computer Forensics Fundamentals', 
    'Technical Communication',
    'Troubleshooting skills'
    # 'Graphics Designing' removed as it doesn't exist
]

# Only drop columns that actually exist in the dataframe
columns_to_remove = [col for col in columns_to_remove if col in df.columns]
if columns_to_remove:
    df = df.drop(columns=columns_to_remove)

# 3. Create imbalance by sampling different amounts from each role
role_counts = df['Role'].value_counts()
remaining_roles = role_counts.index.tolist()

# Create a new empty dataframe
realistic_df = pd.DataFrame(columns=df.columns)

# Sample different amounts from each role to create imbalance
for i, role in enumerate(remaining_roles):
    role_df = df[df['Role'] == role]
    sample_size = max(5, int(len(role_df) * (0.9 - (i * 0.1))))
    sample_size = min(sample_size, len(role_df))
    sampled = role_df.sample(sample_size, random_state=42)
    realistic_df = pd.concat([realistic_df, sampled])

# 4. Save the realistic dataset
realistic_df.to_csv('dataset/realistic_dataset.csv', index=False)

print(f"Original dataset shape: {df.shape}")
print(f"Realistic dataset shape: {realistic_df.shape}")
print("\nRole distribution in realistic dataset:")
print(realistic_df['Role'].value_counts())
print("\nRemaining columns:")
print(realistic_df.columns.tolist())

