#!/bin/python
# TODO invalidate all user inputs with comma
def read_from_disk():
    try:
       with open("data.csv", "r") as f:
        data={}
        events = []
        firstLine = next(f, None)
        if firstLine is not None:
            header=firstLine.rstrip("\n").split(",")
            if is_valid_csv(header):
                for line in f:
                    record = line.rstrip("\n").split(",")
                    start = record[0].strip()
                    end = record[1].strip()
                    name = record[2].strip()
                    location = record[3].strip()
                    events.append({
                        header[0]: name,
                        header[1]: start,
                        header[2]: end,
                        header[3]: location,
                    })
        else:
            print_log("Invalid csv provided")
        data= {
            "count": len(events),
            "events": events
        }
    except FileNotFoundError:
        data = {
            "count": 0,
            "events": []
        }
        write_to_disk(data)
    return data


def write_to_disk(data):
    #Extracting events from object
    events=data["events"]
    # Extract headers from the first object in the event
    headers=[]
    if(len(events)!=0):
        headers = list(events[0].keys())
    else:
        headers=['start', 'end', 'name', 'location']
    with open("data.csv", "w") as f:
         # Write the CSV header
        f.write(','.join(headers) + '\n')
        for obj in events:
                values = [str(obj[key]) for key in headers]
                f.write(','.join(values) + '\n')


def is_valid_csv(header):
    desiredHeader=['start', 'end', 'name', 'location']
    if len(header)!=len(desiredHeader):
        return False
    for target_string in desiredHeader:
        if target_string not in header:
            return False
    return True


def print_header(text, new_line=False):
    print(('\n' if new_line else '') + f'----[ {text[:68]} ]----')


def print_log(text, level='error', new_line=False):
    print(('\n' if new_line else '') + f'{level}: {text}')


def print_event_in_line(event, n):
    print((' ' if n < 10 else '') + str(n) + ') ' +
          event['start'] + ' - ' + event['name'])


def print_event_in_full(event, n):
    print((' ' if n < 10 else '') + str(n) + ') ' + event['start'] + ' to ' + event['end'] +
          ' - ' + event['name'] + ('' if event['location'] == '' else ' @ ') + event['location'])


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
                print_log('Choice must be between 1 to ' +
                          str(len(menu_items)))
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


def is_available_time(start, end, day, state):
    is_available = True
    start = time_to_int(start)
    end = time_to_int(end)
    for i in range(len(state['events'])):
        if day != state['events'][i]['day']:
            continue
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
    day = input('Event day [1-7]: ')
    location = input('Event location [optional]: ')
    if name.strip() == '':
        print_log('Aborting! Name cannot be empty!')
        is_valid = False
    if not (is_valid_time(start) and is_valid_time(end)):
        print_log('Aborting! Invalid time format!')
        is_valid = False
    if not day.strip().isdigit():
        is_valid = False
        print_log('Aborting! day must be a digit!')
    else:
        day = int(day)
        if day < 1 or day > 7:
            is_valid = False
            print_log('Aborting! day must be between 1 to 7!')
    if not is_available_time(start, end, day, state):
        is_valid = False
        print_log('Aborting! Selected time slot is not available!')
    if is_valid:
        state['events'].append({
            'name': name,
            'day': day,
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
        print_log("Must Enter a value between 0 and " +
                  str(len(state['events'])))
    else:
        choice = int(choice) - 1
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
        print_log("Must Enter a value between 0 and " +
                  str(len(state['events'])))
    else:
        choice = int(choice) - 1
        print_event_in_full(state['events'][choice], choice)
        name = input('\nEvent name [empty string is not allowed]: ')
        start = input('Event start time in military time [HH:MM]: ')
        end = input('Event end time in military time [HH:MM]: ')
        day = input('Event day [1-7]: ')
        location = input('Event location [optional]: ')
        # todo: add insertion validations
        # todo: update if not empty string
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
    return state


def main():
    events = []
    _continue = True
    state = {
        'count': 0,
        'events': [],
    }
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
    state = read_from_disk()
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
