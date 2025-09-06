#!/bin/bash
# all_manage_t_kyn_stop.sh
cd /workspaces/t_kyn_communal_the_test/content/t_kyn_test_app;pwd
echo "=====run the app server====="
ps -ef | grep manage_t_kyn.py
ps -ef | grep manage_t_kyn.py | awk -F ' ' '{print $2}' | xargs kill -9
echo "=====run the app server done====="
