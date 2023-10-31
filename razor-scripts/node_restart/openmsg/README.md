# Run openmessaging locally

### 1. download open-messaging benchmark repo
download it elsewhere outside xinda repo, or add to .gitignore
```
git clone https://github.com/openmessaging/benchmark.git
```
### 2. check local java version and install jdk-11 if necessary
```
java -version
```
You should see output like:
```
1.0.20" 2023-07-18 LTS
Java(TM) SE Runtime Environment 18.9 (build 11.0.20+9-LTS-256)
Java HotSpot(TM) 64-Bit Server VM 18.9 (build 11.0.20+9-LTS-256, mixed mode)
```
If the second line Runtime Environment has version less than 18.x and build less than 11.x, install jdk-11 (elsewhere outside xinda repo, or add to .gitignore).
```
tar -xzf jdk-11.0.20_linux-x64.tar destination_dir
```
Export jdk-11 binary to system path. In `~/.bashrc`, add the following line, and replace `destination_dir`:
```
export PATH=destination_dir/jdk-11.0.20/bin:$PATH
```
Refresh `~/.bashrc``, and check java version. You should have JRE 18.9.
```
source ~/.bashrc
java -version
```
### 4. Build benchmark
```
cd benchmark
mvn install
```
### 5. Run driver and worker
First copy `run_driver.sh`, `run_worker1.sh`, and `run_worker2.sh` into `benchmark` folder. Make sure your ports `8082-8085` are not occupied, and kafka docker containers are already up. Then run the following three commands in `benchmark` directory from **different terminals**.
```
./run_worker1.sh
./run_worker2.sh
./run_driver.sh
```
