echo "n_splits = 30; create 'usertable', 'family', {SPLITS => (1..n_splits).map {|i| \"user#{1000+i*(9999-1000)/n_splits}\"}}" | ./opt/hbase-2.5.6/bin/hbase shell
