import sys
import pandas as pd

CITY_DATA = {"chicago": r"Data\chicago.csv",
             "new york city": r"Data\new_york_city.csv",
             "washington": r"Data\washington.csv"}

available_months = {"1": "January",
                    "2": "February",
                    "3": "March",
                    "4": "April",
                    "5": "May",
                    "6": "June"}

available_week_days = {"1": "Monday",
                       "2": "Tuesday",
                       "3": "Wednesday",
                       "4": "Thursday",
                       "5": "Friday",
                       "6": "Saturday",
                       "7": "Sunday"}

city = month = week_day = None
action_tracker = []  # tracks actions in order to provide 'go back' functionality
month_with_week_day = False  # this is True when both month AND week_day are chosen.


def display_current_selection():
    """
    Displays the current selection of city, month and week_day if different than None.
    Returns:
        None
    """
    selection = (f for f in (city.title(), available_months.get(
        str(month)), available_week_days.get(str(week_day))) if f)
    print("---- " + "Current selection: " + " + ".join(selection) + " ----")


def update_tracker(called_func):
    """
    Updates the action tracker in order to provide the 'go back' functionality to the workflow.

    Args:
        (function) called_func - the function it's calling from
    Returns:
        None
    """
    if called_func not in action_tracker:
        action_tracker.append(called_func)


def go_back(action):
    """
    Allows to go back one step in the workflow.
    If already at the start, it loops there.

    Args:
        (function) action - the originating action to go back one step from
    Returns:
        None
    """
    global action_tracker
    if action != get_city:
        action_tracker = action_tracker[:-1]
        action_tracker.pop()()
    else:
        invalid_choice(action)


def invalid_choice(action):
    """
    Prints invalid prompt and repeats the action.

    Args:
        (function) action - the action where the invalid choice occurs
    Returns:
        None
    """
    print("Invalid selection. Please try again...\n")
    action()


def default_actions(choice, action):
    """
    Provides 'go back' and 'exit' functionality to workflow.

    Args:
        (str) choice - the choice passed in from the calling function
        (function) action - the function it's calling from
    Returns:
        None
    """
    if choice.lower() == "g":
        go_back(action)
    elif choice.lower() == "e":
        sys.exit()
    else:
        invalid_choice(action)


def get_city():
    """
    Prompts the user to select the city and calls get_filter.
    'default_actions' function is called to handle 'exit' or invalid choices.
    Returns:
        None
    """
    update_tracker(get_city)
    global city
    choice = input("Which city would you like to see data for?:\n"
                   "(Please type the initial)\n\n"
                   "[C]hicago\n"
                   "[N]ew York\n"
                   "[W]ashington\n\n"
                   "[E]xit program\n")
    if choice.lower() in [c[0] for c in CITY_DATA.keys()]:
        city = {k[0]: k for k, v in CITY_DATA.items()}[choice.lower()]
    else:
        default_actions(choice, get_city)
    get_filter()


def get_filter():
    """
    Prompts the user to specify a filter from 'month', 'week_day', 'both' or 'none'.
    If 'month' or 'both' filter is selected -> 'get_month' is called.
    If 'week day' filter is selected -> 'get_week_day' is called.
    If 'none' is selected -> 'load_data' is called.
    'default_actions' function is called to handle 'exit', 'back' or invalid choices.
    Returns:
         None
    """
    update_tracker(get_filter)
    global month_with_week_day, month, week_day
    month = week_day = None
    display_current_selection()
    choice = input("Would you like to filter by?:\n"
                   "(Please type the initial)\n\n"
                   "[M]onth\n"
                   "[W]eek day\n"
                   "[B]oth\n"
                   "[N]one\n\n"
                   "[G]o back\n"
                   "[E]xit program\n")
    if choice.lower() == 'm':
        month_with_week_day = False
        get_month()
    elif choice.lower() == 'w':
        month_with_week_day = False
        get_week_day()
    elif choice.lower() == 'b':
        month_with_week_day = True
        get_month()
    elif choice.lower() == 'n':
        month_with_week_day = False
        load_data()
    else:
        default_actions(choice, get_filter)


