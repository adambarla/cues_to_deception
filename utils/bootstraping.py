
import os
import numpy as np
import pandas as pd
import scipy.stats as stats
import statsmodels.formula.api as sm
import matplotlib.pyplot as plt
from tqdm import tqdm

from utils.plotting import plot_bootstrap_distribution


def bootstrap(data, formula, n=1000, alpha=0.05, path=os.path.join('data', 'bootstrap')):
    """
    Bootstrap the data and run linear regression on the bootstrapped samples.
    Returns:
      - results_df : DataFrame of shape (n, p) with the raw bootstrap coefficient draws
      - stats_df   : DataFrame of length p summarizing mean, se, CI, t-stat, and p-value
    """
    results_df = pd.DataFrame()

    if not os.path.exists(path):
        os.makedirs(path)
    hashed_params = hash((data.to_string(), formula, n))
    file_name = f"params_hash_{hashed_params}.csv"
    path = os.path.join(path, file_name)
    if os.path.exists(path):
        results_df = pd.read_csv(path)
        print(f"Loaded bootstrap results from {path}")
    else:
        results = []
        for i in tqdm(range(n)):
            sample = data.sample(frac=1, replace=True)
            model  = sm.ols(formula, data=sample).fit()
            results.append(model.params)
        results_df = pd.DataFrame(results)
        results_df.to_csv(path, index=False)
        print(f"Saved bootstrap results to {path}")
    
    # compute studentized CI and p-values
    df_boot = n - 1
    means = results_df.mean()
    ses = results_df.std(ddof=1)
    ci_lower, ci_upper = stats.t.interval(
        1 - alpha,
        df_boot,
        loc=means,
        scale=ses
    )

    t_stats = means / ses
    p_values = 2 * (1 - stats.t.cdf(np.abs(t_stats), df_boot))
    stats_df = pd.DataFrame({
        'mean':    means,
        'se':      ses,
        'ci_lower': ci_lower,
        'ci_upper': ci_upper,
        't_stat':  t_stats,
        'p_value': p_values
    })
    plot_bootstrap_distribution(results_df, means, ses, df_boot)
    return results_df, stats_df
