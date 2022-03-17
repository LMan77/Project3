import datetime
import time
import pandas as pd
import numpy as np

"""
------- First Proposed Change - (1)

Merging of all 3 datasets into 1 by following the below steps
Use a new dataframe which is df41

df1 = pd.read_csv("chicago.csv")
df11 = df1.assign(city = 'chicago')

df2 = pd.read_csv("new_york_city.csv")
df22 = df2.assign(city = 'new york city')

df3 = pd.read_csv("washington.csv")
new_columns = {'Gender':"",'Birth Year':"",'city':'washington'}
df33 = df3.assign(**new_columns)
df33 = df33.astype({"Trip Duration":'int'})

frames = [df11, df22, df33]
df41 = pd.concat(frames)

df = df41


-------- Second Proposed Change - (2)

Review and improve Readability of all codes 


-------- Third Proposed Change - (3) 

Important change to counter error in dataset for Washington.
All metrics affected have been considered.


    # Display counts of gender

    try:
      CG = df['Gender'].value_counts()
      print('\nCount of Gender:', CG)
    except KeyError:
      print("\nSorry, No data available at the moment.")

    # Display earliest, most recent, and most common year of birth
    
    # Earliest year of birth

    try:
      EYB = df['Birth Year'].min()
      print('\n The earliest year of birth:', EYB)
    except KeyError:
      print("\nSorry, No data available at the moment.")

    # Most recent year of birth

    try:
      MRYB = df['Birth Year'].max()
      print('\nThe most recent year of birth:', MRYB)
    except KeyError:
      print("\nSorry, No data available at the moment.")

    # Most common year of birth

    try:
      MCYB = df['Birth Year'].value_counts().idxmax()
      print('\nThe most common year is:', MCYB)
    except KeyError:
      print("\nSorry, No data available at the moment.")

"""   
     
          
def check_data_entry(prompt, valid_entries): 
    """
    Asks user to type in input for city, day and month 
    Since we have 3 inputs to ask the user in get_filters(), it is easier to write a function.
    Args:
        (str) prompt - message to display to the user
        (list) valid_entries - list of string that should be accepted 
    Returns:
        (str) user_input - the user's valid input
    """
    try:
        user_input = str(input(prompt)).lower()

        while user_input not in valid_entries : 
            print('Sorry, it seems like you\'re not typing a correct entry.')
            print('Let\'s try again!')
            user_input = str(input(prompt)).lower()

        print('Great! the chosen entry is: {}\n'.format(user_input))
        return user_input

    except:
        print('Seems like there is an issue with your input')



