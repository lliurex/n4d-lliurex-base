def llxvars(var):

	if "VariablesManager" in objects:
		return objects["VariablesManager"].get_variable(var)
		
	else:
		
		return None