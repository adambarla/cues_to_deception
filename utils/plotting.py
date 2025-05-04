import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import scipy.stats as stats

def plot_bootstrap_distribution(results_df, means, ses, df_boot):
    fig, axes = plt.subplots(
        nrows=1, ncols=len(results_df.columns),
        figsize=(15, 5)
    )
    for i, col in enumerate(results_df.columns):
        ax = axes[i]
        vals = results_df[col]
        ax.hist(vals, bins=30, density=True, alpha=0.6, edgecolor='gray',
                color='lightgray', label='Bootstrap samples')
        ax.set_title(col)
        ax.set_xlabel("Coefficient value")
        ax.set_ylabel("Density")

        # add bootstrap mean & median
        ax.axvline(means[col], color='r', linestyle='-', linewidth=2)
        ax.axvline(vals.median(), color='g', linestyle='-', linewidth=2)

        # overlay Student-t density
        x = np.linspace(vals.min(), vals.max(), 200)
        y = stats.t.pdf(x,
                        df_boot,
                        loc=means[col],
                        scale=ses[col])
        ax.plot(x, y, color='b', linestyle='dashed', linewidth=1)

        ax.legend([
            'samples',
            'mean',
            'median',
            f"Student's t density \n(df={df_boot})",
        ])
    plt.tight_layout()
    plt.show()