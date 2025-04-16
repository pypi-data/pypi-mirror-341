from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pymannkendall as mk
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import acf, adfuller, kpss


class UnivariateAnalysis:
    """
    A class for performing univariate analysis on a time series. This class proposes
    multiple statistical tests to perform a deep and strong EDA (Exploratory Data Analysis).

    Attributs
    ---------

    data : pd.DataFrame
        The data to perfrom the univariate analysis on
    numeric_features : list[str]
        The numeric features of the data

    Methods
    -------
    perform_stationarity_test(feature: str) -> None:
        Perform the Augmented Dickey-Fuller test on a feature.

    perform_kpss_test(feature: str) -> None:
        Perform the KPSS test on a feature.

    perform_man_kendall_test(feature: str) -> None:
        Perform the non-parametric Mann-Kendall test on a feature.

    perform_auto_correlation_test(feature: str) -> None:
        Perform the auto-correlation test on a feature.

    plot_trend_over_raw(
        feature: str,
        slope: float,
        intercept: float,
        start_date: str,
        periods: int,
        freq: str,
    ) -> pd.Series:
        Plot the trend over the raw data.

    plot_acf(features: Optional[list[str]] = None) -> None:
        Plot the ACF of all numeric features in the data attribute.

    plot_histogram(features: Optional[list[str]] = None) -> None:
        Plot the histogram of the given features.

    plot_boxplot(features: Optional[list[str]] = None) -> None:
        Plot the boxplot of the given features.

    detect_anomalies_STL_decomposition(feature: str) -> pd.Series:
        Detect anomalies in the given feature using the Z-score method.

    detect_anomalies_isolation_forest(
        features: list[str],
        contamination: float = 0.05,
        random_state: int = 42,
    ) -> pd.Series:
        Detect anomalies in the given features using the Isolation Forest method.
    """

    def __init__(self, data: pd.DataFrame):
        """
        Initialize the UnivariateAnalysis class.

        Arguments
        ---------
        data: pd.DataFrame
            The data to perform the univariate analysis on
        """
        self.data = data
        self.numeric_features = data.select_dtypes(include=[np.number]).columns

    def perform_stationarity_test(self, feature: str):
        """
        Perform the Augmented Dickey-Fuller test on a feature.
        This test is used to determine if a time series is stationary.
        If the p-value is less than 0.05, we can reject the null hypothesis
        and conclude that the time series is stationary.

        The two hypotheses are:
        - Null hypothesis (H0): The time series is non-stationary.
        - Alternative hypothesis (H1): The time series is stationary or trend-stationary.

        If the p-value is greater than 0.05, we fail to reject the null hypothesis
        and conclude that the time series is non-stationary.

        The method displays the ADF statistic for different significance levels. The more
        negative the statistic, the stronger the evidence against the null hypothesis.

        Arguments
        ---------
        feature: str
            The feature to perform the Augmented Dickey-Fuller test on
        """
        adf_result = adfuller(self.data[feature])
        print("Augmented Dickey-Fuller Test:")
        print(f"ADF Statistic: {adf_result[0]}")
        print(f"p-value: {adf_result[1]}")
        print("Critical values:")
        for key, value in adf_result[4].items():
            print(f"\t{key}: {value}")

    def perform_kpss_test(self, feature: str):
        """
        Perform the KPSS test on a feature.
        This test is used to determine if a time series is stationary.
        If the p-value is less than 0.05, we can reject the null hypothesis
        and conclude that the time series is non-stationary.

        The two hypotheses are:
        - Null hypothesis (H0): The time series is trend-stationary or has a no unit root.
        - Alternative hypothesis (H1): The time series is non-stationary or series has unit root.

        A process has unit root if the autoregressive coefficient is 1 and therefore the process
        is ruled by the following equation:

        y_t = y_t-1 + epsilon_t

        where:
            - y_t is the value of the time series at time t
            - y_t-1 is the value of the time series at time t-1
            - epsilon_t is white noise

        Which is more or less the definition of a random walk.

        The method displays the KPSS statistic for different significance levels. The more
        positive the statistic, the stronger the evidence against the null hypothesis.
        """
        kpss_result = kpss(self.data[feature], regression="c", nlags="auto")
        print("KPSS Test:")
        print(f"KPSS Statistic: {kpss_result[0]}")
        print(f"p-value: {kpss_result[1]}")
        print("Critical values:")
        for key, value in kpss_result[3].items():
            print(f"\t{key}: {value}")

    def perform_man_kendall_test(self, feature: str):
        """
        Perform the non-parametric Mann-Kendall test on a feature.
        This test is used to determine wether a time series has a trend or not.

        The two hypotheses are:
        - Null hypothesis (H0): The time series has no trend.
        - Alternative hypothesis (H1): The time series has a trend.

        If the p-value is less than 0.05, we can reject the null hypothesis
        and conclude that the time series has a trend.
        """
        mk_result = mk.original_test(self.data[feature])
        print("Mann-Kendall Test:")
        has_trend = mk_result[1]

        if has_trend:
            print(f"Mann-Kendall Statistic: {mk_result[0]}")
            print(f"p-value: {mk_result[2]}")
        else:
            print("The time series has no trend.")

        return mk_result

    def perform_auto_correlation_test(self, feature: str):
        """
        Perform the auto-correlation test on a feature.
        This test is used to determine if a time series is auto-correlated.
        If the p-value is less than 0.05, we can reject the null hypothesis
        and conclude that the time series is auto-correlated.

        The two hypotheses are:
        - Null hypothesis (H0): The time series is not auto-correlated.
        - Alternative hypothesis (H1): The time series is auto-correlated.

        If the p-value is less than 0.05, we can reject the null hypothesis
        and conclude that the time series is auto-correlated.
        """
        acf_result = acf(self.data[feature])
        print("Auto-Correlation Test:")
        print(f"ACF Statistic: {acf_result[0]}")
        print(f"p-value: {acf_result[1]}")
        print("Critical values:")
        for key, value in acf_result[3].items():
            print(f"\t{key}: {value}")

    def plot_trend_over_raw(
        self,
        feature: str,
        slope: float,
        intercept: float,
        start_date: str,
        periods: int,
        freq: str,
    ):
        """
        Create a time series with given slope and intercept

        Arguments
        ---------
        slope : float
            The slope of the line
        intercept : float
            The y-intercept
        start_date : str
            Start date in format 'YYYY-MM-DD'
        periods : int
            Number of periods to generate
        freq : str
            Frequency of the time series ('D' for daily, 'W' for weekly, etc.)
        noise : float, optional
            Standard deviation of Gaussian noise to add

        Returns
        -------
        pd.Series
            Time series with specified parameters
        """
        # Create date range
        dates = pd.date_range(start=start_date, periods=periods, freq=freq)

        # Create linear trend
        x = np.arange(periods)
        y = slope * x + intercept

        trend = pd.Series(y, index=dates)

        plt.figure(figsize=(12, 6))
        plt.plot(trend.index, trend, label="Trend")
        plt.plot(self.data.index, self.data[feature], label="Original")
        plt.title(f"Time Series (slope={slope}, intercept={intercept})")
        plt.legend()
        plt.show()

        return trend

    def plot_acf(self, features: Optional[list[str]] = None):
        """
        Plot the ACF of all numeric features in the data attribute

        Arguments
        ---------
        feature: str
            The feature to plot the ACF of
        """
        if features is None:
            features = self.numeric_features

        if isinstance(features, str):
            features = [features]

        for feature in features:
            plt.figure(figsize=(15, 5))
            plot_acf(self.data[feature], title=f"ACF of {feature}")
            plt.show()

    def plot_histogram(self, features: Optional[list[str]] = None):
        """
        Plot the histogram of the given features.

        Arguments
        ---------
        features: list[str], optional
            The features to plot the histogram ofs
        """
        if features is None:
            features = self.numeric_features

        if isinstance(features, str):
            features = [features]

        for feature in features:
            self.data[feature].hist(
                bins=len(self.data[feature].unique()), figsize=(10, 5)
            )
            plt.show()

    def plot_boxplot(self, features: Optional[list[str]] = None):
        """
        Plot the boxplot of the given features.

        Arguments
        ---------
        features: list[str], optional
            The features to plot the boxplot of
        """
        if features is None:
            features = self.numeric_features

        if isinstance(features, str):
            features = [features]

        self.data.boxplot(column=features, figsize=(10, 5))
        plt.show()

    def detect_anomalies_STL_decomposition(self, feature: str):
        """
        Detect anomalies in the given feature using the Z-score method.
        """
        # Decompose the time series into trend, seasonal, and residual components
        decomposition = seasonal_decompose(
            self.data[feature], model="additive", period=4
        )

        # Plot the decomposed components
        plt.figure(figsize=(12, 8))
        plt.subplot(4, 1, 1)
        plt.plot(self.data[feature], label="Original")
        plt.title("Observed")
        plt.subplot(4, 1, 2)
        plt.plot(decomposition.seasonal, label="Seasonal")
        plt.title("Seasonal")
        plt.subplot(4, 1, 3)
        plt.plot(decomposition.trend, label="Trend")
        plt.title("Trend")
        plt.subplot(4, 1, 4)
        plt.plot(decomposition.resid, label="Residual")
        plt.title("Residual")
        plt.legend()
        plt.show()

        estimated = decomposition.trend + decomposition.seasonal
        plt.figure(figsize=(12, 6))
        plt.plot(self.data[feature], label="Original")
        plt.plot(estimated, label="Estimated")
        plt.legend()
        plt.show()

        resid_mean = decomposition.resid.mean()
        resid_std = decomposition.resid.std()

        lower_bound = resid_mean - 3 * resid_std
        upper_bound = resid_mean + 3 * resid_std

        plt.figure(figsize=(12, 6))
        plt.plot(decomposition.resid, label="Residual")

        plt.fill_between(
            decomposition.resid.index,
            upper_bound,
            lower_bound,
            color="orange",
            alpha=0.2,
        )
        plt.axhline(y=resid_mean, color="red", linestyle="--", label="Mean")
        plt.axhline(y=upper_bound, color="orange", linestyle="--", label="Upper Bound")
        plt.axhline(y=lower_bound, color="orange", linestyle="--", label="Lower Bound")
        plt.legend()
        plt.show()

        # Spot the anomalies
        anomalies = self.data[
            (decomposition.resid < lower_bound) | (decomposition.resid > upper_bound)
        ]

        # Create the main plot
        ax = self.data[feature].plot(figsize=(15, 5))

        # Add red dots at anomaly positions
        ax.scatter(
            anomalies.index,
            self.data.loc[anomalies.index, feature],
            color="red",
            s=100,
            label="Anomalies",
        )

        # Add legend
        ax.legend()

        plt.show()

        return anomalies

    def detect_anomalies_isolation_forest(
        self,
        features: list[str],
        contamination: float = 0.05,
        random_state: int = 42,
    ):
        """
        Detect anomalies in the given features using the Isolation Forest method. Isolation
        Forest is an ensemble learning method for anomaly detection. It is based on the idea that
        anomalies are data points that are few and different. The algorithm creates a forest of
        trees and each tree tries to isolate a data point. Anomalies are then the data points
        that are close to the root node of the trees.

        Arguments
        ---------
        features: list[str]
            The features to detect anomalies in
        contamination: float, optional
            The contamination of the data
        random_state: int, optional
            The random state of the Isolation Forest

        Returns
        -------
        pd.Series
            The anomaly score of the data for each data point
        """
        isolation_forest = IsolationForest(
            contamination=contamination,
            random_state=random_state,
        )

        isolation_forest.fit(self.data[[features]])
        self.data["anomaly"] = isolation_forest.predict(self.data[[features]])
        self.data["anomaly"] = self.data["anomaly"].map({1: 0, -1: 1})

        # Create the main plot
        ax = self.data[features].plot(figsize=(15, 5))

        # Add red dots at anomaly positions
        ax.scatter(
            self.data.index,
            self.data.loc[self.data["anomaly"] == 1, features],
            color="red",
            s=100,
            label="Anomalies",
        )

        # Add legend
        ax.legend()

        plt.show()

        return self.data["anomaly"]

    def detect_anomalies_kmeans(
        self,
        features: list[str],
        n_clusters: int = 3,
        random_state: int = 42,
    ):
        """
        Detect anomalies in the given features using the KMeans method. KMeans is a clustering
        method that groups data points into clusters based on their similarity. Anomalies are then
        the data points that are far from the centroid of the clusters.

        Arguments
        ---------
        features: list[str]
            The features to detect anomalies in
        n_clusters: int, optional
            The number of clusters to use, default is 3. This method doesn't handle the choice of
            the optimal number of clusters, so it is important to choose a good number of clusters.
        random_state: int, optional
            The random state of the KMeans

        Returns
        -------
        pd.Series
            The anomaly score of the data for each data point
        """
        kmeans = KMeans(
            n_clusters=n_clusters,
            random_state=random_state,
        )
        kmeans.fit(self.data[[features]])
        self.data["anomaly"] = kmeans.predict(self.data[[features]])

        # Create the main plot
        ax = self.data[features].plot(figsize=(15, 5))

        # Add red dots at anomaly positions
        ax.scatter(
            self.data.index,
            self.data.loc[self.data["anomaly"] == 1, features],
            color="red",
            s=100,
            label="Anomalies",
        )

        # Add legend
        ax.legend()

        plt.show()

        return self.data["anomaly"]
