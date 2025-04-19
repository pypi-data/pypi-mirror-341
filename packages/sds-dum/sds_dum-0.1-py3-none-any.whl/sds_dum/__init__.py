import pandas as pd

# Sample dataset
data = {
    'Country': ['France', 'Spain', 'Germany', 'Germany', 'Spain', 'Germany', 'France', 'Spain', 'France', 'Germany', 'France'],
    'Age': [44, 27, 30, 38, 48, 30, 35, 31, 48, 50, 37],
    'Salary': [72000, 48000, 54000, 61000, 61000, 85000, 58000, 52000, 79000, 83000, 67000],
    'Purchased': ['No', 'Yes', 'No', 'No', 'No', 'Yes', 'Yes', 'No', 'Yes', 'No', 'Yes']
}

# Create a DataFrame
df = pd.DataFrame(data)

# Display original data
print("Original Data:")
print(df)

# Apply One-Hot Encoding to categorical columns (Country and Purchased)
df_dummies = pd.get_dummies(df, columns=['Country', 'Purchased'], drop_first=True)

# Convert boolean columns (True/False) to 1/0
df_dummies = df_dummies.astype({'Country_Germany': 'int', 'Country_Spain': 'int', 'Purchased_Yes': 'int'})

# Display the transformed data
print("\nData with Categorical Columns Converted to Numerical Representation (Feature Dummification):")
print(df_dummies)
