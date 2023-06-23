#!/bin/python
import json #todo: remove all imports
# simpple csv logic instead of json
# and also invalidate all user inputs with comma

def read_from_disk():
    try:
        f = open('data.json')
        d = json.load(f)
        f.close()
    except FileNotFoundError:
        create_data_file()
        d={
            "count":0,
            "events":[]
        }
    return d

def create_data_file():
    with open("data.json", "w") as f:
        f.write("{}")

def write_to_disk(data):
    with open('data.json', 'w') as f:
        json.dump(data, f)

def print_header(text, new_line = False):
    print(('\n' if new_line else '') + f'----[ {text[:68]} ]----')

def print_log(text, level = 'error', new_line = False):
    print(('\n' if new_line else '') + f'{level}: {text}')

def print_event_in_line(event, n):
    print((' ' if n < 10 else '') + str(n) + ') ' + event['start'] + ' - ' + event['name'])

def print_event_in_full(event, n):
    print((' ' if n < 10 else '') + str(n) + ') ' + event['start'] + ' to ' + event['end'] + ' - ' + event['name'] + ('' if event['location'] == '' else ' @ ') + event['location'])

def print_menu(menu_items):
    choice = -1
    while choice == -1:
        print_header('MENU', True)
        for i in range(len(menu_items)):
            print(f'{i+1}: {menu_items[i][0]}')
        choice = input('Enter your choice: ')
        if not choice.isdigit():
            choice = -1
            print_log('Input is not a Digit!')
        else:
            choice = int(choice)
            if choice < 0 or choice > len(menu_items):
                choice = -1
                print_log('Choice must be between 1 to ' + str(len(menu_items)))
    return choice

def is_valid_time(time):
    is_valid = True
    if len(time.strip()) != 5:
        is_valid = False
    elif not (time[2] == ':' or time[2] == ' '):
        is_valid = False
    elif not (time[0].isdigit() and time[1].isdigit()):
        is_valid = False
    elif not (time[3].isdigit() and time[4].isdigit()):
        is_valid = False
    elif not (int(time[0:2]) < 24 and int(time[3:5]) < 60):
        is_valid = False
    return is_valid

def time_to_int(time):
    return int(time[0:2] + time[3:5])

def is_available_time(start, end, state):
    is_available = True
    #todo: check if it si the same day too sryyy
    start = time_to_int(start)
    end = time_to_int(end)
    for i in range(len(state['events'])):
        event_start = time_to_int(state['events'][i]['start']) 
        event_end = time_to_int(state['events'][i]['end']) 
        if start >= event_start and start < event_end:
            is_available = False
            break
        if end > event_start and end <= event_end:
            is_available = False
            break
        if event_start > start and event_start < end:
            is_available = False
            break
    return is_available

def handle_create(state):
    is_valid = True
    print_header('Create New Event', True)
    name = input('\nEvent name [empty string is not allowed]: ')
    start = input('Event start time in military time [HH:MM]: ')
    end = input('Event end time in military time [HH:MM]: ')
    location = input('Event location [optional]: ')
    if name.strip() == '':
        print_log('Aborting! Name cannot be empty!')
        is_valid = False
    if not (is_valid_time(start) and is_valid_time(end)):
        print_log('Aborting! Invalid time format!')
        is_valid = False
    if is_valid:
        # todo: check if time is blocked
        state['events'].append({
            'name': name,
            'start': start.replace(' ', ':'),
            'end': end.replace(' ', ':'),
            'location': location.strip(),
        })
        print(name, 'added!')
    return state

def handle_delete(state):
    print_header('Delete Event', True)
    if len(state['events']) == 0:
        print_log("No Events Found!", "info")
        return state
    for i in range(len(state['events'])):
        print_event_in_line(state['events'][i], i+1)
    choice = input("\nEnter event number to delete: ")
    if not choice.isnumeric():
        print_log("Must Enter a number!")
    elif int(choice) < 1 or int(choice) > len(state['events']):
        print_log("Must Enter a value between 0 and " + str(len(state['events'])))
    else:
        choice = int(choice) -1
        print(state['events'][choice]['name'], 'deleted!')
        del state['events'][choice]
    return state

def handle_update(state):
    print_header('Update Event', True)
    if len(state['events']) == 0:
        print_log("No Events Found!", "info")
        return state
    for i in range(len(state['events'])):
        print_event_in_line(state['events'][i], i+1)
    choice = input("\nEnter event number to update: ")
    if not choice.isnumeric():
        print_log("Must Enter a number!")
    elif int(choice) < 1 or int(choice) > len(state['events']):
        print_log("Must Enter a value between 0 and " + str(len(state['events'])))
    else:
        choice = int(choice) -1
        print_event_in_full(state['events'][choice], choice)
        name = input('\nEvent name [empty string is not allowed]: ')
        start = input('Event start time in military time [HH:MM]: ')
        end = input('Event end time in military time [HH:MM]: ')
        location = input('Event location [optional]: ')
        # todo: add insertion validations
        print_event_in_full({
            'name': name,
            'start': start.replace(' ', ':'),
            'end': end.replace(' ', ':'),
            'location': location.strip(),
        }, choice)
        print(state['events'][choice]['name'], 'updated!')
    return state

def handle_search(state):
    if len(state['events']) == 0:
        print_log("No Events Found!", "info")
        return state
    matches = []
    query = input("\nEnter text to search: ")
    for i in range(len(state['events'])):
        if state['events'][i]['name'].find(query) >= 0:
            matches.append(i)
        elif state['events'][i]['location'].find(query) >= 0:
            matches.append(i)
    if len(matches) == 0:
        print_log("No matches found!")
    else:
        print_header("Search results for " + query, True)
        for i in range(len(matches)):
            print_event_in_full(state['events'][matches[i]], matches[i]+1)
    return state

def handle_display(state):
    # todo: proper display logic with 80 char limit
    for i in range(len(state['events'])):
        print_event_in_line(state['events'][i], i+1)
    is_available_time('08 10', '09 10', state)
    return state

def main():
    events = []
    _continue = True
    state = {
        'count': 0,
        'events': [],
    }
    state = read_from_disk()
    menu_items = [
        ('Create an event', handle_create),
        ('Delete a event', handle_delete),
        ('Update an event', handle_update),
        ('Search Student Record', handle_search),
        ('Dispaly Details', handle_display),
        ('Exit', print),
    ]
    print('Author: Jithu Bhai')
    print('Email: jithu@dmbca.com')
    # while True:
        # t = input('tiem [HH:MM]:')
        # print(is_valid_time(t))
    while _continue:
        print('\n\n\n next iteration:', state['count'])
        choice = print_menu(menu_items)
        if choice == len(menu_items):
            print_header('Thank You.', True)
            _continue = False
        else:
            state = menu_items[choice-1][1](state)
            write_to_disk(state)
        state['count'] += 1

if __name__ == '__main__':
    main()
