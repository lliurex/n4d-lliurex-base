import exceptions
import n4d.responses

class FileUtils:

	NOT_ENOUGH_SPACE=-10
	PERMISSION_DENIED=-20

	def backup(self,target,dest_file):
		aux_temp = tempfile.mkdtemp()
		
		cmd="df " + os.path.dirname(dest_file) + " | awk 'END{print $4}'"
		available_space = int(subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE).communicate()[0].decode("utf-8").strip())
		cmd1="du -cs " + " ".join(target) + " | awk 'END{print $1}'"
		used_space = int(subprocess.Popen(cmd1,shell=True,stdout=subprocess.PIPE).communicate()[0].decode("utf-8").strip())
		if available_space < used_space * 0.05:
			return n4d.responses.build_failed_call_response(FileUtils.NOT_ENOUGH_SPACE)
		try:
			tar = tarfile.open(dest_file,'w:gz')
			for x in target:
				tar.add(x,arcname=x)
			if os.path.exists('/usr/bin/getfacl'):
				acl_folder = os.path.join(aux_temp,'._acls')
				os.makedirs(acl_folder)
				for x in target:
					os.system('getfacl -pR ' + x + ' > ' + os.path.join(acl_folder,os.path.basename(x)))
				tar.add(acl_folder,arcname='._acls')
				shutil.rmtree(acl_folder)
			tar.close()
			return n4d.responses.build_successful_call_response(dest_file)

		except exceptions.IOError as e:
			if e.errno == 28:
				shutil.rmtree(file_path)
				return n4d.responses.build_failed_call_response(FileUtils.NOT_ENOUGH_SPACE)
			else:
				return n4d.responses.build_failed_call_response(ret_msg=str(e))
		except Exception as e:
				return n4d.responses.build_failed_call_response(ret_msg=str(e))
	#def backup

	def restore(self,backup_file,dest):

		try:
			if os.path.exists(backup_file) :
				tmp_dir = tempfile.mkdtemp(dir=dest)
				tar = tarfile.open(backup_file)
				tar.extractall(tmp_dir)
				tar.close()
				
				cmd='rsync -ax --remove-source-files ' + tmp_dir + '/.??* ' + tmp_dir + '/* ' + dest 
				os.system(cmd)

				acl_folder = os.path.join(dest,'._acls')
				if os.path.exists(acl_folder):

					for x in os.listdir(acl_folder):
						os.system('setfacl -R --restore='+os.path.join(acl_folder,x))
				shutil.rmtree(os.path.join(dest,'._acls'))
				return n4d.responses.build_successful_call_response()

		except exceptions.IOError as e:
			if e.errno == 28:
				return n4d.responses.build_failed_call_response(FileUtils.NOT_ENOUGH_SPACE)
			else:
				return n4d.responses.build_failed_call_response(ret_msg=str(e))
		except Exception as e:
				return n4d.responses.build_failed_call_response(ret_msg=str(e))

	#def restore

	def listDir(self, user, path):
		exitstatus = os.system("su -c 'test -r %s' %s"%(path,user))
		if exitstatus == 0:
			result = {'folders':[],'files':[]}
			for root, folders, files in os.walk(path):
				result['folders'] = folders
				result['files'] = files
				break
			return n4d.responses.build_successful_call_response(result)
		
		return n4d.responses.build_failed_call_response(FileUtils.PERMISSION_DENIED,ret_msg="Permission denied")
		
	#de listDir