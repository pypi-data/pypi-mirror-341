import numpy as np
import matplotlib.pyplot as plt
from portwine.analyzers.base import Analyzer

class EquityDrawdownAnalyzer(Analyzer):
    """
    Provides common analysis functionality, including drawdown calculation,
    summary stats, and plotting.
    """

    def compute_drawdown(self, equity_series):
        """
        Computes percentage drawdown for a given equity curve.

        Parameters
        ----------
        equity_series : pd.Series
            The cumulative equity values over time (e.g., starting at 1.0).

        Returns
        -------
        drawdown : pd.Series
            The percentage drawdown at each point in time.
        """
        rolling_max = equity_series.cummax()
        drawdown = (equity_series - rolling_max) / rolling_max
        return drawdown

    def analyze_returns(self, daily_returns, ann_factor=252):
        """
        Computes summary statistics from daily returns.

        Parameters
        ----------
        daily_returns : pd.Series
            Daily returns of a strategy or benchmark.
        ann_factor : int
            Annualization factor, typically 252 for daily data.

        Returns
        -------
        stats : dict
            {
                'TotalReturn': ...,
                'CAGR': ...,
                'AnnualVol': ...,
                'Sharpe': ...,
                'MaxDrawdown': ...
            }
        """
        dr = daily_returns.dropna()
        if len(dr) < 2:
            return {}

        total_ret = (1 + dr).prod() - 1.0
        n_days = len(dr)
        years = n_days / ann_factor
        cagr = (1 + total_ret) ** (1 / years) - 1.0

        ann_vol = dr.std() * np.sqrt(ann_factor)
        sharpe = cagr / ann_vol if ann_vol > 1e-9 else 0.0

        eq = (1 + dr).cumprod()
        dd = self.compute_drawdown(eq)
        max_dd = dd.min()

        return {
            'TotalReturn': total_ret,
            'CAGR': cagr,
            'AnnualVol': ann_vol,
            'Sharpe': sharpe,
            'MaxDrawdown': max_dd,
        }

    def analyze(self, results, ann_factor=252):
        strategy_stats = self.analyze_returns(results['strategy_returns'], ann_factor)
        benchmark_stats = self.analyze_returns(results['benchmark_returns'], ann_factor)

        return {
            'strategy_stats': strategy_stats,
            'benchmark_stats': benchmark_stats
        }

    def plot(self, results, benchmark_label="Benchmark"):
        """
        Plots the strategy equity curve (and benchmark if given) plus drawdowns.
        Also prints summary stats.

        Parameters
        ----------
        results : dict
            Results from the backtest. Will have signals_df, tickers_returns,
            strategy_returns, benchmark_returns, which are all Pandas DataFrames

        benchmark_label : str
            Label to use for benchmark in plot legend and summary stats.
        """
        fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(10, 8), sharex=True)

        strategy_equity_curve = (1.0 + results['strategy_returns']).cumprod()
        benchmark_equity_curve = (1.0 + results['benchmark_returns']).cumprod()

        # Plot equity curves with specified colors and line widths
        ax1.plot(
            strategy_equity_curve.index,
            strategy_equity_curve.values,
            label="Strategy",
            color='mediumblue',   # deeper blue
            linewidth=1,         # a bit thicker
            alpha=0.6
        )
        ax1.plot(
            benchmark_equity_curve.index,
            benchmark_equity_curve.values,
            label=benchmark_label,
            color='black',      # black
            linewidth=0.5,         # a bit thinner
            alpha=0.5
        )
        ax1.set_title("Equity Curve (relative, starts at 1.0)")
        ax1.legend(loc='best')
        ax1.grid(True)

        # Fill between the strategy and benchmark lines
        ax1.fill_between(
            strategy_equity_curve.index,
            strategy_equity_curve.values,
            benchmark_equity_curve.values,
            where=(strategy_equity_curve.values >= benchmark_equity_curve.values),
            interpolate=True,
            color='green',
            alpha=0.1
        )
        ax1.fill_between(
            strategy_equity_curve.index,
            strategy_equity_curve.values,
            benchmark_equity_curve.values,
            where=(strategy_equity_curve.values < benchmark_equity_curve.values),
            interpolate=True,
            color='red',
            alpha=0.1
        )

        # Plot drawdowns
        strat_dd = self.compute_drawdown(strategy_equity_curve) * 100.0
        bm_dd = self.compute_drawdown(benchmark_equity_curve) * 100.0

        ax2.plot(
            strat_dd.index,
            strat_dd.values,
            label="Strategy DD (%)",
            color='mediumblue',   # deeper blue
            linewidth=1,         # a bit thicker
            alpha=0.6
        )
        ax2.plot(
            bm_dd.index,
            bm_dd.values,
            label=f"{benchmark_label} DD (%)",
            color='black',      # black
            linewidth=0.5,         # a bit thinner
            alpha=0.5
        )
        ax2.set_title("Drawdown (%)")
        ax2.legend(loc='best')
        ax2.grid(True)

        # Fill between drawdown lines: red where strategy is below, green where strategy is above
        ax2.fill_between(
            strat_dd.index,
            strat_dd.values,
            bm_dd.values,
            where=(strat_dd.values <= bm_dd.values),
            interpolate=True,
            color='red',
            alpha=0.1
        )
        ax2.fill_between(
            strat_dd.index,
            strat_dd.values,
            bm_dd.values,
            where=(strat_dd.values > bm_dd.values),
            interpolate=True,
            color='green',
            alpha=0.1
        )

        plt.tight_layout()
        plt.show()

    def generate_report(self, results, ann_factor=252, benchmark_label="Benchmark"):
        stats = self.analyze(results, ann_factor)

        strategy_stats = stats['strategy_stats']
        benchmark_stats = stats['benchmark_stats']

        print("\n=== Strategy Summary ===")
        for k, v in strategy_stats.items():
            if k in ["CAGR", "AnnualVol", "MaxDrawdown"]:
                print(f"{k}: {v:.2%}")
            elif k == "Sharpe":
                print(f"{k}: {v:.2f}")
            else:
                print(f"{k}: {v:.2%}")

        print(f"\n=== {benchmark_label} Summary ===")
        for k, v in benchmark_stats.items():
            if k in ["CAGR", "AnnualVol", "MaxDrawdown"]:
                print(f"{k}: {v:.2%}")
            elif k == "Sharpe":
                print(f"{k}: {v:.2f}")
            else:
                print(f"{k}: {v:.2%}")

        # Now show a comparison: percentage difference (Strategy vs. Benchmark).
        print("\n=== Strategy vs. Benchmark (Percentage Difference) ===")
        for k in strategy_stats.keys():
            strat_val = strategy_stats.get(k, None)
            bench_val = benchmark_stats.get(k, None)
            if strat_val is None or bench_val is None:
                print(f"{k}: N/A (missing data)")
                continue

            if isinstance(strat_val, (int, float)) and isinstance(bench_val, (int, float)):
                if abs(bench_val) > 1e-15:
                    diff = (strat_val - bench_val) / abs(bench_val)
                    print_val = f"{diff * 100:.2f}%"
                else:
                    print_val = "N/A (benchmark ~= 0)"
            else:
                print_val = "N/A (non-numeric)"

            print(f"{k}: {print_val}")
