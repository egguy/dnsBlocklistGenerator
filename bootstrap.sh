#!/bin/sh

curl http://s3-us-west-1.amazonaws.com/umbrella-static/top-1m.csv.zip > top-1m.csv.zip
unzip -o top-1m.csv.zip 
rm top-1m.csv.zip

rsync -arpogvt rsync://ftp.ut-capitole.fr/blacklist blacklist/
