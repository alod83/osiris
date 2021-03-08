import datetime

#today = datetime.datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
#print today.timetuple().tm_yday

now = datetime.datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
minutes = (now - midnight).seconds/60
print minutes