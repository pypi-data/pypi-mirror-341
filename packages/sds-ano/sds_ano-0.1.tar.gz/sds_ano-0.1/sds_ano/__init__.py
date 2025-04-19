    import scipy.stats as stats
    class_A = [85, 90, 88, 82, 87]
    class_B = [76, 78, 80, 81, 75]
    class_C = [92, 88, 94, 89, 90]
    print("Null Hypothesis (H₀): There is no significant difference in the mean exam scores of students among Class A, Class B, and Class C.")
    print("Alternative Hypothesis (H₁): At least one class mean is significantly different from the others.\n")
    f_statistic, p_value = stats.f_oneway(class_A, class_B, class_C)
    print(f"F-statistic: {f_statistic}")
    print(f"P-value: {p_value}")
    alpha = 0.05  
    if p_value < alpha:
        print("\nReject the null hypothesis: There is a significant difference in the mean scores of at least one class.")
    else:
        print("\nFail to reject the null hypothesis: There is no significant difference in the mean scores of the classes.")
