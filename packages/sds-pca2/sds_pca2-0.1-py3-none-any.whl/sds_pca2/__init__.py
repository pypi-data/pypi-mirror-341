import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Correct UCI dataset URL
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"

# Load dataset with correct separator (comma)
df = pd.read_csv(url, sep=';')

# Confirm column names (optional debug)
print("Columns:", df.columns)

# Separate features and target
X = df.drop("quality", axis=1)
y = df["quality"]

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Create DataFrame with PCA results
pca_df = pd.DataFrame(X_pca, columns=["PC1", "PC2"])
pca_df["quality"] = y

# Plot
plt.figure(figsize=(10, 6))
scatter = plt.scatter(pca_df["PC1"], pca_df["PC2"], c=pca_df["quality"], cmap="viridis", alpha=0.7)
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.title("PCA of Red Wine Dataset")
plt.colorbar(scatter, label="Wine Quality")
plt.grid(True)
plt.show()

# Show variance explained
print("\nExplained variance ratio:", pca.explained_variance_ratio_)
print("Total variance explained:", sum(pca.explained_variance_ratio_))
