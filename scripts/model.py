import pytensor.tensor as tt
import pymc as pm
import numpy as np
import pandas as pd
import arviz as az

def load(filename):
    try:
        return pd.read_csv(f'data/{filename}')
    except:
        print("Error occured during file read")
        return pd.DataFrame([])

def return_change_point():
    return change_point_results

def create_log_return():
    oil_prices_data['Log_Return'] = np.log(oil_prices_data['Price']).diff().dropna()
    log_return = oil_prices_data['Log_Return'].dropna()
    return log_return

def return_oli_data():
    return alt_price_data

def return_log_return():
    return log_returns_data

def return_posterior_mean_data():
    return posterior_means_data

def return_posterior_sds():
    return posterior_sds_data
def return_impact_probabilities():
    return impact_probabilities_data

def run_analysis():
    global oil_prices_data,alt_price_data, log_returns_data, change_point_results, log_return_data
    global posterior_means_data, posterior_sds_data, impact_probabilities_data, trace_volatility
    oil_prices_data = load('BrentOilPrices.csv')
    oil_prices_data['Date'] = pd.to_datetime(oil_prices_data['Date'], format="mixed")
    alt_price_data = oil_prices_data.copy(deep=True)
    oil_prices_data.set_index('Date', inplace=True)
    log_returns_data  = create_log_return()
    log_return_data = alt_price_data
     

    log_return = log_returns_data.values
    with pm.Model() as pmModel:
        tau = pm.DiscreteUniform('tau', lower=0, upper=len(log_return)-1)
        time_index = np.arange(len(log_return))
        #before and after
        mean_1 = pm.Normal('mean_1', mu=log_return.mean(), sigma=log_return.std() * 2)
        mean_2 = pm.Normal('mean_2', mu=log_return.mean(), sigma=log_return.std() * 2)
        std_1 = pm.HalfNormal('std_1', sigma=log_return.std())
        std_2 = pm.HalfNormal('std_2', sigma=log_return.std())
        mean = pm.math.switch(time_index < tau, mean_1, mean_2)
        std = pm.math.switch(time_index < tau, std_1, std_2)
        mu_log_return = pm.Normal('mu_log_return', mu=0, sigma=0.01)    
        observation = pm.Normal("observation", mu=mu_log_return, sigma=std, observed=log_return)
        print("\nStarting PyMC sampling for Bayesian Volatility Change Point Detection...")
        trace_volatility = pm.sample(draws=2000, tune=1000, chains=4, random_seed=42, return_inferencedata=True, cores=1)
        print("PyMC Sampling Complete.")
    tau_post = trace_volatility.posterior['tau'].mean().item()
    tau_index = int(tau_post)
    tau_hdi = az.hdi(trace_volatility, var_names=['tau'])['tau'].values
    hpd_start_date = oil_prices_data.index[int(tau_hdi[0])].strftime('%Y-%m-%d')
    hpd_end_date = oil_prices_data.index[int(tau_hdi[1])].strftime('%Y-%m-%d')
    change_point_date = oil_prices_data.index[tau_index]
    change_point_results = {
        'tau_post_index': tau_post,
        'change_point_date': change_point_date,
        'hpd_start_date': hpd_start_date,
        'hpd_end_date': hpd_end_date,
        'event_name': None,
        'event_type': None
    }
    posterior_means_data = {
        'mean_1': trace_volatility.posterior['mean_1'].mean().item(),
        'mean_2': trace_volatility.posterior['mean_2'].mean().item()
    }
    posterior_sds_data = {
        'sd_1': trace_volatility.posterior['std_1'].mean().item(),
        'sd_2': trace_volatility.posterior['std_2'].mean().item()
    }

    # --- Calculate and Store Impact Probabilities ---
    prob_mean_increase = (trace_volatility.posterior['mean_2'] > trace_volatility.posterior['mean_1']).mean().item()
    prob_sd_increase = (trace_volatility.posterior['std_2'] > trace_volatility.posterior['std_1']).mean().item()
    
    impact_probabilities_data = {
        'prob_mean_increase': prob_mean_increase,
        'prob_sd_increase': prob_sd_increase
    }

def map_events():
    events = load('events.csv')
    hpd_start = change_point_results['hpd_start_date']
    hdp_end = change_point_results['hpd_end_date']
    if change_point_results != None:
        filter_event = events[(hpd_start <=  events['Approximate_Start_Date']) & (hdp_end > events['Approximate_Start_Date'])]
        print(hpd_start)
        print(hdp_end)
        print(filter_event)
        # change_point_results['event_name'] = filter_event['Event_Name'  ]
        # change_point_results['event_type'] = filter_event['Event_Type']


if __name__ == "__main__":
    run_analysis()