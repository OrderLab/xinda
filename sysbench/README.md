```
git clone https://github.com/akopytov/sysbench.git
```
In the file `sysbench/src/drivers/mysql/drv_mysql.c`, modify `MYSQL_OPT_COMPRESSION_ALGORITHMS` in line 420 to be `MYSQL_OPT_COMPRESS`.
```
cd sysbench
./autogen.sh
./configure --with-pgsql
make -j
./src/sysbench --help
```
check `Compiled-in database drivers:` has `mysql` and `pgsql`
```
cd src/lua
../sysbench oltp_write_only.lua --pgsql-host=localhost --pgsql-port=26257 --pgsql-db=testdb --pgsql-user=root --pgsql-password= --table_size=100000 --tables=3 --threads=1 --db-driver=pgsql prepare

../sysbench oltp_write_only.lua --pgsql-host=localhost --pgsql-port=26257 --pgsql-db=testdb --pgsql-user=root --pgsql-password= --table_size=1000000 --tables=3 --threads=1 --time=20 --report-interval=5 --db-driver=pgsql run

../sysbench oltp_write_only.lua --pgsql-host=localhost --pgsql-port=26257 --pgsql-db=testdb --pgsql-user=root --pgsql-password= --table_size=100000 --tables=3 --threads=1 --db-driver=pgsql cleanup
```