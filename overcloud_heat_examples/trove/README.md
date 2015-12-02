Trove Templates

These are WIP templates.

Description:
This is a post config template that calls a python utility to execute the required steps to configure trove.  This currently executes on all controller nodes.  This should be tested further in an HA deployment.


Instructions:

1) Deploy your overcloud
2) Place all files in your local templates directory (ie /home/stack/templates) 
3) Update the following template files to use the correct IP for your service
	- trove-install.py: update FIXME
	- trove-prep-script.sh: FIXME
	   source ~/overcloudrc
           keystone endpoint-list
4) source overcloudrc and execute 'trove-prep-script.sh'
5) Execute openstack overcloud deploy ... with the new templates added via -e /home/stack/templates/trove-post-deploy.yaml

This update should only take a few moments.

Once completed, verify you are able to view trove resources in horizon.
