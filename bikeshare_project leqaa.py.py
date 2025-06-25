import time
import pandas as pd
import numpy as np

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}


def get_filters():

    print('Hello! Let\'s explore some US bikeshare data!')

    while True:
        city = input("Please enter the city (chicago, new york city, washington): ").lower()
        if city in CITY_DATA:
            break
        print("Invalid input. Please enter one of the listed cities.")

    while True:
        month = input("Please enter the month (all, january, february, ..., june): ").lower()
        if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            break
        print("Invalid input. Please enter a valid month.")

    while True:
        day = input("Please enter the day of the week (all, monday, tuesday, ..., sunday): ").lower()
        if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
            break
        print("Invalid input. Please enter a valid day.")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads and filters data for the specified city, month, and day.
    """
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        month_index = ['january', 'february', 'march', 'april', 'may', 'june'].index(month) + 1
        df = df[df['month'] == month_index]

    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df


def display_raw_data(df):
    """Displays raw data 5 rows at a time upon user request."""
    i = 0
    while True:
        view_data = input("Would you like to view 5 rows of raw data? Enter yes or no: ").lower()
        if view_data != 'yes':
            break
        print(df.iloc[i:i+5])
        i += 5


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    common_month = df['month'].mode()[0]
    print(f"Most Common Month: {common_month}")

    common_day = df['day_of_week'].mode()[0]
    print(f"Most Common Day of Week: {common_day.title()}")

    common_hour = df['hour'].mode()[0]
    print(f"Most Common Start Hour: {common_hour}:00")

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    start_station = df['Start Station'].mode()[0]
    print(f"Most Common Start Station: {start_station}")

    end_station = df['End Station'].mode()[0]
    print(f"Most Common End Station: {end_station}")

    df['Trip'] = df['Start Station'] + " to " + df['End Station']
    common_trip = df['Trip'].mode()[0]
    print(f"Most Common Trip: {common_trip}")

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_duration = df['Trip Duration'].sum()
    print(f"Total Travel Time: {total_duration} seconds")

    mean_duration = df['Trip Duration'].mean()
    print(f"Average Travel Time: {mean_duration:.2f} seconds")

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print("User Type Counts:")
    print(user_types.to_string(), "\n")

    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print("Gender Counts:")
        print(gender_counts.to_string(), "\n")
    else:
        print("Gender data not available for this city.\n")

    if 'Birth Year' in df.columns:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common = int(df['Birth Year'].mode()[0])
        print(f"Earliest Year of Birth: {earliest}")
        print(f"Most Recent Year of Birth: {recent}")
        print(f"Most Common Year of Birth: {common}")
    else:
        print("Birth Year data not available for this city.")

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart != 'yes':
            break


if __name__ == "__main__":
    main()
