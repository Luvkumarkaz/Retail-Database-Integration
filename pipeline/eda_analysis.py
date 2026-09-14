import pandas as pd
from scipy import stats

def run_hypothesis_tests(df):
    """Runs statistical tests relevant for business insights (BCN prep)."""
    if 'has_review' not in df.columns or 'total_revenue' not in df.columns:
        return
        
    print("\n--- EDA Hypothesis Testing ---")
    
    # Test 1: Do users who leave reviews spend more?
    group_review = df[df['has_review'] == True]['total_revenue']
    group_no_review = df[df['has_review'] == False]['total_revenue']
    
    if len(group_review) > 1 and len(group_no_review) > 1:
        t_stat, p_val = stats.ttest_ind(group_review, group_no_review, equal_var=False)
        print(f"Two-Sample T-Test (Review vs No-Review Revenue):")
        print(f"  T-Statistic: {t_stat:.4f}")
        print(f"  P-Value: {p_val:.4f}")
        
        if p_val < 0.05:
            print("  Conclusion: Statistically significant difference in revenue.")
        else:
            print("  Conclusion: No significant difference found.")
    else:
        print("Not enough data points in both groups to run T-Test.")
