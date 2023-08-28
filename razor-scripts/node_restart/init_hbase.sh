# echo "n_splits = 200
# create 'usertable', 'family', {SPLITS => (1..n_splits).map {|i| 'user#{1000+i*(9999-1000)/n_splits}'}}" > /tmp/init_hbase.sh
# n_splits = 200
# create 'usertable', 'family', {SPLITS => (1..n_splits).map {|i| 'user#{1000+i*(9999-1000)/n_splits}'}}
echo "n_splits = 200" | ./opt/hbase-1.2.6/bin/hbase shell
echo "create 'ssss', 'family', {SPLITS => (1..n_splits).map {|i| 'user#{1000+i*(9999-1000)/n_splits}'}}" | ./opt/hbase-1.2.6/bin/hbase shell
