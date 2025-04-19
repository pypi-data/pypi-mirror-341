import requests
import pandas as pd
import concurrent.futures
from tqdm import tqdm

# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# standard data querry for unfiltered data

def get_result(url, date_field, start_date, end_date, start_time, end_time, offset, limit, username, password, fields):
    start_datetime = f'{start_date} {start_time}'
    end_datetime = f'{end_date} {end_time}'
    
    params = {
        'sysparm_limit': str(limit),
        'sysparm_offset': str(offset),
        'sysparm_query': f'{date_field}>=javascript:gs.dateGenerate("{start_datetime}")^{date_field}<=javascript:gs.dateGenerate("{end_datetime}")',
        'sysparm_fields': ','.join(fields),
        'sysparm_display_value': 'true',
        'sysparm_exclude_reference_link': 'true'
    }
    response = requests.get(url, auth=(username, password), params=params, verify=False)
    if response.status_code == 200:
        data = response.json()
        return data.get('result')
    return None

def fetch_data_for_date(url, date_field, start_date, end_date, start_time, end_time, username, password, fields, limit=5000):
    data_list = []
    offset = 0
    while True:
        result = get_result(url, date_field, start_date, end_date, start_time, end_time, offset, limit, username, password, fields)
        if not result:
            break
        data_list.append(result)
        offset += limit
    return data_list

def fetch_filtered_data(instance_url, endpoint, date_field, start_date, end_date, start_time, end_time, username, password, fields=None, limit=5000):
    url = instance_url + endpoint
    data_list = []
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    total_dates = len(date_range)
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(fetch_data_for_date, url, date_field, date.strftime('%Y-%m-%d'), date.strftime('%Y-%m-%d'), start_time, end_time, username, password, fields): date for date in date_range}
        
        with tqdm(total=total_dates, desc="Progress", position=0) as pbar:
            for future in concurrent.futures.as_completed(futures):
                data_list.extend(future.result())
                pbar.update(1)  # Increment the progress bar by 1 for each completed date
    
    combined_data = pd.concat([pd.DataFrame(data) for data in data_list], ignore_index=True)
    return combined_data


# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# custom querry for filtered data

def get_result_custom(url, date_field, start_date, end_date, start_time, end_time, offset, limit, username, password, fields, additional_filter=None):
    start_datetime = f'{start_date} {start_time}'
    end_datetime = f'{end_date} {end_time}'
    
    query = f'{date_field}>=javascript:gs.dateGenerate("{start_datetime}")^{date_field}<=javascript:gs.dateGenerate("{end_datetime}")'
    
    if additional_filter:
        query += f'^{additional_filter}'
    
    params = {
        'sysparm_limit': str(limit),
        'sysparm_offset': str(offset),
        'sysparm_query': query,
        'sysparm_fields': ','.join(fields),
        'sysparm_display_value': 'true',
        'sysparm_exclude_reference_link': 'true'
    }
    response = requests.get(url, auth=(username, password), params=params, verify=False)
    if response.status_code == 200:
        data = response.json()
        return data.get('result')
    return None

def fetch_data_for_date_custom(url, date_field, start_date, end_date, start_time, end_time, username, password, fields, limit=5000, additional_filter=None):
    data_list = []
    offset = 0
    while True:
        result = get_result_custom(url, date_field, start_date, end_date, start_time, end_time, offset, limit, username, password, fields, additional_filter)
        if not result:
            break
        data_list.append(result)
        offset += limit
    return data_list

def fetch_filtered_data_custom(instance_url, endpoint, date_field, start_date, end_date, start_time, end_time, username, password, fields=None, limit=5000, additional_filter=None):
    url = instance_url + endpoint
    data_list = []
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    total_dates = len(date_range)
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(fetch_data_for_date_custom, url, date_field, date.strftime('%Y-%m-%d'), date.strftime('%Y-%m-%d'), start_time, end_time, username, password, fields, limit, additional_filter): date for date in date_range}
        
        with tqdm(total=total_dates, desc="Progress", position=0) as pbar:
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    if result:
                        data_list.extend(result)
                except Exception as e:
                    print(f"Error fetching data: {e}")
                pbar.update(1)  # Increment the progress bar by 1 for each completed date
    
    if data_list:
        combined_data = pd.concat([pd.DataFrame(data) for data in data_list if data], ignore_index=True)
        return combined_data
    else:
        return pd.DataFrame()