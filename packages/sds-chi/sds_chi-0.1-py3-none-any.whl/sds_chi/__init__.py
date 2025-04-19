import pandas as pd
import scipy.stats as stats

# Step 1: Input data
aptitude = [85, 65, 50, 68, 87, 74, 65, 96, 68, 94, 73, 84, 85, 87, 91]
jobprof = [70, 90, 80, 89, 88, 86, 78, 67, 86, 90, 92, 94, 99, 93, 87]

# Step 2: Create DataFrame
df = pd.DataFrame({
    'Aptitude': aptitude,
    'JobProficiency': jobprof
})

# Step 3: Convert scores into categories (Low, Medium, High)
df['Aptitude_Cat'] = pd.cut(df['Aptitude'], bins=[0, 65, 80, 100], labels=['Low', 'Medium', 'High'])
df['JobProf_Cat'] = pd.cut(df['JobProficiency'], bins=[0, 75, 90, 100], labels=['Low', 'Medium', 'High'])

# Step 4: Create contingency table
contingency_table = pd.crosstab(df['Aptitude_Cat'], df['JobProf_Cat'])
print("Contingency Table:\n", contingency_table)

# Step 5: Chi-Square test
chi2, p, dof, expected = stats.chi2_contingency(contingency_table)

print("\nChi-Square Statistic:", chi2)
print("Degrees of Freedom:", dof)
print("P-Value:", p)
print("Expected Frequencies:\n", pd.DataFrame(expected, index=contingency_table.index, columns=contingency_table.columns))

# Step 6: Interpretation
alpha = 0.05
print("\n--- Conclusion ---")
if p < alpha:
    print("Since p-value < 0.05, we reject the Null Hypothesis.")
    print("There is a significant association between aptitude and job proficiency.")
else:
    print("Since p-value >= 0.05, we fail to reject the Null Hypothesis.")
    print("There is no significant association between aptitude and job proficiency.")
