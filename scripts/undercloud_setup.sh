#!/bin/bash

# Setup the Undercloud

rhsm_username=SECRET
rhsm_password=SECRET
rhsm_pool_id=SECRET
prov_network=CHANGEME
hostname=CHANGEME

echo "Setting up 'stack' user"
useradd stack
echo "Redhat1!" | passwd stack --stdin
echo "stack ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/stack
chmod 0440 /etc/sudoers.d/stack
su - stack -c "mkdir -p images templates"
echo "DONE"

echo "Setting up IP forwarding"
echo net.ipv4.ip_forward=1 >> /etc/sysctl.conf
sysctl -p /etc/sysctl.conf
echo "DONE"

echo "Setting hostname to ${hostname}"
hostnamectl set-hostname --static $hostname
hostnamectl set-hostname --transient $hostname
echo "DONE"

echo "Setting up /etc/hosts"
echo "127.0.0.1   $(hostname --fqdn) $(hostname --short)" > /etc/hosts
echo "DONE"

echo "Registering to Red Hat"
subscription-manager register --username=${rhsm_username} --password=${rhsm_password}
subscription-manager attach --pool=${rhsm_pool_id}
subscription-manager repos --disable=*
subscription-manager repos --enable=rhel-7-server-rpms --enable=rhel-7-server-optional-rpms --enable=rhel-7-server-extras-rpms --enable=rhel-7-server-openstack-7.0-rpms --enable=rhel-7-server-openstack-7.0-director-rpms
echo "DONE"

echo "Updating Packages"
yum update -y
yum install -y python-rdomanager-oscplugin
echo "DONE"

echo "Creating undercloud.conf"
bg="su - stack -c"
echo $bg "cp /usr/share/instack-undercloud/undercloud.conf.sample ~/undercloud.conf"
$bg "cp /usr/share/instack-undercloud/undercloud.conf.sample ~/undercloud.conf"
echo $bg "sed -i \"s/192\.0\.2\./${prov_network}/g\" undercloud.conf"
$bg "sed -i \"s/192\.0\.2\./${prov_network}/g\" undercloud.conf"
echo "Uncommenting lines"
for val in $(echo local_ip network_cidr undercloud_public_vip undercloud_admin_vip masquerade_network dhcp_start dhcp_end network_cider network_gateway discovery_iprange) ; do
  echo "Fixing ${val}"
  echo $bg "sed -i \"s/^#${val}/${val}/g\" ~/undercloud.conf"
  $bg "sed -i \"s/^#${val}/${val}/g\" ~/undercloud.conf"
done
$bg "sed -i \"s/#discovery_runbench = false/discovery_runbench = true/g\" undercloud.conf"
echo "DONE"

