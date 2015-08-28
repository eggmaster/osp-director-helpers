#!/bin/bash

echo "Killing Ceph"
  systemctl stop ceph || /bin/true
  pkill ceph-osd || /bin/true
  systemctl | grep ceph | awk '{ print $1 }' | xargs -n1 systemctl stop || /bin/true
  mount | grep ceph | awk '{ print $3 }' | xargs -n 1 umount || /bin/true
echo "DONE"

ZAP_COMMAND="ceph-disk zap"

if ! which ceph-disk > /dev/null 2>&1 ; then
  ZAP_COMMAND="sgdisk -Zog"
fi

echo "Zap Command is $ZAP_COMMAND"

DEV=$1
while [ "${DEV}" != "" ] ; do
  echo "On ${DEV}"
  ${ZAP_COMAND} ${DEV}
  partprobe ${DEV}
  shift
  DEV=$1
done

