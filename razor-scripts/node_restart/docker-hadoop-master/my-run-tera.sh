input_dir=/tmp/tera-input
output_dir=/tmp/tera-output
docker exec -it namenode yarn jar /opt/hadoop-3.2.1/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.2.1.jar teragen 1000000 $input_dir
docker exec -it namenode yarn jar /opt/hadoop-3.2.1/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.2.1.jar terasort $input_dir $output_dir
