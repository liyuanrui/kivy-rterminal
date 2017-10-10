#!/system/bin/sh
DIR=${0%/*}
. $DIR/init.sh && $DIR/python-android5 $DIR/online.py "$@" && $DIR/end.sh

