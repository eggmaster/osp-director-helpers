#!/bin/bash

source /home/stack/overcloudrc
keystone user-create --name sahara --pass sahara
keystone user-role-add --user sahara --role admin --tenant service
keystone service-create --name sahara --type data-processing --description "OpenStack Data Processing"
keystone endpoint-create --service sahara --publicurl 'http://127.0.0.1:8386/v1.1/%(tenant_id)s' --adminurl 'http://127.0.0.1:8386/v1.1/%(tenant_id)s' --internalurl 'http://127.0.0.1:8386/v1.1/%(tenant_id)s'
