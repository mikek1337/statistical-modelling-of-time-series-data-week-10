from flask import Flask, jsonify
import sys
import pandas as pd
sys.path.append('scripts')
from model import run_analysis, return_change_point, return_oli_data, return_log_return, return_posterior_mean_data, return_posterior_sds, return_impact_probabilities

app = Flask(__name__)
run_analysis()
oil_prices_data = return_oli_data()
log_returns_data = return_log_return()
change_point_results = return_change_point()
posterior_means_data = return_posterior_mean_data()
posterior_sds_data = return_posterior_sds()
impact_probabilities_data = return_impact_probabilities()

@app.route('/api/oil_prices', methods=['GET'])
def get_oil_prices():
    """Returns the preprocessed monthly oil prices."""
    if oil_prices_data is not None:
        # Convert pandas Series to a list of dictionaries for JSON serialization
        # Each dictionary contains 'date' and 'price'
        try:
            data_for_json = [{'date': str(idx.strftime('%Y-%m-%d')), 'price': val} 
                for idx, val in oil_prices_data.items()]
            return jsonify(data_for_json)
        except:
            pass
        print(data_for_json)
    return jsonify({"error": "Oil prices data not available"}), 500

@app.route('/api/log_returns', methods=['GET'])
def get_log_returns():
    """Returns the log returns of the oil prices."""
    if log_returns_data is not None:
        data_for_json = [{'date': str(idx.strftime('%Y-%m-%d')), 'log_return': val} 
                         for idx, val in log_returns_data.items()]
        return jsonify(data_for_json)
    return jsonify({"error": "Log returns data not available"}), 500

@app.route('/api/change_point_summary', methods=['GET'])
def get_change_point_summary():
    """Returns the summary of the Bayesian change point detection."""
    if change_point_results:
        return jsonify(change_point_results)
    return jsonify({"error": "Change point summary not available"}), 500

@app.route('/api/posterior_means', methods=['GET'])
def get_posterior_means():
    """Returns the posterior means of the 'before' and 'after' segments."""
    if posterior_means_data:
        return jsonify(posterior_means_data)
    return jsonify({"error": "Posterior means not available"}), 500

@app.route('/api/posterior_sds', methods=['GET'])
def get_posterior_sds():
    """Returns the posterior standard deviations of the 'before' and 'after' segments."""
    if posterior_sds_data:
        return jsonify(posterior_sds_data)
    return jsonify({"error": "Posterior standard deviations not available"}), 500

@app.route('/api/impact_probabilities', methods=['GET'])
def get_impact_probabilities():
    """Returns the calculated probabilities of mean/volatility increase."""
    if impact_probabilities_data:
        return jsonify(impact_probabilities_data)
    return jsonify({"error": "Impact probabilities not available"}), 500

@app.route('/', methods=['GET'])
def index():
    """Simple root endpoint to confirm the API is running."""
    return "Oil Price Analysis Backend is running!"

if __name__ == "__main__":
    app.run(debug=True)