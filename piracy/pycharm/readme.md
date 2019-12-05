# For resetting the PyCharm 2018.1 trial on Windows 10, do the following

## Delete the following key file
(replace USERNAME with your window's account username):

` C:\Users\<USERNAME>\.PyCharm2018.1\config\eval\PyCharm181.evaluation.key
`
## Next, edit the file located in
`C:\Users\USERNAME\.PyCharm2018.1\config\options\options.xml` 

and remove all properties where the name begins with 

`evlsprt,` such as: `... property name="evlsprt3.171" value="18" />`

## Regedit

`HKEY_CURRENT_USER\Software\JavaSoft\Prefs\jetbrains\pycharm`

Next, within all the folders in here, delete all keys (i.e. they look like folders) where "evlsprt" is in the title.
You are done! Open up PyCharm to see that the trial period has been extended!
