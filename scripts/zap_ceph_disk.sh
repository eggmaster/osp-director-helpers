#!/bin/bash

DEV=$1
while [ "${DEV}" != "" ] ; do
  partprobe ${DEV}
  sgdisk --zap-all ${DEV}
  partprobe ${DEV}
  ceph-disk zap ${DEV}
  shift
  DEV=$1
done
  
