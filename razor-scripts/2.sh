loc=~/ycsb-my/faults-meeting4/faults/
status_para_ary=(1 2 3 4 5)
status_ary=(slow flaky)

if [ ! -d ~/ycsb-my/faults-meeting4/r10000_o1000000/ ]; then
	mkdir ~/ycsb-my/faults-meeting4/r10000_o1000000/
fi
if [ ! -d ~/ycsb-my/faults-meeting4/r10000_o1000000/wklb_logs ]; then
	mkdir ~/ycsb-my/faults-meeting4/r10000_o1000000/wklb_logs
fi


scheme_ary=("1-2")
freq_ary=(1 4 8)
for scheme in ${scheme_ary[@]}; do
	for freq in ${freq_ary[@]}; do
		for status in ${status_ary[@]}; do
			for status_para in ${status_para_ary[@]}; do
				echo "## [$(date +%s%N), $(date +"%H:%M:%S")] Sourcing cas1 ${loc}baseline-${scheme}-freq${freq}-${status}${status_para}.sh now" >> ~/ycsb-my/faults-meeting4/r10000_o1000000/wklb_logs/wklb_meta.log
				bash 1.sh b 10000 1000000 $status cas1 "baseline-${scheme}-freq${freq}-${status}${status_para}"
			done
		done
	done
done

scheme_ary=("1-3")
freq_ary=(2 4 8)
for scheme in ${scheme_ary[@]}; do
	for freq in ${freq_ary[@]}; do
		for status in ${status_ary[@]}; do
			for status_para in ${status_para_ary[@]}; do
				echo "## [$(date +%s%N), $(date +"%H:%M:%S")] Sourcing cas1 ${loc}baseline-${scheme}-freq${freq}-${status}${status_para}.sh now" >> ~/ycsb-my/faults-meeting4/r10000_o1000000/wklb_logs/wklb_meta.log
				bash 1.sh b 10000 1000000 $status cas1 "baseline-${scheme}-freq${freq}-${status}${status_para}"
			done
		done
	done
done

