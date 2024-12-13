import datetime

import pandas as pd
import json
import random
from typing import Dict, List, Tuple


def run_login(username: str, password: str) -> Tuple[bool, int]:
    """
    Authenticates a user by checking the provided username and password against data stored on file.

    Args:
        username: user's entered name
        password: user's entered password
    Returns:
        A tuple where:
            - The first value is True or false depending on if the login was successful
            - The second value is an int repressenting what went wrong if unsuccessful.
                0: Empty username
                1: Empty password
                2: No user found
                3: Incorrect password
    """
    print('run login')
    df = pd.read_csv('login.csv')
    users = df['Users'].tolist()
    users = [str(user) for user in users]
    check = username in users

    if username == '':
        return False, 0

    if password == '':
        return False, 1

    if check:
        print('User in system')
        row = df.loc[df['Users'] == username]
        key = row['Passwords'].tolist()
        key = key[0]
        if password == key:
            check_exercise(username)
            return True, -1
        else:
            return False, 3
    else:
        print('No user by that username in system')
        return False, 2


def run_account_create(username: str, password: str) -> Tuple[bool, int]:
    """
    Creates a new user account by validating the provided username and password, and adding the user to the system.

    Args:
        username: The new username.
        password: The new password.

    Returns:
        A tuple where:
            - The first value is a boolean indicating whether the account was successfully created.
            - The second value is an integer indicating the result of the account creation.
                - The second value is generated but using the validate password function above.
    """
    print('Run account create')
    login_check = run_login(username, password)
    if not login_check[0] and login_check[1] == 2:
        df = pd.read_csv('login.csv')
        df.loc[len(df)] = [len(df) + 1, username, password]
        df.to_csv('login.csv', index=False)

        with open('userdata.json', 'r') as f:
            userdata = json.load(f)

        userdata[f'{username}'] = {
            'info': {},
            'weight': {
                'weight': [],
                'dates': []
            },
            'planner': {
                'Sunday': [],
                'Monday': ['Chest'],
                'Tuesday': ['Back'],
                'Wednesday': ['Legs'],
                'Thursday': ['Shoulders'],
                'Friday': ['Cardio'],
                'Saturday': []
            }
        }

        with open('userdata.json', 'w') as f:
            f.write(json.dumps(userdata))
        check_exercise(username)
        return True, -1
    else:
        return False, login_check[1]


def check_exercise(user: str) -> None:
    """
        Checks to see if user has all the workout in profile

        Args:
            user: The username of the user.

        If user is missing an exercise, they will be added.
    """
    with open('userdata.json', 'r') as f:
        userdata = json.load(f)
    with open('workouts.json', 'r') as f:
        workouts = json.load(f)

    workout_keys = workouts.keys()
    workout_keys = list(workout_keys)

    target_data = userdata[user]
    target_keys = target_data.keys()
    target_keys = list(target_keys)

    difference_list = [workout for workout in workout_keys if workout not in target_keys]
    if len(difference_list) == 0:
        print('All workouts up to date')
    else:
        print(f'Adding {len(difference_list)} to profile.')

    for workout in difference_list:
        target_data[workout] = {}
        for attribute in workouts[workout]['attributes']:
            target_data[workout].update({f"{attribute}": []})

    with open('userdata.json', 'w') as f:
        f.write(json.dumps(userdata))


def pick_workout(day: str, user: str) -> List[str]:
    """
    Selects a random workout for a given day based on the user's workout planner.

    Args:
        day: The day of the week (e.g., 'Monday', 'Tuesday').
        user: The username of the user.

    Returns:
        A list of selected workouts for the day, or ['Rest day'] if no workouts are scheduled.
    """
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    if day in weekdays:
        with open('workouts.json', 'r') as f:
            workouts = json.load(f)
        with open('userdata.json', 'r') as f:
            userdata = json.load(f)
        planner = userdata[user]['planner']
        for d in planner:
            if d == day:
                # For now, we will only be looking at the one value that is in the workout planner. Eventually update
                # to run through list of all workouts for that planned day and generate off of that.
                group = planner[d][0]
                group_list = []
                for workout in workouts:
                    if workouts[workout]['group'] == group:
                        group_list.append(workouts[workout]['name'])
                selected_workouts = random.sample(group_list, 3)
                return selected_workouts

    else:
        return ['Rest day']


def get_attributes(workout_name: str) -> str:
    """
    Retrieves the list of attributes for a specific workout.

    Args:
        workout_name: The name of the workout.

    Returns:
        A comma-separated string of attributes for the workout.
    """
    with open('workouts.json', 'r') as f:
        workouts = json.load(f)

    for workout in workouts:
        if workouts[workout]['name'] == workout_name:
            attributes = workouts[workout]['attributes']
            att_str = ''
            for attribute in attributes:
                clean = attribute.capitalize()
                att_str += clean + ', '
            return att_str


