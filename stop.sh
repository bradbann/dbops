#!/usr/bin/env bash
ps -ef |grep dbops |awk '{print $2}' | xargs kill -9
