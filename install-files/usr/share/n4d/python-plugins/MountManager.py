import ctypes
import ctypes.util
import pwd
import re
import lliurex.net
import os
import os.path
import shutil
import tempfile

import n4d.responses

def mm_check_user(f):
	
	def wrap(*args,**kw):
		try:
			if f.func_name=="restricted_mount":
				check=args[3]
			elif f.func_name=="restricted_umount":
				check=args[2]
			else:
				check=""
			user_dir=pwd.getpwnam(args[1])
			if user_dir.pw_dir not in check:
				return False
			return f(*args)
			
		except Exception as e:
			print(e)
			return False
			
	return wrap

class MtabParser:
	
	def __init__(self):
		
		self.lines=[]
		self.mtab="/etc/mtab"
		
	#def init
	
	def open(self):
	
		
		f=open(self.mtab)
		self.lines=f.readlines()
		f.close()
		
		#print self.lines
	
	#def open
	
	def add_line(self,info):
		
		try:
		
			if len(self.lines)>0:
				if type(info)==type({}):
					for item in ["dev","mountpoint","type","options","dump","pass"]:
						if item not in info:
							return -1
			else:
				return -1
			
			line="%s\t%s\t%s\t%s\t%s\t%s\n"%(info["dev"],info["mountpoint"],info["type"],info["options"],info["dump"],info["pass"])
			self.lines.append(line)
			path=tempfile.mktemp()
			f=open(path,"w")
			f.writelines(self.lines)
			f.close()
			#print path
			shutil.move(path,self.mtab)
			return 0
			
		except:
			return -1
		
	#def add_line
	
#class FstabParser


class MountManager:
	
	MOUNT_LOG="/var/log/n4d/mountmanager"
	MOUNT_FAILED=-10
	
	def __init__(self):
		
		self.libc=ctypes.CDLL(ctypes.util.find_library("c"))
		
	#def init
	
	def test(self):
		
		pass
		
	#def test
	
	def log(self,e):
		
		try:
			f=open(MountManager.MOUNT_LOG,"w")
			f.write("[MountManager] " + str(e) + "\n")
			f.close()
		except:
			pass
		
	#def log
	
	def mount(self,source,target,type_,args):
		
		try:
			ret=self.libc.mount(source,target,type_,0,args)
			if ret==0:
				return n4d.responses.build_successful_call_response()
			else:
				return n4d.responses.build_failed_call_response(MountManager.MOUNT_FAILED)
				
		except Exception as e:
			#self.log(e)
			return n4d.responses.build_failed_call_response(ret_msg=str(e))

		
	#def mount
	
	@mm_check_user
	def restricted_mount(self,user,source,target,type_,args):
		try:
			target=target.encode("utf-8")
			try:
				#rule="\\\\\\\\\S+\\\\"
				rule="//\S+/"
				#print source
				x=re.match(rule,source)
				#print x
				hst=x.group().strip("/")
				
				if not lliurex.net.is_valid_ip(hst):
					ret=lliurex.net.get_ip_from_host(hst)
					if ret!=None:
						#source=source.replace(hst,ret)
						args+=",addr="+ret
						
			except Exception as e:
				print(e)
				
			mnt_list=self._mount_list()
			if source in mnt_list:
				for src_item in mnt_list[source]:
					if src_item["dst"]==target:
						return n4d.responses.build_successful_call_response()
				
			if not os.path.exists(target):
				prevmask = os.umask(0)
				os.makedirs(target)
				user_uid=pwd.getpwnam(user)[2]
				user_gid=pwd.getpwnam(user)[3]			
				os.chown(target,user_uid,user_gid)
				os.umask(prevmask)
				
			
			ret=self.libc.mount(ctypes.c_char_p(source),ctypes.c_char_p(target),ctypes.c_char_p(type_),0,ctypes.c_char_p(args))
			if ret==0:
				mp=MtabParser()
				mp.open()
				info={}
				info["dev"]=source
				info["mountpoint"]=target
				info["type"]=type_
				info["options"]=re.sub(",password=\w+","",args)
				info["dump"]=0
				info["pass"]=0
				mp.add_line(info)
				
				return n4d.responses.build_successful_call_response()
			else:
				return n4d.responses.build_failed_call_response(MountManager.MOUNT_FAILED)
				
		except Exception as e:
			print(e)
			return n4d.responses.build_failed_call_response(ret_msg=str(e))

		
	#def restricted_mount
	
	def umount(self,mounted_dir):

		try:
			ret=self.libc.umount(mounted_dir)
			return n4d.responses.build_successful_call_response()
		except Exception as e:
			#self.log(e)
			return n4d.responses.build_failed_call_response(ret_msg=str(e))
	
	#def umount
	
	@mm_check_user
	def restricted_umount(self,user,mounted_dir,lazy=False):
	
		try:
			if not lazy:
				ret=self.libc.umount(mounted_dir)
			else:
				ret=self.libc.umount2(mounted_dir,ctypes.c_int(2))

			if ret==0:
				return n4d.responses.build_successful_call_response()
			else:
				return n4d.responses.build_failed_call_response(MountManager.MOUNT_FAILED)
				
		except Exception as e:
			self.log(e)
			return n4d.responses.build_failed_call_response(ret_msg=str(e))
		
	#def restricted_umount
	
	def _mount_list(self):
		
		f=open("/proc/mounts")
		lines=f.readlines()
		f.close()
		mnt={}
		for line in lines:
			src,dst,ft,opts,dump,pass_=line.split(" ")
			pass_=pass_.strip("\n")
			opts=opts.split(",")
			tmp={}
			
			tmp["dst"]=dst
			tmp["fstype"]=ft
			tmp["options"]=opts
			tmp["dump"]=dump
			tmp["pass"]=pass_
			#print(src,dst,ft,opts,a,b)
			
			if src not in mnt:
				mnt[src]=[]
			
			mnt[src].append(tmp)
		'''
		for item in mnt:
			print(item)
			for item2 in mnt[item]:
				print("\t"+ item2 +" : " + str(mnt[item][item2]))
		'''
		return mnt
		
	#def mount_list
	
	def is_src_mounted(self,src,username=None):
		
		mnt_list=self.mount_list()
		
		if src in mnt_list:
			
			if username==None:
				return n4d.responses.build_successful_call_response((True,mnt_list[src][0]["dst"]))
			
			for item in mnt_list[src]:
				if "options" in item:
					if "username="+username in item["options"]:
						return n4d.responses.build_successful_call_response((True,item["dst"]))
		
		return n4d.responses.build_successful_call_response((False,None))
		
	#def  is_src_mounted
	

#class MountManager

if __name__=="__main__":
	
	mm=MountManager()
	
	print(mm.mount_list())
