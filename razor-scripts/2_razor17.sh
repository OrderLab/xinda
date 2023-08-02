###### razor17
###### ~/ycsb-my/faults-meeting4/2_razor17.sh
###### razor15
###### ~/ycsb-my/faults-meeting4/2_razor15.sh
loc=~/ycsb-my/faults-meeting4/faults/
status_para_ary=(1 2 3 4 5)
status_ary=(slow flaky)

if [ ! -d ~/ycsb-my/faults-meeting4/r10000_o1000000/ ]; then
	mkdir ~/ycsb-my/faults-meeting4/r10000_o1000000/
fi
if [ ! -d ~/ycsb-my/faults-meeting4/r10000_o1000000/wkle_logs ]; then
	mkdir ~/ycsb-my/faults-meeting4/r10000_o1000000/wkle_logs
fi


scheme_ary=("2-2" "3-3")
freq_ary=(1 2 4)
for scheme in ${scheme_ary[@]}; do
	for freq in ${freq_ary[@]}; do
		for status in ${status_ary[@]}; do
			for status_para in ${status_para_ary[@]}; do
				echo "## [$(date +%s%N), $(date +"%H:%M:%S")] Sourcing ${loc}fault-${scheme}-freq${freq}-${status}${status_para}.sh now" >> ~/ycsb-my/faults-meeting4/r10000_o1000000/wkle_logs/wkle_meta.log
				bash 1.sh e 10000 1000000 $status cas1 "${scheme}-freq${freq}-${status}${status_para}"
			done
		done
	done
done

############################################################

scheme_ary=("1-2" "2-3" "1-2-3")
freq_ary=(1 4 8)
for scheme in ${scheme_ary[@]}; do
	for freq in ${freq_ary[@]}; do
		for status in ${status_ary[@]}; do
			for status_para in ${status_para_ary[@]}; do
				echo "## [$(date +%s%N), $(date +"%H:%M:%S")] Sourcing ${loc}fault-${scheme}-freq${freq}-${status}${status_para}.sh now" >> ~/ycsb-my/faults-meeting4/r10000_o1000000/wkle_logs/wkle_meta.log
				bash 1.sh e 10000 1000000 $status cas1 "${scheme}-freq${freq}-${status}${status_para}"
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
				echo "## [$(date +%s%N), $(date +"%H:%M:%S")] Sourcing ${loc}fault-${scheme}-freq${freq}-${status}${status_para}.sh now" >> ~/ycsb-my/faults-meeting4/r10000_o1000000/wkle_logs/wkle_meta.log
				bash 1.sh e 10000 1000000 $status cas1 "${scheme}-freq${freq}-${status}${status_para}"
			done
		done
	done
done


scheme_ary=("1-1" "2-2" "3-3")
freq_ary=(1 2 4)
for scheme in ${scheme_ary[@]}; do
	for freq in ${freq_ary[@]}; do
		for status in ${status_ary[@]}; do
			for status_para in ${status_para_ary[@]}; do
				echo "## [$(date +%s%N), $(date +"%H:%M:%S")] Sourcing ${loc}fault-${scheme}-freq${freq}-${status}${status_para}.sh now" >> ~/ycsb-my/faults-meeting4/r10000_o1000000/wkle_logs/wkle_meta.log
				bash 1.sh e 10000 1000000 $status cas2 "${scheme}-freq${freq}-${status}${status_para}"
			done
		done
	done
done

############################################################

scheme_ary=("1-2" "2-3" "1-2-3")
freq_ary=(1 4 8)
for scheme in ${scheme_ary[@]}; do
	for freq in ${freq_ary[@]}; do
		for status in ${status_ary[@]}; do
			for status_para in ${status_para_ary[@]}; do
				echo "## [$(date +%s%N), $(date +"%H:%M:%S")] Sourcing ${loc}fault-${scheme}-freq${freq}-${status}${status_para}.sh now" >> ~/ycsb-my/faults-meeting4/r10000_o1000000/wkle_logs/wkle_meta.log
				bash 1.sh e 10000 1000000 $status cas2 "${scheme}-freq${freq}-${status}${status_para}"
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
				echo "## [$(date +%s%N), $(date +"%H:%M:%S")] Sourcing ${loc}fault-${scheme}-freq${freq}-${status}${status_para}.sh now" >> ~/ycsb-my/faults-meeting4/r10000_o1000000/wkle_logs/wkle_meta.log
				bash 1.sh e 10000 1000000 $status cas2 "${scheme}-freq${freq}-${status}${status_para}"
			done
		done
	done
done

