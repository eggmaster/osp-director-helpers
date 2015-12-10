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
 rabbit_host_ips = "" #e.g. "x.x.x.x,y.y.y.y"
 
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
 print cmd(["openstack-config", "--set", "/etc/sahara/sahara.conf", "DEFAULT", "plugins", "hdp,cdh,vanilla"])
 print cmd(["openstack-config", "--set", "/etc/sahara/sahara.conf", "DEFAULT", "use_neutron", "true"])
 print cmd(["openstack-config", "--set", "/etc/sahara/sahara.conf", "DEFAULT", "verbose", "true"])
 print cmd(["openstack-config", "--set", "/etc/sahara/sahara.conf", "DEFAULT", "debug", "false"])
 print cmd(["openstack-config", "--set", "/etc/sahara/sahara.conf", "DEFAULT", "rabbit_hosts", rabbit_host_ips])
 print cmd(["openstack-config", "--set", "/etc/sahara/sahara.conf", "DEFAULT", "rpc_backend", "rabbit"])
 print cmd(["openstack-config", "--set", "/etc/sahara/sahara.conf", "DEFAULT", "rabbit_use_ssl", "false"])
 print cmd(["openstack-config", "--set", "/etc/sahara/sahara.conf", "DEFAULT", "rabbit_userid", "guest"])
 print cmd(["openstack-config", "--set", "/etc/sahara/sahara.conf", "DEFAULT", "rabbit_password", "guest"])
 print cmd(["openstack-config", "--set", "/etc/sahara/sahara.conf", "DEFAULT", "rabbit_ha_queues", "true"])

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

 no_firewall_rule = True
 iptables_save_output = cmd(["iptables-save"])
 for line in iptables_save_output:
  if re.search('8386', line):
   no_firewall_rule = False

 if no_firewall_rule:
  print cmd(["iptables", "-A", "INPUT", "-p", "tcp", "-m", "multiport", "--dports", "8386", "-j", "ACCEPT"])
  try:
   iptables_config_file = open("/etc/sysconfig/iptables","w")
   iptables_save_output = cmd(["iptables-save"])
   for line in iptables_save_output:
    iptables_config_file.write(line)
   iptables_config_file.close()
  except:
   print "persisting iptables rules failed!"

 print cmd(["systemctl", "enable", "openstack-sahara-api.service"])
 print cmd(["systemctl", "enable", "openstack-sahara-engine.service"])
 print cmd(["systemctl", "stop", "openstack-sahara-api.service"])
 print cmd(["systemctl", "stop", "openstack-sahara-engine.service"])

 #VERIFY: iiuc pcs will start up the sahara services following these commands
 try:
  print cmd(["pcs", "resource", "create", "sahara-all", "systemd:openstack-sahara-all", "--clone"])
  print cmd(["pcs", "constraint", "order", "start", "keystone-clone", "then", "sahara-all-clone"])
 except:
  print "pcs commands failed!"


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

