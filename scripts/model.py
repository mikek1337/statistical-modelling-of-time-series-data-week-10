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
    return all_posterior_means

def return_posterior_sds():
    return all_posterior_sds
def return_impact_probabilities():
    return all_posterior

def run_analysis():
    global oil_prices_data,alt_price_data, log_returns_data, change_point_results, log_return_data
    global all_posterior_means, all_posterior_sds, all_impact_probabilities, trace_volatility, all_posterior
    oil_prices_data = load('BrentOilPrices.csv')
    oil_prices_data['Date'] = pd.to_datetime(oil_prices_data['Date'], format="mixed")
    alt_price_data = oil_prices_data.copy(deep=True)
    oil_prices_data.set_index('Date', inplace=True)
    log_returns_data  = create_log_return()
    log_return_data = alt_price_data
     

    log_return = log_returns_data.values
    num_change_point = 5
    with pm.Model() as pmModel:
        tau = pm.DiscreteUniform('taus', lower=np.arange(num_change_point), upper=np.arange(len(log_return) - num_change_point, len(log_return)))
        time_index = np.arange(len(log_return))
        #before and after
        segment_means = [pm.Normal(f'mean_{i+1}', mu=log_return.mean(), sigma=log_return.std() * 2)
                     for i in range(num_change_point + 1)]
        segment_stds = [pm.HalfNormal(f'std_{i+1}', sigma=log_return.std())
                    for i in range(num_change_point + 1)]
        current_mean = segment_means[0]
        current_std = segment_stds[0]

        for i in range(num_change_point):
            current_mean =  pm.math.switch(time_index < tau[i], current_mean, segment_means[i+1])
            current_std = pm.math.switch(time_index < tau[i], current_std, segment_stds[i+1])
        observation = pm.Normal("observation", mu=current_mean, sigma=current_std, observed=log_return)
        trace_volatility = pm.sample(draws=2000, tune=1000, chains=4, random_seed=42, return_inferencedata=True, cores=1)
        # mean_1 = pm.Normal('mean_1', mu=log_return.mean(), sigma=log_return.std() * 2)
        # mean_2 = pm.Normal('mean_2', mu=log_return.mean(), sigma=log_return.std() * 2)
        # std_1 = pm.HalfNormal('std_1', sigma=log_return.std())
        # std_2 = pm.HalfNormal('std_2', sigma=log_return.std())
        # mean = pm.math.switch(time_index < tau, mean_1, mean_2)
        # std = pm.math.switch(time_index < tau, std_1, std_2)
        # mu_log_return = pm.Normal('mu_log_return', mu=0, sigma=0.01)    
        # observation = pm.Normal("observation", mu=mu_log_return, sigma=std, observed=log_return)
        # print("\nStarting PyMC sampling for Bayesian Volatility Change Point Detection...")
        # trace_volatility = pm.sample(draws=4000, tune=2000, chains=8, random_seed=42, return_inferencedata=True, cores=1)
        # print("PyMC Sampling Complete.")
    change_point_results = []
    change_points = trace_volatility.posterior['taus'].shape[-1]
    for i in range(change_points):
        tau_post_index = trace_volatility.posterior['taus'].sel(taus_dim_0=i).mean().item()
        single_tau_posterior_samples = trace_volatility.posterior['taus'].isel(taus_dim_0=i)
        tau_index = int(round(tau_post_index))
        # tau_hdi = az.hdi(single_tau_posterior_samples).values
        hdi_values = az.hdi(single_tau_posterior_samples)['taus'].values
        
        data_length = len(oil_prices_data.index)
        hpd_start_idx = max(0, min(data_length - 1, int(round(hdi_values[0]))))
        hpd_end_idx = max(0, min(data_length - 1, int(round(hdi_values[1]))))
        if hpd_end_idx < hpd_start_idx:
            hpd_end_idx = hpd_start_idx
        hpd_start_date = oil_prices_data.index[hpd_start_idx].strftime('%Y-%m-%d')
        hpd_end_date = oil_prices_data.index[hpd_end_idx].strftime('%Y-%m-%d')
        # hpd_start_idx = max(0, int(round(tau_hdi[0])))
        # hpd_end_idx = min(len(oil_prices_data.index) - 1, int(round(tau_hdi[1])))
        change_point_date = oil_prices_data.index[tau_index].strftime('%Y-%m-%d')
        # hpd_start_date = oil_prices_data.index[hpd_start_idx].strftime('%Y-%m-%d')
        # hpd_end_date = oil_prices_data.index[hpd_end_idx].strftime('%Y-%m-%d')
        description = f"Change Point {i+1} in oil price dynamics."

        change_point_results.append({
            'id': f'cp{i+1}',
            'tau_post_index': tau_post_index,
            'change_point_date': change_point_date,
            'hpd_start_date': hpd_start_date,
            'hpd_end_date': hpd_end_date,
            'description': description
        })
    print(change_point_results)
    num_segments = num_change_point + 1 # Number of segments is 1 more than change points

    all_posterior_means = {}
    all_posterior_sds = {}
    all_posterior = {}
    mean=[]
    std=[]

    for i in range(1, num_segments + 1):
        mean_key = f'mean_{i}'
        std_key = f'std_{i}'

        # Check if the parameter exists in the trace before trying to access
        if mean_key in trace_volatility.posterior:
            all_posterior_means['mean_prob'] = trace_volatility.posterior[mean_key].mean().item()
            mean.append(all_posterior_means)
            
        if std_key in trace_volatility.posterior:
            all_posterior_sds['std_prob'] = trace_volatility.posterior[std_key].mean().item()
            std.append(all_posterior_sds)

    all_posterior["all_mean"] = mean;
    all_posterior['all_std'] = std

    all_impact_probabilities = {}

    for i in range(num_change_point):
        # Compare current segment (i+1) with the next segment (i+2)
        current_mean_var = f'mean_{i+1}'
        next_mean_var = f'mean_{i+2}'
        current_std_var = f'std_{i+1}'
        next_std_var = f'std_{i+2}'

        # Ensure both segments exist in the trace
        if next_mean_var in trace_volatility.posterior and current_mean_var in trace_volatility.posterior:
            prob_mean_increase = (trace_volatility.posterior[next_mean_var] > trace_volatility.posterior[current_mean_var]).mean().item()
            prob_mean_decrease = (trace_volatility.posterior[next_mean_var] < trace_volatility.posterior[current_mean_var]).mean().item()
            all_impact_probabilities[f'mean_change_seg{i+1}_to_seg{i+2}'] = {
                'increase_prob': prob_mean_increase,
                'decrease_prob': prob_mean_decrease
            }

        if next_std_var in trace_volatility.posterior and current_std_var in trace_volatility.posterior:
            prob_sd_increase = (trace_volatility.posterior[next_std_var] > trace_volatility.posterior[current_std_var]).mean().item()
            prob_sd_decrease = (trace_volatility.posterior[next_std_var] < trace_volatility.posterior[current_std_var]).mean().item()
            all_impact_probabilities[f'std_change_seg{i+1}_to_seg{i+2}'] = {
                'increase_prob': prob_sd_increase,
                'decrease_prob': prob_sd_decrease
            }

    # tau_post = trace_volatility.posterior['tau'].mean().item()  
    # tau_index = int(tau_post)
    # tau_hdi = az.hdi(trace_volatility, var_names=['tau']    )['tau'].values
    # hpd_start_date = oil_prices_data.index[int(tau_hdi[0])].strftime('%Y-%m-%d')
    # hpd_end_date = oil_prices_data.index[int(tau_hdi[1])].strftime('%Y-%m-%d')
    # change_point_date = oil_prices_data.index[tau_index]
    # change_point_results = {
    #     'tau_post_index': tau_post,
    #     'change_point_date': change_point_date,
    #     'hpd_start_date': hpd_start_date,
    #     'hpd_end_date': hpd_end_date,
    #     'event_name': None,
    #     'event_type': None
    # }
    # print(change_point_results)
    # posterior_means_data = {
    #     'mean_1': trace_volatility.posterior['mean_1'].mean().item(),
    #     'mean_2': trace_volatility.posterior['mean_2'].mean().item()
    # }
    # posterior_sds_data = {
    #     'sd_1': trace_volatility.posterior['std_1'].mean().item(),
    #     'sd_2': trace_volatility.posterior['std_2'].mean().item()
    # }

    # # --- Calculate and Store Impact Probabilities ---
    # prob_mean_increase = (trace_volatility.posterior['mean_2'] > trace_volatility.posterior['mean_1']).mean().item()
    # prob_sd_increase = (trace_volatility.posterior['std_2'] > trace_volatility.posterior['std_1']).mean().item()
    
    # impact_probabilities_data = {
    #     'prob_mean_increase': prob_mean_increase,
    #     'prob_sd_increase': prob_sd_increase
    # }

def map_events(change_point_date):
    events = load('events.csv')
    timeWindow = 204
    change_point_date = pd.to_datetime(change_point_date) 
    events['Approximate_Start_Date'] = pd.to_datetime(events['Approximate_Start_Date'])

    if change_point_results != None:
        print(abs(change_point_date - events['Approximate_Start_Date'])<= pd.Timedelta(timeWindow))
        filter_event = events[abs(change_point_date - events['Approximate_Start_Date']) <= pd.Timedelta(timeWindow)]
        print(filter_event)
        # change_point_results['event_name'] = filter_event['Event_Name'  ]
        # change_point_results['event_type'] = filter_event['Event_Type']


if __name__ == "__main__":
    run_analysis()