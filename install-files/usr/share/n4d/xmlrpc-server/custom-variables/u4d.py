import os, os.path, shutil, grp, pwd, stat, exceptions, inspect
def n4d_mv(orig,dest,force_permission=False,owner=None,group=None,perm=None,create_path=False):
	if (os.path.exists(dest)):
		file_stat = os.stat(dest)
		shutil.move(orig,dest)
		uid = file_stat.st_uid
		gid = file_stat.st_gid
		perm_file = file_stat.st_mode
		if(force_permission):
			if(owner != None):
				uid = pwd.getpwnam(owner).pw_uid
			if(group != None):
				gid = grp.getgrnam(group).gr_gid
			if(perm != None):
				perm_file = int(perm,8)
		os.chmod(dest,perm_file)
		os.chown(dest,uid,gid)
		return True
	else:
		if( not os.path.exists(os.path.dirname(dest))):
			if(create_path):
				os.makedirs(os.path.dirname(dest))
			else:
				return False
		shutil.move(orig,dest)
		uid = 0
		gid = 0
		if(owner != None):
			uid = pwd.getpwnam(owner).pw_uid
		if(group != None):
			gid = grp.getgrnam(group).gr_gid
		if(perm != None):
			os.chmod(dest,int(perm,8))
		os.chown(dest,uid,gid)
		return True
def _n4d_get_user():
        s=inspect.stack()
        for item in s:
                if item[3]=="_dispatch" and "core.py" in item[1]:
                        user = inspect.getargvalues(item[0]).locals["user"]
                        password = inspect.getargvalues(item[0]).locals["password"]
			method = inspect.getargvalues(item[0]).locals["method"]
                        class_name = inspect.getargvalues(item[0]).locals["class_name"]
                        return {'user':user,'pass':password,'method':method,'class':class_name}
	return {}

