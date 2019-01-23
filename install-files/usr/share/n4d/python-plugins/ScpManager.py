import paramiko
import scp
import os
import pwd
import grp
import multiprocessing


class ScpManager:
	
	def __init__(self):
		
		pass
		
	#def 
	
	def startup(self,options):
		
		pass
		
	#def 
	
	
	def send_file(self,user,password,ip,source,dest):
		
		try:
			
			client=paramiko.SSHClient()
			client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			client.connect(ip,username=user,password=password)
			scp_client= scp.SCPClient(client.get_transport())
			scp_client.put(source, dest)
			return {"status":True,"msg":""}
			
		except Exception as e:
			
			return {"status":False,"msg":str(e)}
		
	#def send_file
	
	def _get_file(self,user,password,ip,source,dest):
		
		dest_path="/".join(dest.split("/")[0:-1])
		if not os.path.exists(dest_path):
			e=Exception("ERROR: Destination folder does not exist")
			raise e

		client=paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		client.connect(ip,username=user,password=password)
		scp_client= scp.SCPClient(client.get_transport())
		scp_client.get(source,dest)
		
	#def _get_file
	
	def unrestricted_get_file(self,user,password,ip,source,dest):
		
		try:
			self._get_file(user,password,ip,source,dest)
			return {"status":True,"msg":""}
		except Exception as e:
			
			return {"status":False,"msg":str(e)}
			
	#def unrestricted_get_file
	
	def _check_access(self,user,path,ret_queue):
		
		user_info=pwd.getpwnam(user)
		
		# GROUP BEFORE UID !!!11
		os.setregid(user_info.pw_gid,user_info.pw_gid)
		os.setreuid(user_info.pw_uid,user_info.pw_uid)
		status=False
		
		status=os.access(path,os.W_OK)
		
		# ACL CHECK COULD GO HERE #
		# ################### #
		
		ret_queue.put(status)
		
	#def check_access
	
	def get_file(self,autocompleted_secured_user,remote_user,password,ip,source,dest):

		user=autocompleted_secured_user
		dest_path="/".join(dest.split("/")[0:-1])
		
		if os.path.exists(dest_path):
			ret_queue=multiprocessing.Queue()
			p=multiprocessing.Process(target=self._check_access,args=(user,dest_path,ret_queue))
			p.start()
			p.join()
			ok=ret_queue.get()
			if not ok:
				return {"status":False,"msg":"'%s' is not allowed to write in '%s'"%(user,dest_path)}
			
		try:
			
			self._get_file(remote_user,password,ip,source,dest)
			
			return {"status":True,"msg":""}
			
		except Exception as e:
			
			return {"status":False,"msg":str(e)}		
		
	#def get_file
	
	
#class ScpManager

if __name__=="__main__":
	

	pass

	