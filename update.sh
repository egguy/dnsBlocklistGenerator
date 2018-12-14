#!/bin/bash

mkdir blacklist
rsync -arpogvtPz rsync://ftp.ut-capitole.fr/blacklist blacklist/
