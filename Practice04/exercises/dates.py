#1
import datetime
now = datetime.datetime.now()
before_5days = now - datetime.timedelta(days = 5)
print("5 days ago: ", before_5days)

#2  
today = now.date()
yesterday = (now - datetime.timedelta(days = 1)).date()
tommorow = (now + datetime.timedelta(days = 1)).date()
print("yesterday: ", yesterday)
print("today: ", today)
print("tommorow: ", tommorow)

#3
without_microseconds = now.replace(microsecond = 0)
print("Without microseconds:", without_microseconds)

#4
date1 = datetime.datetime(2025, 2, 27, 12, 0, 0)
date2 = datetime.datetime(2025, 3, 15, 12, 0, 0)

difference = date2 - date1
seconds = difference.total_seconds()

print("Difference in seconds:", seconds)