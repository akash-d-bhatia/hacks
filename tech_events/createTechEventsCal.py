import pandas as pd
from icalendar import Calendar, Event
from datetime import datetime, timedelta
import pytz

def create_ical_from_excel(excel_file_path):
    # Read the events from the Excel file
    events_df = pd.read_excel(excel_file_path)


    current_year = 2024 # hardcoded for now!



    # Create a calendar
    cal = Calendar()
    cal.add('version', '2.0')
    cal.add('prodid', '-//Akash Bhatia//Enterprise Tech Events//EN')

    # Timezone for events
    tz = pytz.timezone('America/Los_Angeles')

    counter = 0
    for index, row in events_df.iterrows():
        # Create an event
        ical_event = Event()
        

        # Handling date ranges
        dates = row['Date'].split('-')
        start_date_str = dates[0].strip()
        end_date_str = dates[-1].strip()

        # Grab the month in name
        event_month_str = start_date_str.split(' ')[0]

        # Add back the month to the end_date_str
        end_date_str = event_month_str + " " + end_date_str
        
        # Adding year to the date for proper formatting
        start_date_str += f" {current_year}"
        end_date_str += f" {current_year}"


        # Converting string to datetime object
        start_date = datetime.strptime(start_date_str, '%B %d %Y')
        end_date = datetime.strptime(end_date_str, '%B %d %Y')

        # Adjusting end date to include the whole day
        end_date += timedelta(days=1)

        # Adding timezone information
        start_date = tz.localize(start_date)
        end_date = tz.localize(end_date)

        # Adding event details
        ical_event.add('summary', row['Event'])
        ical_event.add('dtstart', start_date) 
        ical_event.add('dtend', end_date) 
        ical_event.add('location', row['Location'])
        ical_event.add('dtstamp', datetime.now())
        ical_event.add('uid', 'unique-event-id-' + str(counter))
        ical_event.add('description', row['Description'])
        

        counter += 1

        if counter < 2 :
            # Adding event to calendar
            cal.add_component(ical_event)

    # Return the calendar object
    return cal

# Path to the Excel file
excel_file_path = './TechEventsExcel.xlsx'


# Creating the .ics file from the Excel file
calendar = create_ical_from_excel(excel_file_path)

# Save the calendar to a file
with open('TechEventsCalendar.ics', 'wb') as f:
    f.write(calendar.to_ical())
