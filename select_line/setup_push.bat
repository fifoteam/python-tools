echo off
echo %1
::½øÈëÄ¿Â¼
cd /d %1
@ start	"" "python" setup.py py2exe
@ rd __pycache__ /s/q
echo "python temp file del done!"
git add *
git commit -a -m "AUTO SAVED BY BAT FILE"
git push -u origin master
