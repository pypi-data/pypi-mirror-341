from typing import Optional, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler
from statsmodels.formula.api import ols
from statsmodels.tsa.stattools import ccovf
from tqdm import tqdm


class BivariateAnalysis:
    """
    A class for performing bivariate analysis on a time series. This class proposes
    multiple statistical tests to perform a deep and strong EDA (Exploratory Data Analysis).

    Attributs
    ---------
    data : pd.DataFrame
        The data to perform the bivariate analysis on
    numeric_features : pd.DataFrame
        Non categorical features

    Methods
    -------
    plot_correlation_matrix()
        Plot the correlation matrix of the numeric features.

    plot_cross_correlation_matrix()
        Plot the cross-correlation matrix of the numeric features.

    plot_covariance_matrix()
        Plot the covariance matrix of the numeric features.

    plot_cross_covariance_matrix()
        Plot the cross-covariance matrix of the numeric features.

    perform_anova_numeric_categorical(cat_cols: Union[str, list[str]]) -> tuple[go.Figure, pd.DataFrame]
        Perform ANOVA (Analysis of Variance) between numerical and categorical variables using Fisher's F-statistic.
    """

    def __init__(
        self, data: pd.DataFrame, numeric_features: Optional[list[str]] = None
    ):
        self.data = data.copy()
        if numeric_features is None:
            numeric_features = self.data.select_dtypes(include=[np.number]).columns
        self.numeric_features = numeric_features

    # Create figure with specific size
    def plot_correlation_matrix(self):
        """
        Plot the correlation matrix of the numeric features.
        """

        plt.figure(figsize=(12, 8))

        # Create heatmap using seaborn
        sns.heatmap(
            self.data.loc[:, self.numeric_features].corr(),
            annot=True,  # Add correlation values
            cmap="coolwarm",  # Color scheme
            center=0,  # Center the colormap at 0
            fmt=".2f",  # Format for correlation values
            square=True,  # Make the plot square-shaped
            cbar=True,  # Show colorbar
            xticklabels=True,
            yticklabels=True,
        )

        # Rotate x-axis labels
        plt.xticks(rotation=45, ha="right")
        plt.yticks(rotation=0)

        # Adjust layout to prevent label cutoff
        plt.tight_layout()

        plt.show()

    def plot_cross_correlation_matrix(self):
        """
        Plot the cross-correlation matrix of the numeric features.
        """
        plt.figure(figsize=(12, 8))
        sns.heatmap(
            self.data.loc[:, self.numeric_features].corr(),
            annot=True,
            cmap="coolwarm",
            center=0,
            fmt=".2f",
            square=True,
            cbar=True,
            xticklabels=True,
            yticklabels=True,
        )
        plt.show()

    def plot_covariance_matrix(self):
        """
        Plot the covariance matrix of the numeric features.

        Gives information about the covariance between the features.

        It gives the following information:

        Cov(X, Y) = E[(X - E[X])(Y - E[Y])]
        """
        plt.figure(figsize=(12, 8))
        sns.heatmap(
            self.data.loc[:, self.numeric_features].cov(),
            annot=True,
            cmap="coolwarm",
            center=0,
            fmt=".2f",
            square=True,
            cbar=True,
            xticklabels=True,
            yticklabels=True,
        )
        plt.show()

    def plot_cross_covariance_matrix(self):
        """
        Plot the cross-covariance matrix of the numeric features.

        At the difference of the covariance matrix, the cross-covariance matrix is a matrix of the covariance
        of the features with a lag.

        It gives the following information:

        Cov(X(t), Y(t+lag)) = E[(X(t) - E[X(t)])(Y(t+lag) - E[Y(t+lag)])]

        Parameters
        ----------
        lag : int, default=0
            The lag to use for the cross-covariance matrix.
        """
        plt.figure(figsize=(12, 8))
        sns.heatmap(
            ccovf(self.data.loc[:, self.numeric_features].to_numpy()),
            annot=True,
            cmap="coolwarm",
            center=0,
            fmt=".2f",
            square=True,
            cbar=True,
            xticklabels=True,
            yticklabels=True,
        )
        plt.show()

    def perform_anova_numeric_categorical(
        self, cat_cols: Union[str, list[str]]
    ) -> tuple[go.Figure, pd.DataFrame]:
        """
        Perform ANOVA (Analysis of Variance) between numerical and categorical variables
        using Fisher's F-statistic.

        Arguments
        ---------
        cat_cols : Union[str, list[str]]
            List of categorical column names to include in the ANOVA analysis.

        Returns
        -------
        Tuple[go.Figure, pd.DataFrame]
            The Plotly figure object of the ANOVA heatmap and the DataFrame containing ANOVA results.
        """
        if isinstance(cat_cols, str):
            cat_cols = [cat_cols]

        # Check if the columns exist in the DataFrame
        missing_columns = [col for col in cat_cols if col not in self.data.columns]
        if missing_columns:
            raise ValueError(
                f"The following columns are not in the DataFrame: {missing_columns}"
            )

        # Create a copy of the data to avoid modifying the original
        data_copy = self.data.copy()

        # Standardize numerical data
        std_scaler = StandardScaler()
        numerical_feature_list_std = []
        for num in self.numeric_features:
            data_copy[num + "_std"] = std_scaler.fit_transform(
                data_copy[num].to_numpy().reshape(-1, 1)
            )
            numerical_feature_list_std.append(num + "_std")

        # Perform ANOVA for each combination of numerical and categorical variables
        rows = []
        total_combinations = len(cat_cols) * len(numerical_feature_list_std)

        with tqdm(total=total_combinations, desc="Performing ANOVA") as pbar:
            for cat in cat_cols:
                col = []
                for num in numerical_feature_list_std:
                    try:
                        equation = f"{num} ~ C({cat})"
                        model = ols(equation, data=data_copy).fit()
                        anova_table = sm.stats.anova_lm(model, typ=1)
                        col.append(anova_table.loc[f"C({cat})"]["F"])
                    except Exception as e:
                        print(f"Error in ANOVA for {num} ~ {cat}: {e!s}")
                        col.append(np.nan)
                    pbar.update(1)
                rows.append(col)

        # Store the results in a DataFrame
        anova_result = np.array(rows)
        anova_result_df = pd.DataFrame(
            anova_result, columns=self.numeric_features, index=cat_cols
        )

        # Create a Plotly heatmap
        fig = go.Figure(
            data=go.Heatmap(
                z=anova_result_df.values,
                x=anova_result_df.columns,
                y=anova_result_df.index,
                colorscale="plasma",
                zmin=anova_result_df.values.min(),
                zmax=anova_result_df.values.max(),
                colorbar={"title": "Fisher's F-statistic"},
            )
        )

        # Update layout
        fig.update_layout(
            title="Fisher's Statistic Heatmap",
            xaxis={"title": "Numerical Features"},
            yaxis={"title": "Categorical Features"},
            plot_bgcolor="rgba(0,0,0,0)",  # Remove background grid
            xaxis_showgrid=False,
            yaxis_showgrid=False,
            xaxis_zeroline=False,
            yaxis_zeroline=False,
            width=800,
            height=800,
            margin={
                "l": 100,
                "r": 100,
                "t": 100,
                "b": 100,
            },  # Adjust margins to center the plot
        )

        return fig, anova_result_df