def get_filters(): 
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello!\nLet\'s explore some US bikeshare data!\nAll characters are to be filled in lower case.')

    # Get user input for city (chicago, new york city, washington). 

    valid_cities = ['chicago','new york city','washington']
    prompt_cities = 'Please choose one of the 3 cities (chicago, new york city, washington): '
    city = check_data_entry(prompt_cities, valid_cities)


    # Get user input for month (all, january, february, ... , june).

    valid_months = ['all','january','february','march','april','may','june']
    prompt_month = 'Please choose a month (all, january, february, ... , june): '
    month = check_data_entry(prompt_month, valid_months)

    # get user input for day of week (all, monday, tuesday, ... sunday).
    valid_days = ['all','monday','tuesday','wednesday','thursday','friday','saturday', 'sunday']
    prompt_day = 'Please choose a day (all, monday, tuesday, ... sunday): '
    day = check_data_entry(prompt_day, valid_days)

    print('-'*40)
    return city, month, day
 

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df1 = pd.read_csv("chicago.csv")
    df11 = df1.assign(city = 'chicago')

    df2 = pd.read_csv("new_york_city.csv")
    df22 = df2.assign(city = 'new york city')

    df3 = pd.read_csv("washington.csv")
    df3 = df3.astype({"Trip Duration":'int'})
    new_columns = {'city':'washington'}
    df33 = df3.assign(**new_columns)
   
    frames = [df11, df22]
    df41 = pd.concat(frames)
    
    df5 = df41.merge(df33, 
                   how='outer',
                   suffixes=('', '_DROP')).filter(regex='^(?!.*_DROP)')
    
    df = df5 
                   

  # Start Time column to datetime

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
  # Extract Month from Start Time, new column

    df['month'] = df['Start Time'].dt.month 
    
  # Extract day of week from Start Time, new column  
    
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    

  # Filter by month if applicable

    if month != 'all':
    # Use the index of the months list to get the corresponding int

      months = ['january', 'february', 'march', 'april', 'may', 'june']
               
      month = months.index(month) + 1

   # Filter by month to create the new dataframe

      df = df[df['month'] == month]    
      
   # Filter by day of week when applicable

      if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
  
    return df
  

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel\n')
    start_time = time.time()

    # Display the most common month
    MCM = df['month'].value_counts().idxmax()
    
    if MCM == 1:
         print("The most common month is:", "January")
    elif MCM== 2:
         print("The most common month is:", "February")
    elif MCM == 3:
         print("The most common month is:", "March")
    elif MCM == 4:
         print("The most common month is:", "April")
    elif MCM == 5:
         print("The most common month is:", "May") 
    elif MCM == 6:
         print("The most common month is:","June")
    else:
         print("Not possible to compute at the moment")
                              
    print("")
         
    # Display the most common day of week
   
    MCDW = df['day_of_week'].value_counts().idxmax()
    
    if MCDW == 1:
         print("The most common day of week is:", "Monday")
    elif MCDW== 2:
         print("The most common day of week is:", "Tuesday")
    elif MCDW == 3:
         print("The most common day of week is:", "Wednesday")
    elif MCDW == 4:
         print("The most common day of week is:", "Thursday")
    elif MCDW == 5:
         print("The most common day of week is:", "Friday") 
    elif MCDW == 6:
         print("The most common day of week is:","Saturday") 
    elif MCDW == 7:
         print("The most common day of week is:","Sunday")            
    else:
         print("The most common day of week is:","Monday")
     
    
    print("")

    # Display the most common start hour

    df['hour'] = df['Start Time'].dt.hour
    
    MCH = df['hour'].value_counts().idxmax()
    
    print("The most common hour is: ", MCH)
    print("")
      
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip\n')
    start_time = time.time()

    # Display the most commonly used start station

    MCUST = df['Start Station'].value_counts().idxmax()
    
    print("The most common start station is: ", MCUST)
    print("")

    # Display the most commonly used end station

    MCUES = df['End Station'].value_counts().idxmax()
    
    print("The most common end station is: ", MCUES)
    print("")

    # Display the most frequent combination of start station and end station trip

    print("Most frequent combination of start station and end station trip")
    print("")   
    MFCSSEST = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print(MFCSSEST) 

    print("\nThis took %s seconds." % (time.time() - start_time))
    
    print('-'*40)


def trip_duration_stats(df):

    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display Total Travel Time

    TTL = df['Trip Duration'].sum()
    TTLM = (TTL)/60.0
    TTLM1 = int(TTLM)
    TTLH = (TTL)/3600.0
    TTLH1 = int(TTLH)
    
  
    print("Total Travel Time (minutes) :",TTLM1, "minutes")
    print("Total Travel Time (hours) :",TTLH1, "hours")
    print("")

    # Display Mean Travel Time
    
    MTL = df['Trip Duration'].mean()
    MTLM = (MTL)/60
    MTLM1 = int(MTLM)
    MTLH = (MTL)/3600
    MTLH1 = '{0:.2f}'.format(MTLH)
    
    print("Mean Travel Time (minutes):", MTLM1,"minutes")
    print("Mean Travel Time (hours):",MTLH1, "hours")

    print("\nThis took %s seconds." % (time.time() - start_time))
    
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display Count of user types

    CUT = df['User Type'].value_counts()
    print("Counts of User Types:")
    print("")
    print(CUT)
    
    print("")
   
    # Display Count of gender

    CG = df['Gender'].value_counts()
    
    print("Counts of Gender:")
    print("")
    print(CG)
    print("")
    
    # Display earliest, most recent, and most common year of birth

    # Earliest year of birth

    EYB = int(df['Birth Year'].min())
   
    print("The earliest year of birth is:",EYB)
    print("")
        
    print("")
     
    # Most recent year of birth
     
    MRYB = int(df['Birth Year'].max())
    print("The most recent year of birth is:",MRYB)
    print("")

    # Most common year of birth
    
    MCYB = int(df['Birth Year'].value_counts().idxmax())
    print("The most common year of birth is:",MCYB)
    print("")
         
    print("\nThis took %s seconds." % (time.time() - start_time))
    
    print('-'*40)


def raw_data(df):
        
     """Displays the data due filteration.
      5 rows will "added in each press"""
      
     print('Press "enter" to continuously view 5 rows data of individual trip data or enter "no" to skip:')
     start_loc = 0
     while (input()!= 'no'):
        start_loc = start_loc+5 
        print(df.head(start_loc))
        print("")
        

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('The project ends here.\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
