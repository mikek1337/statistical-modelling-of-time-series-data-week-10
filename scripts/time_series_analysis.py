import pandas as pd
from statsmodels.tsa.stattools import kpss
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt
import pymc as pm

def kpss_test(timeseries:pd.DataFrame)->bool:
    """
        To determine if timeseries is stationary
    """
    kpss_statistic, p_value, n_lags, critical_values = kpss(timeseries,regression='c')
    if p_value > 0.05:
        print(f"Test statistic {kpss_statistic}")
        print("failed to reject if the data is likely level stationary")
        return False
    else:
        print("likely non-stationary")
        return True

def plot_trends_seasonal(timeseries:pd.DataFrame)->None:
    """
    To plot Trends and seasonal timeseries
    """
    decompose = seasonal_decompose(timeseries, model='multiplicative', period=12)
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(16, 12), sharex=True)

    # Original series plot
    decompose.observed.plot(ax=ax1, color='#0077b6')
    ax1.set_title('Original Time Series', fontsize=16, fontweight='bold')
    ax1.set_ylabel('Price ($)')

    # Trend component plot
    decompose.trend.plot(ax=ax2, color='#34a853')
    ax2.set_title('Trend Component', fontsize=16, fontweight='bold')
    ax2.set_ylabel('Price ($)')

    # Seasonal component plot
    decompose.seasonal.plot(ax=ax3, color='#fbbc05')
    ax3.set_title('Seasonal Component', fontsize=16, fontweight='bold')
    ax3.set_ylabel('Seasonal Factor')

    # Residual component plot
    decompose.resid.plot(ax=ax4, color='#ea4335')
    ax4.set_title('Residual Component', fontsize=16, fontweight='bold')
    ax4.set_ylabel('Residual')

    plt.xlabel('Date', fontsize=14, labelpad=15)
    plt.suptitle('Decomposition of Synthetic Brent Oil Price Time Series', fontsize=20, fontweight='bold')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

def get_switchpt(price):
    with pm.Model() as change_point_model:
        
        return 

