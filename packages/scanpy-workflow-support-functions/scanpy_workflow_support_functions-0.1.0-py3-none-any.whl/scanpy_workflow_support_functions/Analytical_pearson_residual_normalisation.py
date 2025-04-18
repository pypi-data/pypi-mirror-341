# 7.3. Analytic Pearson residuals

adata.X = adata.layers["soupX_counts"]

## If Poisson behavior is desired, the overdispersion parameter can instead be set to infinity (theta=np.Inf).


analytic_pearson = sc.experimental.pp.normalize_pearson_residuals(adata, inplace=False, check_values=True, clip=np.Inf)   # theta=np.Inf for Poissan



from scipy.sparse import csr_matrix, issparse

adata.layers["analytic_pearson_residuals"] = csr_matrix(analytic_pearson["X"])


print(adata.layers["analytic_pearson_residuals"])

### PLOTTING SNS.HISTPLOT TO CHECK DISTRIBUTION::

fig, axes = plt.subplots(1, 2, figsize=(10, 5))
p1 = sns.histplot(adata.obs["total_counts"], bins=100, kde=False, ax=axes[0])
axes[0].set_title("Total counts")

p2 = sns.histplot(
    adata.layers["analytic_pearson_residuals"].sum(1), bins=100, kde=False, ax=axes[1]
)
axes[1].set_title("Analytic Pearson residuals")
plt.show()




# IF ABOVE PLOT GIVES ERROR >> RUN BELOW CODE:: 

## try to plot sns.histplot but if it doesnt work >> most likely there is NaN values in analytical_pearson_residuals

print(adata.layers["analytic_pearson_residuals"][1].sum())

# Assuming adata.layers["analytic_pearson_residuals"] is your sparse matrix
matrix = adata.layers["analytic_pearson_residuals"]

# Convert the sparse matrix to a dense matrix and flatten it
dense_matrix = matrix.toarray().flatten()

# Check for nan values
has_nan = np.isnan(dense_matrix).any()
print(f"Has NaN values: {has_nan}")

# Check for inf values
has_inf = np.isinf(dense_matrix).any()
print(f"Has Inf values: {has_inf}")


np.isnan(analytic_pearson["X"]).any()

np.isnan(adata.X.toarray()).any()

data = adata.X.toarray()

row_variance = np.var(data, axis=1)
# Calculate variance for each column
col_variance = np.var(data, axis=0)
# Find rows with zero variance
rows_with_zero_variance = np.where(row_variance == 0)[0]
# Find columns with zero variance
cols_with_zero_variance = np.where(col_variance == 0)[0]
print("Rows with zero variance:", rows_with_zero_variance)
print("Columns with zero variance:", cols_with_zero_variance)

## There are columsn (genes) with no varianze. I guess this genes are not expressed in any cell:
data.sum(0)[cols_with_zero_variance]

## Indeed. Here is the problem. Let's see what happen if we remove these genes:
cols_with_non_zero_variance = np.where(col_variance != 0)[0]


# Subset the data to include only columns with non-zero variance
adata_2 = adata[:, cols_with_non_zero_variance]


## calculate again on these adata_2 >> 0 variance removed genes:: 

analytic_pearson = sc.experimental.pp.normalize_pearson_residuals(adata_2, inplace=False, check_values=True,clip=np.Inf)
from scipy.sparse import csr_matrix, issparse
adata_2.layers["analytic_pearson_residuals"] = csr_matrix(analytic_pearson["X"])

### PLOTTING SNS.HISTPLOT TO CHECK DISTRIBUTION::

fig, axes = plt.subplots(1, 2, figsize=(10, 5))
p1 = sns.histplot(adata_2.obs["total_counts"], bins=100, kde=False, ax=axes[0])
axes[0].set_title("Total counts")

p2 = sns.histplot(
    adata_2.layers["analytic_pearson_residuals"].sum(1), bins=100, kde=False, ax=axes[1]
)
axes[1].set_title("Analytic Pearson residuals")
plt.show()


## so far it gives me this error::

#ValueError: No objects to concatenate