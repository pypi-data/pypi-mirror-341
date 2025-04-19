import scipy.stats as stats
import numpy as np

scores = np.array([72, 88, 64, 74, 67, 79, 85, 75, 89, 77])
hypothesized_mean = 70
sample_mean = np.mean(scores)
sample_std = np.std(scores, ddof=1) 
t_statistic, p_value = stats.ttest_1samp(scores, hypothesized_mean)

print(f"Sample Mean: {sample_mean:.2f}")
print(f"Sample Standard Deviation: {sample_std:.2f}")
print(f"T-statistic: {t_statistic:.2f}")
print(f"P-value: {p_value:.4f}")


alpha = 0.05  

if p_value < alpha:
    print("\nSince the p-value is less than the significance level (alpha), we reject the null hypothesis.")
    print("Conclusion: The sample mean is significantly different from the hypothesized population mean.")
else:
    print("\nSince the p-value is greater than the significance level (alpha), we fail to reject the null hypothesis.")
    print("Conclusion: The sample mean is not significantly different from the hypothesized population mean.")