def get_month():
    """
    Prompts the user to specify the month.
    If 'both' was selected in the 'get_filter step', it then calls 'get_week_day'.
    'default_actions' function is called to handle 'exit', 'back' or invalid choices.
    Returns:
        None
    """
    update_tracker(get_month)
    global month
    month = None  # reset the month choice
    display_current_selection()
    choice = input("Which month?:\n"
                   "(Eg.: Type '1' for January, '2' for February, etc.)\n\n"
                   "[1] January\n"
                   "[2] February\n"
                   "[3] March\n"
                   "[4] April\n"
                   "[5] May\n"
                   "[6] June\n\n"
                   "[G]o back\n"
                   "[E]xit program\n")
    if choice in available_months:
        month = int(choice)
        if month_with_week_day:
            get_week_day()
        else:
            load_data()
    else:
        default_actions(choice, get_month)


def get_week_day():
    """
    Prompts the user to specify the week_day.
    If the choice is valid -> calls 'load_data'.
    For any other choices calls 'default_actions' handler.
    Returns:
        None
    """
    update_tracker(get_week_day)
    global week_day
    week_day = None  # reset the week_day choice
    display_current_selection()
    choice = input("Which week day?\n"
                   "(Eg.: Type '1' for Monday, '2' for Tuesday, etc.)\n\n"
                   "[1] Monday\n"
                   "[2] Tuesday\n"
                   "[3] Wednesday\n"
                   "[4] Thursday\n"
                   "[5] Friday\n"
                   "[6] Saturday\n"
                   "[7] Sunday\n\n"
                   "[G]o back\n"
                   "[E]xit program\n")
    if choice in available_week_days:
        week_day = int(choice)
        load_data()
    else:
        default_actions(choice, get_week_day)


def load_data():
    """
    Loads the data set for the specified city, month and week day.
    It then calls the 'run_stats' function.
    Return:
         None
    """
    print("\nLoading data...\n")
    df = pd.read_csv(CITY_DATA[city], parse_dates=["Start Time", "End Time"])
    df["month"] = df["Start Time"].dt.month
    df["week_day"] = df["Start Time"].dt.weekday
    if month is not None:
        df = df[df["month"] == month]
    if week_day is not None:
        df = df[df["week_day"] == week_day]
    df["hour"] = df["Start Time"].dt.hour
    df["Trip Duration"] = pd.to_timedelta(df["Trip Duration"], unit="s")
    df["route"] = df["Start Station"] + " - " + df["End Station"]
    run_stats(df)


def run_stats(df):
    """
    Calls individual functions for calculating statistics on dataframe based on some conditions.
    For eg., it would only call 'most_popular_month_stat' if 'month' was not selected as a filter.
    Returns:
        None
    """
    all_statistics = {most_popular_month_stat: month is None,
                      most_popular_week_day_stat: week_day is None,
                      most_popular_hour_stat: True,
                      most_popular_start_station_stat: True,
                      most_popular_end_station_stat: True,
                      most_popular_trip_start_end_stat: True,
                      travel_time_stat: True,
                      user_types_stat: True,
                      gender_stat: city in ("chicago", "new york city"),
                      age_stat: city in ("chicago", "new york city")}
    print("The following statistics are available for the current selection:")
    display_current_selection()
    print()
    [f(df) for f, condition in all_statistics.items() if condition]
    what_next()


def most_popular_month_stat(df):
    """
    Prints the most popular month.
    Args:
        (pandas.DataFrame) df - the input dataframe
    Returns:
        None
    """
    print("Most popular month:")
    print(available_months[str(int(df["month"].mode()))])
    print()


def most_popular_week_day_stat(df):
    """
    Prints the most popular day of the week.
    Args:
        (pandas.DataFrame) df - the input dataframe
    Returns:
        None
    """
    print("Most popular day of the week:")
    print(available_week_days[str(int(df["week_day"].mode()) + 1)])
    print()


def most_popular_hour_stat(df):
    """
    Prints the most popular hour of day.
    Args:
        (pandas.DataFrame) df - the input dataframe
    Returns:
        None
    """
    print("Most popular hour of day:")
    print(df["hour"].mode()[0])
    print()