def check_workout(workout_name: str) -> bool:
    """
    Checks if a workout exists in the system.

    Args:
        workout_name: The name of the workout.

    Returns:
        True if the workout exists, False otherwise.
    """
    with open('workouts.json', 'r') as f:
        workouts = json.load(f)
    for workout in workouts:
        if workouts[workout]['name'] == workout_name:
            return True
        else:
            return False


def check_edits(data: Dict[str, str], user: str) -> Tuple[bool, int]:
    """
    Validates and processes the workout data submitted by the user.

    Args:
        data: A dictionary where the key is the workout name and the value is a comma-separated string of attributes.
        user: The username of the user.

    Returns:
        A tuple where:
            - The first value is a boolean indicating whether the data was successfully processed.
            - The second value is an integer code indicating the validation result.
    """
    check = 0
    print(data, user)
    for workout in data:
        print(workout)
        values = data[workout].split(',')
        values = [x.strip() for x in values]
        print(len(values))
        if len(values) == 5:
            try:
                date = datetime.datetime.strptime(values[0], "%m/%d/%Y")
                # values[0] = date
            except:
                check += 1
                return False, 2
            try:
                num = int(values[1])
                values[1] = num
            except:
                check += 1
                return False, 3
            try:
                num = int(values[2])
                values[2] = num
            except:
                check += 1
                return False, 4
            try:
                num = int(values[3])
                values[3] = num
            except:
                check += 1
                return False, 5
            if check == 0:
                send_to_file(workout, values, user)
                return True, -1
            else:
                return False, 1
        else:
            check += 1
            return False, 1


# Update to use dictionaries not lists for data input
def send_to_file(workout: str, value: List[str], user: str) -> None:
    """
        Saves workout data to the user's profile.

        Args:
            workout: The workout name.
            value: A list of values (date, weight, reps, sets, notes).
            user: The username of the user.
    """

    with open('userdata.json', 'r') as f:
        userdata = json.load(f)
    with open('workouts.json', 'r') as f:
        workouts = json.load(f)
    targetData = userdata[user]
    for w in workouts:
        if workouts[w]['name'] == workout:
            workout_id = w
    targetData[workout_id]['dates'].append(value[0])
    targetData[workout_id]['weight'].append(value[1])
    targetData[workout_id]['reps'].append(value[2])
    targetData[workout_id]['sets'].append(value[3])
    targetData[workout_id]['notes'].append(value[4])

    with open('userdata.json', 'w') as f:
        f.write(json.dumps(userdata))


def get_points(tag: str, focus: str, user: str) -> Tuple[List[str], List[int]]:
    """
    Retrieves workout data points (e.g., weight, reps) for a given user and workout tag.
    This is for building the graphs

    Args:
        tag: The workout tag (e.g., 'weight').
        focus: The focus of the data (e.g., 'weight', 'reps').
        user: The username of the user.

    Returns:
        A tuple where:
            - The first value is a list of dates.
            - The second value is a list of corresponding data points (e.g., weight, reps).
    """
    with open('userdata.json', 'r') as f:
        userdata = json.load(f)
    targetData = userdata[user][tag]
    for field in targetData:
        if field == focus:
            y = targetData[focus]
        if field == 'dates':
            x = targetData['dates']
    return x, y


def log_weight(weight: float, date: str, user: str) -> None:
    """
    Logs a user's weight for a specific date.

    Args:
        weight: The weight to log.
        date: The date of the weight entry.
        user: The username of the user.
    """
    with open('userdata.json', 'r') as f:
        userdata = json.load(f)
    targetData = userdata[user]['weight']
    if date in targetData['dates']:
        index = targetData['dates'].index(date)
        targetData['weight'][index] = weight
    else:
        targetData['dates'].append(date)
        targetData['weight'].append(int(weight))
    with open('userdata.json', 'w') as f:
        f.write(json.dumps(userdata))


def pull_workouts() -> List[str]:
    """
    Retrieves a list of all workout names.

    Returns:
        A list of workout names.
    """
    with open('workouts.json', 'r') as f:
        workouts = json.load(f)
    out_list = []
    for workout in workouts:
        out_list.append(workouts[workout]['name'])
    return out_list


def get_workout_id(name: str) -> str:
    """
    Retrieves the workout ID for a given workout name.

    Args:
        name: The name of the workout.

    Returns:
        The ID of the workout.
    """
    with open('workouts.json', 'r') as f:
        workouts = json.load(f)

    for workout in workouts:
        if workouts[workout]['name'] == name:
            return workout
