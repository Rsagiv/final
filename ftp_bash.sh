#!/bin/bash
user='roeis'
passw='roei1234'
lftp -u $user,$passw -e "repeat mirror -R --Remove-source-files --parallel=3 --verbose /home/roeihafifot/tranfer_files" ftp://20.13.30.168