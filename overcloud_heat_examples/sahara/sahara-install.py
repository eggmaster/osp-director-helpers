#!/usr/bin/python
import subprocess
import socket
import re

def install_sahara():
 haproxy_cfg_file = "/etc/haproxy/haproxy.cfg"
 sahara_pass = "sahara"
 sahara_internal_vip = ""
 sahara_external_vip = ""
 controller_0_ip = ""
 controller_1_ip = ""
 controller_2_ip = ""
 
 print cmd(["yum", "-y", "install", "openstack-sahara-api", "openstack-sahara-engine"])

 database_created = False
 try:
  print cmd(["mysql", "-u", "root","-e","create database sahara; grant all on sahara.* to 'sahara'@'%' identified by 'sahara';grant all on sahara.* to 'sahara'@'"+sahara_internal_vip+"' identified by 'sahara';"])
  database_created = True
 except:
  print "Database already created!"

 print cmd(["openstack-config", "--set", "/etc/sahara/sahara.conf", "database", "connection", "mysql://sahara:sahara@"+sahara_internal_vip+"/sahara"])

 #We only want to run sahara-db-manage if the mysql database was created during the current run.
 #Otherwise we assume this script has already been run and we don't want to blow away the db.
 if database_created:
  print cmd(["sahara-db-manage", "--config-file", "/etc/sahara/sahara.conf", "upgrade", "head"])

 print cmd(["openstack-config", "--set", "/etc/sahara/sahara.conf", "keystone_authtoken", "auth_uri", "http://"+sahara_internal_vip+":5000/v2.0/"])
 print cmd(["openstack-config", "--set", "/etc/sahara/sahara.conf", "keystone_authtoken", "identity_uri", "http://"+sahara_internal_vip+":35357"])
 print cmd(["openstack-config", "--set", "/etc/sahara/sahara.conf", "keystone_authtoken", "admin_tenant_name", "service"])
 print cmd(["openstack-config", "--set", "/etc/sahara/sahara.conf", "keystone_authtoken", "admin_user", "sahara"])
 print cmd(["openstack-config", "--set", "/etc/sahara/sahara.conf", "keystone_authtoken", "admin_password", "sahara"])
 print cmd(["openstack-config", "--set", "/etc/sahara/sahara.conf", "DEFAULT", "use_neutron", "true"])

#test to see if haproxy.cfg has already been adjusted

 proxy_cfg_adjusted = False
 proxy_conf = open(haproxy_cfg_file,"r")
 for line in proxy_conf:
  if re.search('listen sahara',line):
   proxy_cfg_adjusted = True
 proxy_conf.close()

 if not proxy_cfg_adjusted:
  proxy_conf = open(haproxy_cfg_file,"a")
  proxy_conf.write("\n\n")
  proxy_conf.write("listen sahara\n")
  proxy_conf.write("  bind %s:8386\n" % sahara_internal_vip)
  proxy_conf.write("  bind %s:8386\n" % sahara_external_vip)
  proxy_conf.write("  server overcloud-controller-0 %s:8386 check fall 5 inter 2000 rise 2\n" % controller_0_ip)
  proxy_conf.write("  server overcloud-controller-1 %s:8386 check fall 5 inter 2000 rise 2\n" % controller_1_ip)
  proxy_conf.write("  server overcloud-controller-2 %s:8386 check fall 5 inter 2000 rise 2\n" % controller_2_ip)
  proxy_conf.close()
 else:
  print "INFO: Not adjusting haproxy.cfg since it appears to have the sahara config already"

 print cmd(["systemctl", "start", "openstack-sahara-api.service"])
 print cmd(["systemctl", "start", "openstack-sahara-engine.service"])
 print cmd(["systemctl", "enable", "openstack-sahara-api.service"])
 print cmd(["systemctl", "enable", "openstack-sahara-engine.service"])

def cmd(args):
    return subprocess.check_output(args)

def main():
 hostname = socket.gethostname()
 if "controller" in hostname:
  print("This is a controller node... continuing")
  install_sahara()
 else:
  print("Not running on a controller node, so I'm not doing anything")

if __name__ == '__main__':
	main()

