import os.path
import subprocess
import n4d.responses

class LliurexVersion:
	
	LLIUREX_VERSION_NOT_FOUND=-20
	LLIUREX_VERSION_ERROR=-20
	
	
	def lliurex_version(self,options=""):
		
		if os.path.exists("/usr/bin/lliurex-version"):
			
			try:
				p=subprocess.Popen("lliurex-version " + options,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
				output,stderr=p.communicate()
				output=output.decode("utf-8")
				stderr=stderr.decode("utf-8")
				if output=="":
					output=stderr
				output=output.strip("\n")
				return n4d.responses.build_successful_call_response(output)
				
			except Exception as e:
				
				return n4d.responses.build_failed_call_response(LliurexVersion.LLIUREX_VERSION_ERROR,str(e))
			
		else:
			return n4d.responses.build_failed_call_response(LliurexVersion.LLIUREX_VERSION_NOT_FOUND)
		
	#def lliurex_version
	
	def check_flavor(self,version):
		if os.path.exists("/usr/bin/lliurex-version"):
			
			try:
				p=subprocess.Popen(["lliurex-version"],stdout=subprocess.PIPE)
				output=p.communicate()[0]
				output=output.strip("\n")
				list_flavor = output.slipt(',')
				if version in list_flavor:
					return n4d.responses.build_successful_call_response(True)
				else:
					return n4d.responses.build_successful_call_response(False)
			except:
				return n4d.responses.build_failed_call_response(LliurexVersion.LLIUREX_VERSION_ERROR,str(e))
			
		else:
			return n4d.responses.build_failed_call_response(LliurexVersion.LLIUREX_VERSION_NOT_FOUND)
			
	#def check_flavor
	
#class LliurexVersion

if __name__=="__main__":
	
	llv=LliurexVersion()
	print llv.lliurex_version()