import os.path
import subprocess

class LliurexVersion:
	
	def lliurex_version(self,options=""):
		
		if os.path.exists("/usr/bin/lliurex-version"):
			
			try:
				p=subprocess.Popen("lliurex-version " + options,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
				output,stderr=p.communicate()
				if output=="":
					output=stderr
				output=output.strip("\n")
				return(True,output)
				
			except:
				return (False, "Error executing lliurex-version")
			
		else:
			return (False,"lliurex-version not found")
		
	#def lliurex_version
	
	def check_flavor(self,version):
		if os.path.exists("/usr/bin/lliurex-version"):
			
			try:
				p=subprocess.Popen(["lliurex-version"],stdout=subprocess.PIPE)
				output=p.communicate()[0]
				output=output.strip("\n")
				list_flavor = output.slipt(',')
				if version in list_flavor:
					return (True,"I'm a " + version)
				else:
					return (False,"I'm not a " + version)
			except:
				return (False, "Error executing lliurex-version")
			
		else:
			return (False,"lliurex-version not found")
	#def check_flavor
	
#class LliurexVersion

if __name__=="__main__":
	
	llv=LliurexVersion()
	print llv.lliurex_version()