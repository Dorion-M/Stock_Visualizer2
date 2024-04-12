import csv
from flask import Flask, render_template, request, jsonify
from API_Functions import api_call
from Graphing_functions import filter_json_data, generate_chart, parse_date_string

app = Flask(__name__)

# Function to read stock tickers from CSV file
def read_stock_tickers_from_csv(csv_file):
    tickers = []
    try:
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if 'Symbol' in row:  # Ensure 'Symbol' column exists
                    tickers.append(row['Symbol'])
                else:
                    raise KeyError("Column 'Symbol' not found in CSV file.")
    except Exception as e:
        print(f"Error reading CSV file: {str(e)}")
    return tickers

# Route for rendering index.html with stock tickers
@app.route('/')
def index():
    # Read stock tickers from CSV file
    csv_file = 'stocks.csv'
    tickers = read_stock_tickers_from_csv(csv_file)
    
    # Render index.html template with stock tickers
    return render_template('index.html', tickers=tickers)

# Route for generating chart based on form submission
@app.route('/generate_chart', methods=['POST'])
def generate_chart_view():
    try:
        # Get form data from request
        stock_symbol = request.form['stock_symbol']
        chart_type = request.form['chart_type']
        time_series_function = request.form['time_series_function']
        start_date = parse_date_string(request.form['start_date'])
        end_date = parse_date_string(request.form['end_date'])

        # Get JSON data from Alpha Vantage API
        json_data = api_call(stock_symbol, time_series_function, start_date)

        if json_data:
            # Filter the JSON data based on the given start_date and end_date
            filtered_data = filter_json_data(json_data, start_date, end_date)

            if filtered_data:
                # Generate the chart
                chart = generate_chart(filtered_data, chart_type, stock_symbol, start_date, end_date)

                # Save the chart to an HTML string
                chart_html = chart.render(is_unicode=True)

                # Return the chart HTML content as JSON response
                return jsonify({'chart_html': chart_html})
            else:
                error_message = "No data found within the specified date range."
                return jsonify({'error_message': error_message}), 400
        else:
            error_message = "Failed to retrieve data from Alpha Vantage API."
            return jsonify({'error_message': error_message}), 500
    except Exception as e:
        error_message = f"Error generating chart: {str(e)}"
        return jsonify({'error_message': error_message}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0")
