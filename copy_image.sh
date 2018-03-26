#!/usr/bin/sh
echo "Pre test"
scp pi@192.168.43.144:/home/pi/HackUVA/images/image.jpg ~/Code/HackUVA/images/image.jpg
echo "Post test"
exit 0