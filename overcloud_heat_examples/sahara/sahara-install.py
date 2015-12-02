#!/usr/bin/python
import subprocess
import socket


def install_sahara():
 sahara_pass = "sahara"
 sahara_ip = "192.168.1.10"

 print cmd(["yum", "-y", "install", "openstack-sahara-api", "openstack-sahara-engine"])
 print cmd(["mysql", "-u", "root","-e","create database sahara; grant all on sahara.* to 'sahara'@'%' identified by 'sahara';grant all on sahara.* to 'sahara'@'"+sahara_ip+"' identified by 'sahara';"])
 print cmd(["openstack-config", "--set", "/etc/sahara/sahara.conf", "database", "connection", "mysql://sahara:sahara@"+sahara_ip+"/sahara"])
 print cmd(["sahara-db-manage", "--config-file", "/etc/sahara/sahara.conf", "upgrade", "head"])
 print cmd(["openstack-config", "--set", "/etc/sahara/sahara.conf", "keystone_authtoken", "auth_uri", "http://"+sahara_ip+":5000/v2.0/"])
 print cmd(["openstack-config", "--set", "/etc/sahara/sahara.conf", "keystone_authtoken", "identity_uri", "http://"+sahara_ip+":35357"])
 print cmd(["openstack-config", "--set", "/etc/sahara/sahara.conf", "keystone_authtoken", "admin_tenant_name", "service"])
 print cmd(["openstack-config", "--set", "/etc/sahara/sahara.conf", "keystone_authtoken", "admin_user", "sahara"])
 print cmd(["openstack-config", "--set", "/etc/sahara/sahara.conf", "keystone_authtoken", "admin_password", "sahara"])
 print cmd(["openstack-config", "--set", "/etc/sahara/sahara.conf", "DEFAULT", "use_neutron", "true"])
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

