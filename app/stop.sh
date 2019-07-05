#!/bin/bash

ssh ubuntu@ec2-34-209-70-4.us-west-2.compute.amazonaws.com 'pkill -f preprocessing.py' &

ssh ubuntu@ec2-50-112-13-159.us-west-2.compute.amazonaws.com 'pkill -f producer.py'
