import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris

# Step 1: Load the Iris dataset
iris = load_iris()
X = iris.data
y = iris.target
feature_names = iris.feature_names

# Step 2: Standardize the data (important for PCA)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Step 3: Apply PCA
pca = PCA(n_components=4)  # Initially reduce to 4 components to check explained variance
X_pca = pca.fit_transform(X_scaled)

# Step 4: Explained variance ratio (to decide the number of components)
explained_variance = pca.explained_variance_ratio_

# Display the results in the requested format
print(f"Original Dataset Shape: {X.shape}")
print("\nExplained Variance Ratio by each Principal Component:")
for i, var in enumerate(explained_variance, 1):
    print(f"PC{i}: {var:.2f}")

# Calculate total explained variance
total_explained_variance = np.sum(explained_variance)
print(f"\nTotal explained variance: {total_explained_variance:.2f}")

# Find number of components to explain 95% variance
cumulative_variance = np.cumsum(explained_variance)
n_components_95_variance = np.where(cumulative_variance >= 0.95)[0][0] + 1

print(f"\nNumber of principal components to explain 95% variance: {n_components_95_variance}")

# Step 5: Visualize the data in the 2D reduced space (using 2 components for visualization)
pca_2d = PCA(n_components=2)
X_pca_2D = pca_2d.fit_transform(X_scaled)

# Visualize the 2D PCA projection
plt.figure(figsize=(8,6))
plt.scatter(X_pca_2D[:, 0], X_pca_2D[:, 1], c=y, cmap='viridis', edgecolor='k', s=50)
plt.title('PCA of Iris Dataset (2 Components)', fontsize=14)
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.colorbar(label='Target Class')
plt.grid(True)
plt.show()
