import pandas as pd
from sklearn.datasets import fetch_openml
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import matplotlib.pyplot as plt

# Load the California Housing dataset
housing = fetch_openml(name="california_housing", version=1)
data = pd.DataFrame(housing.data, columns=housing.feature_names)
data['target'] = housing.target

# Select a subset of the data for simplicity (first 1000 rows and first 3 columns)
X_subset = data.iloc[:1000, :3]  # First 1000 rows and first 3 columns (MedInc, HouseAge, AveRooms)
y_subset = data['target'][:1000]  # Corresponding target for these rows

# Check the original data shape
print("Original Data Shape:", X_subset.shape)

# Apply Standardization (StandardScaler)
scaler_standard = StandardScaler()
X_standardized = scaler_standard.fit_transform(X_subset)

# Apply Normalization (MinMaxScaler)
scaler_minmax = MinMaxScaler()
X_normalized = scaler_minmax.fit_transform(X_subset)

# Visualizing the original data vs standardized data vs normalized data
plt.figure(figsize=(18, 6))

# Plotting the original data for the first two numeric features
plt.subplot(131)
plt.scatter(X_subset.iloc[:, 0], X_subset.iloc[:, 1], c=y_subset, cmap='viridis')
plt.title('Original Data')
plt.xlabel('Feature 1: MedInc')
plt.ylabel('Feature 2: HouseAge')

# Plotting the standardized data for the first two numeric features
plt.subplot(132)
plt.scatter(X_standardized[:, 0], X_standardized[:, 1], c=y_subset, cmap='viridis')
plt.title('Standardized Data')
plt.xlabel('Feature 1 (Standardized): MedInc')
plt.ylabel('Feature 2 (Standardized): HouseAge')

# Plotting the normalized data for the first two numeric features
plt.subplot(133)
plt.scatter(X_normalized[:, 0], X_normalized[:, 1], c=y_subset, cmap='viridis')
plt.title('Normalized Data')
plt.xlabel('Feature 1 (Normalized): MedInc')
plt.ylabel('Feature 2 (Normalized): HouseAge')

plt.tight_layout()
plt.show()

# Display the first few rows of the standardized and normalized data
print("\nStandardized Data:")
print(pd.DataFrame(X_standardized, columns=X_subset.columns).head())

print("\nNormalized Data:")
print(pd.DataFrame(X_normalized, columns=X_subset.columns).head())
