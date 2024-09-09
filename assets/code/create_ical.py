from icalendar import Calendar, Event
from datetime import datetime
import re

text = """
Januar 12. Fr Wiederbeginn der Proben
Februar 09. Fr 19:00 Uhr 161. Generalversammlung
Februar 12. Mo Sportferien Beginn
"""

# German month names to numbers
month_to_num = {
  "Januar": 1, "Februar": 2, "März": 3, "April": 4, "Mai": 5, "Juni": 6,
  "Juli": 7, "August": 8, "September": 9, "Oktober": 10, "November": 11, "Dezember": 12
}

# Create a new calendar
cal = Calendar()

# Split the text into lines and process each line
for line in text.split("\n"):
  print(line)
  # Find date and event name using regex
  match = re.match(r"(\w+) (\d+). (.*?)( \d{2}:\d{2} Uhr)?(.*)", line)
  if match:
    print(match.groups())
    month, day, _, time, event = match.groups()
    # If time is None, event is in the fourth group
    if not time:
      event = match.group(4)
    # Convert month name to number
    month = month_to_num[month]
    # Create a new event
    ev = Event()
    ev.add("summary", event)
    # If a time is provided, include it in the start date
    if time:
      hour, minute = map(int, time.split(":"))
      ev.add("dtstart", datetime(2024, month, int(day), hour, minute))
    else:
      ev.add("dtstart", datetime(2024, month, int(day)))
    # Add the event to the calendar
    cal.add_component(ev)

# Write the calendar to a file
with open("events.ics", "wb") as f:
  f.write(cal.to_ical())