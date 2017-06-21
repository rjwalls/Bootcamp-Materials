#!/usr/bin/env bash

# Change to the script's directory
cd "$(dirname "$0")"

cp flag.orig flag

#unpack (-d) and be quiet about it (-qqq)
upx -qqq -d flag

strings -n 10 flag | grep ":)$" 
