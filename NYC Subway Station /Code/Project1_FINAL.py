{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Problem statement:\n",
    "WTWY needs to optimize their street teams so that they can get the most email signups for their annual OMGYN Gala. Ideally, the email signups will convert at a high rate to gala attendees, and among attendees, many will make contributions to WTWY.\n",
    "\n",
    "MTA data obtained from the NYC Data Portal provides rich information about the travel patterns of New Yorkers -- using this information, can we create a street team deployment plan that will optimize WTWY’s resources toward achieving their goals?"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Import useful libaries for analysis"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "import pickle"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "%matplotlib inline"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Below are a few functions that will help us conveniently download the data from the MTA website"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "def read_MTA_data(list_of_dates):\n",
    "    '''\n",
    "    1. Takes a list of dates in the form of 'yymmdd' and \n",
    "    extracts the .txt file corresponding to the dates \n",
    "    from 'http://web.mta.info/developers/turnstile.html.'\n",
    "    \n",
    "    2. Converts each extraction to a csv file\n",
    "    \n",
    "    3. Concatenates all the csv files into a single dataframe\n",
    "    '''\n",
    "    # Initiate an empty dataframe \n",
    "    combined_df = pd.DataFrame()\n",
    "    \n",
    "    root_url = 'http://web.mta.info/developers/data/nyct/turnstile/turnstile_'\n",
    "    \n",
    "    # loop through the url links and concatenate all the data set into a one\n",
    "    for date in list_of_dates:\n",
    "        # represents a url link matching each date provided\n",
    "        MTA_url = f'{root_url}{date}.txt'\n",
    "        # converts the url into csv file \n",
    "        dataset = pd.read_csv(MTA_url)\n",
    "        # concatenate the obtained dataset to the overall dataframe\n",
    "        combined_df = pd.concat([combined_df, dataset], ignore_index = True)\n",
    "    \n",
    "    return combined_df"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "def all_SAT(year):\n",
    "    '''\n",
    "    Takes in a year yyyy and returns all the saturdays in yyyy\n",
    "    in the format of yymmdd\n",
    "    '''\n",
    "    return pd.date_range(start=str(year), end=str(year+1), \n",
    "                         freq='W-SAT').strftime('%y%m%d').tolist()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "def month_filter(list_of_dates, list_of_months):\n",
    "    \n",
    "    '''\n",
    "    Takes a list of dates in format yymmdd and a list of months in format mm\n",
    "        - The list_of_months contains the months of interest\n",
    "    \n",
    "    Returns a list of dates from the list list_of_dates that only contains\n",
    "    the months of interest\n",
    "    '''\n",
    "    \n",
    "    # Initial an empty list of dates\n",
    "    dates_for_months = []\n",
    "    for month in list_of_months:\n",
    "        # return the dates containing the months of interest in list_of_dates\n",
    "        filtered_dates = list(filter(lambda x: (x[2:4] in month), list_of_dates))\n",
    "        dates_for_months += filtered_dates\n",
    "    \n",
    "    return dates_for_months"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Import MTA data for the months of April, May, June of 2019"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Since the DataFrame is fairly large, we will use pickle to save it to bytes."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create a list of dates (SATURDAY) for the year of 2019\n",
    "sat_2019 = all_SAT(2019)\n",
    "\n",
    "# Filter the year to only April, May, and June\n",
    "months_of_interest = ['04', '05', '06']\n",
    "april_may_june_2019 = month_filter(sat_2019, months_of_interest)\n",
    "\n",
    "# Read each date into a combined dataframe using read_MTA_data containing April, May, and June of 2019\n",
    "summer19_MTA = read_MTA_data(april_may_june_2019)\n",
    "summer19_MTA.head(25)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pickle \n",
    "\n",
    "with open('summer19_MTA.pickle', 'wb') as to_write:\n",
    "    pickle.dump(summer19_MTA, to_write)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Now the DataFrame is saved into bytes. We can open it with without having to run previous cells."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [],
   "source": [
    "with open('summer19_MTA.pickle', 'rb') as to_read:\n",
    "    summer19_MTA = pickle.load(to_read)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>C/A</th>\n",
       "      <th>UNIT</th>\n",
       "      <th>SCP</th>\n",
       "      <th>STATION</th>\n",
       "      <th>LINENAME</th>\n",
       "      <th>DIVISION</th>\n",
       "      <th>DATE</th>\n",
       "      <th>TIME</th>\n",
       "      <th>DESC</th>\n",
       "      <th>ENTRIES</th>\n",
       "      <th>EXITS</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>A002</td>\n",
       "      <td>R051</td>\n",
       "      <td>02-00-00</td>\n",
       "      <td>59 ST</td>\n",
       "      <td>NQR456W</td>\n",
       "      <td>BMT</td>\n",
       "      <td>03/30/2019</td>\n",
       "      <td>00:00:00</td>\n",
       "      <td>REGULAR</td>\n",
       "      <td>6999064</td>\n",
       "      <td>2373568</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>A002</td>\n",
       "      <td>R051</td>\n",
       "      <td>02-00-00</td>\n",
       "      <td>59 ST</td>\n",
       "      <td>NQR456W</td>\n",
       "      <td>BMT</td>\n",
       "      <td>03/30/2019</td>\n",
       "      <td>04:00:00</td>\n",
       "      <td>REGULAR</td>\n",
       "      <td>6999084</td>\n",
       "      <td>2373576</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>A002</td>\n",
       "      <td>R051</td>\n",
       "      <td>02-00-00</td>\n",
       "      <td>59 ST</td>\n",
       "      <td>NQR456W</td>\n",
       "      <td>BMT</td>\n",
       "      <td>03/30/2019</td>\n",
       "      <td>08:00:00</td>\n",
       "      <td>REGULAR</td>\n",
       "      <td>6999107</td>\n",
       "      <td>2373622</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>A002</td>\n",
       "      <td>R051</td>\n",
       "      <td>02-00-00</td>\n",
       "      <td>59 ST</td>\n",
       "      <td>NQR456W</td>\n",
       "      <td>BMT</td>\n",
       "      <td>03/30/2019</td>\n",
       "      <td>12:00:00</td>\n",
       "      <td>REGULAR</td>\n",
       "      <td>6999214</td>\n",
       "      <td>2373710</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>A002</td>\n",
       "      <td>R051</td>\n",
       "      <td>02-00-00</td>\n",
       "      <td>59 ST</td>\n",
       "      <td>NQR456W</td>\n",
       "      <td>BMT</td>\n",
       "      <td>03/30/2019</td>\n",
       "      <td>16:00:00</td>\n",
       "      <td>REGULAR</td>\n",
       "      <td>6999451</td>\n",
       "      <td>2373781</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "    C/A  UNIT       SCP STATION LINENAME DIVISION        DATE      TIME  \\\n",
       "0  A002  R051  02-00-00   59 ST  NQR456W      BMT  03/30/2019  00:00:00   \n",
       "1  A002  R051  02-00-00   59 ST  NQR456W      BMT  03/30/2019  04:00:00   \n",
       "2  A002  R051  02-00-00   59 ST  NQR456W      BMT  03/30/2019  08:00:00   \n",
       "3  A002  R051  02-00-00   59 ST  NQR456W      BMT  03/30/2019  12:00:00   \n",
       "4  A002  R051  02-00-00   59 ST  NQR456W      BMT  03/30/2019  16:00:00   \n",
       "\n",
       "      DESC  ENTRIES  \\\n",
       "0  REGULAR  6999064   \n",
       "1  REGULAR  6999084   \n",
       "2  REGULAR  6999107   \n",
       "3  REGULAR  6999214   \n",
       "4  REGULAR  6999451   \n",
       "\n",
       "   EXITS                                                                 \n",
       "0                                            2373568                     \n",
       "1                                            2373576                     \n",
       "2                                            2373622                     \n",
       "3                                            2373710                     \n",
       "4                                            2373781                     "
      ]
     },
     "execution_count": 8,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "summer19_MTA.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<class 'pandas.core.frame.DataFrame'>\n",
      "RangeIndex: 2664248 entries, 0 to 2664247\n",
      "Data columns (total 11 columns):\n",
      "C/A                                                                     object\n",
      "UNIT                                                                    object\n",
      "SCP                                                                     object\n",
      "STATION                                                                 object\n",
      "LINENAME                                                                object\n",
      "DIVISION                                                                object\n",
      "DATE                                                                    object\n",
      "TIME                                                                    object\n",
      "DESC                                                                    object\n",
      "ENTRIES                                                                 int64\n",
      "EXITS                                                                   int64\n",
      "dtypes: int64(2), object(9)\n",
      "memory usage: 223.6+ MB\n",
      "We have a total of 2664248 data points\n"
     ]
    }
   ],
   "source": [
    "summer19_MTA.info()\n",
    "print(f'We have a total of {np.shape(summer19_MTA)[0]} data points')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Index(['C/A', 'UNIT', 'SCP', 'STATION', 'LINENAME', 'DIVISION', 'DATE', 'TIME',\n",
       "       'DESC', 'ENTRIES',\n",
       "       'EXITS                                                               '],\n",
       "      dtype='object')"
      ]
     },
     "execution_count": 10,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Let's examine the column names\n",
    "summer19_MTA.columns"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Eliminate column name mistakes such as 'EXITS         '"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Use string method strip to eliminate all spacings before and after in a string.\n",
    "summer19_MTA.columns = summer19_MTA.columns.str.strip()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Make Unique Station names with combination of STATION and LINENAME"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [],
   "source": [
    "summer19_MTA['Unique_Station'] = summer19_MTA['STATION'] + '_' + summer19_MTA['LINENAME']"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Since the ENTRIES and EXITS are accumulations of traffic per every 4 hours, we create two columns that accounts for the differences to track the actual number of entires and exits.\n",
    "\n",
    "In addition, we will treat the sum of number of entries and exits in a specifc station to be our total traffic for that station."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [],
   "source": [
    "summer19_MTA['ENTRIES DIFF'] = summer19_MTA['ENTRIES'].diff()\n",
    "summer19_MTA['EXITS DIFF'] = summer19_MTA['EXITS'].diff()\n",
    "summer19_MTA['Total_Traffic'] = summer19_MTA['ENTRIES DIFF'] + summer19_MTA['EXITS DIFF']"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "We want to convert the date to the day of the week"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {},
   "outputs": [],
   "source": [
    "import datetime\n",
    "import calendar\n",
    "\n",
    "def findDay(date): \n",
    "    \n",
    "    '''\n",
    "    grabs the data in the format mm/dd/yy \n",
    "    and returns the day of the week\n",
    "    '''\n",
    "    mmddyy = datetime.datetime.strptime(date, '%m/%d/%Y').weekday() \n",
    "    return (calendar.day_name[mmddyy]) "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Create a new column to indicate what day of the week it is. We can use this information later."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {},
   "outputs": [],
   "source": [
    "summer19_MTA['DAY_OF_WEEK'] = summer19_MTA['DATE'].apply(lambda date: findDay(date))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Let's group by each unique station and sum the total traffic in April, May, and June of 2019"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>ENTRIES</th>\n",
       "      <th>EXITS</th>\n",
       "      <th>ENTRIES DIFF</th>\n",
       "      <th>EXITS DIFF</th>\n",
       "      <th>Total_Traffic</th>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Unique_Station</th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>1 AV_L</th>\n",
       "      <td>799849750681</td>\n",
       "      <td>828041356350</td>\n",
       "      <td>-5.677284e+07</td>\n",
       "      <td>-9.944337e+07</td>\n",
       "      <td>-1.562162e+08</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>103 ST-CORONA_7</th>\n",
       "      <td>39770511766</td>\n",
       "      <td>40001193343</td>\n",
       "      <td>5.963920e+07</td>\n",
       "      <td>1.046125e+08</td>\n",
       "      <td>1.642517e+08</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>103 ST_1</th>\n",
       "      <td>36123986643</td>\n",
       "      <td>19507779049</td>\n",
       "      <td>1.471258e+08</td>\n",
       "      <td>1.387234e+08</td>\n",
       "      <td>2.858493e+08</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>103 ST_6</th>\n",
       "      <td>283467824157</td>\n",
       "      <td>507193667658</td>\n",
       "      <td>-3.908337e+09</td>\n",
       "      <td>3.902927e+09</td>\n",
       "      <td>-5.409978e+06</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>103 ST_BC</th>\n",
       "      <td>16335771399</td>\n",
       "      <td>14068256692</td>\n",
       "      <td>6.274388e+07</td>\n",
       "      <td>1.079485e+08</td>\n",
       "      <td>1.706924e+08</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>104 ST_A</th>\n",
       "      <td>929908198748</td>\n",
       "      <td>544226211876</td>\n",
       "      <td>2.181723e+10</td>\n",
       "      <td>1.271053e+10</td>\n",
       "      <td>3.452776e+10</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>104 ST_JZ</th>\n",
       "      <td>1715206978839</td>\n",
       "      <td>1385219485966</td>\n",
       "      <td>4.322307e+07</td>\n",
       "      <td>5.862511e+07</td>\n",
       "      <td>1.018482e+08</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>110 ST_6</th>\n",
       "      <td>21024033135</td>\n",
       "      <td>20218237598</td>\n",
       "      <td>-4.293304e+09</td>\n",
       "      <td>-3.844511e+09</td>\n",
       "      <td>-8.137816e+09</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>111 ST_7</th>\n",
       "      <td>28809071524</td>\n",
       "      <td>17589378769</td>\n",
       "      <td>-2.965029e+06</td>\n",
       "      <td>-4.931508e+07</td>\n",
       "      <td>-5.228011e+07</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>111 ST_A</th>\n",
       "      <td>31361894403</td>\n",
       "      <td>11327343682</td>\n",
       "      <td>-2.184806e+10</td>\n",
       "      <td>-1.271699e+10</td>\n",
       "      <td>-3.456505e+10</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                       ENTRIES          EXITS  ENTRIES DIFF    EXITS DIFF  \\\n",
       "Unique_Station                                                              \n",
       "1 AV_L            799849750681   828041356350 -5.677284e+07 -9.944337e+07   \n",
       "103 ST-CORONA_7    39770511766    40001193343  5.963920e+07  1.046125e+08   \n",
       "103 ST_1           36123986643    19507779049  1.471258e+08  1.387234e+08   \n",
       "103 ST_6          283467824157   507193667658 -3.908337e+09  3.902927e+09   \n",
       "103 ST_BC          16335771399    14068256692  6.274388e+07  1.079485e+08   \n",
       "104 ST_A          929908198748   544226211876  2.181723e+10  1.271053e+10   \n",
       "104 ST_JZ        1715206978839  1385219485966  4.322307e+07  5.862511e+07   \n",
       "110 ST_6           21024033135    20218237598 -4.293304e+09 -3.844511e+09   \n",
       "111 ST_7           28809071524    17589378769 -2.965029e+06 -4.931508e+07   \n",
       "111 ST_A           31361894403    11327343682 -2.184806e+10 -1.271699e+10   \n",
       "\n",
       "                 Total_Traffic  \n",
       "Unique_Station                  \n",
       "1 AV_L           -1.562162e+08  \n",
       "103 ST-CORONA_7   1.642517e+08  \n",
       "103 ST_1          2.858493e+08  \n",
       "103 ST_6         -5.409978e+06  \n",
       "103 ST_BC         1.706924e+08  \n",
       "104 ST_A          3.452776e+10  \n",
       "104 ST_JZ         1.018482e+08  \n",
       "110 ST_6         -8.137816e+09  \n",
       "111 ST_7         -5.228011e+07  \n",
       "111 ST_A         -3.456505e+10  "
      ]
     },
     "execution_count": 16,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "summer19_MTA.groupby('Unique_Station').sum().head(10)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Some of the total traffic for each unique station are negative which does not make senses. We need to investigate why this is the case."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 1152x288 with 2 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "plt.figure(figsize = [16,4])\n",
    "plt.subplot(1,2,1)\n",
    "sns.distplot(summer19_MTA['Total_Traffic'][1:]);\n",
    "plt.title('Distribution of Total Traffic', size = 20);\n",
    "plt.subplot(1,2,2)\n",
    "sns.boxplot(summer19_MTA.Total_Traffic[1:]);\n",
    "plt.title('Box Plot of Total Traffic', size = 20);\n",
    "sns.despine()\n",
    "plt.savefig('Initial Distribution Plots.png')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Plotting the distribution and box plot, we can see that we have some very large positive values or very large negative values. We need to filter down the values to something that makes sense.\n",
    "\n",
    "1. we should remove all negative traffic\n",
    "2. We can calculate the IQR for total traffic per four hours per scp to use as our mask filter."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "We have a total of 2664248 data points\n"
     ]
    }
   ],
   "source": [
    "# remove all negative traffic\n",
    "mask = summer19_MTA['Total_Traffic'] > 0\n",
    "summer19_MTA_pos = summer19_MTA[mask]\n",
    "\n",
    "print(f'We have a total of {np.shape(summer19_MTA)[0]} data points')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "-627.5 1112.5\n"
     ]
    }
   ],
   "source": [
    "# calculate the 25th, 50th, and 75th quartiles\n",
    "q25, q50, q75 = np.percentile(summer19_MTA.Total_Traffic[1:], [25, 50, 75])\n",
    "\n",
    "# interquartile range use to calculate the max and min values from the data set\n",
    "IQR = q75 - q25\n",
    "\n",
    "# calculate the min and max values. Anything outside these values are outliers.\n",
    "min_traffic = q25 - (1.5 * IQR)\n",
    "max_traffic = q75 + (1.5 * IQR)\n",
    "\n",
    "print(min_traffic, max_traffic)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Filter out all the outliers based on the IQR calculated above on the total traffic"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "We have a total of 2135517 data points\n"
     ]
    }
   ],
   "source": [
    "total_traffic_mask = ((summer19_MTA_pos['Total_Traffic'] > min_traffic) & (summer19_MTA_pos['Total_Traffic'] < max_traffic))\n",
    "summer19_MTA_cleaned = summer19_MTA_pos[total_traffic_mask]\n",
    "\n",
    "print(f'We have a total of {np.shape(summer19_MTA_cleaned)[0]} data points')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Using a logic mask with the max total traffic per SCP to be 1 second per person."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "total_traffic_mask = ((summer19_MTA['Total_Traffic'] > 0) & (summer19_MTA['Total_Traffic'] < 30000))\n",
    "summer19_MTA_cleaned = summer19_MTA[total_traffic_mask]\n",
    "print(f'We have a total of {np.shape(summer19_MTA_cleaned)[0]} data points')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "We will examine the distribution and box plot again after the filter"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 1152x288 with 2 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "plt.figure(figsize = [16,4])\n",
    "\n",
    "plt.subplot(1,2,1)\n",
    "sns.distplot(summer19_MTA_cleaned.Total_Traffic);\n",
    "plt.title('Distribution of Total Traffic', size = 20);\n",
    "\n",
    "plt.subplot(1,2,2)\n",
    "sns.boxplot(summer19_MTA_cleaned.Total_Traffic);\n",
    "plt.title('Box Plot of Total Traffic', size = 20);\n",
    "plt.savefig('Distribution after filter.png')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "We should normalize the total_traffic since the goal is to find the top stations. Large numbers presents problems in terms of visualizing them on graphs"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/Users/bentleyou/anaconda3/lib/python3.7/site-packages/ipykernel_launcher.py:6: SettingWithCopyWarning: \n",
      "A value is trying to be set on a copy of a slice from a DataFrame.\n",
      "Try using .loc[row_indexer,col_indexer] = value instead\n",
      "\n",
      "See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy\n",
      "  \n"
     ]
    }
   ],
   "source": [
    "# tt = Total Traffic\n",
    "\n",
    "tt_min = summer19_MTA_cleaned['Total_Traffic'].min()\n",
    "tt_max = summer19_MTA_cleaned['Total_Traffic'].max()\n",
    "\n",
    "summer19_MTA_cleaned['Total_Traffic'] = (summer19_MTA_cleaned.Total_Traffic - tt_min) / (tt_max - tt_min)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Distribution of after normalization. The total traffic per time slot should be between 0 and 1."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 1152x288 with 2 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "plt.figure(figsize = [16,4])\n",
    "\n",
    "plt.subplot(1,2,1)\n",
    "sns.distplot(summer19_MTA_cleaned.Total_Traffic);\n",
    "plt.title('Distribution of Total Traffic', size = 20);\n",
    "\n",
    "plt.subplot(1,2,2)\n",
    "sns.boxplot(summer19_MTA_cleaned.Total_Traffic);\n",
    "plt.title('Box Plot of Total Traffic', size = 20);\n",
    "plt.savefig('Distribution after normalization.png')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>C/A</th>\n",
       "      <th>UNIT</th>\n",
       "      <th>SCP</th>\n",
       "      <th>STATION</th>\n",
       "      <th>LINENAME</th>\n",
       "      <th>DIVISION</th>\n",
       "      <th>DATE</th>\n",
       "      <th>TIME</th>\n",
       "      <th>DESC</th>\n",
       "      <th>ENTRIES</th>\n",
       "      <th>EXITS</th>\n",
       "      <th>Unique_Station</th>\n",
       "      <th>ENTRIES DIFF</th>\n",
       "      <th>EXITS DIFF</th>\n",
       "      <th>Total_Traffic</th>\n",
       "      <th>DAY_OF_WEEK</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>A002</td>\n",
       "      <td>R051</td>\n",
       "      <td>02-00-00</td>\n",
       "      <td>59 ST</td>\n",
       "      <td>NQR456W</td>\n",
       "      <td>BMT</td>\n",
       "      <td>03/30/2019</td>\n",
       "      <td>04:00:00</td>\n",
       "      <td>REGULAR</td>\n",
       "      <td>6999084</td>\n",
       "      <td>2373576</td>\n",
       "      <td>59 ST_NQR456W</td>\n",
       "      <td>20.0</td>\n",
       "      <td>8.0</td>\n",
       "      <td>0.024302</td>\n",
       "      <td>Saturday</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>A002</td>\n",
       "      <td>R051</td>\n",
       "      <td>02-00-00</td>\n",
       "      <td>59 ST</td>\n",
       "      <td>NQR456W</td>\n",
       "      <td>BMT</td>\n",
       "      <td>03/30/2019</td>\n",
       "      <td>08:00:00</td>\n",
       "      <td>REGULAR</td>\n",
       "      <td>6999107</td>\n",
       "      <td>2373622</td>\n",
       "      <td>59 ST_NQR456W</td>\n",
       "      <td>23.0</td>\n",
       "      <td>46.0</td>\n",
       "      <td>0.061206</td>\n",
       "      <td>Saturday</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>A002</td>\n",
       "      <td>R051</td>\n",
       "      <td>02-00-00</td>\n",
       "      <td>59 ST</td>\n",
       "      <td>NQR456W</td>\n",
       "      <td>BMT</td>\n",
       "      <td>03/30/2019</td>\n",
       "      <td>12:00:00</td>\n",
       "      <td>REGULAR</td>\n",
       "      <td>6999214</td>\n",
       "      <td>2373710</td>\n",
       "      <td>59 ST_NQR456W</td>\n",
       "      <td>107.0</td>\n",
       "      <td>88.0</td>\n",
       "      <td>0.174617</td>\n",
       "      <td>Saturday</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>A002</td>\n",
       "      <td>R051</td>\n",
       "      <td>02-00-00</td>\n",
       "      <td>59 ST</td>\n",
       "      <td>NQR456W</td>\n",
       "      <td>BMT</td>\n",
       "      <td>03/30/2019</td>\n",
       "      <td>16:00:00</td>\n",
       "      <td>REGULAR</td>\n",
       "      <td>6999451</td>\n",
       "      <td>2373781</td>\n",
       "      <td>59 ST_NQR456W</td>\n",
       "      <td>237.0</td>\n",
       "      <td>71.0</td>\n",
       "      <td>0.276328</td>\n",
       "      <td>Saturday</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>5</th>\n",
       "      <td>A002</td>\n",
       "      <td>R051</td>\n",
       "      <td>02-00-00</td>\n",
       "      <td>59 ST</td>\n",
       "      <td>NQR456W</td>\n",
       "      <td>BMT</td>\n",
       "      <td>03/30/2019</td>\n",
       "      <td>20:00:00</td>\n",
       "      <td>REGULAR</td>\n",
       "      <td>6999796</td>\n",
       "      <td>2373837</td>\n",
       "      <td>59 ST_NQR456W</td>\n",
       "      <td>345.0</td>\n",
       "      <td>56.0</td>\n",
       "      <td>0.360036</td>\n",
       "      <td>Saturday</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "    C/A  UNIT       SCP STATION LINENAME DIVISION        DATE      TIME  \\\n",
       "1  A002  R051  02-00-00   59 ST  NQR456W      BMT  03/30/2019  04:00:00   \n",
       "2  A002  R051  02-00-00   59 ST  NQR456W      BMT  03/30/2019  08:00:00   \n",
       "3  A002  R051  02-00-00   59 ST  NQR456W      BMT  03/30/2019  12:00:00   \n",
       "4  A002  R051  02-00-00   59 ST  NQR456W      BMT  03/30/2019  16:00:00   \n",
       "5  A002  R051  02-00-00   59 ST  NQR456W      BMT  03/30/2019  20:00:00   \n",
       "\n",
       "      DESC  ENTRIES    EXITS Unique_Station  ENTRIES DIFF  EXITS DIFF  \\\n",
       "1  REGULAR  6999084  2373576  59 ST_NQR456W          20.0         8.0   \n",
       "2  REGULAR  6999107  2373622  59 ST_NQR456W          23.0        46.0   \n",
       "3  REGULAR  6999214  2373710  59 ST_NQR456W         107.0        88.0   \n",
       "4  REGULAR  6999451  2373781  59 ST_NQR456W         237.0        71.0   \n",
       "5  REGULAR  6999796  2373837  59 ST_NQR456W         345.0        56.0   \n",
       "\n",
       "   Total_Traffic DAY_OF_WEEK  \n",
       "1       0.024302    Saturday  \n",
       "2       0.061206    Saturday  \n",
       "3       0.174617    Saturday  \n",
       "4       0.276328    Saturday  \n",
       "5       0.360036    Saturday  "
      ]
     },
     "execution_count": 24,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "summer19_MTA_cleaned.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Let's bin our date time together into categories"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 112,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/Users/bentleyou/anaconda3/lib/python3.7/site-packages/ipykernel_launcher.py:6: SettingWithCopyWarning: \n",
      "A value is trying to be set on a copy of a slice from a DataFrame\n",
      "\n",
      "See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy\n",
      "  \n"
     ]
    }
   ],
   "source": [
    "# We need to turn our datetime into integers\n",
    "# We can grab the hours from each time \n",
    "summer19_MTA_cleaned['TIME_INT'] = summer19_MTA_cleaned['TIME'].apply(lambda x: int(x.split(':')[0]))\n",
    "\n",
    "# Convert the 0th hour to 23rd to capture 8PM to midnight traffic\n",
    "summer19_MTA_cleaned['TIME_INT'][summer19_MTA_cleaned['TIME_INT'] == 0] = 23"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 113,
   "metadata": {},
   "outputs": [],
   "source": [
    "def simplify_time(df):\n",
    "    '''\n",
    "    Takes an interger and bins it into the follow group names\n",
    "    Creates another column called 'TIME_OF_DAY' \n",
    "    Return the new dateframe\n",
    "    '''\n",
    "    bins = (0, 4, 8, 12, 16, 20, 23)\n",
    "    group_names = ['Midnight-4AM', '4AM-8AM', '8AM-Noon', 'Noon-4PM', '4PM-8PM', '8PM-Midnight']\n",
    "    categories = pd.cut(df.TIME_INT, bins, labels=group_names, include_lowest = True)\n",
    "    df['TIME_OF_DAY'] = categories\n",
    "    return df"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 114,
   "metadata": {},
   "outputs": [],
   "source": [
    "simplify_time(summer19_MTA_cleaned);"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 29,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>C/A</th>\n",
       "      <th>UNIT</th>\n",
       "      <th>SCP</th>\n",
       "      <th>STATION</th>\n",
       "      <th>LINENAME</th>\n",
       "      <th>DIVISION</th>\n",
       "      <th>DATE</th>\n",
       "      <th>TIME</th>\n",
       "      <th>DESC</th>\n",
       "      <th>ENTRIES</th>\n",
       "      <th>EXITS</th>\n",
       "      <th>Unique_Station</th>\n",
       "      <th>ENTRIES DIFF</th>\n",
       "      <th>EXITS DIFF</th>\n",
       "      <th>Total_Traffic</th>\n",
       "      <th>DAY_OF_WEEK</th>\n",
       "      <th>TIME_INT</th>\n",
       "      <th>TIME_OF_DAY</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>A002</td>\n",
       "      <td>R051</td>\n",
       "      <td>02-00-00</td>\n",
       "      <td>59 ST</td>\n",
       "      <td>NQR456W</td>\n",
       "      <td>BMT</td>\n",
       "      <td>03/30/2019</td>\n",
       "      <td>04:00:00</td>\n",
       "      <td>REGULAR</td>\n",
       "      <td>6999084</td>\n",
       "      <td>2373576</td>\n",
       "      <td>59 ST_NQR456W</td>\n",
       "      <td>20.0</td>\n",
       "      <td>8.0</td>\n",
       "      <td>0.024302</td>\n",
       "      <td>Saturday</td>\n",
       "      <td>4</td>\n",
       "      <td>Midnight-4AM</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>A002</td>\n",
       "      <td>R051</td>\n",
       "      <td>02-00-00</td>\n",
       "      <td>59 ST</td>\n",
       "      <td>NQR456W</td>\n",
       "      <td>BMT</td>\n",
       "      <td>03/30/2019</td>\n",
       "      <td>08:00:00</td>\n",
       "      <td>REGULAR</td>\n",
       "      <td>6999107</td>\n",
       "      <td>2373622</td>\n",
       "      <td>59 ST_NQR456W</td>\n",
       "      <td>23.0</td>\n",
       "      <td>46.0</td>\n",
       "      <td>0.061206</td>\n",
       "      <td>Saturday</td>\n",
       "      <td>8</td>\n",
       "      <td>4AM-8AM</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>A002</td>\n",
       "      <td>R051</td>\n",
       "      <td>02-00-00</td>\n",
       "      <td>59 ST</td>\n",
       "      <td>NQR456W</td>\n",
       "      <td>BMT</td>\n",
       "      <td>03/30/2019</td>\n",
       "      <td>12:00:00</td>\n",
       "      <td>REGULAR</td>\n",
       "      <td>6999214</td>\n",
       "      <td>2373710</td>\n",
       "      <td>59 ST_NQR456W</td>\n",
       "      <td>107.0</td>\n",
       "      <td>88.0</td>\n",
       "      <td>0.174617</td>\n",
       "      <td>Saturday</td>\n",
       "      <td>12</td>\n",
       "      <td>8AM-Noon</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>A002</td>\n",
       "      <td>R051</td>\n",
       "      <td>02-00-00</td>\n",
       "      <td>59 ST</td>\n",
       "      <td>NQR456W</td>\n",
       "      <td>BMT</td>\n",
       "      <td>03/30/2019</td>\n",
       "      <td>16:00:00</td>\n",
       "      <td>REGULAR</td>\n",
       "      <td>6999451</td>\n",
       "      <td>2373781</td>\n",
       "      <td>59 ST_NQR456W</td>\n",
       "      <td>237.0</td>\n",
       "      <td>71.0</td>\n",
       "      <td>0.276328</td>\n",
       "      <td>Saturday</td>\n",
       "      <td>16</td>\n",
       "      <td>Noon-4PM</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>5</th>\n",
       "      <td>A002</td>\n",
       "      <td>R051</td>\n",
       "      <td>02-00-00</td>\n",
       "      <td>59 ST</td>\n",
       "      <td>NQR456W</td>\n",
       "      <td>BMT</td>\n",
       "      <td>03/30/2019</td>\n",
       "      <td>20:00:00</td>\n",
       "      <td>REGULAR</td>\n",
       "      <td>6999796</td>\n",
       "      <td>2373837</td>\n",
       "      <td>59 ST_NQR456W</td>\n",
       "      <td>345.0</td>\n",
       "      <td>56.0</td>\n",
       "      <td>0.360036</td>\n",
       "      <td>Saturday</td>\n",
       "      <td>20</td>\n",
       "      <td>4PM-8PM</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>6</th>\n",
       "      <td>A002</td>\n",
       "      <td>R051</td>\n",
       "      <td>02-00-00</td>\n",
       "      <td>59 ST</td>\n",
       "      <td>NQR456W</td>\n",
       "      <td>BMT</td>\n",
       "      <td>03/31/2019</td>\n",
       "      <td>00:00:00</td>\n",
       "      <td>REGULAR</td>\n",
       "      <td>6999957</td>\n",
       "      <td>2373867</td>\n",
       "      <td>59 ST_NQR456W</td>\n",
       "      <td>161.0</td>\n",
       "      <td>30.0</td>\n",
       "      <td>0.171017</td>\n",
       "      <td>Sunday</td>\n",
       "      <td>23</td>\n",
       "      <td>Midnight-4AM</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>7</th>\n",
       "      <td>A002</td>\n",
       "      <td>R051</td>\n",
       "      <td>02-00-00</td>\n",
       "      <td>59 ST</td>\n",
       "      <td>NQR456W</td>\n",
       "      <td>BMT</td>\n",
       "      <td>03/31/2019</td>\n",
       "      <td>04:00:00</td>\n",
       "      <td>REGULAR</td>\n",
       "      <td>6999983</td>\n",
       "      <td>2373876</td>\n",
       "      <td>59 ST_NQR456W</td>\n",
       "      <td>26.0</td>\n",
       "      <td>9.0</td>\n",
       "      <td>0.030603</td>\n",
       "      <td>Sunday</td>\n",
       "      <td>4</td>\n",
       "      <td>Midnight-4AM</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>8</th>\n",
       "      <td>A002</td>\n",
       "      <td>R051</td>\n",
       "      <td>02-00-00</td>\n",
       "      <td>59 ST</td>\n",
       "      <td>NQR456W</td>\n",
       "      <td>BMT</td>\n",
       "      <td>03/31/2019</td>\n",
       "      <td>08:00:00</td>\n",
       "      <td>REGULAR</td>\n",
       "      <td>6999998</td>\n",
       "      <td>2373900</td>\n",
       "      <td>59 ST_NQR456W</td>\n",
       "      <td>15.0</td>\n",
       "      <td>24.0</td>\n",
       "      <td>0.034203</td>\n",
       "      <td>Sunday</td>\n",
       "      <td>8</td>\n",
       "      <td>4AM-8AM</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>9</th>\n",
       "      <td>A002</td>\n",
       "      <td>R051</td>\n",
       "      <td>02-00-00</td>\n",
       "      <td>59 ST</td>\n",
       "      <td>NQR456W</td>\n",
       "      <td>BMT</td>\n",
       "      <td>03/31/2019</td>\n",
       "      <td>12:00:00</td>\n",
       "      <td>REGULAR</td>\n",
       "      <td>7000069</td>\n",
       "      <td>2373957</td>\n",
       "      <td>59 ST_NQR456W</td>\n",
       "      <td>71.0</td>\n",
       "      <td>57.0</td>\n",
       "      <td>0.114311</td>\n",
       "      <td>Sunday</td>\n",
       "      <td>12</td>\n",
       "      <td>8AM-Noon</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>10</th>\n",
       "      <td>A002</td>\n",
       "      <td>R051</td>\n",
       "      <td>02-00-00</td>\n",
       "      <td>59 ST</td>\n",
       "      <td>NQR456W</td>\n",
       "      <td>BMT</td>\n",
       "      <td>03/31/2019</td>\n",
       "      <td>16:00:00</td>\n",
       "      <td>REGULAR</td>\n",
       "      <td>7000220</td>\n",
       "      <td>2374010</td>\n",
       "      <td>59 ST_NQR456W</td>\n",
       "      <td>151.0</td>\n",
       "      <td>53.0</td>\n",
       "      <td>0.182718</td>\n",
       "      <td>Sunday</td>\n",
       "      <td>16</td>\n",
       "      <td>Noon-4PM</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "     C/A  UNIT       SCP STATION LINENAME DIVISION        DATE      TIME  \\\n",
       "1   A002  R051  02-00-00   59 ST  NQR456W      BMT  03/30/2019  04:00:00   \n",
       "2   A002  R051  02-00-00   59 ST  NQR456W      BMT  03/30/2019  08:00:00   \n",
       "3   A002  R051  02-00-00   59 ST  NQR456W      BMT  03/30/2019  12:00:00   \n",
       "4   A002  R051  02-00-00   59 ST  NQR456W      BMT  03/30/2019  16:00:00   \n",
       "5   A002  R051  02-00-00   59 ST  NQR456W      BMT  03/30/2019  20:00:00   \n",
       "6   A002  R051  02-00-00   59 ST  NQR456W      BMT  03/31/2019  00:00:00   \n",
       "7   A002  R051  02-00-00   59 ST  NQR456W      BMT  03/31/2019  04:00:00   \n",
       "8   A002  R051  02-00-00   59 ST  NQR456W      BMT  03/31/2019  08:00:00   \n",
       "9   A002  R051  02-00-00   59 ST  NQR456W      BMT  03/31/2019  12:00:00   \n",
       "10  A002  R051  02-00-00   59 ST  NQR456W      BMT  03/31/2019  16:00:00   \n",
       "\n",
       "       DESC  ENTRIES    EXITS Unique_Station  ENTRIES DIFF  EXITS DIFF  \\\n",
       "1   REGULAR  6999084  2373576  59 ST_NQR456W          20.0         8.0   \n",
       "2   REGULAR  6999107  2373622  59 ST_NQR456W          23.0        46.0   \n",
       "3   REGULAR  6999214  2373710  59 ST_NQR456W         107.0        88.0   \n",
       "4   REGULAR  6999451  2373781  59 ST_NQR456W         237.0        71.0   \n",
       "5   REGULAR  6999796  2373837  59 ST_NQR456W         345.0        56.0   \n",
       "6   REGULAR  6999957  2373867  59 ST_NQR456W         161.0        30.0   \n",
       "7   REGULAR  6999983  2373876  59 ST_NQR456W          26.0         9.0   \n",
       "8   REGULAR  6999998  2373900  59 ST_NQR456W          15.0        24.0   \n",
       "9   REGULAR  7000069  2373957  59 ST_NQR456W          71.0        57.0   \n",
       "10  REGULAR  7000220  2374010  59 ST_NQR456W         151.0        53.0   \n",
       "\n",
       "    Total_Traffic DAY_OF_WEEK  TIME_INT   TIME_OF_DAY  \n",
       "1        0.024302    Saturday         4  Midnight-4AM  \n",
       "2        0.061206    Saturday         8       4AM-8AM  \n",
       "3        0.174617    Saturday        12      8AM-Noon  \n",
       "4        0.276328    Saturday        16      Noon-4PM  \n",
       "5        0.360036    Saturday        20       4PM-8PM  \n",
       "6        0.171017      Sunday        23  Midnight-4AM  \n",
       "7        0.030603      Sunday         4  Midnight-4AM  \n",
       "8        0.034203      Sunday         8       4AM-8AM  \n",
       "9        0.114311      Sunday        12      8AM-Noon  \n",
       "10       0.182718      Sunday        16      Noon-4PM  "
      ]
     },
     "execution_count": 29,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "summer19_MTA_cleaned.head(10)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Let's create another column differentiating weekdays and weekends"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 30,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/Users/bentleyou/anaconda3/lib/python3.7/site-packages/ipykernel_launcher.py:2: SettingWithCopyWarning: \n",
      "A value is trying to be set on a copy of a slice from a DataFrame.\n",
      "Try using .loc[row_indexer,col_indexer] = value instead\n",
      "\n",
      "See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy\n",
      "  \n"
     ]
    }
   ],
   "source": [
    "summer19_MTA_cleaned['WEEKEND'] = (summer19_MTA_cleaned['DAY_OF_WEEK']\n",
    "                                   .apply(lambda x: 'WEEKEND' \n",
    "                                          if (x == 'Saturday' or x == 'Sunday') \n",
    "                                          else 'WEEKDAY'))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "After data cleaning, let's pickle the cleaned data frame"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 31,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pickle \n",
    "\n",
    "with open('summer19_MTA_cleaned.pickle', 'wb') as to_write:\n",
    "    pickle.dump(summer19_MTA_cleaned, to_write)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 32,
   "metadata": {},
   "outputs": [],
   "source": [
    "with open('summer19_MTA_cleaned.pickle', 'rb') as to_read:\n",
    "    summer19_MTA_cleaned = pickle.load(to_read)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Let's count all the total traffic per station for the months of April, May, and June of 2019. Below displays the top candidates."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 33,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Unique_Station</th>\n",
       "      <th>ENTRIES</th>\n",
       "      <th>EXITS</th>\n",
       "      <th>ENTRIES DIFF</th>\n",
       "      <th>EXITS DIFF</th>\n",
       "      <th>Total_Traffic</th>\n",
       "      <th>TIME_INT</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>94</th>\n",
       "      <td>34 ST-PENN STA_ACE</td>\n",
       "      <td>670283993176</td>\n",
       "      <td>715364962094</td>\n",
       "      <td>5251396.0</td>\n",
       "      <td>4303253.0</td>\n",
       "      <td>8576.776778</td>\n",
       "      <td>347573</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>312</th>\n",
       "      <td>GRD CNTRL-42 ST_4567S</td>\n",
       "      <td>580325761542</td>\n",
       "      <td>537573481170</td>\n",
       "      <td>4457804.0</td>\n",
       "      <td>4385398.0</td>\n",
       "      <td>7936.803780</td>\n",
       "      <td>289547</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>90</th>\n",
       "      <td>34 ST-HERALD SQ_BDFMNQRW</td>\n",
       "      <td>976660703407</td>\n",
       "      <td>937652785399</td>\n",
       "      <td>4035201.0</td>\n",
       "      <td>4110163.0</td>\n",
       "      <td>7311.983798</td>\n",
       "      <td>275743</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>302</th>\n",
       "      <td>FULTON ST_2345ACJZ</td>\n",
       "      <td>306473275121</td>\n",
       "      <td>340456131519</td>\n",
       "      <td>4155459.0</td>\n",
       "      <td>3971517.0</td>\n",
       "      <td>7290.098110</td>\n",
       "      <td>327214</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>103</th>\n",
       "      <td>42 ST-PORT AUTH_ACENQRS1237W</td>\n",
       "      <td>1464593492427</td>\n",
       "      <td>1220246777724</td>\n",
       "      <td>3878724.0</td>\n",
       "      <td>2342674.0</td>\n",
       "      <td>5585.650765</td>\n",
       "      <td>198939</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>448</th>\n",
       "      <td>TIMES SQ-42 ST_1237ACENQRSW</td>\n",
       "      <td>1984085919748</td>\n",
       "      <td>1029532078965</td>\n",
       "      <td>2865069.0</td>\n",
       "      <td>2706036.0</td>\n",
       "      <td>5001.166517</td>\n",
       "      <td>184935</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>289</th>\n",
       "      <td>FLUSHING-MAIN_7</td>\n",
       "      <td>90929349471</td>\n",
       "      <td>87244537783</td>\n",
       "      <td>2884312.0</td>\n",
       "      <td>2427216.0</td>\n",
       "      <td>4770.527453</td>\n",
       "      <td>149095</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>235</th>\n",
       "      <td>CANAL ST_JNQRZ6W</td>\n",
       "      <td>881131763593</td>\n",
       "      <td>1543023208107</td>\n",
       "      <td>2771874.0</td>\n",
       "      <td>2370918.0</td>\n",
       "      <td>4616.092709</td>\n",
       "      <td>153690</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>124</th>\n",
       "      <td>59 ST_456NQRW</td>\n",
       "      <td>191775112849</td>\n",
       "      <td>122469424546</td>\n",
       "      <td>2147214.0</td>\n",
       "      <td>2413130.0</td>\n",
       "      <td>4091.318632</td>\n",
       "      <td>198612</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>404</th>\n",
       "      <td>PATH NEW WTC_1</td>\n",
       "      <td>1422459420</td>\n",
       "      <td>1673071952</td>\n",
       "      <td>2253297.0</td>\n",
       "      <td>2131509.0</td>\n",
       "      <td>3932.065707</td>\n",
       "      <td>201047</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                   Unique_Station        ENTRIES          EXITS  ENTRIES DIFF  \\\n",
       "94             34 ST-PENN STA_ACE   670283993176   715364962094     5251396.0   \n",
       "312         GRD CNTRL-42 ST_4567S   580325761542   537573481170     4457804.0   \n",
       "90       34 ST-HERALD SQ_BDFMNQRW   976660703407   937652785399     4035201.0   \n",
       "302            FULTON ST_2345ACJZ   306473275121   340456131519     4155459.0   \n",
       "103  42 ST-PORT AUTH_ACENQRS1237W  1464593492427  1220246777724     3878724.0   \n",
       "448   TIMES SQ-42 ST_1237ACENQRSW  1984085919748  1029532078965     2865069.0   \n",
       "289               FLUSHING-MAIN_7    90929349471    87244537783     2884312.0   \n",
       "235              CANAL ST_JNQRZ6W   881131763593  1543023208107     2771874.0   \n",
       "124                 59 ST_456NQRW   191775112849   122469424546     2147214.0   \n",
       "404                PATH NEW WTC_1     1422459420     1673071952     2253297.0   \n",
       "\n",
       "     EXITS DIFF  Total_Traffic  TIME_INT  \n",
       "94    4303253.0    8576.776778    347573  \n",
       "312   4385398.0    7936.803780    289547  \n",
       "90    4110163.0    7311.983798    275743  \n",
       "302   3971517.0    7290.098110    327214  \n",
       "103   2342674.0    5585.650765    198939  \n",
       "448   2706036.0    5001.166517    184935  \n",
       "289   2427216.0    4770.527453    149095  \n",
       "235   2370918.0    4616.092709    153690  \n",
       "124   2413130.0    4091.318632    198612  \n",
       "404   2131509.0    3932.065707    201047  "
      ]
     },
     "execution_count": 33,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "top = 10 # filter to top stations\n",
    "top_unique_stations = (summer19_MTA_cleaned.groupby(['Unique_Station'])\n",
    "                       .sum()\n",
    "                       .reset_index()\n",
    "                       .sort_values(by = 'Total_Traffic', ascending = False)\n",
    "                       .head(top))\n",
    "top_unique_stations"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Let's visualize this with a horizontal bar graph for the top ten unique stations for both weekdays and weekends"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 135,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAABFoAAAJrCAYAAADQyPehAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEgAACxIB0t1+/AAAADh0RVh0U29mdHdhcmUAbWF0cGxvdGxpYiB2ZXJzaW9uMy4xLjEsIGh0dHA6Ly9tYXRwbG90bGliLm9yZy8QZhcZAAAgAElEQVR4nOzdd7xsVX338c+XIoIgKChgLFfFDnpVFGIDazSiYkSJEhVjSx71eTQCYrAbjBEsscVgiSViiYWoIFawohS5NAHFgIqCEhBEevk9f6w1MAxz2j37criXz/v1mtecWWvttdfeM7PP7N9ea+1UFZIkSZIkSVq8tZa6AZIkSZIkSWsKAy2SJEmSJEkDMdAiSZIkSZI0EAMtkiRJkiRJAzHQIkmSJEmSNBADLZIkSZIkSQMx0CJJ0iqS5PwkK5a6HSsryTZJDk7y+ySV5IylbtOkJAf1tm2y1G1ZE6xO+zPJU5IcmeSC3uaPLnWb5mvafk6yvKe9aynbppn5Hi1Mkocn+U6S8/p+O3yp2yTdUAy0SNIA+g+IhTx2vxG0eaex9nxkhjJb9/xD++tNk/w2yaVJtpml7tf15T42Je9+ST6Q5OQkf0xyWZIz+4nH3yRZdwHb8PAkn+3LX95PuE5L8sUk/5DkZmNlN+ltOmi+9c9j/SuSnD9UfTcmSW4OfAnYEfgC8EbgBj+5SPKu/r4tv6HXvSZaU/Znkq2BzwFbAAfQPp8L+m4nOarvi5NWQROXVD82jY7vT52l3DvHyhk8GNhYYGa1DbivrCSbA18B7gN8gvYd/egcyyzr/7u/keRX/f/6OUkOSfKXcyz79CQ/SHJhf/wgydNnKHuX/jvlC0lOH/sObDbHOv4iydeS/KH/DvpZkrck2XC25XTTtM5SN0CS1hBvnJL2cmBj4F+ByZPxG9uPrucmeVdVHT9boao6N8nzgK8Cn0zyoKq6bLxMkm2B1wJnAC8bS18L+BdgD6CA7wNfAy4Gbgc8CngKsDvwmLkanOT/AO8DrgK+AZzSs+4MbAfsDHwc+N+56lqFHgRcsYTrX4ytgWXAflW11xK3RZr0eNrv2L+rqkMWunAPNG1LOxbdO8nDqur7A7dxNi8B9gb+uIrXcyXwQuCLkxlJ1gOe3ct4TqChPRy4JfCSqnr/PJfZG3gx8DPg68A5wF1p/8+fkOT1VfWmyYWSvAZ4M/A74D968jOAzyZ5bVX908Qij6D9brsa+AXwJ2DWYEmSPYD9gEtoFx/Opv3WeHVv2w5Vtaq/z1qNeFCVpAFU1Rsm03qvlY2Bd1XVGTdwkxbiNGAr2g+Iv5ircFV9Lcl7aUGUfwb+YZSXZAPgP2k9Jp898aPjrbQgy8+BXSaDOkkCPA143lxtSLIp8A7gUmDHqvrxlLp2BC6aq65Vqap+vpTrX6Tb9effLmkrpOkW+/l8cX9+G/Aq4EW04O8Noqp+cwOt6ivAk5Pcsap+NZH3V8CmtCDMjL1epJW0Mt/R7wAfraofjSf2CzjfBV6f5FPj/1t777Y39PU8sKrO7ulvAX4CvCHJF6tqvOfad4GHAsdV1UW9x9H9ZmpUkq1ov3cuAR40XleSfYF/BN5Eu8AmNVXlw4cPHz5WwYPWo6OAZXOUuzdwIHAWcDlwJvCRacsB+/c6t6WdGBxP+8d/NvDvwGYLaN9Ova4P0HqEFPAXE2W27umHTqTfHDiJdjXo0WPp7+/l951Sz9W0q0Z3maNd682j7Y/r6zl8ntv68l5+2uPlvcxatJOvLwGn04I45wOHA0+bqG/5LPUdNFbufGDFlPbcgvbD8Kd9PRcA3waeNKXsaF3vAu5BOyk6r7/vPxzf/2PLrA/sBRzX23BR36bPAw+bY19tMte+6uU2owW7fgFcBpxLO6l76JQ6dx4tT7uS+HXgDz1tk1nacv4M7Th/rMxBPe3WwCuAk3t7fgu8G9hghrrvAnyQ9j29jHbl9HPAfRfwHRp/b+4DfLlv1wV9X2zVy/0Z8DHa1dbR+7b9DHWu7H7dnvY9/iPte/YN4P43xP4EHtw/W7/qZX8PHAW8bb77stfz3L5vLqT1dFvR27DOlG2e9lg+z/Vs0N+j39IuOv68r2/qZ7G343za93b/vp2X0q667wWsPcN36CDgTrRhE2fTjoE7T+znTcaWu+bztJD9NkubC/jL/vyGKWW+3T9ffzNtvbQebW8GftQ/u5cDv+6f5btMlN2+1/GFGdqzFu27dhFwy0Vs17zbNOU7Oq/jZ1/u1rQek2f19/pE4O8X+h6NlV8xkT76n7TzlGWu+fxMpL9r9DkHngMc27fjnL79t5mhDZvTjik/69vyB+BQ4BErsf+fBHyrfx8upR0f3gDcYso2T3tcb3sXsO7P9jqeP5H+7p7+iinL/EPP+9d5fl+m/oYaq+eDU/LWpR0/LgTWX8z31sea9bBHiyQtoSQPpw3DWZ/2A/DntBO25wFPSbJjVZ0wZdHXAo8GPgMcDDySFnjZIcn2VbXQeUP2BI4B9kvyjaq6erbCVXVpkt2AHwMf6/O1bE/7IXoM7YfXuBcCAT5RVf8zR92XzZbfnduf75TkZlV1+Rzlf0QbtvQq4FTg0xN5ADejBZ1+DBxG+xF/W1pA6nNJ9qiqt/eyZ9O6Hf8d7UfxW8fqO4VZ9F4/h9OCZcfTfiRuDDwd+FKSV1XV26Ysei/gSFrw5D9oc1M8Azi0v+fHjJX9PPAE2tW8/6CdjNyeFuTYkdmv3F/at+2ewK604V2jffSjvg1b0E5S7gz8gPYDeMvenscneXZVfWpK3Y+jnah+kxbkuB1t6NdM3ko7sd6OFkg8e6yNkz5AG352MO079Thar6s7MHG1PsnDerkNgUOA/6KdjPwV8JdJ/qKqvjdLuybdGziCFlz4MO2EbidgeZIdaVdpz6QFVEfv29eT3KWqrhnatoj9ugPt8/1t2nwlo672hyfZuqp+3csNvj+TPJT2eb4U+G/aSe8mwN17+XkNO0vyftrx42zaSeNltJO6dwCPSvKUflw6hfb5fPyU7Th7st4Z/DVtSMO/V9WVST5Ouxr9bOA9MyyzFi2QdlfasAFo++FfgPvSghWTbkc7nvyWdqxem3aSf0M6knaceV6SN42O7f0K/Y6048+09x/aPn457Xh4FO2k/p7AbsCTkjy4qk4DqKofJflJT79dVU32Yng8Lej04Vrc8Ip5t2nCvI+ffb6N79L+Fx9FD2LQej99exFtH8o/Ak+kXRT4Fm2IznOA+/Ttv+b/d5J70tq8ZS/7Zdr388nAt5PsVlWfmc9Kk+xF+7yfTzs2/QF4LPB64Il96MzFXPv/cXtaL9nPcO3/xVn/P85hNAz3yon0R/XnQ6cs81Xg7WNlVtYW/fl6v1+q6ookZwJ3ox2TDl/kurSmWOpIjw8fPnysqQ/m6NFCu5I6KvOUibzn9/RjJtJHPVouAu49kXcA87hyM1b+mh4t/fVH++u/HSsztUfLWP5ePf/LtCt/FwH3mFLumF5ul4H27bq03iBFO5F5Ee1kZ91Zlpl6lXAsfy3gzlPSN+jruAi41UTeCsZ6A0xZ9no9Wmg/VIsW7FlrLP0OtODOVcDWY+njVwdfPlHXrj39wIl6ivbjOhPlA9x6nvt452nr7Hmf6Xlvm0i/H+2k7U+MXV3lur0Qdl3ge33NVdwZ8kc9A04BthhLX492xbeAu0+8n7+lXX3cdqKuu9CCeKcx0UthhnWPvzcvmch7e08/j3aClrG8l/W81w+4X586scyrevpbVvH+/HBP22FKXfPqYUcLChYtCHrriXUe3vP+z0K2Y471/agve+/++o603ibHz1B+dLX7WGDDsfSNaEGMYqw3GtftFfZexr7nU/bzqu7Rshnw0v73E8by39rTtgZ2mbZe2sn5tB5MD6EFwj41kf6CXs9rZtneBy1yuxbapgUdP3v623r6R7ju9/ZetP8D836PWDU9Ws6h95br6WvRer0V8Lix9PTP7JXAEyfq2ox2Yed85tHDqH9OrurrvtPEuj/J9OPWjNu4Eu/7bWm90C4Hbj+Rdznt+3u9//+0CyhXA5fN9/syQ/7ot84BU/JGPVqKNmfUorbVx5rz8K5DkrR0Hk27wveNqvrv8Yyq+jDtB9IDkjxgyrIfqqqfTqTtQ7u699w+8exCvaYv/+be62I+9qedCO1Eu+KzR1WdOqXclv35zJVo1/VU1RW0k8wf0YYt/DvtSuXoTgOvWMA2jOq8uqpOn5J+ca9/A9qVw8V6Hu3K3B41duWxWq+Dt9F+uP7tlOVOrKrJu4J8lvZD+cFTyl9aVTWeUM2irqgn2Zg2l87/MjEJdFUdR+upcgvgmVMWP7zmefV0Jbym+tj83pbLaJMhw3X3z9Npn8e3VtXR4xVU6231blqvhe0WsO4Tqup9E2mjO25dBbx24r0Y5V1z559F7teDq2pystMD+vO0z8Z8zHd/jlwymVBjvXXmMPq8v3b889nX+cr+8gXzrGtWvffddsCRo2NotblLDgO2SbL9LIu/rqr+NNa+C4HXTWzDuAuBV9ccPQRvAP9Je39eCJB2Z7fdgSOq6sSZFqqqs/rxbzL9h7Tg8+ScXgfSToZfOP4/KMntaP8jjq2qoxazISvRppGFHD93p528/+P497aqTqZ9D5fav9RYr53++fpwfzm+LY+gHWP+o6oOHq+gfzf/idabcqd5rPO5tP9N+1XVLyfWvSdtf/1tnx9tUEnWph17btnXf+ZY3gb0QEf/XXAd1Xq7XgLcLMn6i2jGwbRAym5J7jWR91par2SAWy1iHVrDGGiRpKUzCqDM1BX5sP58/yl535lMqKpzaL08NqZdmV+Q/uPlnbTu7nvMc5mruXZowP9U1b/NUHT046tmyF+wqvpZVf057Wr/K2k/8s+kXdl8B3Bski1nqeL6jUy2SvLBJD9Pcsnolo9c+yP2zxbT5iR3oHVB/9n4j8Uxo8/CtPf8mMmEfhLwG8Z+3PWAzfdod0E4Ksk/JnlE2u2ah3Bf2hCIH1fVtMmGZ9uGIwdqwzRHT0kbDZkZ//H75/35HkneMPmgbR+0q9fzdb33hmsngDyxJobDVRs6cRFtONfIYvbr9ba9qv7Q17GyP/znuz9HQ5m+leTDSZ6VZNkC1zXjsbDakI4/AvftJ1yL9aL+/B8T6R+dyJ/mesddZj9On9yDMUuq2lDSz9GG1mxOGzayOfMIGiTZJcmhSX6X5IqxY+LDgVuNn7z2AMjHaD2EHj9WzfNpn+0PDLE9C2nTmHkdP8eO0aeOBxrHHD7ENizSQo91m89wrHtEz5/PsW627+hvaT3gNqW994PpgZsDaAG0r3JtYHNB1fTnlf79UW3y27fRLrgck+QTSfZP8l1aoGU0xHu2obC6iXGOFklaOhv357NmyB+lbzIl73czLDP6YbjxDPlzeSvtyvGeSf59nstcMvE8zW9pPV5uT7vqOJhqdy+65g5GSe5HO2laTrtLwO7zqaffueCHtB9Sh9Hm7vgj7YfTaL6S9RbZ3MW85zPNu3Ml7SRm3BNpPZyeAezb0y5K8ilgr34SvrIWsw3znUNjZUzbP6Ox/OP7Z9P+/Ow56pv1Vp8TLphl3dPyRvnrjr2+oT4b8zWv/VlV30zyaNpQpd3oPTuSnEDrofLf16vl+jYGrpylB8xZtHlvNmTm/TmnfgL+N7RhWJ+eyP48bZjPrkleXtefR+TSKWlU1QVJLmP6MXdVft4X6oO0z/zutDm9/kjr0TGjJK+nzbd1Dm1+j1/TjvNFm+fmHrRj4vix/9+A/0ubWPyQ3rPl+bRhbwcudiNWsk0w/+/I6H2c63/sUlrose5J/TGT+Rzr5nN8ui/t+PTLGcosSA+y/DvtmPJV2vDI6wQyquriJFcAGyRZd7JXS5Kb0Sbvv7yqZpqLaF6qau8kx9Fuzb4zbV8fDzyFNvxxG9pE4BJgoEWSltLohGGLGfK3nCg3bvMZlhnVtVInI1V1YZI30u628CZmnhhyob5PuyL2aNoJzSpTVccleQHtqt9CJsDbmzbnwlOr6qDxjCR/Twu0LNZi3vN561fR9wb27r0LdqAF0F7Q1z3bj+65LGYbBuvRtAijdu1QVd9d0pZc1w3y2VgVqurbtIk11wceRLvTzUuAzyd5SFXN1ZPpAmDTJJtW1blT8regBTz/NCVvIZ7BtYGqP8wyyuFvaHdQG3fzJLecDLb0IV/rMf0E/MbweQegqr6X5BRaEGQL2kTA03pOAZDkFsCraZN/PmhyyGGSJ8ywnlOSHEabHPX2tJPvO/X1Ler9W9k2LdDo+zXX/9jFGg0nm3YuNi2YujJG2/Lcqvr4rCXnX9cWtF5AkwY9PvUA3QdpQZYv0+Z3m2nS+5/RJi7einYXpHF3pfVo+dkQ7ao2Gfn1JiRP8ub+56KGxmnN4tAhSVo6x/bnHWfIH6X/ZEreDpMJSW5Du/vJBUyZGX8BDqB1A35+r28IH6SddDxnrmEFSRbbawTa3AhwbZdhuLZL70xX+LeiXRX80pS86+3vsTrn3WOgD+s5B7h7n7dg0iP787T3fKVU1RlV9TFa0Ols2pCixezj42nbvd0MXfSH3oa53reFGt1BaYj5doZ0Q+3XoffnNarqkqr6blXtTbszytrML6g347Gwz1G1MW2i2sV2y39hf/4CbTjg5OPAiXKTph0HRu/LsVPybmxGd/paC/jQHGXvQJ+MeEpAY1Paie1M3k9775/PtUOx5ttDclW1aV7GjtH3SLsL2KQdF7uObtSr8A5T8rYdaB1DHutm+45uSetJdB4D9GbpQwQ/RguyfBF42ixBFrh2ONPjp+Q9YaLM4JI8mBZQPK4PMZIAAy2StJS+CfyKdtvW61yJS7I7rQfIiqqadmL1giSTQZB9aROyfXwxky9W1ZW0YQBrc+2wk0XpEy7uT5vM89A+TOc60uzMPHq8JNk6yYvTbsM5mbc27SQP2i06Ry6i3ZVipjHkZ9CuLj50or5daFfCpzkX2DDJredq85iP0u6E8NbxiQOT/BltvpuruXa+iAVL8mdJps0XcUvasKjLWMQ48qq6gHaiehva8KTxdW9NO0m9mOsPzVhZox4OQ439/xQt4LRX2q2Xr6N/Dh8x0Hwg83YD7tdB92eSHad9D7m2R8D1Ji6d4iP9+U29h8io7psB+/WXH77eUgvQj5cPpc3j9IyqesGUx260uRaWJ3nQlGreNL6tSTai9fyD68/5Mpgky/s8JCsWWdWHabekfuIM/1fG/Yp2LNp+PDDb53r6N9qxfCYH0YaL/j1totUjq2pqICrJir5ty6flD9imhfgo7Rj9lom23ouZg3ALNerl9ZyJbdmcNkntEL5NmyT+uUmm/g9L8sAk8+lB81Havt+z91QaLR/anfTWAz4yMen3giVZh3YXo7+hDW17xrRJbid8kPY/bY/x4Fj/+5U9b9GTGCe55ZS029OCQsU8b2Wvmw6HDknSEqmqK5M8hzb2+MtJvkC7rex9aFeB/8DM84t8EzgyyWdoY4IfSbuTxs9YucniJtv2pSTfYeaeHCtjb1qA/5XAcUm+R7tKdjGt2/GOwJ1p2zaXzWgTK74ryfeBk2iBlM2Bx9GuEv6aawMuVNXVvUv745P8F3Ai7QfY1/vQhnfTbnN6aM8/hzbPy6OB/2J6sOVbwGNpcxF8kzb3w6lV9V+ztP2NwGNo8yVsneQbtCDIM4BbA/v0eWdW1t2Aw5IcT/uRPZrs8Ul9PW/qwbTF+H+0u1vsk+ThtLlttqBtw81oXdWHGqv+LVrA71+T/DltbolLq2r/lamsqi5K8lTaXSQO65/z42l3groD7Xt0R1rQ8oae2PCG2K+D7k/afBkPTHI4cDptboz70b6Hv2MeQcOqOiTJB2knsT9N8nnaXUyeBNyddoxc7ESq10yCO0fPmA/TbqP7Iq47DOBC2twYJ/VjNcBf0T4rB1bVtJ5wQxldGF3U97YH8w6asyDXzH1xAPB3wPFJDqYFMh5N+ywewbWTrU4ue2WSD3Ht/6LZerPMe9sW06YFejNtnqvn9SDnt2gB0F1p/5+evNgVVNWpSb5M+4wfk+TrtOP/Tn199xhgHVcneTqtzZ9JsidtSO2FtPnSHtDXcy9mnsNmVNeJSV5LO3Ycn2R0x6bH9nqOpR0LFms/2n7+I+33zGumDPH7UVUdOta2E9KGPL8JWNF/F4V23NycNlfUde6ulXa3ovHhgaPA83vS5lwCePdEQPLtSbalBcnOBZbRPgsb0G4d/vWV22StsepGcI9pHz58+FgTH7QeEgUsm6Pc1rSr1L+jnVz8hnZycpcpZffvdW5Lm2zwBNrJ/e9oP2Zvs4D27dTr+sAM+dvSrmAVcOgc7S/a3VXms9770U6aTqb94Btt85dpwYd15lHHBrTb9H4QWEELNl1J++H3Y9oP/FtNWe4OtLtvnEM7iS7aD6RR/qNod+w5nzYE63Da3Q52nizby69Hu8PRL2kn6gUcNJZ/Pq1X0mQ7NqT9KDylv39/pE3A+5QpZZf3et81w75YAZw/9vq2ve7v0iYovKzv328Af7WAz8fUbR7Lvw3thPR/+nt4Hm0C4UcstK55tOXFtMDYpb2e8e09qKdtspD10u4g9Y7+HlzSP4s/o/V42RXIPNo143tDm2fhOp+HifyZPhuD7ddZ1jHY/qSdaHwCOLXvwwtp3+39gdst8H3+W9pwhz/19+Q4WmB23Sll39Xbsnwe9a5HOzG6mrmPx7fu++VCYKPx7xjtpP7ttJ4VlwE/p/X+W2eijlnf+5n280yfJ9qtdYt2S/j57ssVfZnN5lF2lxnWux7wmv7eXko7jnyYFvyb8XPSl73T6LMFbDDL+3IJ7f/YnN+3lWnTTPt0Yj+dPyX91rQT8bP7ek6i9dCZtb4p9Tywlz9ySt4taPOgjY7Tp9CCrbea9vmZ7TM/W7t6fW/s36eLaBc3fgH8N/A8YL0FfK6eQvtfdUFv86m0wNSGU8q+vLdp5wXUP3oPZ3vM9F4+gxac/lN//JDWI2Za2U3msZ6dJ5Z5Ou3/6v/Sjs1nAZ+hzRc0r+3zcdN6pGpRPbwkSTegJPvTTjweVFXTbvEoSRpQH7KzrKqGmqR0oev/CO0E9061yAllbyh9GOgXgfdW1ctmKPMI2i2zd6uqRd+R6MaoDws+BDi4qnZa6vZIuuE4R4skSZJ047UD8J7VKMgSYA9ar4DJuzeN24HWc+szN0S7lshT+/MRS9oKSTc452iRJEmSbqSq6q5L3Yb56PNXPA54CG3i4f+sqsnb7V6jqt5MG3ayRumTsP5f2vDbx9KGrc11lydJaxgDLZIkSZIW62G0yVLPB/4TeMnSNmfJbEGb/P082p3E9qmq3y1tkyTd0JyjRZIkSZIkaSDO0SJJkiRJkjQQhw5Jq8hmm21Wy5YtW+pmSJIkSZJWgWOOOeZ/q+o2k+kGWqRVZNmyZRx9tHfflSRJkqQ1UZJfTkt36JAkSZIkSdJADLRIkiRJkiQNxECLJEmSJEnSQAy0SJIkSZIkDcTJcKVV5OQzz+WBe358qZshSZIkSauNY/Z7zlI3YdHs0SJJkiRJkjQQAy2SJEmSJEkDMdAiSZIkSZI0EAMtkiRJkiRJAzHQIkmSJEmSNBADLZIkSZIkSQMx0CJJkiRJkjQQAy2SJEmSJEkDMdAiSZIkSZI0EAMtkiRJkiRJAzHQIkmSJEmSNBADLZIkSZIkSQMx0CJJkiRJkjQQAy2SJEmSJEkDMdAiSZIkSZI0EAMtkiRJkiRJAzHQIkmSJEmSNBADLTdSSW6e5MgkxyU5Kckbp5R5T5I/zbD85km+0pf/aZJDkmyTZEV/nJfk9P73N6cs/4Ykv+n5JyZ58pT00WOTJDsmqSRPGqvjK0l27H8fnuTosbxtkxw+Zb1rJXl3X+cJSY5KcuckP+7r+lWSc8bWvawvd/++/r+Y5/59ai9/z4n0u/d9dVqSk5N8tu/LHZNcMLHdj5nPuiRJkiRJNx3rLHUDNKPLgEdV1Z+SrAt8P8lXq+pH0AIVwCazLP8m4BtV9a+9/H2r6gRgeX/9UeArVfW5Wep4Z1Xtn+RewPeS3HY8fbxgEoAzgX2AL89Q322TPKGqvjrLOncFbgfct6quTnJ74KKq2q6vZ3dg26p66cRyzwS+35+/Nkv9k+X/GnhDr/vmwMHAP1TVl3vaI4Hb9GW+V1U7zaNuSZIkSdJNlD1abqSqGfVWWbc/CiDJ2sB+wF6zVLElLfAxqu/4RbTlZOBKYLM5ih4HXJDksTPk7we8Zo46tgTOqqqr+7rPrKo/zLZAWpRnF2B34HE9YDJb+Q2BhwLPpwVaRp4FHDEKsvT1H1ZVJ87RZkmSJEmSAAMtN2pJ1k6yAvg9rXfKj3vWS4EvVdVZsyz+PuDDSQ5Lsk+S2y2iHdsBVwPn9KRXjA2fOWyi+D8xczDlCOCy3ktkJp8FntTrfnuS+8+jiQ8FTq+qXwCHA385R/mdgUOr6mfAeUke0NO3Bo6ZZbmHTwwduutkgSQvSnJ0kqOvvPjCeTRdkiRJkrQmMdByI1ZVV1XVcuD2wIOTbN0DJk8H3jPHsl8D7gJ8ELgncGyS28y2zBSv6IGe/YFdq6p6+juranl/XCdoUlXfA0jy8BnqnC0QQ1WdCdwDeDUtuPOtJI+eo53PBD7d//50fz1k+ZHvjW338h7YmWz/AVW1bVVtu84GG82zWkmSJEnSmsI5WlYDVXV+nzj28cDJwFbAaX1elA2SnFZVW01Z7jzgQODAJF8BHgF8fto6kuwLPLEvt7wnX28ulnnalzZXy5VT2vTtJG8Gtp9p4aq6DPgq8NUkv6P1QPnWDO1eG3ga8OQk+wABNk2yUVVdr0tJkk2BRwFbJylgbaCS7AWcBOywoC2VJEmSJGmMPVpupJLcJskm/e/1gccAp1TVwVW1RVUtq6plwMXTgixJHpVkg/73RsBdgV/NtL6q2mfUU2Oxba+qrwO3Au43Q5F9mWF+mSQPGA1zSrIWcF/gl7Os7jHAcVV1h75P7kQLJu08Q/ldgI9X1Z16+TsApwMPowWlHpLkiWPteXySbWZZvyRJkiRJ1zDQcuO1JXBYkuOBo2hztHxlAcs/EDi6L38E8KGqOmqgto3P0XLNLRJMrJ4AACAASURBVJYn7Esb8nQ9VXUI1873Mum2wJeTnAgcT+sV895Z2vJM4IsTaZ+nTWy7oPJVdQmwE/CyJD9P8lPaBLu/7+Um52jZZZZ2SZIkSZJugnLttBuShnSLLe5c93z2G5e6GZIkSZK02jhmv+csdRPmLckxVbXtZLo9WiRJkiRJkgbiZLhaI/VJb6dNoPvoqjr3hm6PJEmSJOmmwUCL1kg9mLLoiX0lSZIkSVoIhw5JkiRJkiQNxECLJEmSJEnSQAy0SJIkSZIkDcRAiyRJkiRJ0kAMtEiSJEmSJA3EQIskSZIkSdJADLRIkiRJkiQNxECLJEmSJEnSQAy0SJIkSZIkDcRAiyRJkiRJ0kAMtEiSJEmSJA3EQIskSZIkSdJADLRIkiRJkiQNZJ2lboC0prrX7Tfl6P2es9TNkCRJkiTdgOzRIkmSJEmSNBADLZIkSZIkSQMx0CJJkiRJkjQQAy2SJEmSJEkDMdAiSZIkSZI0EAMtkiRJkiRJAzHQIkmSJEmSNBADLZIkSZIkSQMx0CJJkiRJkjQQAy2SJEmSJEkDWWepGyCtqS4/6yR+9aZtlroZkiRJklYzd3zdCUvdBC2CPVokSZIkSZIGYqBFkiRJkiRpIAZaJEmSJEmSBmKgRZIkSZIkaSAGWiRJkiRJkgZioEWSJEmSJGkgBlokSZIkSZIGYqBFkiRJkiRpIAZaJEmSJEmSBmKgRZIkSZIkaSAGWiRJkiRJkgZioEWSJEmSJGkgBlokSZIkSZIGYqBFkiRJkiRpIAZaJEmSJEmSBmKgRZIkSZIkaSAGWiRJkiRJkgZioEWSJEmSJGkgBloGkmTzJAcm+Z8kxyQ5IslTe96OSS5IcmySU5LsP7bc7knO6Xk/T/K1JA+ZZT3PSXJikpOS/DTJHj39o0l+k2S9/nqzJGck2SbJiv44L8np/e9vJlmW5JL++qdJPp5k3bE2f2We237Lvu739tcbJDm4b+tJSd46yz77SpLj+voPma29C2lDTzs8yalj9d12LO8ZfZ0nJTmwpz1yrOyKJJcm2bnn7dTfo1FbXzyffSNJkiRJumlZZ6kbsCZIEuAg4GNV9ayedifgyWPFvldVOyVZHzg2yRer6gc97zNV9dK+3COBLyR5ZFWdPLGeJwAvBx5XVb9NcnPg2WNFrgL+Fvi3UUJVnQAs78t/FPhKVX2uv14G/KKqlidZG/gG8AzgkwvcBW8GvjORtn9VHZbkZsC3kjyhqr46UeZNwDeq6l97e+47W3tXog0Au1XV0eMJSe4GvBp4aFX9YRSAqarDxtZ9a+A04Os9+HQA8OCqOrMHs5bNo02SJEmSpJsYe7QM41HA5VX1gVFCVf2yqt4zWbCqLgFWAH82raJ+sn8A8KIp2a8G9qiq3/ayl1bVB8fy3wW8IsmCA2hVdRVw5EztmkmSBwKbA18fq+vivh1U1eXAT4DbT1l8S+DMseWOX2i7Z2rDHF4IvK+q/tDX+/spZXYBvlpVFwMb0YKS5/byl1XVqSvTVkmSJEnSms1AyzDuQwsmzCnJrYC7Ad+dpdhPgHtOSd8aOGaW5X4FfJ/r9nKZl947Zjvg0AUssxbwdmDPWcpsAjwJ+NaU7PcBH05yWJJ9ktxuYa2eVxv+ow8Dem3veQRwd+DuSX6Q5EdJHj9lub8GPgVQVecBXwJ+meRTSXbr653WnhclOTrJ0edddNVCN0eSJEmStJoz0LIKJHlfn8vjqLHkhyc5HjibNhzm7NmqWMTq30ILOsz3vb1rkhW03hq/WmCvkv8DHFJVv56W2XvWfAp4d1X9z2R+VX0NuAvwQVpg6dgkt1nA+udqw25VtQ3w8P4YBaDWoQW7dgSeCXyoB4RG7d4S2Ab42lhbXwA8mtbrZw/gI9MaU1UHVNW2VbXtrW+x9gI3RZIkSZK0ujPQMoyTgAeMXlTVS2gn5eNBg+9V1X1pJ/B/n2T5LPXdHzh5SvpJwANna0hVnUYbmvSM+TW9zdECbAVsn+TJMxVMst3YRLFPBv4ceGmSM4D9gedMTHx7APDzqnrXLO09r6oOrKpnA0cBj5hnu0dmbENV/aY/XwgcCDy4L3Mm8N9VdUVVnQ6cSgu8jDwD+GJVXTHR1hOq6p3AY4GnLbCdkiRJkqSbAAMtw/g2cPMkfz+WtsG0glX1M+CfgVdNy0+yA21+lg9Oyf5n4G1Jtuhl10vyf6eU25fW62LequosYG/aPDAzlflxVS3vjy9V1W5VdceqWtbX9/Gq2ru37Z+AjWmT906V5FFJNuh/bwTclTb8aSHtntqGJOsk2azXvS6wE3BiX+wg4JE9bzPaUKLxHjfPpA8b6mU2TLLjWP5y4JcLaackSZIk6abBuw4NoKqq3wb4nUn2As4BLmKGYArwAWCPJHfur3dN8jBacOZ04GmTdxzq6zkkyebAN/t8I8WUISxVdVKSnzDWy2aeDgLekOTh/fWjk5w5lv/0qjpirkqS3B7YBzgF+EmfGuW9VfWhiaIPBN6b5Epa0O9DVXUUw1gP+FoPsqwNfJNrg1dfAx6X5Ke0OzXtWVXn9rYvA+7Ade9gFGCvJP8OXEJ7b3cfqJ2SJEmSpDVIqmqp2yCtke77Z+vXV1681VI3Q5IkSdJq5o6vO2Gpm6B5SHJMVW07me7QIUmSJEmSpIE4dEirhSTbAJ+YSL6sqrZbivZIkiRJkjSNgRatFqrqBNoktJIkSZIk3Wg5dEiSJEmSJGkgBlokSZIkSZIGYqBFkiRJkiRpIAZaJEmSJEmSBmKgRZIkSZIkaSAGWiRJkiRJkgZioEWSJEmSJGkgBlokSZIkSZIGYqBFkiRJkiRpIAZaJEmSJEmSBmKgRZIkSZIkaSAGWiRJkiRJkgayzlI3QFpT3WzL+3DH1x291M2QJEmSJN2A7NEiSZIkSZI0EAMtkiRJkiRJAzHQIkmSJEmSNBADLZIkSZIkSQMx0CJJkiRJkjQQAy2SJEmSJEkDMdAiSZIkSZI0EAMtkiRJkiRJAzHQIkmSJEmSNBADLZIkSZIkSQNZZ6kbIK2pTvn9KTz0PQ9d6mZIkiRJq60fvOwHS90EacHs0SJJkiRJkjQQAy2SJEmSJEkDMdAiSZIkSZI0EAMtkiRJkiRJAzHQIkmSJEmSNBADLZIkSZIkSQMx0CJJkiRJkjQQAy2SJEmSJEkDMdAiSZIkSZI0EAMtkiRJkiRJAzHQIkmSJEmSNBADLZIkSZIkSQMx0CJJkiRJkjQQAy2SJEmSJEkDMdAiSZIkSZI0EAMtkiRJkiRJAzHQIkmSJEmSNBADLZIkSZIkSQNZIwMtSW6e5MgkxyU5Kckbp5R5T5I/zbD85km+0pf/aZJDkmyTZEV/nJfk9P73N6cs/4Yke0yknZFks/73VWN1rUiyd08/PMmpfb1HJVk+Ucf9k1SSv5hIv9529Db8ptf/8yRfSHLvGbZ3+yQ/7mVPTvKGsbydkxyf5JQkJybZZVodY+U/OrZvTkny+rG80faN6ntvkk3G8if3y7IkO/Ztfv6U/bDH2Dp/k2S9/nqzJGeMlb9Pkm8n+VmSXyR5Y5K1et7uSc4Za+8revomSc5Nkv76z/s6b99fb9w/B2vkd0iSJEmStHLW1JPEy4BHVdX9gOXA45NsP8pMsi2wyUwLA28CvlFV96uqewN7V9UJVbW8qpYDXwL27K8fsxLtu2RUV3+8dSxvt97u9wP7TSz3TOD7/Xk+3tnrvxvwGeDbSW4zpdzHgBf1bdsa+CxAkvsB+wNPqap7Ak8C/iXJA+dY7569ruXAc5PceWL77gvcl/Y+/fdY3uR+OaOnnwDsOlbur4HjJtZ5FfC3kw1Jsj7t/XprVd0d2AZ4MPD/xop9prf3ocA+Se5QVecDZwP36mUeAhzbnwG2B35cVVfPsS8kSZIkSTcha2SgpZpRL491+6MAkqxNC2DsNUsVWwJnjtV3/Cpq6myOAP5s9KL3rNgF2B14XJKbL6SyqvoM8HXgWVOybwuc1ctdVVU/7el7AG+pqtN73unAW4BXznO1ozZeNKU9l9Pegzv2gM5sfgXcvPc0CvB44KsTZd4FvCLJOhPpzwJ+UFVf7+u9GHgpsOeUNp0LnEZ7/wF+wLWBlYcA75x4/cM52i1JkiRJuolZIwMt0AIqSVYAv6f1Tvlxz3op8KWqOmuWxd8HfDjJYUn2SXK7lWjCK8aHwQDjdaw/MURm1ynLPx44aOz1Q4HTq+oXwOHAX65Em34C3HNK+juBU5N8McmLx4I49wGOmSh7NDB1CNKY/fo2nwl8uqp+P61QVV1F65kyatP4fvniRPHPAU+nBTh+QusNM+5XtN4+z55Iv9429H24/viwJYAkd6QFh0aBtR9ybWDlLsB/Adv21w+hBWKuI8mLkhyd5Ogr/nTFtM2WJEmSJK3BJq/+rzH6SfzyfjL9xSRbA+fRTtZ3nGPZryW5Cy3Y8QTg2CRbV9U5C2jCO6tq/9GL8TlD6ENkZljuk0luAawNPGAs/ZnAp/vfn6YFFL6wgPYAZFpiVb0pySeBx9F6gDyTto9C7wk0Vx0T9qyqzyXZEPhWkodU1Uy9P8brm22/fJY2/OmewKe4NgAy7i20YUIHT9Q/uQ2T6901ySOBewAvrKpLe/oPgL370KczqurSNBsCDwSOnKy0qg4ADgDY8I4bTluvJEmSJGkNtsb2aBnpc20cTgua3B/YCjitBz42SHLaDMudV1UHVtWzgaOAR8y0jiT7jvVcWazdgDsDB9J61oyGOz0NeF1v93uAJyTZaIF13x84eVpGVf2iqv4NeDRwvySbAidxbQ+OkQfQerXMqQ/fOhx42LT8vl3bzNSmibrOBq4AHgt8a4YypwErgGeMJV9vG3oQ7X/7ZwPaHC33AR4OvD3JFr2+nwO3os1Nc0QvewzwPFrvoqmTKUuSJEmSbrrWyEBLktuMhoX0yVAfA5xSVQdX1RZVtayqlgEXV9VWU5Z/VJIN+t8bAXelDU2Zqqr2GZsod9Gq6grgNcD2Se7V239cVd2ht/1OwOeBnedbZ5Kn0XqsfGpK3hNHd9cB7kabWPZ82kS4r06yrJdbBryc60/SO9M61wG2A34xJW9d4J+BXy9gDpzXAa/qvZVmsi9tbpmRTwIPS/KYvt71gXcDr59csKqOAD7BdSfKPaK/PmLs9ctxfhZJkiRJ0hRr6tChLYGP9R4TawGfraqvLGD5BwLvTXJlX/5DVXXUgO1bf6L3y6FVtfd4gaq6JMnbaUGDtYHJOUs+D/w9LTCwQZIzx/Le0Z9fkeRvgFsAJ9LuxDRt+NOzgXcmuRi4knZnoKuAFUleBXy53zp5GfDIqjp1ju3bL8lrgJvRep+MD3H6ZJLLgPWAbwJPmaOua8wy/Gi8zElJfkIfdtX345OB9yR5P22C4X+qqk/OUMW/AD9J8paqupA2fOgvubYXzxG0+VoMtEiSJEmSridVTiOh+UnyVloPlb/odw1a7STZmRaIemRV/XJVrmvDO25Y99tzrhsqSZIkSZrJD152vftPSDcaSY6pqsnpNtbYHi1aBSZ73ayOquogrns3J0mSJEmSBmOgRSslyftot5we969V9R9L0R5JkiRJkm4MDLRopVTVS5a6DZIkSZIk3diskXcdkiRJkiRJWgoGWiRJkiRJkgZioEWSJEmSJGkgBlokSZIkSZIGYqBFkiRJkiRpIAZaJEmSJEmSBmKgRZIkSZIkaSAGWiRJkiRJkgZioEWSJEmSJGkgBlokSZIkSZIGYqBFkiRJkiRpIAZaJEmSJEmSBmKgRZIkSZIkaSDrLHUDpDXVPW97T37wsh8sdTMkSZIkSTcge7RIkiRJkiQNxECLJEmSJEnSQAy0SJIkSZIkDcRAiyRJkiRJ0kAMtEiSJEmSJA3EQIskSZIkSdJADLRIkiRJkiQNxECLJEmSJEnSQAy0SJIkSZIkDcRAiyRJkiRJ0kDWWeoGSGuqC089le88YoelboYkSZK02tnhu99Z6iZIK80eLZIkSZIkSQMx0CJJkiRJkjQQAy2SJEmSJEkDMdAiSZIkSZI0EAMtkiRJkiRJAzHQIkmSJEmSNBADLZIkSZIkSQMx0CJJkiRJkjQQAy2SJEmSJEkDMdAiSZIkSZI0EAMtkiRJkiRJAzHQIkmSJEmSNBADLZIkSZIkSQMx0CJJkiRJkjQQAy2SJEmSJEkDMdAiSZIkSZI0EAMtkiRJkiRJAzHQciOT5KokK8Yey5LsnuS9E+UOT7Jt//uMJJuN5b1gbPnLk5zQ/9635/9VTzs5yfFJnjS27H8m+XWSm/XXWyQ5bYa2vi7JSb2OY5M8KMmX+rpOS3LBWDu2m6GOTyc5NcmJST6UZJ2xNh7flz0qyUMmlts4yVlJ3jWW9v1e12idm04sc2KST0ykJcleY21YkWS3sfqWJ3nIxHuyIsllSV448zspSZIkSbopWmepG6DruaSqlo8nJFlQBVX1IeBDfdkzgYdX1fn99QOAfwEeU1W/THJX4BtJ/qeqThpVATwX+OBM60jycOBxwP2r6vIktwHWqaon9/zHAC+tqp3naO7HgWcCAT4DPK+v9+vAF6uqeps/Dmw9ttxbgMOm1LdrVa2Y0t77AlcCj0qyflVd0rNeAjwS2LaqLkyyCfDk8WWr6ofA8rG6/hLYD/jPObZNkiRJknQTY4+Wm549gTdX1S8BquoXtMDLHmNl3gnskWTtWerZEjinqi7v9ZxTVWcttDFVdUg1VwNHArfv6X+qqurFbkEL/gCQ5MHAJsC3F7CqZ9KCNd8GdhpL/0fg76rqwr7e86vq4zNVkuS2wAeA3caCNZIkSZIkAQZabozWHxue8sVVUP99gGMm0o7u6SOnAz8GnjVLPYcCd+1Dbt7Xe7istD5Uabde7yhtlySnAgcBL+hpa9N6k+w5Q1Wf6PvuHyfSn0HrMfMpWtCFJLcC1h0FnebpI8C/Tus10+t8UZKjkxx9wRVXLKBaSZIkSdKawEDLjc8lVbW8P57a02qGsjOlzyZTlpuW9hbgVczwGamqPwIPAP4OOBf4XJJnr0R7Rj4AfLOqjhhbx+eq6h7ALsCbe/LLgP+uqt9OqWPXqtoGeATw6CTPAkjy58CZVfUb4BvAdkk2pm33vCV5KbAe8I6ZylTVAVW1bVVtu/G66y6kekmSJEnSGsBAy+rhXOBWE2m3Bv53Jeo6Cdh2Iu0BwE/HE6rqlJ72VzNVVFVXVtVhVfU64P/NVnY2Sd4MbAzsNcN6DgPu1edP2R54eZIzgLcCfzua5LcHUkZBoE8BD+5VPBPYui/zc+CWwFOr6jzgiiR3nEcb7wPsDTx3bEiTJEmSJEnXYaBl9XAU8NAkWwD0uw2tB/x6JeraH3jNKLiQ5C60nitvn1J2X2YYopPkXkm2Gku6H7CQITijev4O2JE258nVY+lbpc8CPLq7Up8/5a+r6o5VtYwW+PhIVe2TZN3RnZeSrAs8ETixDzV6GnDvqlrWl/sr+vAhWrDm/Uk26stuMnk3oSTrAQcCL5uhJ40kSZIkSYB3HVotVNXvkvw/4JAkawF/Ap45HpgAjk8yev3ZqvqHGeo6Osk+va51gCuAV1bViVPKHpfkOODeU6raEHh3H4JzFXAq8KKFbFcPgrwXOAP4UY+r/FdV7UubU2W3JFcAFwO7zlHdzYGv9SDLOsDXaPOpPAo4vap+N1b2MOA/k2wOvIc22e4xSS6n7Y+39XLrAJf1ttwLeH2S14/V85GqevdCtlmSJEmStGaLoyCk60tyc+AXwD1HdyRaqHtstFEdcP8HDNswSZIk6SZgh+9+Z6mbIM0pyTFVNTk1h0OHpElJtgNW0O4utFJBFkmSJEnSTZNDh3SDSPIlYHLS2T2q6ptL0Z7ZVNWPgXsudTskSZIkSasfAy26QVTVk5e6DZIkSZIkrWoOHZIkSZIkSRqIgRZJkiRJkqSBGGiRJEmSJEkaiIEWSZIkSZKkgRhokSRJkiRJGoiBFkmSJEmSpIEYaJEkSZIkSRqIgRZJkiRJkqSBGGiRJEmSJEkaiIEWSZIkSZKkgayz2AqS3Ap4GHAxcFhVXb3oVkmSJEmSJK2G5t2jJcmLk/wgya3H0u4PnAIcBHwd+H6SDYZvpiRJkiRJ0o3fQoYO/TWwTlWdN5a2H7AZ8AlaoGU74O+Ga54kSZIkSdLqYyFDh+4GHDJ6kWRT4JHAR6rqhT3tSOBZwDuGbKS0OtroHvdgh+9+Z6mbIUmSJEm6AS2kR8tmwO/HXj+0P39hLO17wLJFtkmSJEmSJGm1tJBAyx9owZaRHYACfjiWdhVw8wHaJUmSJEmStNpZyNChk4Gd+l2GrgJ2BY6qqgvGyiwDzh6ueZIkSZIkSauPhfRoeTdwO+BM4FfAlsC/jTKTrE27zfPxQzZQkiRJkiRpdTHvQEtVHQS8FPg5cAawd1V9fKzIY4CNaHcfkiRJkiRJuslZyNAhqur9wPtnyPsaLdAiSZIkSZJ0k7SQoUOSJEmSJEmaxYJ6tAAkCXA34FbA2tPKVNUPp6VLkiRJkiStyRYUaEnyauCVtCDLbKYGYCRJkiRJktZk8w60JHklsC9wIfAp4NfAlauoXZIkSZIkSaudhfRoeTHwW+CBVfW7VdQeaY3x+zMv4L2v/PJSN0OSJOl6Xvr2Jy11EyRpjbWQyXDvCHzRIIskSZIkSdJ0Cwm0/A7nXpEkSZIkSZrRQgItnwMem2S9VdUYSZIkSZKk1dlCAi2vBc4BPpPkDquoPZIkSZIkSauthUyGuwK4GbAd8KQk5wLnTylXVXWPIRonSZIkSZK0OllIoGUDoGh3HhpZf9jmSJIkSZIkrb7mHWipqtuvyoZIkiRJkiSt7hYyR4skSZIkSZJmsdKBliQbJNkyyQZDNkiSJEmSJGl1taBAS5K1kuyR5BTgQuBM4MIkp/T0tVdJKyVJkiRJklYD856jJcm6wCHAo3rSWf2xJXA34F+AJyR5fFVdMXRDJUmSJEmSbuwW0qPlFcCjgUOB+1TV7avqQX2S3HsDXwV27OUkSZIkSZJuchYSaNkN+CnwpKo6ZTyjqk4FngKcDPzNcM2TJEmSJElafSwk0HI34OCqunpaZlVdBRwMbDVEwyRJkiRJklY3Cwm0XAHcYo4yG/RykiRJkiRJNzkLCbQcD+ySZNNpmUluDezSy0mSJEmSJN3kLCTQ8j7gtsCRSZ6b5I5J1k1yhyTPBn7U89+/KhoqSZIkSZJ0Yzfv2ztX1aeTPADYA/jIlCIB3lFVnxqqcZIkSZIkSauThfRooar2Ah4BfBw4AfhVf/44sENV7bHQBiRZO8mxSb4ylvbJJKcmOTHJR5KsO2W5DXq5E3q57ye5U5IV/XF2kt+Mvb7ZxPK75/+zd+dxllT1/f9fbxhRAVFwBxQUkAAKI05EQI2IghqNEDEwGrdo1Lj7ExfErxLjQgKKGo0G9x0VxD3igqgsAjMw7LIOKuKGIIi4sHx+f9RpKe7cXgZqaHr69Xw87qNvnTpV9bm3+9LTb845lfym7Ts7yb/29u2R5PQkP27n36O372NJlrfjTkuya2s/srVdkOTK3nV3GlP7giSXJXn7SPvFSe7W235Ukq8leU7vfH9pNS1LcmB7He8dOc8xSRZN874/OEkl2X2k/V5JDktyYXtfvpHkAUk2TfLHXh3LkjyzV/cRvXPsleRjk7yfZybZa7r3s+17YvvZOK3V8oLW/sgkpyS5buRcC5OckOSsdr29e/s+3M5zepLDk6zb2g/pvZ7zkvyu9/3sf9/PTfKG3vYRSf5xqvdYkiRJkjT/zHhEy4SqOhY4dsAaXk53W+j1em2f5sbbRH8GeB7w/jHH/aqqHgSQZEvgl1W1sG0fAFxdVQdPce3PVdVLktwDOCvJV4B7AQcDj62q5UnuB3w7yUVVNbH+zKur6vAkuwCHAltU1Z7tuo8C9q2qJ05x3d2Ac4F/SvL6qqop+lJVHwU+2s5/MbBLVV3Wtp891bFTWEz3fVwMHNXOFeBI4ONVtU9rWwjcE/gZcOHE+zvGoiTbVNVZ/cYk27Hi+/mdJMuramnrtsL7mS5cOxR4aFVdkuT2wKat/0+BZ9ONruq7BnhmVZ2fZENgaZKjqup3wCur6qpW0zuBlwAHVtUre7W+FHhw2zwe2An4Urp1ia4Gduxda0fgxZO8F5IkSZKkeWqlRrQMLcnGwN8DH+q3V9U3qgFOAjYec/i9gZ/3jjm3qv58c+qoql8DFwKb0P3x/raqWt72LQfeDrx6zKEnABvdjEsuBt5NFxg87ObUfEu0QGUvurBityR3aLt2Aa6tqg9M9K2qZVX1wxmc9mDg9WPax72fbwNeNaZv//28E10Q+Nt23J+r6tz2/OIWet3kVuNVdV5Vnd+eXwr8Grh7254IWQLcERgXbi0GJqa+HUcXtNC+fg24ezr3A/5YVb+c9N2QJEmSJM1LkwYtSTZsjzVGtqd9rMT13wW8hpE/mHs13A54BvDNMbs/Ary2TRV5S5ItVuK6o9e5P3B/4AJgG2DpSJclrX3U44AvreS17gjsSveH+2fp/ri/pfbuT+kBppw2BOwMLK+qC4FjgCe09gey4mvv22xk6tAjevs+D2yfZPORYyZ7P7cec/6/vp9VdTnwFeAnST6b5OkTP4szkeShwFp0AdpE20eBXwJ/A/z3SP9NgPsBR7empcAD000524kuBDoX2KptHzfJdZ+fZEmSJVdfc+VMy5UkSZIkrSam+sP1EroRF5v3tn82g8dPZ3LhJE8Eft2bPjLO/wA/GDeioqqW0YUjBwEbACcn2Wom1+7ZuwUTnwVe0P64DyuOdhhtOyjJRcCn6EZnrIwnAt+rqmuAI4A9k6zZ9o0bZTHltKLmc1W1cOJBF2RMZTFwWHt+GDMPey7sX2fk+3I93fdiv5FjJns/+8a+n1X1PLpQ6iQmX4R5BUnuDXwSeE5V/TXEq6rnABvSTVXbe+SwfYDD6nMEhAAAIABJREFUq+r61vfPwFnA9nSjjk6kC1t2ao/jx127qg6tqkVVtWjdte88k3IlSZIkSauRqdZo+QzdH8hXjmwPZWfgH5I8AbgDsF6ST1XVPwMkeRPdtI8XTHaCqroa+CLwxSQ30I3MOGdc3yQvBiYWvJ0YwfG5qnrJSNez6EaEnN5r2x44u7f96nbdlwEfBx4y9Uu9icXAzm2tFYC70k3Z+Q7dNJn1gcvavg16zwfRQp2n0L33+9OFHndNcie6177XVMdP45N0QUt/nZbJ3s9+GDTp+1lVZwBnJPkksJxuutOkkqwHfB14Q1X9aHR/VV2f5HPtmh/t7dqHFddcOZ5u8ec7VdUVSX5Et7bLg4EPIEmSJEnSiEmDlonAY7LtW6qq9qONfugtIDsRsjwP2B3YtT8ioS/JzsDZ7Q/gteimohwzxfXeB7yvd/xkXQ8GvpDk6Kq6OMmmdGuP3CSAqKobkrwbeFaS3avqqOlecwsBHg7cZ2I9mSTPoQtfvtPqfwbwxhaI/DMrOTVpBh4DnFZVf73bUJKPA3vQRpQk+deq+mDb97fA2sBPpjtxVV2b5BDgddw4BWfc+/kK4Kkjx97k/aSbmrOoqo5pXRZOV0P7OTgS+ERVfaHXHmCzqrqgPX8S8OPe/i3pAq4TRk55HPAObvy5Op1udMs9uWmYJEmSJEkSMMuL4U7hA3R/zJ7Q1gJ545g+mwHfT3IGcCrdCIkjxvRbKW1K0muBryb5MfBV4DWtfbRvAW+hW2dmJv4ROHpk0d4v040uuT3wH8DmSU6je00X0IUfQ1pMF0b0HQE8rb2ePYHHpru981nAAcClrd/oGi0vG3P+D9ML8Ebez/OA84B/m1jYtm/k/QzwmnS3VV4G/DttNEuSv01yCV1Y87+tToB/ohuB8uxejQvbuT7eflbOoFtI+c0j78lhY+7+dDzd9LQTWn3X0S2wu2SyAFCSJEmSNL9lmjsL39gx+Qvw71X11in67AccUFW3H6g+rWaSHAjsAOxeVX+Z7XpWpfvea4t6zdPfOdtlSJIkreAl73jSbJcgSXNekqVVtcLNaKZao2Vc3zWn6bPGSp5T80xVvW62a5AkSZIkaVUZOhS5C/Cngc+pmynJicDo6KJntAVmJUmSJEnSwKYMWpLsNNJ03zFt0I10uS/wNLo1OHQbUFU7zHYNkiRJkiTNJ9ONaDmWG2/pXMBz2mOctD5ODZEkSZIkSfPSdEHL2+jCk9Dd4vgHwA/H9Lse+C3dHXW87a0kSZIkSZqXpgxaquoNE8+TPAv4UlW9a5VXJUmSJEmSNAfNeDHcqrrPqixEkiRJkiRprltjtguQJEmSJElaXazU7Z2TBNgD2B3YiBVvHQxQVbX7ALVJkiRJkiTNKTMOWpKsBXwN2JUb7zCUXpfqtUuSJEmSJM07KzN16DXAY4ADgXvRhSpvBu4LPBP4OXAYcMeBa5QkSZIkSZoTViZo2Rs4tar2r6pft7YbquqSqvoUsAvwJODFQxcpSZIkSZI0F6xM0HJ/4LjedgG3++tG1YXA14F/GaY0SZIkSZKkuWVlgpbrgGt621cDdx/pczFdICNJkiRJkjTvrEzQ8nNg4972ecDDRvpsB1xxS4uSJEmSJEmai1YmaDmOmwYrXwa2TfK/SXZP8nZgN+CYAeuTJEmSJEmaM1I1s7sxJ3k0sB/wr1V1cZJ1gO8D23PjrZ2XA39XVZesonqlOWPRokW1ZMmS2S5DkiRJkrQKJFlaVYtG2xfM9ARVdTRwdG/7D0l2BP4R2JxufZYvV9XVt7xcSZIkSZKkuWfGQcs4VXUt8LmBapEkSZIkSZrTZrxGS5JvJfnnafo8Lcm3bnlZkiRJkiRJc8/KLIb7GKa/dfP9gF1vfjmSJEmSJElz18oELTNxR+C6gc8pSZIkSZI0J6xs0DLpLYqSbAQ8DvCOQ5IkSZIkaV6aMmhJcm2SvyT5S2t608T2yONa4Kd0t3p2cVxJkiRJkjQvTXfXoRO5cRTLTsDP6QKVUdcDvwW+C/zvYNVJkiRJkiTNIVMGLVX18InnSW4APlxVb17lVUmSJEmSJM1B041o6dsCuHxVFSKtbn6x/ELe+s97zXYZkiRpJez/qcNnuwRJ0hw346Clqi4cbUuyBrA1EODsqrp+wNokSZIkSZLmlOkWw900yTOTbDFm327Az4DTgGXApUmevGrKlCRJkiRJuu2b7vbOzwU+SrfY7V8l2QT4InBv4BfABcDdgc8n2XoV1ClJkiRJknSbN13Q8nDgzKq6aKT9ZcDawEeA+1TVlsBi4HbASwevUpIkSZIkaQ6YLmi5P3DmmPbHA9cBr66qAqiqz9HdDvrvBq1QkiRJkiRpjpguaLk78JN+Q5J1gS2BpVV1xUj/JcB9hitPkiRJkiRp7pguaClgvZG2hXR3GVo6pv+VdNOHJEmSJEmS5p3pgpafADuNtD2KLoA5aUz/uwG/uuVlSZIkSZIkzT3TBS3fBrZL8rok6yRZCLyI7i5E3xzTfxEjU40kSZIkSZLmi+mClv+kmw70VuAquulC9wI+XlW/7ndMcl/gwcAPVkGdkiRJkiRJt3lTBi1VdSmwC/BD4Fq6aUHvBl4ypvu/ANcwfqSLJEmSJEnSam/BdB2q6jS6dVmm63cAcMAtrkiSJEmSJGmOmm7qkCRJkiRJkmbIoEWSJEmSJGkgBi2SJEmSJEkDMWiRJEmSJEkaiEGLJEmSJEnSQAxaJEmSJEmSBnKbD1qS3DXJsvb4ZZKf97avaX02TVJJ/qN33N2SXJvkvW37gJFjlyW5S5K1k3w6yRlJzkxybJJ1x9TxL63P6a3fk1t7krwhyflJzkvy/STbTvOa7pvk6iT7tu37JPleknOSnJXk5ZMct2WSY1rt5yQ5NMnuvddzdZJz2/NPTPF+fq/1fW+vfe0kX0/y41bDgb19L2yvfVl7f7Zu7U8feT9vSLKwd9yD2/dl95Ea7pXksCQXJjk7yTeSPKB9H/84cs5ntmMuTnJE7xx7JflYb3uP9r35cfv+7NXb97Eky9v5Tkuya2/fE5Oc2trPTvKC9nPx2yRpfXZsr2Pjtn3nJJcnuc1/fiRJkiRJt64F03VIsgFwB+CXVXXDJH3WBO4J/KmqLh+ywKr6LbCwXecA4OqqOrhtX93rehHwROD/te2nAmeNnO6QiWN7te8H/KqqHtS2twSuHemzMbA/sH1VXdmCmLu33S8GdgK2q6prkuwGfDXJ1lX1h0le1iHA//W2rwNeVVWnJLkTsDTJt6vq7JHj3tNew5dbXQ+qqjOAo9r2McC+VbVkkusC/InuPXpge/QdXFXfS7IW8N0kj6+q/wM+U1UfaNf4B+CdwOOq6tPApydqAb5cVct651sMHNu+TtQY4Ejg41W1T2tbSPfz8zPgwqpayHiLkmxTVTf5vibZDjgYeGxVLU9yP+A7SZZX1dLW7dVVdXiSXYBDgS2S3K49f2hVXZLk9sCmVfW7JL8EtgLOpvv+ntq+fh54GHDiZJ8HSZIkSdL8NeX/kU9yd2A58Klp/qi8AfgkcGGSuw5Y38r4I3BOkkVte2+6P4qnc2/g5xMbVXVuVf15pM89gN8DV7c+V1fV8rbvtcBLq+qatu9bwA+Ap4+7WJI96EKhv4YFVfWLqjqlPf89cA6w0SS1XtI77owZvL6bqKo/VNWxdIFLv/2aqvpee/4X4BRg47Z9Va/rOkCNOfVi4LMTGy1Q2Qt4NrBbkju0XbsA104EN+38y6rqhzMo/2Dg9WPa9wXeNvE9aV/fBrxqTN8TuPG9vRNd2Pjbdtyfq+rctu84umCF9vWQke3jZ1CvJEmSJGmemW7qw3Pp/rAeO5VlQlUV8DJgPeB5w5R2sxwG7NNGoFwPXDqy/5W9KSnfa20fAV6b5IQkb0myxZjzngb8Clie5KNJngSQZD1gnaq6cKT/EmDr0ZMkWYcumPn3yV5Akk2BBwMnjtl9CHB0kv9L8sokd5nsPLdEO++TgO/22l6c5ELgv+i+16P2phe0ADsDy9t7cwzwhNb+QGApk9tsZOrQI3r7Pg9sn2TzkWO2GXPOsd8D4HHAlwDa6KuvAD9J8tk2FWriM3E8NwYr9we+AEyEeDvRBTErSPL8JEuSLPnDn0bzOkmSJEnS6m66oOXxwCkzGTnRpnOcRDd9Z7Z8E3gs3eiKz43Zf0hVLWyPXaAbTUH3h/RBwAbAyUm26h9UVdfT/YG+F3AecEibxjSZTNL+762Gq8ftbFOSjgBeMTKKZKKOj9JNZ/kC8CjgR226y2CSLKALTN5TVRf1rv2+qtqMLih6w8gxOwDXVNWZvebFdMEX7eviGZZwYe97tHBkpMv1dN+n/UbLZsVRNqPfg4OSXAR8im60y8Treh6wK93P7r50wRu0ES1tGtLFVfWn7qVmXeAhrf8KqurQqlpUVYvWucOg3xpJkiRJ0hwwXdCyDfCjlTjfyXRBwKxoU16W0k0ZOWKa7v3jrq6qL1bVi+j+EH/CmD5VVSdV1duBfYCntDDkD0nuP9J9e2BJkj17IzMWATsA/5XkYuAVwOuTvASgrRdyBPDpqvriFLVeWlUfqaon063tMrrOyi11KHB+Vb1rkv2HAXuMtO3DTacNrQk8BXhje63/DTy+rT9zFl1QcXN9EngkcN9e21ncONpkwvZ0o1omvBrYnC4k+ni/Y1WdUVWH0IV0T2lt5wPr043sOaF1XQo8h26kztiwTJIkSZI0v00XtKwHXLkS57uyHTOb3gG8ti2iO60kOydZvz1fi266yU9G+myYZPte08Jen4OA9yS5Y+v7GLqA6vCqOrI3MmNJVT2iqjatqk2Bd9GtK/Letp7Jh4FzquqdU9T6uBbIkORewF3prS9zSyV5C3BnuhCo396fTvX3wPm9fWvQLTx8WK/PY4DTquo+7fVuQhci7QEcDdw+yb/2zvG3Sf5uJjVW1bV0U6j6NR4M7NemXU1Mv3oF3femf+wNwLuBNdLdrWndJI/qdel/X6ELWF7OjUHLCe28rs8iSZIkSRprursOXcmNd9eZibsDK0x5uTW1KUyjdxua8Mok/9zb3gPYDHh/CzvWAL7OiqNhbgccnGRDukVkfwO8sO37b+AuwOktBFkLeGCbajJTOwPPAM5IMnHXntdX1TdG+u0GvDvJxLlfXVW/XInrAN2tkukCsbXa4ry70X3f9gd+DJzS7mz83qr6EPCSFiBdC1wBPKt3ukcCl/SnGdFNEzpy5LJHAP9WVZ9MsifwriSvo3s/L+bG4GSz3nsA8JGqes/IuT5Mb/pSVS1L8lq6uz3dHtgU2KW3sC29vtUCpdfQff9fk+R/6RZT/gPd4r0TjqMb3TQxMuYEumlmBi2SJEmSpLHSrWM7yc7keGD9qprRdKAk5wCXV9XOA9U3p7T1O44ETq6qcXfH0a0gyYF007R2b9PJZsVGd12/XvT4XWfr8pIk6WbY/1OHz3YJkqQ5IsnSqhpdxmLaqUPfBB6Q5GkzuMBiYMt2zLzU1np5rCHL7Kqq11XVLrMZskiSJEmS5qfpgpb3AVcDhyZ51mSdkjwT+CDdVKP3DVeebq62BsmykcfodB5JkiRJkjSgKddoqarfthDlC8BHkrwJOAa4hO52uhsDuwCb0N16d3FVXb5KK9aMVNVRwFGzXYckSZIkSfPJdIvhUlVfTvI44AN0t8d9Nl3IApD29QLgBVX1vVVRpCRJkiRJ0lwwbdACUFVHJ/kb4NHAw4F704UslwLHAke3W+dKkiRJkiTNW1MGLUnWraqrAVqQ8p32kCRJkiRJ0ojpFsM9LcmOt0olkiRJkiRJc9x0Qct9gR8keXOSNW+NgiRJkiRJkuaq6YKWnYCLgP2B45NsvupLkiRJkiRJmpumDFqq6mRgIXAo8LfAqUmef2sUJkmSJEmSNNdMN6KFqvpjVf0b8ETgD8D7k3w5yZZJ7jvuscqrliRJkiRJug2a0e2dAarqG0m2AT5BF7o8cbKuK3NeSZIkSZKk1cXKBiLbtkeAXwJ/HrwiSZIkSZKkOWpGQUuS2wFvB14BXAe8Fji4qmoV1iZJkiRJkjSnTBu0tOlCn6YbyXI28PSqOm1VFyZJkiRJkjTXTLkYbpKXAycDDwL+G3iIIYskSZIkSdJ4mWr2T5IbgF8Az6mqb91qVUmrgUWLFtWSJUtmuwxJkiRJ0iqQZGlVLRptn+72zkcCDzJkkSRJkiRJmt6Ua7RU1VNurUIkSZIkSZLmuimDliTTjXgZq6puuHnlSJIkSZIkzV3T3XXo2ptxzprBeSVJkiRJklY70wUiP6MLTmZiXeCut6wcSZIkSZKkuWu6NVo2ne4ESW4HvBTYvzVdfIurkiRJkiRJmoNu1hosE5I8FTgHOAgI8BpgqwHqkiRJkiRJmnNu1loqSXYC3gE8FLgOeA/w5qq6YsDaJEmSJEmS5pSVClqSbA4cCOxJN4LlcOB1VXXRKqhNkiRJkiRpTplR0JJkA+BNwAuAtYATgFdV1Y9WYW2SJEmSJElzypRBS5K1gFcA+wF3Bi6kG8FyxK1QmzSn/ekXv+ectx4922VIkrTa2Wr/R892CZIkTWq6ES3nAvcFLqcLXN5XVdev8qokSZIkSZLmoOmClk2AoluPZV9g3yTTnbOqapMBapMkSZIkSZpTZrJGS4AN2kOSJEmSJEmTmDJoqao1bq1CJEmSJEmS5jqDFEmSJEmSpIEYtEiSJEmSJA3EoEWSJEmSJGkgBi2SJEmSJEkDMWiRJEmSJEkaiEGLJEmSJEnSQAxaJEmSJEmSBmLQIkmSJEmSNBCDFkmSJEmSpIEYtEiSJEmSJA3EoEWSJEmSJGkgBi2SJEmSJEkDMWiRJEmSJEkaiEHLairJ9UmW9R6bJnlUkq+N6Xtxkrv1tv/aL8k9k3wtyWlJzk7yjda+aZIzR85zQJJ92/OPJdmrPT8myZJev0VJjultP7T1OT/JKUm+nuRBk7yui5P8cKRt2Zha3p3k50nW6LU9O8l7e7Vek+Qevf1XT/F+bjnyfl6V5BWT9ZckSZIkzU8LZrsArTJ/rKqF/YYkm96M87wZ+HZVvbudY9ubWc89kjy+qv5vpKZ7Ap8HnlZVx7e2hwObAWdMcq47JblPVf0syVajO1u4sifwM+CRwDGTnOcy4FXAa6crvqrOBRa2868J/Bw4crrjJEmSJEnziyNaNJ17A5dMbFTV6TfzPAcBbxjT/hLg4xMhS7vGsVX1pSnO9Xlg7/Z8MfDZkf27AGcC72/7J/MRYO8kG0xT+6hdgQur6icreZwkSZIkaTVn0LL6umNvmsstGXnxPuDDSb6XZP8kG/b2bdafTgO8cIrznAD8OckuI+3bAKesZE2HA//Ynj8J+OrI/onw5UjgiUluN8l5rqYLW16+ktffhxXDHUmSJEmSDFpWY3+sqoXtsec0fWuytqo6Crg/8EHgb4BTk9y99bmwd42FwAemuc5bGD+q5a+SnJjknCTvnqLb5cAVSfYBzgGu6R2/FvAE4EtVdRVwIrDbFOd6D/CsJOtNU3v//P8AfGGS/c9PsiTJksv/8LuZnFKSJEmStBoxaBHAb4H1e9sb0K1fAkBVXV5Vn6mqZwAn0617stKq6mjgDsDDes1nAdv3+uwA/D/gzknW7I2YefPI6T5HN9pmdGTJ44A7A2ckuRh4OFNMH6qq3wGfAV40w5fxeOCUqvrVJOc7tKoWVdWiDda5ywxPKUmSJElaXbgYrqBbLPYZwBvbQq//DHwJIMmjgR9V1TVJ7kS3SO1Pb8G13ko38uWitv0+4MQkR/XWaVkboKqupy1AO8aRdOvHHAX0pzMtBp5XVZ9t9a8DLE+y9hQ1vZMuQJrJ52HcmjCSJEmSJAGOaJmPdk1ySe+xI/AfwOZJTgNOBS4APtX6PwRYkuR0unVWPlRVJ9/ci1fVN4Df9LZ/Sbew7duTXJDkeGAv4L3TnOf3VfWfVfWXibYWpuwOfL3X7w/AsXRruUx2rsvogpvbT3XNdv7HAl+cqp8kSZIkaf5K1bjlOSTdUg/caMv6woveP9tlSJK02tlq/0fPdgmSJJFkaVUtGm13RIskSZIkSdJAXKNF6klyV+C7Y3btWlW/vbXrkSRJkiTNLQYtUk8LUyZbgFeSJEmSpCk5dUiSJEmSJGkgBi2SJEmSJEkDMWiRJEmSJEkaiEGLJEmSJEnSQAxaJEmSJEmSBmLQIkmSJEmSNBCDFkmSJEmSpIEYtEiSJEmSJA3EoEWSJEmSJGkgBi2SJEmSJEkDMWiRJEmSJEkaiEGLJEmSJEnSQAxaJEmSJEmSBrJgtguQVld3uPed2Gr/R892GZIkSZKkW5EjWiRJkiRJkgZi0CJJkiRJkjQQgxZJkiRJkqSBGLRIkiRJkiQNxKBFkiRJkiRpIAYtkiRJkiRJAzFokSRJkiRJGohBiyRJkiRJ0kAMWiRJkiRJkgZi0CJJkiRJkjSQBbNdgLS6uvTSSznggANmuwxJkm6T/B0pSVpdOaJFkiRJkiRpIAYtkiRJkiRJAzFokSRJkiRJGohBiyRJkiRJ0kAMWiRJkiRJkgZi0CJJkiRJkjQQgxZJkiRJkqSBGLRIkiRJkiQNxKBFkiRJkiRpIAYtkiRJkiRJAzFokSRJkiRJGohBiyRJkiRJ0kAMWiRJkiRJkgZi0CJJkiRJkjQQgxZJkiRJkqSBGLRIkiRJkiQNxKBFkiRJkiRpIAYtkiRJkiRJAzFomUOS3CvJYUkuTHJ2km8keUBv/yuT/CnJnXttj0pSSZ7Ua/takkf1tu+e5NokLxi53sVJ7jZFPWsn+XSSM5KcmeTYJJskWdYev0zy8972WpOc5+r2ddNW60t7+96b5NnteZK8Icn5Sc5L8v0k247Ue0aS09u+TVr7nr0aJh43JHl823/fJN9Kck57XzdN8uQkX+qde78kF/S2n5TkK5O9N5IkSZKk+cmgZY5IEuBI4Jiq2qyqtgZeD9yz120xcDKw58jhlwD7T3H6pwI/asevjJcDv6qqB1XVA4HnAr+sqoVVtRD4AHDIxHZV/WUG5/w18PJJQpkXAzsB21XVA4C3Al9Nsk6vzy5VtS1wDPAGgKo6slfDQuB/gB8CR7VjPgEcVFVbAQ9tNRwP7Ng7747AVUnu0bZ3Ao6bweuRJEmSJM0jBi1zxy7AtVX1gYmGqlpWVT8ESLIZsC5duDAamJwGXJnksZOcezHwKmDjJButRE33Bn7eq+fcqvrzShw/zm+A7wLPGrPvtcBLq+qadr1vAT8Anj6m7wnACq+ljQB6I/CMqrohydbAgqr6djvn1VV1TVX9hu4927wduhFwBF3AQvt6/M18jZIkSZKk1ZRBy9zxQGDpFPsXA5+lG6mxZW/kxYS30EZ49CW5D3CvqjoJ+Dyw90rU9BHgtUlOSPKWJFusxLFTORB4VZI1e3WuB6xTVReO9F0CbD3mHI8DvtRvSHI74DPAvlX109b8AOB3Sb6Y5NQkB/WuezywU5ItgfPpRv3slGQBsC3d6KGbSPL8JEuSLLnmmmtW8mVLkiRJkuY6g5bVxz7AYVV1A/BFuulAf9Ub+fKIMcd9vj0/jJWYPlRVy4D7AwcBGwAnJ9nqZlV/0/MuB04CnjaD7hnZ/l6SXwOPoQtV+v4DOKuqDuu1LQAeAewL/C3d63l223cc3ciVnehGyJwE7AA8GDi3qv40pvZDq2pRVS1ae+21Z1C+JEmSJGl1YtAyd5wFPGTcjrYg7BbAt5NcTBeejAtM3sqKa7UsBp7djvsKsN3KjExpU22+WFUvAj4FPGGmx07jbXRThdZo17kK+EOS+4/0255uVMuEXYBN6N6vN080tsV/nwK8ZOT4S4BTq+qiqrqObhTM9m3f8fSClqr6PXAH4FG4PoskSZIkaQyDlrnjaOD2Sf51oiHJ3yb5O7qw5ICq2rQ9NgQ2mrjrzoS2psn6wHbt+C3ppuNsNHEs8Ha6oGZaSXZOsn57vhbdFJ6f3NIX2mr9MXA28MRe80HAe5LcsV3zMcA2wOEjx/4ReAXwzCQbtBo/CjyzhSV9JwPrJ7l72350uy7t64Z0I15ObW3LgBfi+iySJEmSpDEMWuaIqiq6uwk9tt3e+SzgAOBSumDkyJFDjmR8YPJWYOP2fPGY447gpqNhTk9ySXu8c6TvZsD3k5xBF0QsacfPWFvvZLIFdPu1Avw33fSd09sInE8Aj51kCs8v6NaseTFdMHIP4P0jt3jeu6qup5s29N32OgJ8sJ2jgBOBy6rq2nbqE+imFxm0SJIkSZJWkO5vSWl2JNkO+GBVPXQlj1uXLiQ6uapev0qKu4U23HDDev7znz/bZUiSdJt0wAEHzHYJkiTdIkmWVtWi0fYFs1GMBJDkhcDL6Kb5rJSquhqY7HbVkiRJkiTNCoMW3SqS3BX47phdj6iq397a9UiSJEmStCoYtOhW0cKUhbNdhyRJkiRJq5KL4UqSJEmSJA3EoEWSJEmSJGkgBi2SJEmSJEkDMWiRJEmSJEkaiEGLJEmSJEnSQAxaJEmSJEmSBmLQIkmSJEmSNBCDFkmSJEmSpIEYtEiSJEmSJA3EoEWSJEmSJGkgBi2SJEmSJEkDMWiRJEmSJEkaiEGLJEmSJEnSQFJVs12DtFpatGhRLVmyZLbLkCRJkiStAkmWVtWi0XZHtEiSJEmSJA3EoEWSJEmSJGkgBi2SJEmSJEkDMWiRJEmSJEkaiEGLJEmSJEnSQAxaJEmSJEmSBmLQIkmSJEmSNBCDFkmSJEmSpIEYtEiSJEmSJA3EoEWSJEmSJGkgC2a7AGl1dcUV5/D5Lzx0tsuQJK0m/umpJ812CZIkaQYc0SJJkiRJkjQQgxZJkiRJkqSBGLRIkiRJkiQNxKBFkiRJkiRpIAYtkiRJkiRJAzFokSRJkiRJGohBiyRJkiRJ0kAMWiRJkiRJkgZi0CJJkiRJkjQQgxZJkiRJkqSBGLRIkiRJkiTWum5GAAAdbElEQVQNxKBFkiRJkiRpIAYtkiRJkiRJAzFokSRJkiRJGohBiyRJkiRJ0kAMWiRJkiRJkgZi0CJJkiRJkjQQg5Z5KMnFSc5IsizJkl77dklOaPu+mmS9MceukeQ9Sc5s/U5Ocr8kJ7bz/TTJb9rzZUk2naaWryQ5s7d9QJKf945/Qm/ftq2+s9q179B7PUf0+u2V5GO97T2SnJ7kx63uvXr7PpZkebvWaUl2be1PTvKlXr/9klzQ235Skq/M4O2WJEmSJM0jC2a7AM2aXarqspG2DwH7VtX3k/wL8Grg/4302RvYENi2qm5IsjHwh6raASDJs4FFVfWS6QpI8o/A1WN2HVJVB4/0XQB8CnhGVZ2W5K7Atb0ui5JsU1VnjRy3HXAw8NiqWp7kfsB3kiyvqqWt26ur6vAkuwCHAlsAx7fnE3YErkpyj6r6NbATcNx0r1GSJEmSNL84okV9WwI/aM+/DTxlTJ97A7+oqhsAquqSqrpiZS+UZF3g/wPeMsNDdgNOr6rT2nV/W1XX9/YfDLx+zHH7Am+rquXtuOXA24BXjel7ArBR6/cb4Mokm7d9GwFH0AUstK/Hz7B2SZIkSdI8YdAyPxXwrSRLkzy/134m8A/t+VOB+4w59vPAk9pUm3ckefDNrOE/gHcA14zZ95I21ecjSdZvbQ8AKslRSU5J8poxdW3fC0YmbAMsHWlbAmw95rqPA77U2z4e2CnJlsD5wI/a9gJgW+Dk0RMkeX6SJUmWXHXVdWMuIUmSJElanRm0zE87V9X2wOOBFyd5ZGv/l7a9FLgT8JfRA6vqErqRL/sBNwDfnVjXZKaSLAQ2r6ojx+x+P7AZsBD4BV0YA900t4cDT29f9xy57vXAQa2um1yOLlgabes7KMlFdFOT3tZrP45u5MpOdKNdTgJ2AB4MnFtVfxotvqoOrapFVbVovfWcmSdJkiRJ841ByzxUVZe2r78GjgQe2rZ/XFW7VdVDgM8CF05y/J+r6v+q6tV0wcQeK1nCjsBDklwMHAs8IMkx7dy/qqrr29SkD07UBlwCfL+qLquqa4BvANuPnPeTwCOB+/bazgIWjfTbnm5Uy4RXA5sDbwA+3ms/nl7QUlW/B+4APArXZ5EkSZIkjWHQMs8kWSfJnSae0619cmbbvkf7ugZd6PCBMcdvn2TDXr9tgZ+sTA1V9f6q2rCqNqUbnXJeVT2qnfPeva57TtQGHAVsm2TtNnXn74CzR857LXAI8Ipe88HAfhN3P2pfX0E3+qV/7A3Au4E1kuzems+mW/j3EcCprW0Z8EJcn0WSJEmSNIZBy/xzT+DYJKfRTYX5elV9s+1bnOQ84MfApcBHxxx/D+Cr7ZbMpwPXAe8dsL7/arduPh3YBXglQFtw951066IsA06pqq+POf7D9O6mVVXLgNe2ms8DzgP+rarOHT2wqopucd7X9LZPBC5rIQ50U4juj0GLJEmSJGmMdH9LSvNDkgPp1lnZvapWWINmSJtttk69/cBtVuUlJEnzyD899aTZLkGSJPUkWVpVo0tV4Gqdmleq6nWzXYMkSZIkafVl0KJVKsmJwO1Hmp9RVWfMRj2SJEmSJK1KBi1apapqh9muQZIkSZKkW4uL4UqSJEmSJA3EoEWSJEmSJGkgBi2SJEmSJEkDMWiRJEmSJEkaiEGLJEmSJEnSQAxaJEmSJEmSBmLQIkmSJEmSNBCDFkmSJEmSpIEYtEiSJEmSJA3EoEWSJEmSJGkgBi2SJEmSJEkDMWiRJEmSJEkaiEGLJEmSJEnSQBbMdgHS6mr99bfin5560myXIUmSJEm6FTmiRZIkSZIkaSAGLZIkSZIkSQMxaJEkSZIkSRqIQYskSZIkSdJADFokSZIkSZIGYtAiSZIkSZI0EIMWSZIkSZKkgRi0SJIkSZIkDcSgRZIkSZIkaSAGLZIkSZIkSQNZMNsFSKurs6+4iu0OP2q2y5Ak3Uacttfus12CJEm6FTiiRZIkSZIkaSAGLZIkSZIkSQMxaJEkSZIkSRqIQYskSZIkSdJADFokSZIkSZIGYtAiSZIkSZI0EIMWSZIkSZKkgRi0SJIkSZIkDcSgRZIkSZIkaSAGLZIkSZIkSQMxaJEkSZIkSRqIQYskSZIkSdJADFokSZIkSZIGYtAiSZIkSZI0EIMWSZIkSZKkgRi0SJIkSZIkDcSgRZIkSZIkaSAGLZIkSZIkSQMxaFmNJbk+ybIkZyb5QpK1e/v2TFJJ/qZtP6j1XZbk8iTL2/PvJNk0yZkj5z4gyb5jrnlAkmuS3KPXdvWYmiYer0vy5CRf6vXZL8kFve0nJfnKyHVmdEySE9t1fprkN73rbppk3ST/m+TCJGcl+UGSHaZ4Pz+S5Nej74UkSZIkSRMMWlZvf6yqhVX1QOAvwAt7+xYDxwL7AFTVGa3vQuArwKvb9mNuxnUvA141TU0TjwOB44Ede312BK7qhTU7AceNnGdGx1TVDu01vRH4XO+6FwMfAi4HtqiqbYBnA3eb4nV9DHjcFPslSZIkSfOcQcv88UNgc4Ak6wI7A8+lBS0D+wiwd5INZtK5qn4DXJlk89a0EXAEXVhC+3r8LT2mL8lmwA7AG6rqhnbOi6rq61PU+QO6YEaSJEmSpLEMWuaBJAuAxwNntKY9gG9W1XnA5Um2n8FpNutP+eGmo2NGXU0Xtrx8zL47jkwd2ru1Hw/slGRL4HzgR217AbAtcPKYc92cYyZsAyyrquun6LPSkjw/yZIkS6676sohTy1JkiRJmgMWzHYBWqXu2EIR6Ea0fLg9Xwy8qz0/rG2fMs25LmxTcIBuLZZp+r8HWJbkHSPtf+yfp+c4ulEoawInACfRTfd5MHBuVf1poGNWqao6FDgUYO3NHlC39vUlSZIkSbPLoGX1tkKokeSuwKOBByYpupCikrymqgYLBqrqd0k+A7xohoccD7y01fPBqvp9kjsAj2LF9VluyTETzgK2S7LGxNQhSZIkSZJuKacOzT97AZ+oqk2qatOqug+wHHj4KrjWO4EXMLNA72xgQ+ARwKmtbWKK0mRrrdycYwCoqguBJcC/JwlAki2SPHkGtUqSJEmSNJZBy/yzGDhypO0I4GlDX6iqLmvXun2veXSNlgNb3wJOBC6rqmtb3xOA+zNJaHJzjhnxPOBewAVJzgA+CFw6Weckn23n3zLJJUmeO4NrSJIkSZLmkQw4W0RSz9qbPaC2+M//nu0yJEm3EafttftslyBJkgaUZGlVLRptd0SLJEmSJEnSQFwMV+ppiwV/d8yuXavqt7d2PZIkSZKkucWgReppYcq4209LkiRJkjQtpw5JkiRJkiQNxKBFkiRJkiRpIAYtkiRJkiRJAzFokSRJkiRJGohBiyRJkiRJ0kAMWiRJkiRJkgZi0CJJkiRJkjQQgxZJkiRJkqSBGLRIkiRJkiQNxKBFkiRJkiRpIAYtkiRJkiRJAzFokSRJkiRJGsiC2S5AWl1tvf56LNlr99kuQ5IkSZJ0K3JEiyRJkiRJ0kAMWiRJkiRJkgZi0CJJkiRJkjQQgxZJkiRJkqSBGLRIkiRJkiQNJFU12zVIq6UkvwfOne06pNuYuwGXzXYR0m2Qnw1pRX4upBX5ubht2aSq7j7a6O2dpVXn3KpaNNtFSLclSZb4uZBW5GdDWpGfC2lFfi7mBqcOSZIkSZIkDcSgRZIkSZIkaSAGLdKqc+hsFyDdBvm5kMbzsyGtyM+FtCI/F3OAi+FKkiRJkiQNxBEtkiRJkiRJAzFokQaW5HFJzk1yQZLXzXY90qqU5D5JvpfknCRnJXl5a98gybeTnN++rt/ak+Q97fNxepLte+d6Vut/fpJnzdZrkoaSZM0kpyb5Wtu+X5IT28/455Ks1dpv37YvaPs37Z1jv9Z+bpLdZ+eVSMNJcpckhyf5cfvdsaO/MzTfJXll+3fUmUk+m+QO/s6Y2wxapAElWRN4H/B4YGtgcZKtZ7cqaZW6DnhVVW0FPAx4cfuZfx3w3araAvhu24bus7FFezwfeD90wQzwJmAH4KHAmyb+oS3NYS8Hzult/ydwSPtcXAE8t7U/F7iiqjYHDmn9aJ+lfYBtgMcB/9N+z0hz2buBb1bV3wDb0X1G/J2heSvJRsDLgEVV9UBgTbr/9vs7Yw4zaJGG9VDggqq6qKr+AhwGPHmWa5JWmar6RVWd0p7/nu4fzBvR/dx/vHX7OLBHe/5k4BPV+RFwlyT3BnYHvl1Vl1fVFcC36f6RIM1JSTYG/h74UNsO8Gjg8NZl9HMx8Xk5HNi19X8ycFhV/bmqlgMX0P2ekeakJOsBjwQ+DFBVf6mq3+HvDGkBcMckC4C1gV/g74w5zaBFGtZGwM9625e0Nmm114auPhg4EbhnVf0CujAGuEfrNtlnxM+OVjfvAl4D3NC27wr8rqqua9v9n/G//vy3/Ve2/n4utLq5P/Ab4KNtWt2HkqyDvzM0j1XVz4GDgZ/SBSxXAkvxd8acZtAiDStj2ry1l1Z7SdYFjgBeUVVXTdV1TFtN0S7NOUmeCPy6qpb2m8d0rWn2+bnQ6mYBsD3w/qp6MPAHbpwmNI6fDa322rS3JwP3AzYE1qGbNjfK3xlziEGLNKxLgPv0tjcGLp2lWqRbRZLb0YUsn66qL7bmX7Xh3bSvv27tk31G/OxodbIz8A9JLqabQvpouhEud2nDwuGmP+N//flv++8MXI6fC61+LgEuqaoT2/bhdMGLvzM0nz0GWF5Vv6mqa4EvAjvh74w5zaBFGtbJwBZtlfC16Bak+sos1yStMm1O8IeBc6rqnb1dXwEm7gLxLODLvfZntjtJPAy4sg0TPwrYLcn67f/s7NbapDmnqvarqo2ralO63wNHV9XTge8Be7Vuo5+Lic/LXq1/tfZ92h0m7ke3IOhJt9LLkAZXVb8EfpZky9a0K3A2/s7Q/PZT4GFJ1m7/rpr4XPg7Yw5bMH0XSTNVVdcleQndL/s1gY9U1VmzXJa0Ku0MPAM4I8my1vZ64EDg80meS/cPiKe2fd8AnkC3QNs1wHMAquryJP9BF1YCvLmq/v/27jxar6o+4/j3AWSQxKCAMpSKiNQSZBaxFQgy1ZIKMmjRJSsySSss6CLKqKIgrRArXbJsgTayGCxgiAiBiIIkUlwMISCBUoZCEDAYAjIEMhD49Y/ffuHNyTn3vu+9b+5N0uez1l5v7jn77LPPPvu8N3vfvfd5YWguwWzInAxcKels4F7KgqDl8zJJj5F/lfxbgIh4UNLV5H+4lwBfiYg3hj7bZj11PHBF+YPU4+TvgdXw7wz7fyoi7pQ0CZhJftffC1wE3IB/Z6y0lJ1fZmZmZmZmZmY2WJ46ZGZmZmZmZmbWI+5oMTMzMzMzMzPrEXe0mJmZmZmZmZn1iDtazMzMzMzMzMx6xB0tZmZmZmZmZmY94o4WMzMzWy4kjZUUksYPd156SdIMSfOHOx8rghWtLCQdV+rcIcOdF+uMpHmSHhjufJiZ9ZI7WszMzFZwpeHYTRg3wPNMKMfv3ONL6PT8Yzu4tkE16iWNKOlM6VW+rXOlY6a/e9zzjjk35juzPJ6PFa0zzsxsKKwx3BkwMzOzfn2rZtuJwCjgX4AXK/vuW+45Wr4eBX7csG/xUGakwcHAWsOdiZXcxcDvG/b9ZhDpXg7cDDwziDRsaO0KvDHcmTAz6yV3tJiZma3gIuLM6rYyamUUcH5EzB7iLC1vj9Rd84oiIp4c7jysAi6KiBm9TjQiXmTZjkdbgUXEY8OdBzOzXvPUITMzs1WYpK0l/VjSHEmLJT0taaKkzSvx5gEnlR/vrpuqU9I6T9LMMhVjkaQnJP1Q0kZDd1VL5XuGpPmS1pR0pqTHS76elHSWpDXa4h4HvFJ+3L9uuoqkbcrPF0gaLWmypOckvdmaUtXXVAhJn5b0C0kvlHw8KukcSSNq4u4saVLJ6yJJc0vaEzq8dkk6RtLPyn1YIOlFSdMlHTrY8qocN07SfZIWSnq21KENO8nnQElaR9IsSW9I2rtm/+Ryr05s27bUGi2t6WjA+sDoyj2/oO24vSRNlfRMKY85km6XdHKHeX1rPSJJYyRNk/SKpJckTZG0bcNxa0o6QdLdJf5r5R4dXRO337rZT1mOL/fwRUmvljozWdLurbKj/+ej4zrXyi+wE7BuJb0pbfFqp3VJeqekb0h6sJznJUm3Sjqgn7LZStI1ymdwgaQ7JO3TV/mYmfWaR7SYmZmtoiTtBkwF1gF+Sk7JGQ18CThA0piImFWinwscCHycpad1tE/V+TxwBDAN+DU53H9b4FiyYbZzRDy3PK+pgYDJwPbAz4FXgb8BzgDWA44v8e4C/hE4lWWnJ1Wnq4wG7iSnYV0GjCzpNmdCOhf4KjAXuA54jmxkngrsJ2m3iHitxP0YcBuwqMR9suR1K+AEoJN1SlYHLizXdSvwB2BDYCxwtaRTIuK7dVmls/JqXdfXgW8DzwMTgfnA/iX/y01ELJD0OeBu4DJJ20XE3JKn44HPANdHxPl9JPMIOfXuayXfP2zbd1dJ62BgEnl91wHPAhsAWwNfBurKsMkYso7dCPwA+DD5XI2RtGdE3N2KKGkdsvx3Bx4k69nrwN7ARZJ2iohja87Rdd0EriLv8b3AJWS927Sc+5Pk89zJ89FNnZtLlv0xZHme05beI31ltpTNrcAuwCyyLN8FHApcK+n0iDin5tCtyLJ5sFzne4HPAjdK+kRE3NnXec3MeiYiHBwcHBwcHFayAMwGAti8Yf8abXEOqOw7smy/p7J9Qtm+c0OamwFr1mw/sBx3XmX72LJ9fIfX1Ir/CHBmQziocsyMcsztwKi27e8CniYblOu1bR9R4k9pyMM2ZX8ApzfEmQHMb8j7LcDIyr7jyr6z2rZdWLbtVZP+Bh2Wl4AtaravQzaMFwDrD7K8/hxYQnY+bFKpX1NLWvM7yW/l/Bf1cY/fUznmiHLMTeWadwAWAk/VxG2V9SGV7fOABxrydFM5ZstB3IvW/Q9gXGXfF8r23zY8b/8ErFYp2/+s1o9O6mZD3jYux0wHVFOH1m/7ub/nY6B1rrGO1N0b4DslH5OA1du2bwrMITt5t28om/GVtA4u26/utMwcHBwcBhs8dcjMzGzVtBfwfuCXEfGz9h0R8R/kX7Z3lLRjpwlGxFMRscxitBFxLfAEsN/gsvyWDwHfbAgHNRxzUkS81Janl8m/4q9Jjtzo1myyAdypE8rnkRHxSvuOiLgAeIxscFctqG6IiHmdnDDS4zXbFwD/BqwN7NFweKfldTg5iuF7EfH7tvhLyNE7A3U0zff4PZXrmQhcAewLnFXyuQZwWES8MIg8LHUasvNm6Y0d3os290fEJZU0riA7G7aVtBPklCFyJNjjwGkR8WZb/CW8PaKprs7Mpru62bIoIqKSt4iI5ztNYJB1rhtHkB18J0XEWwvlRsQzlI6pEqfqIeB7lbxdQ45W2qUH+TIz64inDpmZma2aWh0ov2rYfys5MmAHYGYnCUpaDRgHfBH4CDnNZPW2KL1q9N4QEWO7iP8m2XFU9VT5fPcA8jCzvYHXgY+T0zfGSWqK8wFJa0XEInLEwtHATZJ+Qo6E+U1EPNFNJiV9kJwWsyfwJ+TIgnab1hzWTXm16tH0auSIeEDS82Tjulsfje4Wwz2WbCifXn4+PSL+awDnrdPqxLlP0lXks3F7RMwZQFrLlFPb9p3J5+0ecsrdumRH2zca6swSckRRVVd1MyLmSLoV2EfSDHIa4W3AXRGxTOdSfwZY57pJf2NgI+DhqF94uvWdtkPNvpnVzqTiaeADg8mXmVk33NFiZma2ahpVPpsai63t63WR5oXAUWSj5UZyHZdWQ+0YcvrJcFhQOi+qlpTP1Wv29efZTiNKWotsNEOOyOjLCHJkwTRJnwROJte++VJJ60Hg6xHx0w7OuzU5XWMEuW7OVOBlclrFVsBh1L+GupvyatWjPzRk41lg8/7yOlgRMV/STeRop4VkXexV2pcqFzc+kVyT5e8BJN0BnBIRTZ0ndfoqJ3i7PNcvn6NLaLLMIsp0UTfbfBo4DfgccHbZ9pqkK4GvdjoyaBB1rhuD+e5qeuPUEgb2PWBmNiDuaDEzM1s1taaFNL0NaONKvD4p31J0FLkw6R5lqkD7/mXekrKSq/ureH3EiEWSFgFzI+JPuzhuGjBN0trAR4G/Br4CTCoL51YX6K36GtkoPTQiJrXvKPfjsE7z0odW/XgfuWBv1ZC8bUrSvmTZzCMXVr2Y5mlkXYuIycBkSSOBXcmOiS+Ti6h+pG66TIP3NWxvldNLlc/LIuLwbrPbZXwiYj7Z0XKapPeT03uOJKffbAJ8qsOkhrLO9eS7y8xsOHiNFjMzs1VTa2rImIb9re3t04Za0xHq/vK7ZfmcWtPJ8iGysbYy6OsaB+MOYDNVXpvdiYhYGBG3RcSp5AiX1cg3xPRnS3Ia0LU1+3qxTga8XT+WSU/SNrw9MmO5Ub46/DJyatZfkNf7mfI64k69QQf3PCJeiYhfRsTxwPeBdwLdvBp494btrfJrPZe/JacN/WWZkjdkIuLJiLiUXMfpGWDf8pYf6P/5GEid66js2/I3hxy180FJm9VE2bN8djTl0cxsOLijxczMbNV0M/A74K8kLfXXaknjyLU37ouI9sZKa1HMulEZs8vn7mpbUELSKPINMiuF0km0gPprHIx/Lp8TJb23ulPSSEm7tP08poyeqGqNiHitg3POJv8vt1vlXAeS05F64VKyoXySpLc60yStAZzXo3M0Kp0Ql5Ov6f27iHiUHIXxO2CCpLp1Ouo8D2ws6R0159inTP+q6uZetGxXnq/29L9Ars9yf0TcA0stHrsFeR3LnF/SZpL+rItz15K0ScOi1yPJKW+LKR0sHTwfs+m+zj0PrC1pwy6y/SPgHcB32zuiSh08hRzV86Mu0jMzG1KeOmRmZrYKioglkg4n11C4XtJk8s03o8nREn8kF7Zt11pk8vulU+AlYHFEnBsRj0maQr7G9h5JvyLfDrMfOZ3jf8jXP/fCVpLO7GP/uRHRTeO36hZgrKRrgFnk+g03R8QdA00wIq6TdDZwBvCYpJ+Tb2J6F7mGyR7kujaHlEPOAHYti5Q+QTZutyXL8zlgYgen/QG55sYNZUHducB2wN7AT4DPDvR62q7rIUnfBr4F3C/pamA+sD/5/8iHyQVRu3WMpKYFj++KiBvLv08jR15cGhGXlzz9UdLnyTVCrpK0Y5ka05dbyFc/T5V0O/A6cHdE3AT8K/BuSdPJjoQ3gI+RnQmPkIvHdupG4OLS8fDfwIfJ15+/Sk69a3cq+VrifwAOkjSNXH9kI3K9k13Jt1k93MX562wB3CZpFnAfOYplPfJ7YD3gnMrbxPp6PgZS524hpybdIOkX5Bo7j0bEVX3k+WxyJNFhwNZlfZ6RJf31gW9GRN2CzmZmK4ZevSfawcHBwcHBYegC2SAMYPN+4m0DXEku0rmYbGRdAmzREP8osnG1sKQ/v23fSHIUw/+W/U8C55NrNsxoj1vijy1pjO/wmlrx+wsbtB2zzHnb9h1X4h9S2b4p2Sh8jmxUv5XHUl4BXNBHPvs6557AZHLqw2KyITqzlNv2lWu9lOygepnsvHiIHBmzaRf1YAzwa3IR0JfJt9t8qqnsB1JeZd84crrLwlKXJpKjTBrT66Ps+ru/F5S4nyAb+Q8DI2rSOq3Ev7yDez4K+HdyAecllfN8Ebia7IicT3YwzqK8arrLuju+3JNpwCvlntwAbNdwXOs1xdPIzs/F5GLT08lpZBtXnuU+62bDOTYgO8qml+tfVD5vabjXjc/HAOvcmsAE8vvi9RJnStv+ecADNflYFziTfC4Wtp3roJq4fZZNt/XUwcHBYbBBEV2vp2VmZmZmZkUZnXM9+QafCcOdHzMzG15eo8XMzMzMzMzMrEfc0WJmZmZmZmZm1iPuaDEzMzMzMzMz6xGv0WJmZmZmZmZm1iMe0WJmZmZmZmZm1iPuaDEzMzMzMzMz6xF3tJiZmZmZmZmZ9Yg7WszMzMzMzMzMesQdLWZmZmZmZmZmPeKOFjMzMzMzMzOzHvk/j2syFF720+YAAAAASUVORK5CYII=\n",
      "text/plain": [
       "<Figure size 1152x720 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "plt.figure(figsize = [16,10])\n",
    "sns.barplot(x = 'Total_Traffic', y = 'Unique_Station', data = top_unique_stations)\n",
    "plt.title('Top NYC Stations for the months of April, May, and June of 2019', fontsize = 20)\n",
    "plt.xlabel('Total Entries and Exits per station', fontsize = 20)\n",
    "plt.ylabel('NYC Stations', fontsize = 20);\n",
    "plt.savefig('Overall TOP NYC Stations.png', bbox_inches = 'tight')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Let's see the top stations for weekdays versuys weekends"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 35,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Unique_Station</th>\n",
       "      <th>Total_Traffic</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>90</th>\n",
       "      <td>34 ST-HERALD SQ_BDFMNQRW</td>\n",
       "      <td>1888.076508</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>312</th>\n",
       "      <td>GRD CNTRL-42 ST_4567S</td>\n",
       "      <td>1744.849685</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>94</th>\n",
       "      <td>34 ST-PENN STA_ACE</td>\n",
       "      <td>1708.066607</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>103</th>\n",
       "      <td>42 ST-PORT AUTH_ACENQRS1237W</td>\n",
       "      <td>1465.750675</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>448</th>\n",
       "      <td>TIMES SQ-42 ST_1237ACENQRSW</td>\n",
       "      <td>1181.265527</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>235</th>\n",
       "      <td>CANAL ST_JNQRZ6W</td>\n",
       "      <td>1135.490549</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>339</th>\n",
       "      <td>JKSN HT-ROOSVLT_EFMR7</td>\n",
       "      <td>1097.246625</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>25</th>\n",
       "      <td>14 ST-UNION SQ_LNQR456W</td>\n",
       "      <td>1083.328533</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>123</th>\n",
       "      <td>59 ST COLUMBUS_ABCD1</td>\n",
       "      <td>1061.417642</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>93</th>\n",
       "      <td>34 ST-PENN STA_123ACE</td>\n",
       "      <td>987.854185</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                   Unique_Station  Total_Traffic\n",
       "90       34 ST-HERALD SQ_BDFMNQRW    1888.076508\n",
       "312         GRD CNTRL-42 ST_4567S    1744.849685\n",
       "94             34 ST-PENN STA_ACE    1708.066607\n",
       "103  42 ST-PORT AUTH_ACENQRS1237W    1465.750675\n",
       "448   TIMES SQ-42 ST_1237ACENQRSW    1181.265527\n",
       "235              CANAL ST_JNQRZ6W    1135.490549\n",
       "339         JKSN HT-ROOSVLT_EFMR7    1097.246625\n",
       "25        14 ST-UNION SQ_LNQR456W    1083.328533\n",
       "123          59 ST COLUMBUS_ABCD1    1061.417642\n",
       "93          34 ST-PENN STA_123ACE     987.854185"
      ]
     },
     "execution_count": 35,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# WEEKENDS\n",
    "top = 10 # filter to top stations\n",
    "weekends = summer19_MTA_cleaned[summer19_MTA_cleaned['WEEKEND'] == 'WEEKEND']\n",
    "\n",
    "top_unique_stations_weekends = (weekends.groupby(['Unique_Station'])\n",
    "                       .sum()\n",
    "                       .reset_index()\n",
    "                       .sort_values(by = 'Total_Traffic', ascending = False)\n",
    "                       .head(top))\n",
    "#top_unique_stations\n",
    "top_unique_stations_weekends[['Unique_Station', 'Total_Traffic']]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 36,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 1152x720 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "plt.figure(figsize = [16,10])\n",
    "sns.barplot(x = 'Total_Traffic', y = 'Unique_Station', data = top_unique_stations_weekends)\n",
    "plt.title('Top NYC Stations for the months of April, May, and June of 2019 (WEEKENDS)', fontsize = 20)\n",
    "plt.xlabel('Total Entries and Exits per station', fontsize = 20)\n",
    "plt.ylabel('NYC Stations', fontsize = 20);\n",
    "plt.savefig('TOP NYC Stations on Weekends.png', bbox_inches = 'tight')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 37,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Unique_Station</th>\n",
       "      <th>Total_Traffic</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>94</th>\n",
       "      <td>34 ST-PENN STA_ACE</td>\n",
       "      <td>6868.710171</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>302</th>\n",
       "      <td>FULTON ST_2345ACJZ</td>\n",
       "      <td>6367.778578</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>312</th>\n",
       "      <td>GRD CNTRL-42 ST_4567S</td>\n",
       "      <td>6191.954095</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>90</th>\n",
       "      <td>34 ST-HERALD SQ_BDFMNQRW</td>\n",
       "      <td>5423.907291</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>103</th>\n",
       "      <td>42 ST-PORT AUTH_ACENQRS1237W</td>\n",
       "      <td>4119.900090</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>289</th>\n",
       "      <td>FLUSHING-MAIN_7</td>\n",
       "      <td>3885.751575</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>448</th>\n",
       "      <td>TIMES SQ-42 ST_1237ACENQRSW</td>\n",
       "      <td>3819.900990</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>404</th>\n",
       "      <td>PATH NEW WTC_1</td>\n",
       "      <td>3751.805581</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>235</th>\n",
       "      <td>CANAL ST_JNQRZ6W</td>\n",
       "      <td>3480.602160</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>124</th>\n",
       "      <td>59 ST_456NQRW</td>\n",
       "      <td>3258.932493</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                   Unique_Station  Total_Traffic\n",
       "94             34 ST-PENN STA_ACE    6868.710171\n",
       "302            FULTON ST_2345ACJZ    6367.778578\n",
       "312         GRD CNTRL-42 ST_4567S    6191.954095\n",
       "90       34 ST-HERALD SQ_BDFMNQRW    5423.907291\n",
       "103  42 ST-PORT AUTH_ACENQRS1237W    4119.900090\n",
       "289               FLUSHING-MAIN_7    3885.751575\n",
       "448   TIMES SQ-42 ST_1237ACENQRSW    3819.900990\n",
       "404                PATH NEW WTC_1    3751.805581\n",
       "235              CANAL ST_JNQRZ6W    3480.602160\n",
       "124                 59 ST_456NQRW    3258.932493"
      ]
     },
     "execution_count": 37,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# WEEKDAYS\n",
    "top = 10 # filter to top stations\n",
    "weekdays = summer19_MTA_cleaned[summer19_MTA_cleaned['WEEKEND'] == 'WEEKDAY']\n",
    "\n",
    "top_unique_stations_weekdays = (weekdays.groupby(['Unique_Station'])\n",
    "                       .sum()\n",
    "                       .reset_index()\n",
    "                       .sort_values(by = 'Total_Traffic', ascending = False)\n",
    "                       .head(top))\n",
    "#top_unique_stations\n",
    "top_unique_stations_weekdays[['Unique_Station', 'Total_Traffic']]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 136,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 1152x1152 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "plt.figure(figsize = [16,16])\n",
    "sns.barplot(x = 'Total_Traffic', y = 'Unique_Station', data = top_unique_stations_weekdays)\n",
    "plt.title('Top NYC Stations for the months of April, May, and June of 2019 (WEEKDAYS)', fontsize = 20)\n",
    "plt.xlabel('Total Entries and Exits per station', fontsize = 20)\n",
    "plt.ylabel('NYC Stations', fontsize = 20);\n",
    "plt.savefig('Top NYC Stations Weekdays.png', bbox_inches = 'tight')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Let's examine the trend of total traffic throughout the week"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 39,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>ENTRIES</th>\n",
       "      <th>EXITS</th>\n",
       "      <th>ENTRIES DIFF</th>\n",
       "      <th>EXITS DIFF</th>\n",
       "      <th>Total_Traffic</th>\n",
       "      <th>TIME_INT</th>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>DAY_OF_WEEK</th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>Friday</th>\n",
       "      <td>9110407454713</td>\n",
       "      <td>7041622732793</td>\n",
       "      <td>58232711.0</td>\n",
       "      <td>43018708.0</td>\n",
       "      <td>90851.060306</td>\n",
       "      <td>3915300</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Monday</th>\n",
       "      <td>9164587769941</td>\n",
       "      <td>7107276277123</td>\n",
       "      <td>53643256.0</td>\n",
       "      <td>39778304.0</td>\n",
       "      <td>83805.571557</td>\n",
       "      <td>3901970</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Saturday</th>\n",
       "      <td>7575870411015</td>\n",
       "      <td>5855446366739</td>\n",
       "      <td>33453313.0</td>\n",
       "      <td>26198029.0</td>\n",
       "      <td>53458.659766</td>\n",
       "      <td>3224421</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Sunday</th>\n",
       "      <td>9136449754706</td>\n",
       "      <td>7124205641417</td>\n",
       "      <td>32774647.0</td>\n",
       "      <td>27370014.0</td>\n",
       "      <td>53855.558956</td>\n",
       "      <td>3936769</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Thursday</th>\n",
       "      <td>8919831949247</td>\n",
       "      <td>6940603077978</td>\n",
       "      <td>58226326.0</td>\n",
       "      <td>42998915.0</td>\n",
       "      <td>90832.471647</td>\n",
       "      <td>3842948</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Tuesday</th>\n",
       "      <td>9102669064148</td>\n",
       "      <td>7098131270579</td>\n",
       "      <td>57208242.0</td>\n",
       "      <td>42208177.0</td>\n",
       "      <td>89201.938794</td>\n",
       "      <td>3889080</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Wednesday</th>\n",
       "      <td>9033961015501</td>\n",
       "      <td>7025969326268</td>\n",
       "      <td>58379814.0</td>\n",
       "      <td>43297221.0</td>\n",
       "      <td>91237.007201</td>\n",
       "      <td>3876883</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                   ENTRIES          EXITS  ENTRIES DIFF  EXITS DIFF  \\\n",
       "DAY_OF_WEEK                                                           \n",
       "Friday       9110407454713  7041622732793    58232711.0  43018708.0   \n",
       "Monday       9164587769941  7107276277123    53643256.0  39778304.0   \n",
       "Saturday     7575870411015  5855446366739    33453313.0  26198029.0   \n",
       "Sunday       9136449754706  7124205641417    32774647.0  27370014.0   \n",
       "Thursday     8919831949247  6940603077978    58226326.0  42998915.0   \n",
       "Tuesday      9102669064148  7098131270579    57208242.0  42208177.0   \n",
       "Wednesday    9033961015501  7025969326268    58379814.0  43297221.0   \n",
       "\n",
       "             Total_Traffic  TIME_INT  \n",
       "DAY_OF_WEEK                           \n",
       "Friday        90851.060306   3915300  \n",
       "Monday        83805.571557   3901970  \n",
       "Saturday      53458.659766   3224421  \n",
       "Sunday        53855.558956   3936769  \n",
       "Thursday      90832.471647   3842948  \n",
       "Tuesday       89201.938794   3889080  \n",
       "Wednesday     91237.007201   3876883  "
      ]
     },
     "execution_count": 39,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "total_traffic_per_week = summer19_MTA_cleaned.groupby('DAY_OF_WEEK').sum()\n",
    "total_traffic_per_week.sort_index()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 40,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 720x720 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "plt.figure(figsize = [10,10])\n",
    "sns.lineplot(x = total_traffic_per_week.index , \n",
    "             y = total_traffic_per_week.Total_Traffic, \n",
    "             data = total_traffic_per_week.sort_values(by = 'Total_Traffic'));\n",
    "plt.xlabel('Day of the Week', size = 20)\n",
    "plt.ylabel('Total Traffic', size = 20)\n",
    "plt.title('Total Traffic by Day of the week', size = 20);\n",
    "plt.savefig('Traffic by Day of the Week.png')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "We see the total traffic dramatically decreases over the Saturday and Sunday period."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Now let's examine the total traffic per time slot"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 41,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>C/A</th>\n",
       "      <th>UNIT</th>\n",
       "      <th>SCP</th>\n",
       "      <th>STATION</th>\n",
       "      <th>LINENAME</th>\n",
       "      <th>DIVISION</th>\n",
       "      <th>DATE</th>\n",
       "      <th>TIME</th>\n",
       "      <th>DESC</th>\n",
       "      <th>ENTRIES</th>\n",
       "      <th>EXITS</th>\n",
       "      <th>Unique_Station</th>\n",
       "      <th>ENTRIES DIFF</th>\n",
       "      <th>EXITS DIFF</th>\n",
       "      <th>Total_Traffic</th>\n",
       "      <th>DAY_OF_WEEK</th>\n",
       "      <th>TIME_INT</th>\n",
       "      <th>TIME_OF_DAY</th>\n",
       "      <th>WEEKEND</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>A002</td>\n",
       "      <td>R051</td>\n",
       "      <td>02-00-00</td>\n",
       "      <td>59 ST</td>\n",
       "      <td>NQR456W</td>\n",
       "      <td>BMT</td>\n",
       "      <td>03/30/2019</td>\n",
       "      <td>04:00:00</td>\n",
       "      <td>REGULAR</td>\n",
       "      <td>6999084</td>\n",
       "      <td>2373576</td>\n",
       "      <td>59 ST_NQR456W</td>\n",
       "      <td>20.0</td>\n",
       "      <td>8.0</td>\n",
       "      <td>0.024302</td>\n",
       "      <td>Saturday</td>\n",
       "      <td>4</td>\n",
       "      <td>Midnight-4AM</td>\n",
       "      <td>WEEKEND</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>A002</td>\n",
       "      <td>R051</td>\n",
       "      <td>02-00-00</td>\n",
       "      <td>59 ST</td>\n",
       "      <td>NQR456W</td>\n",
       "      <td>BMT</td>\n",
       "      <td>03/30/2019</td>\n",
       "      <td>08:00:00</td>\n",
       "      <td>REGULAR</td>\n",
       "      <td>6999107</td>\n",
       "      <td>2373622</td>\n",
       "      <td>59 ST_NQR456W</td>\n",
       "      <td>23.0</td>\n",
       "      <td>46.0</td>\n",
       "      <td>0.061206</td>\n",
       "      <td>Saturday</td>\n",
       "      <td>8</td>\n",
       "      <td>4AM-8AM</td>\n",
       "      <td>WEEKEND</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>A002</td>\n",
       "      <td>R051</td>\n",
       "      <td>02-00-00</td>\n",
       "      <td>59 ST</td>\n",
       "      <td>NQR456W</td>\n",
       "      <td>BMT</td>\n",
       "      <td>03/30/2019</td>\n",
       "      <td>12:00:00</td>\n",
       "      <td>REGULAR</td>\n",
       "      <td>6999214</td>\n",
       "      <td>2373710</td>\n",
       "      <td>59 ST_NQR456W</td>\n",
       "      <td>107.0</td>\n",
       "      <td>88.0</td>\n",
       "      <td>0.174617</td>\n",
       "      <td>Saturday</td>\n",
       "      <td>12</td>\n",
       "      <td>8AM-Noon</td>\n",
       "      <td>WEEKEND</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>A002</td>\n",
       "      <td>R051</td>\n",
       "      <td>02-00-00</td>\n",
       "      <td>59 ST</td>\n",
       "      <td>NQR456W</td>\n",
       "      <td>BMT</td>\n",
       "      <td>03/30/2019</td>\n",
       "      <td>16:00:00</td>\n",
       "      <td>REGULAR</td>\n",
       "      <td>6999451</td>\n",
       "      <td>2373781</td>\n",
       "      <td>59 ST_NQR456W</td>\n",
       "      <td>237.0</td>\n",
       "      <td>71.0</td>\n",
       "      <td>0.276328</td>\n",
       "      <td>Saturday</td>\n",
       "      <td>16</td>\n",
       "      <td>Noon-4PM</td>\n",
       "      <td>WEEKEND</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>5</th>\n",
       "      <td>A002</td>\n",
       "      <td>R051</td>\n",
       "      <td>02-00-00</td>\n",
       "      <td>59 ST</td>\n",
       "      <td>NQR456W</td>\n",
       "      <td>BMT</td>\n",
       "      <td>03/30/2019</td>\n",
       "      <td>20:00:00</td>\n",
       "      <td>REGULAR</td>\n",
       "      <td>6999796</td>\n",
       "      <td>2373837</td>\n",
       "      <td>59 ST_NQR456W</td>\n",
       "      <td>345.0</td>\n",
       "      <td>56.0</td>\n",
       "      <td>0.360036</td>\n",
       "      <td>Saturday</td>\n",
       "      <td>20</td>\n",
       "      <td>4PM-8PM</td>\n",
       "      <td>WEEKEND</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "    C/A  UNIT       SCP STATION LINENAME DIVISION        DATE      TIME  \\\n",
       "1  A002  R051  02-00-00   59 ST  NQR456W      BMT  03/30/2019  04:00:00   \n",
       "2  A002  R051  02-00-00   59 ST  NQR456W      BMT  03/30/2019  08:00:00   \n",
       "3  A002  R051  02-00-00   59 ST  NQR456W      BMT  03/30/2019  12:00:00   \n",
       "4  A002  R051  02-00-00   59 ST  NQR456W      BMT  03/30/2019  16:00:00   \n",
       "5  A002  R051  02-00-00   59 ST  NQR456W      BMT  03/30/2019  20:00:00   \n",
       "\n",
       "      DESC  ENTRIES    EXITS Unique_Station  ENTRIES DIFF  EXITS DIFF  \\\n",
       "1  REGULAR  6999084  2373576  59 ST_NQR456W          20.0         8.0   \n",
       "2  REGULAR  6999107  2373622  59 ST_NQR456W          23.0        46.0   \n",
       "3  REGULAR  6999214  2373710  59 ST_NQR456W         107.0        88.0   \n",
       "4  REGULAR  6999451  2373781  59 ST_NQR456W         237.0        71.0   \n",
       "5  REGULAR  6999796  2373837  59 ST_NQR456W         345.0        56.0   \n",
       "\n",
       "   Total_Traffic DAY_OF_WEEK  TIME_INT   TIME_OF_DAY  WEEKEND  \n",
       "1       0.024302    Saturday         4  Midnight-4AM  WEEKEND  \n",
       "2       0.061206    Saturday         8       4AM-8AM  WEEKEND  \n",
       "3       0.174617    Saturday        12      8AM-Noon  WEEKEND  \n",
       "4       0.276328    Saturday        16      Noon-4PM  WEEKEND  \n",
       "5       0.360036    Saturday        20       4PM-8PM  WEEKEND  "
      ]
     },
     "execution_count": 41,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "summer19_MTA_cleaned.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 138,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>ENTRIES</th>\n",
       "      <th>EXITS</th>\n",
       "      <th>ENTRIES DIFF</th>\n",
       "      <th>EXITS DIFF</th>\n",
       "      <th>Total_Traffic</th>\n",
       "      <th>TIME_INT</th>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>TIME_OF_DAY</th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>Midnight-4AM</th>\n",
       "      <td>10359709599031</td>\n",
       "      <td>8094865621635</td>\n",
       "      <td>15892845.0</td>\n",
       "      <td>16666860.0</td>\n",
       "      <td>28995.439244</td>\n",
       "      <td>973032</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4AM-8AM</th>\n",
       "      <td>11920298904913</td>\n",
       "      <td>9388816459917</td>\n",
       "      <td>35453281.0</td>\n",
       "      <td>22548278.0</td>\n",
       "      <td>51858.585059</td>\n",
       "      <td>2623818</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>8AM-Noon</th>\n",
       "      <td>10898662569650</td>\n",
       "      <td>8439194796158</td>\n",
       "      <td>80248377.0</td>\n",
       "      <td>55691165.0</td>\n",
       "      <td>122032.160216</td>\n",
       "      <td>3860278</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Noon-4PM</th>\n",
       "      <td>10489836850110</td>\n",
       "      <td>8154102819392</td>\n",
       "      <td>79801205.0</td>\n",
       "      <td>59405207.0</td>\n",
       "      <td>124964.670567</td>\n",
       "      <td>5456243</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4PM-8PM</th>\n",
       "      <td>8951575281510</td>\n",
       "      <td>6802211081851</td>\n",
       "      <td>85067950.0</td>\n",
       "      <td>61845144.0</td>\n",
       "      <td>131932.126913</td>\n",
       "      <td>6270559</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                     ENTRIES          EXITS  ENTRIES DIFF  EXITS DIFF  \\\n",
       "TIME_OF_DAY                                                             \n",
       "Midnight-4AM  10359709599031  8094865621635    15892845.0  16666860.0   \n",
       "4AM-8AM       11920298904913  9388816459917    35453281.0  22548278.0   \n",
       "8AM-Noon      10898662569650  8439194796158    80248377.0  55691165.0   \n",
       "Noon-4PM      10489836850110  8154102819392    79801205.0  59405207.0   \n",
       "4PM-8PM        8951575281510  6802211081851    85067950.0  61845144.0   \n",
       "\n",
       "              Total_Traffic  TIME_INT  \n",
       "TIME_OF_DAY                            \n",
       "Midnight-4AM   28995.439244    973032  \n",
       "4AM-8AM        51858.585059   2623818  \n",
       "8AM-Noon      122032.160216   3860278  \n",
       "Noon-4PM      124964.670567   5456243  \n",
       "4PM-8PM       131932.126913   6270559  "
      ]
     },
     "execution_count": 138,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "total_traffic_time_of_day = summer19_MTA_cleaned.groupby('TIME_OF_DAY').sum()\n",
    "total_traffic_time_of_day.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 148,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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hmCbaYfzeaGbbrp1vRtq5zT7vRaxTadv50R+n+FnF3oZn3Dbje+Rdcwh9r8+2P/5I3ge6s8r8laF7/0xD3/B4cRm9u+Pr5GzPnhclwPfwA8jbvJxPtq4g/0Pq51GC9p+TdxPR2+nfC64nz2N92P/1PLvNrN/z+D1Oz947e4N3k//wA/dSo2yzxn49s0W/OQQW/CfET8GxrXk/QYcF7zOy4Bjj+Q1oFvr3Sx4UkREpJWY2fH4Qne/cM7dFnY80vbMz1xRBCxyzk0PORwREekkzOxBfILkHOfc38OOp6U6a9wiXZFq6oiIHKFG45Trl2Wyfzz4M+0bkYTof/Fd3O871IYiIiIAZtYPP/x5Nb5nRafQWeMW6apUU0dE5Mj92MyOAd7Cd10diB+Dnw087Jx7s7mdpXMzs/74IXtDgWvx3dZnN7uTiIh0e2Z2MX5mzYuBZODbzrnWqMPXpjpr3CJdnZI6IiJH7ll8UcFz8HUBqvBFku9AU1p3B4Px48/34AsYfsG14qwlIiLSZX0GP2PiBuB251xnuSDQWeMW6dJUU0dEREREREREpBNST51m9O7d2+Xm5oYdhoiIiAALFizY7pzLDjuOrkLtHBERkY7jSNs5Suo0Izc3l8LCwrDDEBEREcDMisOOoStRO0dERKTjONJ2jma/EhERERERERHphJTUERERERERERHphJTUERERERERERHphJTUERERERERERHphJTUERERERERERHphJTUERERERERERHphJTUERERERERERHphJTUERERERERERHphJTUERERERERERHphJTUERERERERERHphJTUERERERERERHphJTUERERERERERHphJTUERERERERERHphJTUERGRbmFPdQ1vrdrO4/PWsq+2LuxwRERERKST2Fdbx+J1O/ntf1bz3vqdYYdzgLiwAxAREWkL5ZX7WFBUytw1Jcxbs4P31pdRU+cAKNq+m6+fNSbkCEVERESkIyqv3MfC4lIWFJcyv6iEd9eVsXdfLQBfOX0UEwdmhBzhfkrqiIhIl1Cyu5p5a0r8rWgH728sp85BfKwxcWAGnzthKAV5Wfxz2WZ+/eZqZgzN4pTRfcMOW0RERERCtmHnXgqLSigs8kmcD7ZU4BzExhhjc9K4ZPogpudmkZ+bSd+0pLDDPYCSOiIi0iltKa9s6IUzb00JK7fs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\n",
      "text/plain": [
       "<Figure size 1152x432 with 2 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "plt.figure(figsize = [16,6])\n",
    "\n",
    "plt.subplot(1,2,1)\n",
    "sns.lineplot(x = total_traffic_time_of_day.index, y = 'Total_Traffic', data = total_traffic_time_of_day);\n",
    "plt.title('Total Traffic throughout the day', size = 20);\n",
    "plt.ylabel('Total Cumulative Traffic', size = 15);\n",
    "plt.xlabel('Time of Day', size = 20);\n",
    "\n",
    "plt.subplot(1,2,2)\n",
    "sns.lineplot(x = total_traffic_per_week.index , \n",
    "             y = total_traffic_per_week.Total_Traffic, \n",
    "             data = total_traffic_per_week.sort_values(by = 'Total_Traffic'));\n",
    "plt.xlabel('Day of the Week', size = 20)\n",
    "plt.ylabel('Total Traffic', size = 15)\n",
    "plt.title('Total Traffic by Day of the week', size = 20);\n",
    "plt.savefig('Traffic by Time and Day.png', boxx_inches = 'tight')\n",
    "plt.tight_layout()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The busiest times of each days are earlying morning at 8AM all the way to evening time at 8PM."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 44,
   "metadata": {},
   "outputs": [],
   "source": [
    "group_names = ['Midnight-4AM', '4AM-8AM', '8AM-Noon', 'Noon-4PM', '4PM-8PM', '8PM-Midnight']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 45,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>TIME_OF_DAY</th>\n",
       "      <th>Monday</th>\n",
       "      <th>Tuesday</th>\n",
       "      <th>Wednesday</th>\n",
       "      <th>Thursday</th>\n",
       "      <th>Friday</th>\n",
       "      <th>Saturday</th>\n",
       "      <th>Sunday</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>Midnight-4AM</td>\n",
       "      <td>7642.663366</td>\n",
       "      <td>10497.593159</td>\n",
       "      <td>11710.711971</td>\n",
       "      <td>12032.320432</td>\n",
       "      <td>12442.480648</td>\n",
       "      <td>1866.626463</td>\n",
       "      <td>11617.001800</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>4AM-8AM</td>\n",
       "      <td>8791.835284</td>\n",
       "      <td>9388.177318</td>\n",
       "      <td>9721.990099</td>\n",
       "      <td>9224.481548</td>\n",
       "      <td>8974.081008</td>\n",
       "      <td>3335.212421</td>\n",
       "      <td>2422.807381</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>8AM-Noon</td>\n",
       "      <td>20029.055806</td>\n",
       "      <td>21198.774077</td>\n",
       "      <td>21104.288029</td>\n",
       "      <td>21021.487849</td>\n",
       "      <td>20757.111611</td>\n",
       "      <td>10277.581458</td>\n",
       "      <td>7643.861386</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>Noon-4PM</td>\n",
       "      <td>18767.312331</td>\n",
       "      <td>19306.466247</td>\n",
       "      <td>19571.265527</td>\n",
       "      <td>19497.684068</td>\n",
       "      <td>19633.885689</td>\n",
       "      <td>15207.855086</td>\n",
       "      <td>12980.201620</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>4PM-8PM</td>\n",
       "      <td>20171.088209</td>\n",
       "      <td>20323.807381</td>\n",
       "      <td>20294.375338</td>\n",
       "      <td>20377.250225</td>\n",
       "      <td>20542.225023</td>\n",
       "      <td>16302.918992</td>\n",
       "      <td>13920.461746</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>5</th>\n",
       "      <td>8PM-Midnight</td>\n",
       "      <td>8403.616562</td>\n",
       "      <td>8487.120612</td>\n",
       "      <td>8834.376238</td>\n",
       "      <td>8679.247525</td>\n",
       "      <td>8501.276328</td>\n",
       "      <td>6468.465347</td>\n",
       "      <td>5271.225023</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "    TIME_OF_DAY        Monday       Tuesday     Wednesday      Thursday  \\\n",
       "0  Midnight-4AM   7642.663366  10497.593159  11710.711971  12032.320432   \n",
       "1       4AM-8AM   8791.835284   9388.177318   9721.990099   9224.481548   \n",
       "2      8AM-Noon  20029.055806  21198.774077  21104.288029  21021.487849   \n",
       "3      Noon-4PM  18767.312331  19306.466247  19571.265527  19497.684068   \n",
       "4       4PM-8PM  20171.088209  20323.807381  20294.375338  20377.250225   \n",
       "5  8PM-Midnight   8403.616562   8487.120612   8834.376238   8679.247525   \n",
       "\n",
       "         Friday      Saturday        Sunday  \n",
       "0  12442.480648   1866.626463  11617.001800  \n",
       "1   8974.081008   3335.212421   2422.807381  \n",
       "2  20757.111611  10277.581458   7643.861386  \n",
       "3  19633.885689  15207.855086  12980.201620  \n",
       "4  20542.225023  16302.918992  13920.461746  \n",
       "5   8501.276328   6468.465347   5271.225023  "
      ]
     },
     "execution_count": 45,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "total_traffic_time_of_day = summer19_MTA_cleaned.groupby(['DAY_OF_WEEK', 'TIME_OF_DAY']).sum().reset_index()\n",
    "temp = total_traffic_time_of_day[['DAY_OF_WEEK', 'TIME_OF_DAY', 'Total_Traffic']]\n",
    "temp.head(50)\n",
    "\n",
    "# temp_cols = [['Friday', 'Monday', 'Saturday', 'Sunday', 'Sunday', 'Thursday', 'Tuesday', 'Wednesday']]\n",
    "heat_map_df = pd.DataFrame({'TIME_OF_DAY': group_names, \n",
    "                            'Monday': temp.iloc[6:12]['Total_Traffic'].values,\n",
    "                            'Tuesday': temp.iloc[30:36]['Total_Traffic'].values,\n",
    "                            'Wednesday': temp.iloc[36:42]['Total_Traffic'].values,\n",
    "                            'Thursday': temp.iloc[24:30]['Total_Traffic'].values,\n",
    "                            'Friday': temp.iloc[0:6]['Total_Traffic'].values,\n",
    "                            'Saturday': temp.iloc[12:18]['Total_Traffic'].values,\n",
    "                            'Sunday': temp.iloc[18:24]['Total_Traffic'].values\n",
    "                           })\n",
    "heat_map_df"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Heatmap comparing the Time of Day and Day of the Week."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 47,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 1152x1152 with 2 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "heat_map_ready = heat_map_df.set_index('TIME_OF_DAY')\n",
    "plt.figure(figsize = [16,16])\n",
    "chart = sns.heatmap(heat_map_ready, cmap = 'seismic', square = True,cbar_kws={\"shrink\": .70});\n",
    "plt.title('Total Traffic (Day vs Time) Heat Map', size = 20); \n",
    "plt.xlabel('Day of the Week', size = 15);\n",
    "plt.ylabel('Time of the Day', size = 15);\n",
    "chart.set_yticklabels(chart.get_yticklabels(), rotation = 0);\n",
    "plt.ylim([6, 0]);\n",
    "plt.savefig('Time and Day Traffic HeatMap.png', bbox_inches = 'tight');\n",
    "# sns.despine()\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Convincingly, we will recommend weekdays to be the best time to promote the WTWY Gala"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 51,
   "metadata": {},
   "outputs": [],
   "source": [
    "def top_station_barplot(x, y, data, title, xlabel, labelsize):\n",
    "    plt.figure(figsize = [16, 10])\n",
    "    sns.barplot(x = x, y = y, data = data)\n",
    "    plt.title(title, size = labelsize)\n",
    "    plt.xlabel(xlabel, size = labelsize)\n",
    "    plt.ylabel('Total Traffic', size = labelsize)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Let's examine the best stations to target throughout Monday through Friday."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 52,
   "metadata": {},
   "outputs": [],
   "source": [
    "def day_df(DAY_OF_WEEK, top):\n",
    "    \n",
    "    '''\n",
    "    Takes the day of the week as an argument\n",
    "    Returns a dataframe from summer19_MTA_cleaned that is filtered by the argument\n",
    "    \n",
    "    '''\n",
    "    \n",
    "    mask = summer19_MTA_cleaned['DAY_OF_WEEK'] == DAY_OF_WEEK\n",
    "    top_stations = (summer19_MTA_cleaned[mask].groupby('Unique_Station')\n",
    "                       .sum()\n",
    "                       .sort_values(by = 'Total_Traffic', ascending = False))\n",
    "    \n",
    "    return top_stations.head(top)\n",
    "    "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 53,
   "metadata": {},
   "outputs": [],
   "source": [
    "top_stations_monday = day_df('Monday', top = 5)\n",
    "top_stations_tuesday = day_df('Tuesday', top = 5)\n",
    "top_stations_wednesday = day_df('Wednesday', top = 5)\n",
    "top_stations_thursday = day_df('Thursday', top = 5)\n",
    "top_stations_friday = day_df('Friday', top = 5)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 61,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'34 ST-PENN STA_ACE'"
      ]
     },
     "execution_count": 61,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "top_stations_monday.index[0]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 131,
   "metadata": {},
   "outputs": [],
   "source": [
    "def top_station_barplot(x, y, data, title, xlabel, ylabel, labelsize, palette = 'husl'):\n",
    "    '''\n",
    "    Takes the the values of x and y from the dataframe data\n",
    "    Returns a barplot with title, xlabel and labelsize\n",
    "    '''\n",
    "    sns.barplot(x = x, y = y, data = data, palette = palette)\n",
    "    plt.title(title, size = labelsize)\n",
    "    plt.xlabel(xlabel, size = labelsize)\n",
    "    plt.ylabel(ylabel, size = labelsize)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Let's plot all the top stations from Monday through Friday"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 127,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "['34 ST-PENN STA_ACE',\n",
       " 'FULTON ST_2345ACJZ',\n",
       " 'GRD CNTRL-42 ST_4567S',\n",
       " '34 ST-HERALD SQ_BDFMNQRW',\n",
       " '42 ST-PORT AUTH_ACENQRS1237W',\n",
       " 'PATH NEW WTC_1']"
      ]
     },
     "execution_count": 127,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "list(top_stations_monday.index) + list(['PATH NEW WTC_1'])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 132,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 1440x864 with 5 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "plt.figure(figsize = [20,12])\n",
    "\n",
    "top_stations = list(top_stations_monday.index) + list(['PATH NEW WTC_1'])\n",
    "\n",
    "colors_mon = ([\"#9b59b6\" if (x == top_stations[0])\n",
    "           else \"#3498db\" if (x == top_stations[1])\n",
    "           else \"#95a5a6\" if (x == top_stations[2])\n",
    "           else \"#e74c3c\" if (x == top_stations[3])\n",
    "           else \"#34495e\" if (x == top_stations[4])\n",
    "           else \"#2ecc71\" for x in top_stations_monday.index])\n",
    "\n",
    "plt.subplot(3,2,1)\n",
    "top_station_barplot(y = top_stations_monday.index, \n",
    "                    x = 'Total_Traffic', \n",
    "                    data = top_stations_monday, \n",
    "                    title = 'Top Stations (Monday)', \n",
    "                    xlabel = 'Total Traffic', ylabel = 'Top Stations', labelsize = 20, palette = colors_mon)\n",
    "\n",
    "colors_tue = ([\"#9b59b6\" if (x == top_stations[0])\n",
    "           else \"#3498db\" if (x == top_stations[1])\n",
    "           else \"#95a5a6\" if (x == top_stations[2])\n",
    "           else \"#e74c3c\" if (x == top_stations[3])\n",
    "           else \"#34495e\" if (x == top_stations[4])\n",
    "           else \"#2ecc71\" for x in top_stations_tuesday.index])\n",
    "\n",
    "plt.subplot(3,2,2)\n",
    "top_station_barplot(y = top_stations_tuesday.index, \n",
    "                    x = 'Total_Traffic', \n",
    "                    data = top_stations_tuesday, \n",
    "                    title = 'Top Stations (Tuesday)', \n",
    "                    xlabel = 'Total Traffic', ylabel = 'Top Stations', labelsize = 20, palette = colors_tue)\n",
    "\n",
    "colors_wed = ([\"#9b59b6\" if (x == top_stations[0])\n",
    "           else \"#3498db\" if (x == top_stations[1])\n",
    "           else \"#95a5a6\" if (x == top_stations[2])\n",
    "           else \"#e74c3c\" if (x == top_stations[3])\n",
    "           else \"#34495e\" if (x == top_stations[4])\n",
    "           else \"#2ecc71\" for x in top_stations_wednesday.index])\n",
    "\n",
    "plt.subplot(3,2,3)\n",
    "top_station_barplot(y = top_stations_wednesday.index, \n",
    "                    x = 'Total_Traffic', \n",
    "                    data = top_stations_wednesday, \n",
    "                    title = 'Top Stations (Wednesday)', \n",
    "                    xlabel = 'Total Traffic', ylabel = 'Top Stations', labelsize = 20, palette = colors_wed)\n",
    "\n",
    "colors_thur = ([\"#9b59b6\" if (x == top_stations[0])\n",
    "           else \"#3498db\" if (x == top_stations[1])\n",
    "           else \"#95a5a6\" if (x == top_stations[2])\n",
    "           else \"#e74c3c\" if (x == top_stations[3])\n",
    "           else \"#34495e\" if (x == top_stations[4])\n",
    "           else \"#2ecc71\" for x in top_stations_thursday.index])\n",
    "\n",
    "plt.subplot(3,2,4)\n",
    "top_station_barplot(y = top_stations_thursday.index, \n",
    "                    x = 'Total_Traffic', \n",
    "                    data = top_stations_thursday, \n",
    "                    title = 'Top Stations (Thursday)', \n",
    "                    xlabel = 'Total Traffic', ylabel = 'Top Stations', labelsize = 20, palette = colors_thur)\n",
    "\n",
    "colors_fri = ([\"#9b59b6\" if (x == top_stations[0])\n",
    "           else \"#3498db\" if (x == top_stations[1])\n",
    "           else \"#95a5a6\" if (x == top_stations[2])\n",
    "           else \"#e74c3c\" if (x == top_stations[3])\n",
    "           else \"#34495e\" if (x == top_stations[4])\n",
    "           else \"#2ecc71\" for x in top_stations_friday.index])\n",
    "\n",
    "plt.subplot(3,2,5)\n",
    "top_station_barplot(y = top_stations_friday.index, \n",
    "                    x = 'Total_Traffic', \n",
    "                    data = top_stations_friday, \n",
    "                    title = 'Top Stations (Friday)', \n",
    "                    xlabel = 'Total Traffic', ylabel = 'Top Stations', labelsize = 20, palette = colors_fri)\n",
    "plt.tight_layout()\n",
    "plt.savefig('Day of the Week vs Total Traffic subplot (top 5)', bbox_inches = 'tight')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Throughout Monday and Friday, the top 5 stations rankings stayed the same exact for the fifth ranked station during Wednesday.\n",
    "\n",
    "\n",
    "Let's look at each of the top five stations by time of the day.\n",
    "\n",
    "* We can use a similar subplot approach and plot the time of day and the total traffic"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 87,
   "metadata": {},
   "outputs": [],
   "source": [
    "def day_df(Stations, top = 6):\n",
    "    \n",
    "    '''\n",
    "    Takes the time of the day as an argument\n",
    "    Returns a dataframe from summer19_MTA_cleaned that is filtered by the argument\n",
    "    \n",
    "    '''\n",
    "    \n",
    "    # filters by argument station and weekday data only\n",
    "    mask = (summer19_MTA_cleaned['Unique_Station'] == Stations) & (summer19_MTA_cleaned['WEEKEND'] == 'WEEKDAY')\n",
    "    top_stations = (summer19_MTA_cleaned[mask].groupby('TIME_OF_DAY')\n",
    "                       .sum().reset_index()\n",
    "                       .sort_values(by = 'Total_Traffic', ascending = False))\n",
    "    \n",
    "    return top_stations.head(top)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 88,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Unique_Station</th>\n",
       "      <th>ENTRIES</th>\n",
       "      <th>EXITS</th>\n",
       "      <th>ENTRIES DIFF</th>\n",
       "      <th>EXITS DIFF</th>\n",
       "      <th>Total_Traffic</th>\n",
       "      <th>TIME_INT</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>94</th>\n",
       "      <td>34 ST-PENN STA_ACE</td>\n",
       "      <td>670283993176</td>\n",
       "      <td>715364962094</td>\n",
       "      <td>5251396.0</td>\n",
       "      <td>4303253.0</td>\n",
       "      <td>8576.776778</td>\n",
       "      <td>347573</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>312</th>\n",
       "      <td>GRD CNTRL-42 ST_4567S</td>\n",
       "      <td>580325761542</td>\n",
       "      <td>537573481170</td>\n",
       "      <td>4457804.0</td>\n",
       "      <td>4385398.0</td>\n",
       "      <td>7936.803780</td>\n",
       "      <td>289547</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>90</th>\n",
       "      <td>34 ST-HERALD SQ_BDFMNQRW</td>\n",
       "      <td>976660703407</td>\n",
       "      <td>937652785399</td>\n",
       "      <td>4035201.0</td>\n",
       "      <td>4110163.0</td>\n",
       "      <td>7311.983798</td>\n",
       "      <td>275743</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>302</th>\n",
       "      <td>FULTON ST_2345ACJZ</td>\n",
       "      <td>306473275121</td>\n",
       "      <td>340456131519</td>\n",
       "      <td>4155459.0</td>\n",
       "      <td>3971517.0</td>\n",
       "      <td>7290.098110</td>\n",
       "      <td>327214</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>103</th>\n",
       "      <td>42 ST-PORT AUTH_ACENQRS1237W</td>\n",
       "      <td>1464593492427</td>\n",
       "      <td>1220246777724</td>\n",
       "      <td>3878724.0</td>\n",
       "      <td>2342674.0</td>\n",
       "      <td>5585.650765</td>\n",
       "      <td>198939</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                   Unique_Station        ENTRIES          EXITS  ENTRIES DIFF  \\\n",
       "94             34 ST-PENN STA_ACE   670283993176   715364962094     5251396.0   \n",
       "312         GRD CNTRL-42 ST_4567S   580325761542   537573481170     4457804.0   \n",
       "90       34 ST-HERALD SQ_BDFMNQRW   976660703407   937652785399     4035201.0   \n",
       "302            FULTON ST_2345ACJZ   306473275121   340456131519     4155459.0   \n",
       "103  42 ST-PORT AUTH_ACENQRS1237W  1464593492427  1220246777724     3878724.0   \n",
       "\n",
       "     EXITS DIFF  Total_Traffic  TIME_INT  \n",
       "94    4303253.0    8576.776778    347573  \n",
       "312   4385398.0    7936.803780    289547  \n",
       "90    4110163.0    7311.983798    275743  \n",
       "302   3971517.0    7290.098110    327214  \n",
       "103   2342674.0    5585.650765    198939  "
      ]
     },
     "execution_count": 88,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "top_unique_stations.head(5)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 89,
   "metadata": {},
   "outputs": [],
   "source": [
    "top_stations_PENN = day_df('34 ST-PENN STA_ACE')\n",
    "top_stations_GRAND = day_df('GRD CNTRL-42 ST_4567S')\n",
    "top_stations_HERALD = day_df('34 ST-HERALD SQ_BDFMNQRW')\n",
    "top_stations_FULTON = day_df('FULTON ST_2345ACJZ')\n",
    "top_stations_42STPORT = day_df('42 ST-PORT AUTH_ACENQRS1237W')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 134,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 1440x864 with 5 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "plt.figure(figsize = [20,12])\n",
    "plt.subplot(3,2,1)\n",
    "top_station_barplot(y = 'TIME_OF_DAY', \n",
    "                    x = 'Total_Traffic', \n",
    "                    data = top_stations_PENN, \n",
    "                    title = 'TIME OF DAY (PENN)', \n",
    "                    xlabel = 'Total Traffic', ylabel = 'Time of Day', labelsize = 20)\n",
    "plt.subplot(3,2,2)\n",
    "top_station_barplot(y = 'TIME_OF_DAY', \n",
    "                    x = 'Total_Traffic', \n",
    "                    data = top_stations_GRAND, \n",
    "                    title = 'TIME OF DAY (GRAND)', \n",
    "                    xlabel = 'Total Traffic', ylabel = 'Time of Day', labelsize = 20)\n",
    "plt.subplot(3,2,3)\n",
    "top_station_barplot(y = 'TIME_OF_DAY', \n",
    "                    x = 'Total_Traffic', \n",
    "                    data = top_stations_HERALD, \n",
    "                    title = 'TIME OF DAY (HERALD)', \n",
    "                    xlabel = 'Total Traffic', ylabel = 'Time of Day', labelsize = 20)\n",
    "plt.subplot(3,2,4)\n",
    "top_station_barplot(y = 'TIME_OF_DAY', \n",
    "                    x = 'Total_Traffic', \n",
    "                    data = top_stations_FULTON, \n",
    "                    title = 'TIME OF DAY (FULTON)', \n",
    "                    xlabel = 'Total Traffic', ylabel = 'Time of Day', labelsize = 20)\n",
    "plt.subplot(3,2,5)\n",
    "top_station_barplot(y = 'TIME_OF_DAY', \n",
    "                    x = 'Total_Traffic', \n",
    "                    data = top_stations_42STPORT, \n",
    "                    title = 'TIME OF DAY (42ST PORT)', \n",
    "                    xlabel = 'Total Traffic', ylabel = 'Time of Day', labelsize = 20)\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.savefig('Time vs Traffic by Station subplot (top 5)', bbox_tight = 'tight')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 124,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>TIME_OF_DAY</th>\n",
       "      <th>ENTRIES</th>\n",
       "      <th>EXITS</th>\n",
       "      <th>ENTRIES DIFF</th>\n",
       "      <th>EXITS DIFF</th>\n",
       "      <th>Total_Traffic</th>\n",
       "      <th>TIME_INT</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>4PM-8PM</td>\n",
       "      <td>72366028824</td>\n",
       "      <td>73455013688</td>\n",
       "      <td>985249.0</td>\n",
       "      <td>869106.0</td>\n",
       "      <td>1666.913591</td>\n",
       "      <td>48280</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>8AM-Noon</td>\n",
       "      <td>17253823757</td>\n",
       "      <td>14276848395</td>\n",
       "      <td>982427.0</td>\n",
       "      <td>793185.0</td>\n",
       "      <td>1595.724572</td>\n",
       "      <td>32938</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>Noon-4PM</td>\n",
       "      <td>98667211195</td>\n",
       "      <td>102635901697</td>\n",
       "      <td>901750.0</td>\n",
       "      <td>858837.0</td>\n",
       "      <td>1581.684968</td>\n",
       "      <td>53304</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>4AM-8AM</td>\n",
       "      <td>97169763940</td>\n",
       "      <td>106586135266</td>\n",
       "      <td>764150.0</td>\n",
       "      <td>431208.0</td>\n",
       "      <td>1072.827183</td>\n",
       "      <td>27529</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>5</th>\n",
       "      <td>8PM-Midnight</td>\n",
       "      <td>92952991102</td>\n",
       "      <td>100850822265</td>\n",
       "      <td>551004.0</td>\n",
       "      <td>394117.0</td>\n",
       "      <td>847.655266</td>\n",
       "      <td>77648</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>Midnight-4AM</td>\n",
       "      <td>89090211728</td>\n",
       "      <td>97608949690</td>\n",
       "      <td>69720.0</td>\n",
       "      <td>48973.0</td>\n",
       "      <td>103.904590</td>\n",
       "      <td>13020</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "    TIME_OF_DAY      ENTRIES         EXITS  ENTRIES DIFF  EXITS DIFF  \\\n",
       "4       4PM-8PM  72366028824   73455013688      985249.0    869106.0   \n",
       "2      8AM-Noon  17253823757   14276848395      982427.0    793185.0   \n",
       "3      Noon-4PM  98667211195  102635901697      901750.0    858837.0   \n",
       "1       4AM-8AM  97169763940  106586135266      764150.0    431208.0   \n",
       "5  8PM-Midnight  92952991102  100850822265      551004.0    394117.0   \n",
       "0  Midnight-4AM  89090211728   97608949690       69720.0     48973.0   \n",
       "\n",
       "   Total_Traffic  TIME_INT  \n",
       "4    1666.913591     48280  \n",
       "2    1595.724572     32938  \n",
       "3    1581.684968     53304  \n",
       "1    1072.827183     27529  \n",
       "5     847.655266     77648  \n",
       "0     103.904590     13020  "
      ]
     },
     "execution_count": 124,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "top_stations_HERALD = day_df('34 ST-PENN STA_ACE')\n",
    "top_stations_HERALD.head(10)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 123,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array([ 4,  8, 12, 23, 20, 16,  9, 11,  7, 17, 13,  5])"
      ]
     },
     "execution_count": 123,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "summer19_MTA_cleaned[summer19_MTA_cleaned['Unique_Station'] == '34 ST-HERALD SQ_BDFMNQRW'].TIME_INT.unique()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
