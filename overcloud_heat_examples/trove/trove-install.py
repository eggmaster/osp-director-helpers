#!/usr/bin/python
import subprocess
import socket


def install_trove():
 #set these
 trove_pass = "trovetest"
 trove_ip = "192.168.1.10"
 controller_vip=""
 
 print cmd(["yum","install","-y","openstack-trove","python-troveclient"])
 print cmd(["openstack-config","--set","/etc/trove/trove.conf","DEFAULT","bind_host","192.168.1.22X"])
 print cmd(["openstack-config","--set","/etc/trove/trove.conf","DEFAULT","log_dir","/var/log/trove"])
 print cmd(["openstack-config","--set","/etc/trove/trove.conf","DEFAULT","trove_auth_url","http://"+controller_vip+":35357/v2.0"])
 print cmd(["openstack-config","--set","/etc/trove/trove.conf","DEFAULT","os_region_name","regionOne"])
 print cmd(["openstack-config","--set","/etc/trove/trove.conf","oslo_messaging_rabbit","rabbit_hosts","hacontroller1,hacontroller2,hacontroller3"])
 print cmd(["openstack-config","--set","/etc/trove/trove.conf","oslo_messaging_rabbit","rabbit_ha_queues","true"])
 print cmd(["openstack-config","--set","/etc/trove/trove.conf","oslo_messaging_rabbit","rabbit_password","guest"])
 print cmd(["openstack-config","--set","/etc/trove/trove.conf","DEFAULT","rpc_backend","rabbit"])
 print cmd(["openstack-config","--set","/etc/trove/trove.conf","database","connection","","mysql://trove:"+trove_pass+"@"+controller_vip+"/trove"])
 print cmd(["openstack-config","--set","/etc/trove/trove.conf","database","max_retries","-1"])
 print cmd(["openstack-config","--set","/etc/trove/trove.conf","keystone_authtoken","admin_tenant_name","services"])
 print cmd(["openstack-config","--set","/etc/trove/trove.conf","keystone_authtoken","admin_user","trove"])
 print cmd(["openstack-config","--set","/etc/trove/trove.conf","keystone_authtoken","admin_password",trove_pass])
 print cmd(["openstack-config","--set","/etc/trove/trove.conf","keystone_authtoken","service_host",controller_vip])
 print cmd(["openstack-config","--set","/etc/trove/trove.conf","keystone_authtoken","identity_uri","http://"+controller_vip+":35357/"])
 print cmd(["openstack-config","--set","/etc/trove/trove.conf","keystone_authtoken","auth_uri","http://"+controller_vip+":35357/v2.0"])
 print cmd(["openstack-config","--set","/etc/trove/trove.conf","DEFAULT","control_exchange","trove"])

 print cmd(["openstack-config","--set","/etc/trove/trove-conductor.conf","DEFAULT","trove_auth_url","http://"+controller_vip+":35357/v2.0"])
 print cmd(["openstack-config","--set","/etc/trove/trove-conductor.conf","DEFAULT","os_region_name","regionOne"])
 print cmd(["openstack-config","--set","/etc/trove/trove-conductor.conf","DEFAULT","log_file","trove-conductor.log"])
 print cmd(["openstack-config","--set","/etc/trove/trove-conductor.conf","oslo_messaging_rabbit","rabbit_hosts","hacontroller1,hacontroller2,hacontroller3"])
 print cmd(["openstack-config","--set","/etc/trove/trove-conductor.conf","oslo_messaging_rabbit","rabbit_ha_queues","true"])
 print cmd(["openstack-config","--set","/etc/trove/trove-conductor.conf","oslo_messaging_rabbit","rabbit_password","guest"])
 print cmd(["openstack-config","--set","/etc/trove/trove-conductor.conf","DEFAULT","rpc_backend","rabbit"])
 print cmd(["openstack-config","--set","/etc/trove/trove-conductor.conf","database","connection","","mysql://trove:"+trove_pass+"@"+controller_vip+"/trove"])
 print cmd(["openstack-config","--set","/etc/trove/trove-conductor.conf","database","max_retries","-1"])
 print cmd(["openstack-config","--set","/etc/trove/trove-conductor.conf","keystone_authtoken","admin_tenant_name","services"])
 print cmd(["openstack-config","--set","/etc/trove/trove-conductor.conf","keystone_authtoken","admin_user","trove"])
 print cmd(["openstack-config","--set","/etc/trove/trove-conductor.conf","keystone_authtoken","admin_password",trove_pass])
 print cmd(["openstack-config","--set","/etc/trove/trove-conductor.conf","keystone_authtoken","service_host",controller_vip])
 print cmd(["openstack-config","--set","/etc/trove/trove-conductor.conf","keystone_authtoken","identity_uri","http://"+controller_vip+":35357/"])
 print cmd(["openstack-config","--set","/etc/trove/trove-conductor.conf","keystone_authtoken","auth_uri","http://"+controller_vip+":35357/v2.0"])
 print cmd(["openstack-config","--set","/etc/trove/trove-conductor.conf","DEFAULT","control_exchange","trove"])

 print cmd(["openstack-config","--set","/etc/trove/trove-taskmanager.conf","DEFAULT","trove_auth_url","http://"+controller_vip+":35357/v2.0"])
 print cmd(["openstack-config","--set","/etc/trove/trove-taskmanager.conf","DEFAULT","os_region_name","regionOne"])
 print cmd(["openstack-config","--set","/etc/trove/trove-taskmanager.conf","oslo_messaging_rabbit","rabbit_hosts","hacontroller1,hacontroller2,hacontroller3"])
 print cmd(["openstack-config","--set","/etc/trove/trove-taskmanager.conf","oslo_messaging_rabbit","rabbit_ha_queues","true"])
 print cmd(["openstack-config","--set","/etc/trove/trove-taskmanager.conf","oslo_messaging_rabbit","rabbit_password","guest"])
 print cmd(["openstack-config","--set","/etc/trove/trove-taskmanager.conf","DEFAULT","rpc_backend","rabbit"])
 print cmd(["openstack-config","--set","/etc/trove/trove-taskmanager.conf","DEFAULT","nova_proxy_admin_user","trove"])
 print cmd(["openstack-config","--set","/etc/trove/trove-taskmanager.conf","DEFAULT","nova_proxy_admin_pass",trove_pass])
 print cmd(["openstack-config","--set","/etc/trove/trove-taskmanager.conf","DEFAULT","nova_proxy_admin_tenant_name","${SERVICES_TENANT_ID}"])
 print cmd(["openstack-config","--set","/etc/trove/trove-taskmanager.conf","DEFAULT","log_file","trove-taskmanager.log"])
 print cmd(["openstack-config","--set","/etc/trove/trove-taskmanager.conf","database","connection","","mysql://trove:"+trove_pass+"@"+controller_vip+"/trove"])
 print cmd(["openstack-config","--set","/etc/trove/trove-taskmanager.conf","database","max_retries","-1"])
 print cmd(["openstack-config","--set","/etc/trove/trove-taskmanager.conf","keystone_authtoken","admin_tenant_name","services"])
 print cmd(["openstack-config","--set","/etc/trove/trove-taskmanager.conf","keystone_authtoken","admin_user","trove"])
 print cmd(["openstack-config","--set","/etc/trove/trove-taskmanager.conf","keystone_authtoken","admin_password",trove_pass])
 print cmd(["openstack-config","--set","/etc/trove/trove-taskmanager.conf","keystone_authtoken","service_host",controller_vip])
 print cmd(["openstack-config","--set","/etc/trove/trove-taskmanager.conf","keystone_authtoken","identity_uri","http://"+controller_vip+":35357/"])
 print cmd(["openstack-config","--set","/etc/trove/trove-taskmanager.conf","keystone_authtoken","auth_uri","http://"+controller_vip+":35357/v2.0"])
 print cmd(["openstack-config","--set","/etc/trove/trove-taskmanager.conf","DEFAULT","cloudinit_loaction","/etc/trove/cloudinit"])
 print cmd(["openstack-config","--set","/etc/trove/trove-taskmanager.conf","DEFAULT","network_driver","trove.network.neutron.NeutronDriver"])
 print cmd(["openstack-config","--set","/etc/trove/trove-taskmanager.conf","DEFAULT","control_exchange","trove"])
 print cmd(["openstack-config","--set","/etc/trove/trove-taskmanager.conf","DEFAULT","exists_notification_transformer"])

 print cmd(["openstack-config","--set","/etc/trove/trove.conf","DEFAULT","default_datastore","mysql"])
 print cmd(["openstack-config","--set","/etc/trove/trove.conf","DEFAULT","add_addresses","True"])
 print cmd(["openstack-config","--set","/etc/trove/trove.conf","DEFAULT","network_label_regex","^private$"])

 print cmd(["cp","/usr/share/trove/trove-dist-paste.ini","/etc/trove/api-paste.ini"])
 print cmd(["openstack-config","--set","/etc/trove/api-paste.ini","filter:authtoken","auth_uri","http://"+controller_vip+":35357/"])
 print cmd(["openstack-config","--set","/etc/trove/api-paste.ini","filter:authtoken","identity_uri","http://"+controller_vip+":35357/"])
 print cmd(["openstack-config","--set","/etc/trove/api-paste.ini","filter:authtoken","admin_password",trove_pass])
 print cmd(["openstack-config","--set","/etc/trove/api-paste.ini","filter:authtoken","admin_user","trove"])
 print cmd(["openstack-config","--set","/etc/trove/api-paste.ini","filter:authtoken","admin_tenant_name","services"])
 print cmd(["openstack-config","--set","/etc/trove/trove.conf","DEFAULT","api_paste_config","/etc/trove/api-paste.ini"])


def cmd(args):
    return subprocess.check_output(args)

def main():
 hostname = socket.gethostname()
 if "controller" in hostname:
  print("This is a controller node... continuing")
  install_trove()
 else:
  print("Not running on a controller node, so I'm not doing anything")

if __name__ == '__main__':
	main()

