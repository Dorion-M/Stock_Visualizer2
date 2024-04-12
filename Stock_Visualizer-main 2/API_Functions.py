import requests

def api_call(stock_symbol, time_series_function, start_date):
    base_url = 'https://www.alphavantage.co/query?' #base url
    time_series_functions = {
        '1': 'TIME_SERIES_INTRADAY',
        '2': 'TIME_SERIES_DAILY',
        '3': 'TIME_SERIES_WEEKLY',
        '4': 'TIME_SERIES_MONTHLY'
    }

    function = time_series_functions[time_series_function]
    api_key = 'NB0AK6IK339LRUMR'
    params = f'function={function}&symbol={stock_symbol}&apikey={api_key}'  #construct the parameters based on user input

    if function == 'TIME_SERIES_INTRADAY':
        interval = '60min'

        params += f'&interval={interval}&outputsize=full&month={start_date.year}-{start_date.strftime("%m")}'
    elif function == 'TIME_SERIES_DAILY':
        params += f'&outputsize=full'

    r = requests.get(base_url + params)  

    if r.status_code == 200:  
        #print(r.json())          
        return r.json()                  
    else:
        print(f"Error: {r.status_code} - {r.text}")
        return None

