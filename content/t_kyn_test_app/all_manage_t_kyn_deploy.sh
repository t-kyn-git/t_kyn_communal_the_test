#!/bin/bash
# all_manage_t_kyn_deploy.sh
cd /workspaces/t_kyn_communal_the_test/content/t_kyn_test_app;pwd
./django_preinstall.sh
echo "=====view the app help====="
python manage_t_kyn.py
echo "=====run the app server====="
nohup python manage_t_kyn.py runserver > /dev/null 2>&1 &
ps -ef | grep manage_t_kyn.py
echo "=====run the app server done====="
