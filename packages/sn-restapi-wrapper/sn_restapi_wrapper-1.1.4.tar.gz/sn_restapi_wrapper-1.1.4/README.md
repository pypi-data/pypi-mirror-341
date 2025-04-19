# sn_restapi_wrapper 

### About 

This package acts as a wrapper for ServiceNow RESTAPI application enabling a user to extract data from any table within ServiceNow within a particular time duration, ideally as a date-time format. 

The package overcomes the standard limitation of the ServiceNow RESTAPI by using a function of offset, with a rate limit of  5000 and then iterating over the users given time duration. To speed the efficiency of the package threading is used to execute tasks concurrently within the same process for a given time duration- where the tasks are split by the date.

### Installation 
Install the package into your env using ```pip install sn-restapi-wrapper```

### Requirements
The core-package requires these applications to be present at minimum
1. requests 
2. pandas 
3. concurrent.futures
4. tqdm 

### Usage

#### Standard Query - Without filters
```python
# ServiceNow credentials instance URL and endpoint
instance_url = 'https://xxx.service-now.com'  # Replace with specified url
endpoint = '/api/now/table/xxx'  # Replace with table name [incident, incident_task, ...]

# Replace 'username' and 'password' with ServiceNow credentials
username = 'xxx' 
password = 'xxx'

# Import the sn_restapi_wrapper as srw 
import sn_restapi_wrapper as srw

# Example usage:

# Specify a list of field names to extract
fields = []

# Important: specify fields names used in the backed system. If no fields are mentioned as a list all fields will be pulled but be more time consuming.

# Important: specify start/end date and  start/end time within specified format
start_date = 'yyyy-mm-dd'
end_date = 'yyyy-mm-dd'
start_time = 'HH:mi:ss'
end_time = 'HH:mi:ss'
date_field = 'xxx' # Ensure the date field is properly specified  e.g 'sys_created_on'

# Pulling data into a pandas dataframe
data = srw.fetch_filtered_data(
	instance_url, 
	endpoint, 
	date_field, 
	start_date, 
	end_date, 
	start_time, 
	end_time, 
	username, 
	password, 
	fields
)

# Examine data frame
data.shape
```
#### Custom Query - With filters
```python
# ServiceNow credentials instance URL and endpoint
instance_url = 'https://xxx.service-now.com'  # Replace with specified url
endpoint = '/api/now/table/xxx'  # Replace with table name [incident, incident_task, ...]

# Replace 'username' and 'password' with ServiceNow credentials
username = 'xxx' 
password = 'xxx'

# Import the sn_restapi_wrapper as srw 
import sn_restapi_wrapper as srw

# Example usage:

# Specify a list of field names to extract
fields = []

# Important: specify fields names used in the backed system. If no fields are mentioned as a list all fields will be pulled but be more time consuming.

# Important: specify start/end date and  start/end time within specified format
start_date = 'yyyy-mm-dd'
end_date = 'yyyy-mm-dd'
start_time = 'HH:mi:ss'
end_time = 'HH:mi:ss'
date_field = 'xxx' # Ensure the date field is properly specified  e.g 'sys_created_on'
filter = 'xxxxxxx' # Ensure additional filter is specified

# Pulling data into a pandas dataframe fetch_filtered_data_custom for filtered data
data = srw.fetch_filtered_data_custom(
	instance_url, 
	endpoint, 
	date_field, 
	start_date, 
	end_date, 
	start_time, 
	end_time, 
	username, 
	password, 
	fields,
	additional_filter=filter
)

# Examine data frame
data.shape
```
### License
This project is licensed under the MIT License. However, this doesnot include the ServiceNow RestAPI which is the sole property of ServiceNow. This is only a wrapper for the ServiceNow RestAPI.

### Contact
For support, please contact mihinduperera35@gmail.com