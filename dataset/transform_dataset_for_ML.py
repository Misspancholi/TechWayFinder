
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_csv('cleaned_dataset.csv')

# Define mapping for skill levels to numeric values
skill_map = {
    'No Experience': 0,
    'Not Interested': 0,
    'Poor': 1,
    'Beginner': 2,
    'Average': 3,
    'Intermediate': 4,
    'Professional': 5,
    'Excellent': 6
}

# Apply the mapping to all skill-related columns (excluding the target 'Role')
skill_columns = df.columns[:-1]
for col in skill_columns:
    df[col] = df[col].map(skill_map)

# Fill missing values with column-wise mode
for col in skill_columns:
    df[col].fillna(df[col].mode()[0], inplace=True)

# Optional: Add derived features
df['Technical_Score'] = df[['Database Fundamentals', 'Software Development', 
                            'Programming Skills', 'Networking', 'AI ML', 
                            'Data Science']].mean(axis=1)

df['Management_Score'] = df[['Project Management', 'Business Analysis', 
                             'Technical Communication']].mean(axis=1)

# Encode Role as categorical labels for ML
le = LabelEncoder()
df['Role_Encoded'] = le.fit_transform(df['Role'])

# Save the cleaned and transformed dataset
df.to_csv('realistic_IT_roles_dataset.csv', index=False)
