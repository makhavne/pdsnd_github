import calendar
import numpy as np
import pandas as pd
import time

SEPARATOR = '-' * 40

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Would you like to see data for Chicago, New York City, or Washington?\n")
    while city.lower() not in CITY_DATA.keys():
        city = input(
            "\nInput {} was invalid. Please re-enter city - Chicago, New York City, or Washington?\n".format(city))

    # TO DO: get user input for month (all, january, february, ... , june)
    time_filter_list = ["month", "day", "both", "none"]
    time_filter = input(
        "\nWould you like to filter the data by month, day, both or not at all? (Enter none for no time filter)\n")
    while time_filter.lower() not in time_filter_list:
        time_filter = input(
            "\nInput {} was invalid. Would you like to filter the data by month, day, both or not at all? (Enter none "
            "for no time filter)\n".format(
                time_filter))

    if time_filter.lower() == "both" or time_filter.lower() == "month":
        month_list = ["january", "february", "march", "april", "may", "june"]
        month = input("\nWhich month? January, February, March, April, May, or June?\n")
        while month.lower() not in month_list:
            month = input(
                "\nInput {} was invalid. "
                "Please re-enter month as January, February, March, April, May, or June?\n".format(
                    month))
    else:
        month = "all"

    if time_filter.lower() == "both" or time_filter.lower() == "day":
        day_raw = input("\nWhich day? Please enter response as integer (e.g.: 1 = Monday)\n")
        while not day_raw.isdigit() or (int(day_raw) < 1 or int(day_raw) > 7):
            day_raw = input(
                "\nInput {} was invalid. "
                "Please re-enter day as integer (e.g.: 1 = Monday ... 7 = Sunday)\n".format(
                    day_raw))
        day = calendar.day_name[int(day_raw) - 1]
    else:
        day = "all"

    print("\nWe will fetch data for city - " + city.lower())
    print("For all months" if month.lower() == 'all' else ("Filtered by month - " + month.lower()))
    print("For all days" if day.lower() == 'all' else ("Filtered by day of week - " + day.lower()))

    print(SEPARATOR)
    return city.lower(), month.lower(), day


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

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # print(df['Start Time'].head(3))
    # print(df['month'].head(3))
    # print(df['day_of_week'].head(5))

    # filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    print(SEPARATOR)
    print(df.head(5))
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print("The most common month = {}".format(df['month'].mode()[0]))

    # TO DO: display the most common day of week
    print("The most common day of week = {}".format(df['day_of_week'].mode()[0]))

    # TO DO: display the most common start hour
    print("The most common start hour = {}".format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print(SEPARATOR)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("The most common start station = {}".format(df['Start Station'].mode()[0]))

    # TO DO: display most commonly used end station
    print("The most common end station = {}".format(df['End Station'].mode()[0]))

    # TO DO: display most frequent combination of start station and end station trip
    popular_route = df.groupby(['Start Station', 'End Station'])['Start Station'].size().sort_values(ascending=False)
    print("The most common start-end station combination = {}".format(popular_route.index[0]))

    # Another way: df['combined'] = df['Start Station']+ " === "+ df['End Station']
    # print(df['combined'].value_counts().index[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print(SEPARATOR)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print("Total travel time = {}".format(sum(df['Trip Duration'])))

    # TO DO: display mean travel time
    print("Mean travel time = {}".format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print(SEPARATOR)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Count of user types")
    print(user_types)

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender_types = df['Gender'].value_counts()
        print("\nCount of gender types")
        print(gender_types)
    else:
        print("\nNo data for gender types in selected dataset")

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print("\nEarliest year of birth = {}".format(int(df['Birth Year'].dropna().min())))
        print("Most recent year of birth = {}".format(int(df['Birth Year'].dropna().max())))
        print("Most common year of birth = {}".format(int(df['Birth Year'].dropna().mode()[0])))
    else:
        print("\nNo data for birth year in selected dataset")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print(SEPARATOR)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        num_of_lines = 5
        total_rows = df.shape[0]
        view_raw_data = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n').lower()
        if view_raw_data in ('yes', 'y'):
            indexCounter = 0
            while True:
                print(df.iloc[indexCounter:indexCounter + num_of_lines])
                indexCounter += num_of_lines

                if indexCounter >= total_rows:
                    print('\nPrinted all rows')
                    break
                else:
                    continue_viewing = input(
                        '\nWould you like to see next 5 lines of raw data? Enter yes or no.\n').lower()
                    if continue_viewing not in ('yes', 'y'):
                        break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
