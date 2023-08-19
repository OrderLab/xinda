###################### /data/ruiming/xinda/razor-scripts/node_restart/run_razor13.sh ######################
function create_dir_if_not_exist() {
    if [ ! -d $1 ]; then
        mkdir $1
        print_red_underlined "[$(date +%s%N), $(date +"%H:%M:%S")] Directory $1 created."
    else
        print_red_underlined "[$(date +%s%N), $(date +"%H:%M:%S")] Directory $1 already exists."
        #exit 1
    fi
}

data_dir=/data/ruiming/data/node_restart
cd $data_dir
log_dir1=r10000_o10000000
create_dir_if_not_exist $log_dir1
main_bash_loc=/data/ruiming/xinda/razor-scripts/node_restart/0810.sh 

iteration_1st_half=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50)
iteration_2nd_half=(51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100)
iteration_full=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100)
iteration_123=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 )
iteration_4=(76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100)
iteration_1=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25)
iteration_234=(26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100)
# razor14
iteration_1_60=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60)
# razor15
iteration_61_100=(61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100)
iteration_1_20=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20)
# razor16
iteration_21_80=(21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80)
# razor17
iteration_81_100=(81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100)
iteration_1_40=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40)
# razor19
iteration_41_100=(41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100)


## Setup 17 (1-50)
duration=60
location=cas1
severity=slow3
wkl=a
start_time=30
setup=setup17
log_dir2=${log_dir1}/${setup}
create_dir_if_not_exist $log_dir2
meta_log_loc=${data_dir}/${log_dir2}/wkla_meta.log

for iter in ${iteration_1st_half[@]}; do
    end_time=$((start_time+duration))
    if [ $end_time -ge 120 ]; then
        end_time=120
    fi
    # echo restart-slow3-dur${duration}-${start_time}-$((start_time+duration))
    echo "## [$(date +%s%N), $(date +"%H:%M:%S")] Sourcing ${iter}/${setup} $location restart-${severity}-dur${duration}-${start_time}-${end_time}.sh now" >> $meta_log_loc
    bash $main_bash_loc $wkl 10000 10000000 slow $location restart-${severity}-dur${duration}-${start_time}-${end_time} $severity $iter $setup
    echo "## [$(date +%s%N), $(date +"%H:%M:%S")] Sourcing ${iter}/${setup} $location norestart-${severity}-dur${duration}-${start_time}-${end_time}.sh now" >> $meta_log_loc
    bash $main_bash_loc $wkl 10000 10000000 slow $location norestart-${severity}-dur${duration}-${start_time}-${end_time} $severity $iter $setup
done
