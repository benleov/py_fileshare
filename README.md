py_fileshare
=============================

This script generates unique HTTP URL's for every file in a given directory, meaning you can give a user the link in the format http://server/files/index.py?file=12386123978624914, which will then provide a download link for a given file. Providing the directory doesnt have browse access, the scripts allow you to give anonymous access to a particular file. 

NOTE: It is NOT very secure; if a user guesses any file in that directory it will allow access. This is NOT designed as a secure way to distribute sensitive data. 

Requirements
-------------------------------

To run these files you need [mod python](http://modpython.org/) enabled on your [Apache](http://www.apache.org/) server.

Usage: index.py
-------------------------------

This script is designed to take a file parameter on the URL...i.e if this was in a file called index.py, you could execute it with index.py?file=1923782936025293856 from your browser, where that long number is the MD hash of the file you want. 

In Apache, setup the directory where you will host the files as follows.

```

<Directory /var/www/files>

Options -Indexes FollowSymLinks MultiViews
AllowOverride AuthConfig

Order allow,deny
Allow from all

AddHandler mod_python .py
PythonHandler mod_python.publisher
PythonDebug On
</Directory>

```

This will allow any python script in /var/www/files to be executed by the python handler.

Usage: list_files.py
-------------------------------

This file will print out the unique URL's for all the files in the scripts directory. You will want to password protet this file. To do so, configure Apache to restrct it, with something like this.


```
<Location /files/list_file.py>
AuthType Basic
AuthName "AuthName"

AuthUserFile /files/htpasswd
Require valid-user
</Location>
```

in the virtual host tag add this, substituting list_files.py for the location that you put the script above, and /files/htpasswd with the file that contains the passwords of valid users.



