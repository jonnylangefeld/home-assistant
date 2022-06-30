#!/bin/bash

backup_name=$1
encryption_key=$2

gpg --batch --passphrase "${encryption_key}" ${backup_name}

backup_name=$(echo ${backup_name} | sed "s/.gpg//g")
mkdir /tmp/restore
tar xf ${backup_name} -C /tmp/restore

mkdir restore
tar xf /tmp/restore/homeassistant.tar.gz -C ./restore
