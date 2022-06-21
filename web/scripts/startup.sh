#!/bin/bash

# Create the temp directory for the php-fpm module
if [ ! -d "/run/php-fpm" ];
then
    mkdir /run/php-fpm
fi

# start the php-fpm module
/usr/sbin/php-fpm

# start apache
/usr/sbin/httpd -D "FOREGROUND"