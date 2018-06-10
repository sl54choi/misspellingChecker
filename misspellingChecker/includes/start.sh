#!/bin/bash
cd /var/www/html/result
#/usr/bin/python3.5 /var/www/html/wp-content/plugins/0misspelling-checker/includes/misspelling.py -i input.csv -o output.csv -l output.log
/usr/bin/python3.5 $1 -i $2 -o $3 -l $4 -t $5
#sudo ./start.sh /var/www/html/wp-content/plugins/0misspelling-checker/includes/misspelling.py "" /var/www/html/result/output.csv. /var/www/html/result/output.log https://aws.amazon.com/freertos
