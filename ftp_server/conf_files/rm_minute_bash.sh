#!/bin/bash
sudo find /ftphome/tranfer_files/ -type f -maxdepth 1 -cmin +1 -delete
