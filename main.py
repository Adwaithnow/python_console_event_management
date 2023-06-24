#!/bin/python

def read_from_disk(file_name, headers):
    events = []
    try:
        with open(file_name, "r") as f:
            line = next(f, None)
            if not line:
                return events
            if set(line.rstrip("\n").split(",")) != set(headers):
                box(' ')
                box("Error! Invalid headers")
                return events
            line = next(f, None)
            while line:
                if line == '\n' or line.strip() == '':
                    continue
                event = {}
                fields = line.rstrip('\n').split(',')
                for i in range(len(headers)):
                    event[headers[i]] = fields[i]
                events.append(event)
                line = next(f, None)
    except FileNotFoundError:
        events = []
    return events

def write_to_disk(file_name, headers, data):
    with open(file_name, "w") as f:
        f.write(','.join(headers) + '\n')
        for event in data:
            values = [str(event[key]) for key in headers]
            f.write(','.join(values) + '\n')

def boxify(text, center = False, length = 80):
    length, content, filler = length - 4, '', ' '
    for i in range(int(len(text)/length if len(text)%length == 0 else (len(text)/length)+1)):
        chars = text[(i * length):((i * length) + length)]
        fill = filler * (int((length - len(chars)) / 2) if center else length - len(chars))
        if center:
            chars = f'|{fill} {chars} {fill}'
            content += chars + ('|\n' if len(chars) == (length + 3) else f'{filler}|\n')
        else:
            content += f'| {chars} {fill}|\n'
    return content
def box(text, center = False, length = 80):
    print(boxify(text, center, length), end='')

def print_header(text, new_line=False, length = 80):
    if new_line:
        box(' ')
    filler, text = '=', text[:(length - 12)]
    fill = filler * int(((length - len(text) - 4) / 2))
    string = f'{fill}[ {text} ]{fill}'
    print(string + ('' if len(string) == length else filler))
    if new_line:
        box('  ')

def print_log(text, level='error'):
    # box(('\n' if new_line else '') + f'{level}: {text}')
    box(f'{level}: {text}')

def print_event(event, n, show_day = True):
    text = str(n) + ') '
    if show_day:
        text += int_to_day(int(event['day'])).lower()[:3] + ' '
    text += event['start'] + ' to '
    text += event['end'] + ' - '
    text += event['name']
    if event['location'].strip() != '':
        text += ' at [location]: ' + event['location']
    box(text)


def print_menu(menu_items):
    choice = -1
    while choice == -1:
        print_header('MENU', True)
        for i in range(len(menu_items)):
            box(f'{i+1}: {menu_items[i][0]}')
        choice = input(boxify('Enter your choice: '))
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

def int_to_day(day):
    if day == 1:
        return 'Monday'
    elif day == 2:
        return 'Tuesday'
    elif day == 3:
        return 'Wednesday'
    elif day == 4:
        return 'Thursday'
    elif day == 5:
        return 'Friday'
    elif day == 6:
        return 'Saturday'
    elif day == 7:
        return 'Sunday'
    else:
        return 'invalid'

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
    name = input(boxify('Event name [empty string is not allowed]: '))
    start = input(boxify('Event start time in military time [HH:MM]: '))
    end = input(boxify('Event end time in military time [HH:MM]: '))
    day = input(boxify('Event day [1-7 | 0 for all]: '))
    location = input(boxify('Event location [optional]: '))
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
        if day < 0 or day > 7:
            is_valid = False
            print_log('Aborting! day must be between 1 to 7!')
        else:
            if day != 0:
                if not is_available_time(start, end, day, state):
                    is_valid = False
                    print_log('Aborting! Selected time slot is not available on ' + int_to_day(day))
            else:
                for i in range(1, 8):
                    if not is_available_time(start, end, i, state):
                        is_valid = False
                        print_log('Aborting! Selected time slot is not available on ' + int_to_day(i))
    if is_valid:
        if day != 0:
            state['events'].append({
                'name': name,
                'day': int(day),
                'start': start.replace(' ', ':'),
                'end': end.replace(' ', ':'),
                'location': location.strip(),
            })
        else:
            for i in range(1, 8):
                state['events'].append({
                    'name': name,
                    'day': i,
                    'start': start.replace(' ', ':'),
                    'end': end.replace(' ', ':'),
                    'location': location.strip(),
                })
        box(name + ' added!')
    return state


