import time

def get_backup_name(plugin_name):
	
	timestamp=time.strftime("%d%m%Y_%H%M%S")
	
	return timestamp + "_" + plugin_name + ".tar.gz"
	
#def get_backup_name

