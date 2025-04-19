import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# Create the dataset
data = {
    'Country': ['France', 'Spain', 'Germany', 'Spain', 'Germany', 'France', 'Spain', 'France', 'Germany', 'France'],
    'Age': [44, 27, 30, 38, 40, 35, 31, 48, 50, 37],
    'Salary': [72000, 48000, 54000, 61000, 85000, 58000, 52000, 79000, 83000, 67000],
    'Purchased': ['No', 'Yes', 'No', 'No', 'Yes', 'Yes', 'No', 'Yes', 'No', 'Yes']
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Extract numerical features
numerical_features = ['Age', 'Salary']
X = df[numerical_features]

# 1. Standardization (Z-score normalization)
standard_scaler = StandardScaler()
X_standardized = standard_scaler.fit_transform(X)
X_standardized_df = pd.DataFrame(X_standardized, columns=numerical_features)

# 2. Normalization (Min-Max scaling)
minmax_scaler = MinMaxScaler()
X_normalized = minmax_scaler.fit_transform(X)
X_normalized_df = pd.DataFrame(X_normalized, columns=numerical_features)

# Print the data
print("Original Data:")
print(X)
print("\nStandardized Data (Z-score normalization):")
print(X_standardized_df)
print("\nNormalized Data (Min-Max scaling):")
print(X_normalized_df)

# Create scatter plots
plt.figure(figsize=(15, 5))

# Original Data
plt.subplot(1, 3, 1)
plt.scatter(X['Age'], X['Salary'], color='blue', alpha=0.6)
plt.title('Original Data')
plt.xlabel('Age')
plt.ylabel('Salary')

# Standardized Data
plt.subplot(1, 3, 2)
plt.scatter(X_standardized_df['Age'], X_standardized_df['Salary'], color='green', alpha=0.6)
plt.title('Standardized Data')
plt.xlabel('Age (Standardized)')
plt.ylabel('Salary (Standardized)')

# Normalized Data
plt.subplot(1, 3, 3)
plt.scatter(X_normalized_df['Age'], X_normalized_df['Salary'], color='red', alpha=0.6)
plt.title('Normalized Data')
plt.xlabel('Age (Normalized)')
plt.ylabel('Salary (Normalized)')

plt.tight_layout()
plt.show()
