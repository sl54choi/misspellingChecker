#!/bin/bash
cd /var/www/html/result
/usr/bin/python3.5 /var/www/html/wp-content/plugins/0misspelling-checker/includes/misspelling.py -i input.csv -o output.csv -l output.log
echo "start.sh run successful."
