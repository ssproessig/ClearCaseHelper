# ClearCaseHelper #
A collection of some clearcase helpers I found useful.

## ct-update-changelog ##
### Description ###
A command-line helper that takes the .updt result file of a "cleartool update" call and extracts all author and commit message for every change in that .updt file.

### Usage ###
<pre>
D:\myview>cleartool update
...
...
D:\myview>ct-update-changelog -u update.2012-11-30T110925+0100.updt
Collecting update information for 'update.2012-11-30T110925+0100.txt'...

[file.txt]
1->2: ssproess: added sample content
</pre>

### Requirements ###
* tested with Python 2.7

### Creating a Windows .exe ###
* install py2exe  [see http://www.py2exe.org/]
<pre>
D:\ClearCaseHelper\ct-update-changelog>python setup.py py2exe
...
D:\ClearCaseHelper\ct-update-changelog>cd dist
D:\ClearCaseHelper\ct-update-changelog\dist>dir ct-update-changelog.exe
</pre>
