Sahara Templates

These are templates that have been vetted on RHEL OSP 7.1 Director.

Description:
This is a post config template that calls a python utility to execute the required steps to configure sahara.  This currently executes on all controller nodes.  This should be tested further in an HA deployment.

Requirements:
1) All baremetal controller nodes should be registered to satellite or upstream cdn to obtain the sahara rpms.

Instructions:

0. Deploy your overcloud
1. Create a subdirectory in your local templates directory `mkdir /home/stack/templates/sahara`
2. Place all files in your local templates directory (/home/stack/templates NOTE: this is hardcoded in some of the scripts so you will have to adjust if you use an alternate location)
3. Update the following template files to use the correct IP for your service
  * sahara-install.py: update the "sahara_ip" variable
  * sahara-prep-script.sh: replace 127.0.0.1 if wanted, 127.0.0.1 has tested successfully. To verify correct enpoints issue the following from the stack@undercloud:
    ```
source ~/overcloudrc
keystone endpoint-list
    ```
4. source overcloudrc and execute 'sahara-prep-script.sh'
5. Execute openstack overcloud deploy ... with the new templates added via -e /home/stack/templates/sahara-post-deploy.yaml

This update should only take a few moments.

Once completed, verify you are able to view sahara resources in horizon.
