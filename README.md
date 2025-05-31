# ICapital Scraping tool Jobs
This tool is for take all the jobs in the website and classified by locations.

## Installation
# Create your enviroment in python
# This app have been tested with python 3.13
Then
Use pip to install the requirements

```bash
pip install -r requirements.txt
```


## Usage
By default works have this arguments: Department: 0 - 'All Departments', Offices: 1 - 'CA ON -Toronto', Employment Type: 1 - 'Full-time', Job Listing Level: 0 - 'All Jobs Levels'.


## Help Info
usage: icapitalscrap.py [-h] [--department DEPARTMENT] [--office OFFICE] [--employment_type EMPLOYMENT_TYPE] [--job_level JOB_LEVEL]

This are the arguments that can be passed if not passed the script take the next option Department: 0 - 'All Departments' Offices: 1 - 'CA ON -Toronto' Employment Type: 1 - 'Full-time' Job Listing Level: 0 - 'All Jobs Levels'


options:

  -h, --help            show this help message and exit

  --department DEPARTMENT
                        The departments aviables: 0-All Departments, 1-Alternative Solutions, 2-Alternatives Distribution, 3-Asset Managers,
                        4-Client Architecture Solutions, 5-Corporate Finance, 6-Corporate Technology, 7-Data Solutions, 8-Data and Analytics,
                        9-Distributed Ledger, 10-Fund Finance Central Services, 11-Fund Finance Hedge Funds, 12-Fund Finance Private Capital,
                        13-Fund Origination, 14-Global PR and Comms, 15-Intl Client Solutions - APAC, 16-Investor Relations, 17-People,
                        18-Platform Infrastructure, 19-Platform Operations, 20-Platform Technology Support, 21-Portfolio Analytics,
                        22-Portfolio Management, 23-Product Development, 24-Product and Audience, 25-Regulatory and Compliance, 26-Research and
                        Education, 27-Software Engineering, 28-Structured Investments,

  --office OFFICE       The office aviables: 0-All Offices, 1-CA ON - Toronto, 2-CH - Zurich, 3-CN - Hong Kong, 4-PT - Lisbon, 5-Remote, 6-SG -
                        Singapore, 7-UK GB - Edinburgh, 8-US CT - Greenwich, 9-US CT - Stamford, 10-US NY - New York City, 11-US UT - Salt Lake
                        City,

  --employment_type EMPLOYMENT_TYPE
                        The Employment Type aviables: 0-All Employment Types, 1-Full-time, 2-Part-time,

  --job_level JOB_LEVEL
                        The Job Level aviables: 0-All Job Levels, 1-Analyst, 2-Associate, 3-Assistant Vice President, 4-Vice President,
                        5-Senior Vice President, 6-Managing Director

                        
