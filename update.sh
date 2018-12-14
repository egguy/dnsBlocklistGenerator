#!/bin/bash

curl http://s3-us-west-1.amazonaws.com/umbrella-static/top-1m.csv.zip --compressed |zcat > top-1m.csv

mkdir blacklist
rsync -arpogvtPz rsync://ftp.ut-capitole.fr/blacklist blacklist/
