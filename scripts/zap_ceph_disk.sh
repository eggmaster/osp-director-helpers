#!/bin/bash

echo "Killing Ceph"
systemctl stop ceph || /bin/true
pkill ceph || /bin/true
systemctl | grep ceph | awk '{ print $1 }' | xargs -n1 systemctl stop || /bin/true
echo "DONE"

DEV=$1
while [ "${DEV}" != "" ] ; do
  echo "On ${DEV}"
  mount -a | egrep "^${DEV}" | awk '{ print $3 }' | xargs -n 1 umount
  ceph-disk zap ${DEV}
  partprobe ${DEV}
  ceph-disk zap ${DEV}
  gdisk ${DEV}
  shift
  DEV=$1
done
  
