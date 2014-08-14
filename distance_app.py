import easygui
from requests import get

def make_url(origin, dest, mode='driving', lang='en-EN', units='imperial'):
	url='http://maps.googleapis.com/maps/api/distancematrix/json?origins={}&destinations={}&mode={}&language={}&units={}'.format(origin, dest, mode, lang, units)
	return url


def get_dist_data(origin, dest,mode='driving', lang='en-EN', units='imperial'):
	data = get_json_data(origin, dest, mode, lang, units)
	try:
		return data['rows'][0]['elements'][0]['distance']['text'].split()[0]
	except:
		return None


def get_json_data(origin, dest,mode='driving', lang='en-EN', units='imperial'):
	url = make_url(origin, dest, mode, lang, units)
	return get(url).json()
	

def get_file_loc():
	return easygui.fileopenbox(title="Select Address File", filetypes=['*.txt'])
	

def get_file_data(filename=None):
	if not filename:
		filename = get_file_loc()
	if filename:
		with open(filename) as datafile:
			data = datafile.readlines()
			for line in range(len(data)):
				data[line] = data[line].strip()
			return data
	else:
		return None
	
def get_total_distance(origin, destinations, file=None):
	distance = 0
	for address in destinations:
		current_dist = get_dist_data(origin, address)
		if current_dist == None:
			return None
		distance += float(current_dist)
		if file:
			file.write('{}: {}\n'.format(address, current_dist))
	return distance
		
def main():
	base_address = easygui.enterbox(msg='Main Address: ')
	other_addresses = get_file_data()
	if other_addresses:
		if easygui.ynbox('Do you want to log data? '):
			filename = easygui.enterbox(msg='Enter Filename',title='Log File Name')
			if not filename:
				filename = 'default_log.txt'
			logfile = open(filename, 'at')
			total_distance = get_total_distance(base_address, other_addresses, logfile)
		else:
			total_distance = get_total_distance(base_address, other_addresses)
		if logfile:
			logfile.close()
		if total_distance:
			msg = '{} miles'.format(total_distance)
			easygui.msgbox(msg)
		else:
			easygui.msgbox('Error finding distance')
	else:
		easygui.msgbox('Error with Address File')
		
if __name__ in '__main__':
	main()

	
	

