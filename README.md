# misspellingChecker for WordPress
*※ This guidance is based on Python 3.5.*
1. Prerequisites
* user define
```
sudo chown -R www-data:www-data /var/www/html
sudo chmod -R 755 /var/www/html
```
* sudo define: /etc/sudoders
```
# User privilege specification
root	ALL=(www-data) NOPASSWD: /var/www/html/wp-content/plugins/0misspelling-checker/includes/start.sh, /var/www/html/wp-content/plugins/0misspelling-checker/includes/exec.sh
www-data	ALL=(ALL) NOPASSWD: /var/www/html/wp-content/plugins/0misspelling-checker/includes/start.sh, /var/www/html/wp-content/plugins/0misspelling-checker/includes/exec.sh
```
* sudo define: /etc/sudoders.d/mysudoers
```
www-data	ALL=(ALL) NOPASSWD: /var/www/html/wp-content/plugins/0misspelling-checker/includes/start.sh, /var/www/html/wp-content/plugins/0misspelling-checker/includes/misspelling.py
```
2. References
* Log file: /var/www/html/result/error_output.txt
```
e.g.
Traceback (most recent call last):
  File "/var/www/html/wp-content/plugins/0misspelling-checker/includes/misspelling.py", line 6, in <module>
    import pandas as pd
ImportError: No module named 'pandas'
```
* Bash file for execution: /var/www/html/wp-content/plugins/0misspelling-checker/includes/start.sh
```
#!/bin/bash
cd /var/www/html/result
/usr/bin/python3.5 /var/www/html/wp-content/plugins/0misspelling-checker/includes/misspelling.py -i input.csv -o output.csv -l output.log
echo "start.sh run successful."
```
