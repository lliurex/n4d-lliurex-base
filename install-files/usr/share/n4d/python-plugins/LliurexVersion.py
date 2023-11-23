import os.path
import subprocess
import n4d.responses

class LliurexVersion:
	
	LLIUREX_VERSION_SUCCESS = 0
	LLIUREX_VERSION_NOT_FOUND = -20
	LLIUREX_VERSION_ERROR = -30
	_LLIUREX_VERSION_COMMAND_ = "/usr/bin/lliurex-version"
	
	def run_cmd(self, options = ""):
		if (os.path.exists(LliurexVersion._LLIUREX_VERSION_COMMAND_)):

			try:
				p=subprocess.Popen(LliurexVersion._LLIUREX_VERSION_COMMAND_+" " + options, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
				output, stderr = p.communicate()
				output = output.decode("utf-8")
				stderr = stderr.decode("utf-8")
				if (output == ""):
					output = stderr
				output = output.strip("\n")
				return (LliurexVersion.LLIUREX_VERSION_SUCCESS, output)

			except Exception as e:
				return (LliurexVersion.LLIUREX_VERSION_ERROR,str(e))

		else:
			return (LliurexVersion.LLIUREX_VERSION_NOT_FOUND,"{0} not found".format(LliurexVersion._LLIUREX_VERSION_COMMAND_))

	#def run_cmd

	def lliurex_version(self,options = ""):

		status, output = self.run_cmd(options)

		if (status < 0):
			return n4d.responses.build_failed_call_response(status, output)

		return n4d.responses.build_successful_call_response(output)
		
	#def lliurex_version
	
	def check_flavor(self, version):
		status, output = self.run_cmd()

		if (status < 0):
			return n4d.responses.build_failed_call_response(status, output)

		list_flavor = output.split(',')
		return n4d.responses.build_successful_call_response(version in list_flavor)

	#def check_flavor

	def flavors(self):
		status, output = self.run_cmd()

		if (status < 0):
			return n4d.responses.build_failed_call_response(status, output)

		list_flavor = output.split(',')
		return n4d.responses.build_successful_call_response(list_flavor[:-1])

	#def flavors

	def version(self):
		status, output = self.run_cmd()

		if (status < 0):
			return n4d.responses.build_failed_call_response(status, output)

		tmp = output.split(',')
		ver = tmp[-1].strip()
		return n4d.responses.build_successful_call_response(ver)

	#def version
	
#class LliurexVersion

if __name__=="__main__":
	
	llv=LliurexVersion()
	print(llv.lliurex_version())