def handle_delete(state):
    print_header('Delete Event', True)
    if len(state['events']) == 0:
        print_log("No Events Found!", "info")
        return state
    for i in range(len(state['events'])):
        print_event(state['events'][i], i+1)
    box(' ')
    choice = input(boxify("Enter event number to delete: "))
    if not choice.isnumeric():
        print_log("Must Enter a number!")
    elif int(choice) < 1 or int(choice) > len(state['events']):
        print_log("Must Enter a value between 0 and " +
                  str(len(state['events'])))
    else:
        choice = int(choice) - 1
        box(state['events'][choice]['name'] + ' deleted!')
        del state['events'][choice]
    return state


def handle_update(state):
    print_header('Update Event', True)
    if len(state['events']) == 0:
        print_log("No Events Found!", "info")
        return state
    for i in range(len(state['events'])):
        print_event(state['events'][i], i+1)
    box(' ')
    choice = input(boxify("Enter event number to update: "))
    if not choice.isnumeric():
        print_log("Must Enter a number!")
    elif int(choice) < 1 or int(choice) > len(state['events']):
        print_log("Must Enter a value between 0 and " +
                  str(len(state['events'])))
    else:
        choice = int(choice) - 1
        print_event(state['events'][choice], choice)
        box(' ')
        box('Enter empty string [Enter or Return key] to use previour value.')
        box('name: ' + state['events'][choice]['name'])
        name = input(boxify('Event name: '))
        box('start time: ' + state['events'][choice]['start'])
        start = input(boxify('Event start time in military time [HH:MM]: '))
        box('end time: ' + state['events'][choice]['end'])
        end = input(boxify('Event end time in military time [HH:MM]: '))
        box('day: ' + state['events'][choice]['day'])
        day = input(boxify('Event day [1-7]: '))
        box('location: ' + state['events'][choice]['location'])
        location = input(boxify('Event location [optional]: '))
        if name.strip() != '':
            state['events'][choice]['name'] = name
        if location.strip() != '':
            state['events'][choice]['location'] = location
        if start.strip() != '' and is_valid_time(start):
            state['events'][choice]['start'] = start
        if end.strip() != '' and is_valid_time(end):
            state['events'][choice]['end'] = end
        if day.strip() != '' and day.strip().isdigit():
            day = int(day.strip())
            if day > 1 or day < 7:
                state['events'][choice]['day'] = day
        box(state['events'][choice]['name'] + ' updated!')
    return state


def handle_search(state):
    if len(state['events']) == 0:
        print_log("No Events Found!", "info")
        return state
    matches = []
    box(' ')
    query = input(boxify("Enter text to search: "))
    for i in range(len(state['events'])):
        if state['events'][i]['name'].find(query) >= 0:
            matches.append(i)
        elif state['events'][i]['location'].find(query) >= 0:
            matches.append(i)
    if len(matches) == 0:
        box(' ')
        box("No matches found!")
    else:
        print_header("Search results for " + query, True)
        for i in range(len(matches)):
            print_event(state['events'][matches[i]], matches[i]+1)
    return state


def handle_display(state):
    print_header('All Events', True)
    if len(state['events']) == 0:
        print_log("No Events Found!", "info")
        return state
    days = { 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [] }
    for i in range(len(state['events'])):
        state['events'][i]['index'] = i + 1
        days[int(state['events'][i]['day'])].append(state['events'][i])
    for day in days:
        events = sorted(days[day], key=lambda k: time_to_int(k['start']))
        print_header(int_to_day(day))
        for j in range(len(events)):
            index = events[j]['index']
            print_event(events[j], index + 1, False)
    return state

def main():
    state = {
        'count': 0,
        'events': [],
    }
    file_name = "data.csv"
    menu_items = [
        ('Create new event', handle_create),
        ('Delete an event', handle_delete),
        ('Update an event', handle_update),
        ('Search events', handle_search),
        ('Dispaly all Events', handle_display),
        ('Exit', print),
    ]
    print('Author: Jithu Bhai')
    print('Email: jithu@dmbca.com')
    headers = ('name', 'day', 'start', 'end', 'location')
    state['events'] = read_from_disk(file_name, headers)
    _continue = True
    while _continue:
        choice = print_menu(menu_items)
        if choice == len(menu_items):
            print_header('Thank You.', True)
            _continue = False
        else:
            state = menu_items[choice-1][1](state)
            write_to_disk(file_name, headers, state['events'])
        state['count'] += 1

if __name__ == '__main__':
    main()
