class Event:#set name of class to call it
  def __init__(self, title, startHour,startMinute,endHour,endMinute,dayNumber,venue=None):#func set ver
    self.title = title #set title
    self.startHour = startHour#set start hour
    self.startMinute = startMinute#set start minute
    self.endHour = endHour#set end Hour
    self.endMinute = endMinute#set end endMinute
    self.dayNumber = dayNumber#set day number
    self.venue = venue#set end date

events=[]
try:
    #Following functions validate input, if data is ok then it return True else False
    def is_valid_string(name):
      """Returns True if the name is a valid name of a person, False otherwise."""
      if name.strip()=='':
        return False
      for char in name:
        if not char.isalpha() and not char.isspace():
          return False
      return True
    
    def is_valid_date(hour,minute):
        """Returns True if the date is a valid , False otherwise."""
        try:
            hour = int(hour)
            minute = int(minute)
            if hour < 0 or hour > 23:
                return False
            if minute < 0 or minute > 59:
                return False
        except ValueError:
            return False
        return True
    
    def check_overlap(hour,minute,dayNumber):
            """Returns True if the date is a valid , False otherwise."""
            try:
                for event in events:
                   if(event.dayNumber==dayNumber):
                      if(event.startHour==hour):
                         return not (event.startMinute <= minute)
                      # if start_time1 <= end_time2 and start_time2 <= end_time1:
                      #      return False
                      # else:
                      #     return True
                    
            except ValueError:
                return False
            return True
    
    #Below functions create recursive prompt until they enter desired input
    def get_valid_name(message):
      """Prompts the user to enter a name until they enter a valid name."""
      message=message+' :'
      while True:
        name = input(message)
        if is_valid_string(name):
          return name
        else:
          print(f"Invalid {message}. Please try again. later")

    def get_valid_start_date(message):
      """Prompts the user to enter a date until they enter a valid date."""
      message=message+' :'
      while True:
       try:
        date = input(message)
        hour, minute = date.split(":")
        if(minute=="0"):
            minute="00"
        if is_valid_date(hour,minute):
          return hour,minute
        else:
          print(f"Invalid {message}. \nDate must be 24 hour format \nExample 09:00 \nPlease try again.") 
       except:
          print(f"Invalid {message}. \nDate must be 24 hour format \nExample 09:00 \nPlease try again.") 

    def dinsertion():
        eventName=get_valid_name("Event Name")
        startHour,startMinute=get_valid_start_date("Start Time(09:00)")
        endHour,endMinute=get_valid_start_date("End Time(09:00)")
        print("Dont know day number type no otherwise type day number")
        dayNumber=input("Day number : ")
        if(dayNumber.lower()=='no'):
          print("According to ISO 8601, weekdays are numbered from 1 to 7, starting with Monday and ending with Sunday.\nSo, Monday is 1, \nTuesday is 2, \nWednesday is 3, \nThursday is 4, \nFriday is 5, \nSaturday is 6, \nSunday is 7.")
        venue=input("Venue (Optional) : ").strip()
        venue= None if venue=='' else venue
        events.append(Event(eventName,startHour,startMinute,endHour,endMinute,dayNumber,venue))
        print("Successfull")

    def deletion():
        startTime=input("Start Time : ")
        deleted="Item not found please try again\n"
        for e in events:
          if e.startTime == startTime:
            events.remove(e)
            deleted="Deletion Successful\n"
        print(deleted)
    
          
    def display():
        if(len(events)!=0):
          print("Timetable Overview")
          print("-------------------------------------------------------------")
          print("Start Time | End Time  | Title                     | Location")
          print("-------------------------------------------------------------")
          for obj in events:
            print("{}:{}      | {}:{}    | {} | {}".format(
            obj.startHour,obj.startMinute, obj.endHour,obj.endMinute, obj.title, obj.venue))
        else:
          print("No events")

    def search():
        no=int(input("Enter the Roll Number : "))

    def update():
      startTime=input("Start Time : ")
      updated="Item not found please try again\n"
      for e in events:
          if e.startTime == startTime:
            e.title=get_valid_name("Event Name")
            e.startHour,e.startMinute=get_valid_start_date("Start Time(09:00)")
            e.endHour,e.endMinute=get_valid_start_date("End Time(09:00)")
            print("Dont know day number type no otherwise type day number")
            e.dayNumber=input("Day number : ")
            if(e.dayNumber.lower()=='no'):
             print("According to ISO 8601, weekdays are numbered from 1 to 7, starting with Monday and ending with Sunday.\nSo, Monday is 1, \nTuesday is 2, \nWednesday is 3, \nThursday is 4, \nFriday is 5, \nSaturday is 6, \nSunday is 7.")
            venue=input("Venue (Optional) : ").strip()
            venue= None if venue=='' else venue
          updated="Updated Successful\n"
      print(updated)
      
        

    def error():
        print("\t--------Invalid Option--------\n\tPLEASE ENTER CORRECT OPTION")

    print("\t------Welcome to Event Management System------")
    print("Author: Jithu Bhai")
    print("Email: jithu@dmbca.com")
    while True:
        print("\t1.Create an event\n\t2.Delete a event\n\t3.Update an event\n\t4.Search Student Record")
        print("\t5.Dispaly Details\n\t6.Exit")
        ch=input("Enter the choice :")
        switch={'1':dinsertion,'2':deletion,'3':update,'4':search,'5':display,'6':exit}
        switch.get(ch,error)()
except TypeError:
    print("Exception  : ",TypeError)