def most_popular_start_station_stat(df):
    """
    Prints the most popular start station.
    Args:
        (pandas.DataFrame) df - the input dataframe
    Returns:
        None
    """
    print("Most popular start station:")
    print(df["Start Station"].value_counts().idxmax())
    print()


def most_popular_end_station_stat(df):
    """
    Prints the most popular end station.
    Args:
        (pandas.DataFrame) df - the input dataframe
    Returns:
        None
    """
    print("Most popular end station:")
    print(df["End Station"].value_counts().idxmax())
    print()


def most_popular_trip_start_end_stat(df):
    """
    Prints the most popular trip route, from start to end.
    Args:
        (pandas.DataFrame) df - the input dataframe
    Returns:
        None
    """
    print("Most popular trip route, from start to end:")
    print(df["route"].value_counts().idxmax())
    print()


def travel_time_stat(df):
    """
    Prints the average trip duration and the total (sum of all trips' durations).
    Args:
        (pandas.DataFrame) df - the input dataframe
    Returns:
        None
    """
    print("Travel time:")
    print("Average per trip: " + str(df["Trip Duration"].mean()))
    print("Total: " + str(df["Trip Duration"].sum()))
    print()


def user_types_stat(df):
    """
    Displays user types breakdown.
    Args:
        (pandas.DataFrame) df - the input dataframe
    Returns:
        None
    """
    print("User types breakdown:")
    user_types = df["User Type"].value_counts()
    print("\n".join(f"{r}: {user_types[r]}" for r in user_types.index))
    print()


def gender_stat(df):
    """
    Displays gender breakdown.
    Args:
        (pandas.DataFrame) df - the input dataframe
    Returns:
        None
    """
    print("Gender breakdown:")
    gender_types = df["Gender"].value_counts()
    print("\n".join(f"{r}: {gender_types[r]}" for r in gender_types.index))
    print()


def age_stat(df):
    """
    Displays age statistics (earliest, most recent and most common year of birth).
    Args:
        (pandas.DataFrame) df - the input dataframe
    Returns:
        None
    """
    print("Birth years:")
    print("Earliest: " + str(int(df["Birth Year"].min())))
    print("Most recent: " + str(int(df["Birth Year"].max())))
    print("Most common: " + str(int(df["Birth Year"].mode()[0])))


def display_raw_data():
    """
    Displays raw data, 3 rows at a time as (index, Series) pairs.
    If 'Display more data...' is selected -> continues with the generator.
    If 'StopIteration' occurs -> it calls 'what_next' function.
    if 'Restart with a new data set' is selected -> it calls 'get_city'
    'default_actions' function is called to handle 'exit', 'back' or invalid choices.
    Returns:
         None
    """
    rows = pd.read_csv(CITY_DATA[city]).iterrows()
    print("\nDisplaying 3 entries of raw data:\n")
    while True:
        try:
            [print(next(rows), "\n") for x in range(3)]
        except StopIteration:
            print("\nThat's all the data!!!\n")
            break
        choice = input("\nWhat would you like to do next?\n"
                       "[D]isplay more data...\n"
                       "[R]estart with a new data set (discard all filters)\n"
                       "[G]o back\n"
                       "[E]xit program\n\n")
        if choice.lower() == "d":
            continue
        elif choice.lower() == "r":
            action_tracker.clear()
            get_city()
        else:
            default_actions(choice, what_next)
    what_next()


def what_next():
    """
    Prompts the user with choices.
    If 'Display raw data' is selected -> calls 'display_raw_data'.
    if 'Restart with a new data set' is selected -> it calls 'get_city'
    'default_actions' function is called to handle 'exit', 'back' or invalid choices.
    Returns:
         None
    """
    update_tracker(what_next)
    choice = input("\nWhat would you like to do next?\n"
                   "[D]isplay raw data\n"
                   "[R]estart with a new data set (discard all filters)\n"
                   "[G]o back\n"
                   "[E]xit program\n")
    if choice.lower() == "r":
        action_tracker.clear()
        get_city()
    elif choice.lower() == "d":
        display_raw_data()
    else:
        default_actions(choice, what_next)


def main():
    get_city()


if __name__ == '__main__':
    main()
