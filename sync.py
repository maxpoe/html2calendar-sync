import sys
import requests
from bs4 import BeautifulSoup
from icalendar import Calendar, Event, vText
import pytz
from datetime import datetime
from dateutil.relativedelta import relativedelta
import re

URL = "https://fas.thws.de/fileadmin/share/vlplan/wochen/BMG%20WiSe%2024-25_4_BMG%204.%20Sem.%20SoSe%2026.html"
TIMEZONE = pytz.timezone("Europe/Berlin")

def fetch_html(url):
    print(f"Fetching URL: {url}")
    response = requests.get(url)
    response.raise_for_status()
    # Explicitly use latin1 to avoid UnicodeDecodeError based on prior testing
    response.encoding = "latin1"
    return response.text

def parse_date(date_str):
    """
    Parses strings like 'Mo, 16.03.2026' into a datetime.date object.
    Returns None if parsing fails.
    """
    try:
        # Split by comma and space to get just the date part
        date_part = date_str.split(", ")[1].strip()
        # Parse into a datetime object
        dt = datetime.strptime(date_part, "%d.%m.%Y").date()
        return dt
    except Exception as e:
        print(f"Failed to parse date string {date_str}: {e}")
        return None

def parse_time_range(time_range_str):
    """
    Parses strings like '8:15 - 9:45 Uhr' or '8:15-11:30' into start and end time tuples (hour, minute).
    """
    try:
        # Remove 'Uhr' and any extra spaces
        time_range_str = time_range_str.replace("Uhr", "").strip()
        parts = time_range_str.split("-")
        
        start_str = parts[0].strip()
        end_str = parts[1].strip()
        
        start_time = datetime.strptime(start_str, "%H:%M").time()
        end_time = datetime.strptime(end_str, "%H:%M").time()
        
        return start_time, end_time
    except Exception as e:
        print(f"Failed to parse time range string {time_range_str}: {e}")
        return None, None

def extract_events(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find("table")
    if not table:
        print("No schedule table found.")
        return []
    
    rows = table.find_all("tr")
    events = []
    
    # We don't have a rigid assumption of columns, we just look for blocks 
    # that look like event data: A date block followed by time block followed by content.
    # Looking at the sample:
    # ['Mi, 18.03.2026', '8:15 - 9:45 Uhr', 'SU Praxisbezogenes Projekt [BMG]', 'PRXP', 'Umgang m. psychischen Belastungen bei Studierenden', 'Prof. Dr. Holger Truckenbrodt', 'M.1.02']
    
    for row in rows:
        cols = row.find_all("td")
        if not cols:
            continue
        
        for col in cols:
            strings = list(col.stripped_strings)
            # An event block usually has at least Date, Time, Title, and Room/Lecturer
            if len(strings) >= 5:
                # We need to verify if the first string looks like a date and second like a time
                date_str = strings[0]
                time_str = strings[1]
                
                if "," in date_str and ("-" in time_str or "Uhr" in time_str):
                    
                    event_date = parse_date(date_str)
                    start_time, end_time = parse_time_range(time_str)
                    
                    if event_date and start_time and end_time:
                        title = strings[2]
                        # The rest could be variable (shortcode, detail, lecturer, room), we just join them into a description
                        # Usually, the last one is the room, second to last is lecturer
                        location = strings[-1] if len(strings) > 3 else ""
                        description = "\\n".join(strings[3:-1])
                        
                        start_dt = TIMEZONE.localize(datetime.combine(event_date, start_time))
                        end_dt = TIMEZONE.localize(datetime.combine(event_date, end_time))
                        
                        events.append({
                            "title": title,
                            "start": start_dt,
                            "end": end_dt,
                            "location": location,
                            "description": description
                        })
    return events

def generate_ical(events):
    cal = Calendar()
    cal.add('prodid', '-//THWS Schedule Sync//mxm.dev//')
    cal.add('version', '2.0')
    cal.add('dtstamp', datetime.now(TIMEZONE))
    
    for e in events:
        event = Event()
        event.add('summary', e['title'])
        event.add('dtstart', e['start'])
        event.add('dtend', e['end'])
        
        if e['location']:
            event.add('location', vText(e['location']))
        if e['description']:
            event.add('description', e['description'])
            
        # Give a unique ID based on start time and title
        uid = f"{e['start'].strftime('%Y%m%dT%H%M%S')}-{hash(e['title'])}@thws.sync"
        event.add('uid', uid)
        
        cal.add_component(event)
        
    return cal.to_ical()

def main():
    try:
        html = fetch_html(URL)
        events = extract_events(html)
        print(f"Extracted {len(events)} events.")
        
        if not events:
            print("No events to generate.")
            sys.exit(0)
            
        ical_data = generate_ical(events)
        
        with open("schedule.ics", "wb") as f:
            f.write(ical_data)
        
        print("Successfully generated schedule.ics")
        
    except Exception as e:
        print(f"Error during execution: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
