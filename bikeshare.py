import time
import pandas as pd
import numpy as np
import calendar as cal

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("For which city are you interested "+
                     "in: Chicago, New York City or Washington?")
        
        city = city.lower()
        
        # error handling for city
        if city not in ('new york city', 'chicago', 'washington'):
            print("Please enter a valid city.")
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Which month would you like pick " + city.title() + 
                      "? You can choose between January, February, March, " +
                      "April, May and June, or type all if you do not wish "+
                      "to specify a month.")
        
        month = month.lower()
        
        # error handling for month
        if month not in ('january', 'february', 'march', 'april', 'may', 
                         'june', 'all'):
            print("Please enter a correct month.")
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Now pick a day please." +
                    "You can choose between Monday, Tuesday, Wednesday," +
                    "Thursday, Friday, Saturday or Sunday, or type all if " +
                    "you do not wish to specify a day.")
        
        day = day.lower()
        
        # error handling
        if day not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                       'saturday', 'sunday', 'all'):
            print("Please enter a valid day.")
            continue
        else:
            break

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
    
    df = pd.read_csv(CITY_DATA[city])
    
    #converts Start Time to datetime 
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month and day
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.weekday
    
    # filtering dataset
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['Month'] == month]
    
    if day != 'all':
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day) 
        df = df[df['Weekday'] == day]
    
    return df


def time_stats(df, city, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month    
    # Use calendar library to get month names
    list(cal.month_name)
    
    #Figures out most common Month
    ind_month = df['Month'].value_counts().idxmax()
    
    # Prints full name of month
    if month != 'all':
        print('You picked ',month.title(),', so, the most common '+
              'month in',city.title(),'is', cal.month_name[ind_month], ';) \n\n')
    
    else:
        print('The most common month in ',city.title(),' is', 
              cal.month_name[ind_month], '.\n\n')
    

    # display the most common weekday    
    # Use calendar again to get names
    list(cal.day_name)
    
    # Top weekday
    ind_day = df['Weekday'].value_counts().idxmax()
    
    #Full name of weekday
    if day != 'all':
        print('You selected',day.title(),'so the most common '+
              'day of the week in',city.title(),'is', cal.day_name[ind_day], ';) \n\n')    
    else:
        print('The most common day of the week is', cal.day_name[ind_day], '\n\n')
    
        
    # display the most common start hour
    # Get hour from start time
    df['Start Hour'] = df['Start Time'].dt.hour    
    
    #Print the most common start hour
    print('The most common start hour for your selection is', 
          df['Start Hour'].value_counts().idxmax(), 'o\'clock.\n')
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most common start station for your selection is', 
          df['Start Station'].value_counts().idxmax(), '.\n\n')

    # display most commonly used end station
    print('The most common end station for your selection is', 
          df['End Station'].value_counts().idxmax(), '.\n\n')

    # display most frequent combination of start station and end station trip
    # combines start and stop stations to one single column
    df['Station Combination'] = df['Start Station'] + ' (start) and ' + df['End Station'] + ' (end).'
    
    #Pirnts combo
    print('The most common station combination for your selection is ', 
          df['Station Combination'].value_counts().idxmax(), '\n')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    #Calculates travel time
    trip_sum_sec = df['Trip Duration'].sum()
    
    #converts travel time
    trip_sum_h = round(trip_sum_sec / 60 / 60 ,0)
    
    #Prints total travel time
    print('The total travel time for your selection is', trip_sum_h, 'hours.\n\n')

    # display mean travel time
    #calculate travel mean
    trip_mean_sec = df['Trip Duration'].mean()
    
    # Converts to 0 decimals
    trip_mean_min = round(trip_mean_sec / 60  ,0)    
    
    #Prints travel mean
    if trip_mean_min < 60:
        print('The mean travel time for your selection is', trip_mean_min, 'minutes.\n\n')
    else:
        trip_mean_h = round(trip_mean_min / 60 ,1)
        print('The mean travel time for your selection is', trip_mean_h, 'hours.\n\n')
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users. Statistics will be calculated using NumPy."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    usertypes = df['User Type'].values
    
    #count different user type
    ct_subscriber  = (usertypes == 'Subscriber').sum()
    ct_customer = (usertypes == 'Customer').sum()
    
    #Prints user type counts
    print('The number of subscribers in', city.title(), 'is:',ct_subscriber,'\n')
    print('The number of customers in', city.title(), 'is:',ct_customer,'\n')

    # Display counts of gender
    # Display earliest, most recent, and most common year of birth
    # gender and year of birth are missing from the Washington dataset
    if city.title() != 'Washington':
        # counts of gender
        gender = df['Gender'].values
        
  
        ct_male  = (gender == 'Male').sum()
        ct_female = (gender == 'Female').sum()
        
        
        print('The number of men in', city.title(), 'is:',ct_male,'\n')
        print('The number of women in', city.title(), 'is:',ct_female,'\n')
        
        # year of birth
        
        birthyear = df['Birth Year'].values
        
        
        birthyear_unique = np.unique(birthyear[~np.isnan(birthyear)])
        
        latest_birthyear = birthyear_unique.max()
        
        earliest_birthyear = birthyear_unique.min()
        
        # Prints latest and earliest birth year
        print('The most recent birth year of users in', city.title(), 'is:',
              latest_birthyear ,'\n')
        print('The earliest birth year of users in', city.title(), 'is:',
              earliest_birthyear,'\n')   
        
        # Prints most common birth year
        print('The most common birth year of users in', city.title(), 'is:', 
              df['Birth Year'].value_counts().idxmax(), '\n')
    
    else:
        # print message if Washington was chosen as city
        print('Apologies. Gender and birth year information are not available for Washington!')

    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        # arguments adapted to run function properly
        time_stats(df, city, month, day)
        station_stats(df)
        trip_duration_stats(df)
        # arguments adapted to run function properly
        user_stats(df, city)
        
        
  
        restart = input('Replay? yes or no? ')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
