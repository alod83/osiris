import numpy as np

def concatenate(x1,x2,axis=0):
    if  len(x1) == 0:
        return x2
    else:
        return np.concatenate((x1, x2), axis)
        
def print_result(output,result):
	if output is None:
		print result
	else:
		with open(output, 'ab') as fh:
			fh.write(result)

def get_day_of_year(date):
	import datetime
	return date.timetuple().tm_yday
	
def get_minutes_from_midnight(date):
	import datetime
	midnight = date.replace(hour=0, minute=0, second=0, microsecond=0)
	minutes = (date - midnight).seconds/60
	return minutes
	
def get_keys_by_value(dictOfElements, valueToFind):
    listOfKeys = list()
    listOfItems = dictOfElements.items()
    for item  in listOfItems:
        if item[1] == valueToFind:
            listOfKeys.append(item[0])
    return  listOfKeys