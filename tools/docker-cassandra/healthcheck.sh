if [[ "$(nodetool status | grep 'UN ' | awk '{print $2}' | wc -l)" == 2 ]]
then
	exit 0
else
	exit 1
fi
