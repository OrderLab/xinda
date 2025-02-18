package adr

import (
	"math"
	"time"
	"sort"
)

type SlowDetection struct {
	values          []int64
	ts		[]int64
	freq []int64
	latestFreq int64
	instantFreq int64
	lastFreqCheck int64
	historySlow    []bool
	historyFreqState    []int
	maxCapacity    int
	maxCapacityTimes    int
	p25           int64
	p50         int64
	p75         int64
	p90         int64
	p95         int64
	p99         int64
	warnThresh     int64
	fatalThresh    int64
	defaultWarnNs  int64
	freqCheckCV float64
	freqCheckUpp float64
	freqCheckLow float64
	statusValidLength int
	alreadyFatal bool
}

// NewSlowDetection is a constructor for SlowDetection
func NewSlowDetection() *SlowDetection {
	return &SlowDetection{
		values:        make([]int64, 0),
		ts:		make([]int64, 0),
		freq: make([]int64, 0),
		historySlow:       make([]bool, 0),
		historyFreqState: make([]int, 0),
		maxCapacity:  100,
		latestFreq: -1,
		instantFreq: -1,
		lastFreqCheck: -1,
		maxCapacityTimes: 1000,
		p25:         10000000000,
		p50:       10000000000,
		p75:       10000000000,
		p90:       10000000000,
		p95:       10000000000,
		p99:       10000000000,
		warnThresh:   10000000000,
		fatalThresh:  0,
		defaultWarnNs: 10000000000,
		// minWarnNs: 100000,
		freqCheckCV: 0,
		freqCheckUpp: 10000000,
		freqCheckLow: 0,
		statusValidLength: -1,
		alreadyFatal: false,
		// mutex: sync.Mutex{},
	}
}

func (sd *SlowDetection) getTS() int64 {
    return time.Now().UnixMilli()
}

// min function to find the minimum of two int64 values
func (sd *SlowDetection) max(num1, num2 int64) int64 {
	if num1 > num2 {
		return num1
	}
	return num2
}

// addTime method to add time and isThisSlow to the slices
func (sd *SlowDetection) AddTime(timeInNanos int64) {
	sd.warnThresh = sd.GetWarnThreshold(sd.defaultWarnNs).Nanoseconds()
	isThisSlow := timeInNanos > sd.warnThresh
	
	if len(sd.historySlow) >= sd.maxCapacity {
		sd.historySlow = sd.historySlow[1:]
	}
	sd.historySlow = append(sd.historySlow, isThisSlow)

	if !isThisSlow {
		if len(sd.values) == 0 {
			sd.values = append(sd.values, timeInNanos)
		} else {
			i := sort.Search(len(sd.values), func(i int) bool { return sd.values[i] >= timeInNanos })
			sd.values = append(sd.values, 0)
			copy(sd.values[i+1:], sd.values[i:])
			sd.values[i] = timeInNanos
		}
	}
}

func (sd *SlowDetection) AddFreq() int64 {
	curTime := sd.getTS()
	if (len(sd.freq) >= sd.maxCapacity) {
		sd.freq = sd.freq[1:]
	}
	if (len(sd.ts) >= sd.maxCapacity) {
		sd.latestFreq = curTime - sd.ts[0]
		sd.ts = sd.ts[1:]
		sd.instantFreq = curTime - sd.lastFreqCheck;
		sd.lastFreqCheck = curTime
		sd.freq = append(sd.freq, sd.latestFreq)
	}
	sd.ts = append(sd.ts, curTime)
	return sd.latestFreq
}

func (sd *SlowDetection) CheckFreq() {
	if (sd.latestFreq == -1 || len(sd.freq) < sd.maxCapacity) {
		return
	}
	sum := int64(0)
	for _, value := range sd.freq {
		sum += value
	}
	mean := float64(sum) / float64(sd.maxCapacity)
	varianceSum := float64(0)
	for _, value := range sd.freq {
		varianceSum += (float64(value) - mean) * (float64(value) - mean)
	}
	stdDev := math.Sqrt(varianceSum / float64(sd.maxCapacity))
	sd.freqCheckCV = stdDev / mean
	sd.freqCheckUpp = mean + stdDev
	sd.freqCheckLow = mean - stdDev
}

func (sd *SlowDetection) GetfreqCheckCV() float64 {
	return sd.freqCheckCV
}

func (sd *SlowDetection) GetfreqCheckUpp() float64 {
	return sd.freqCheckUpp
}

func (sd *SlowDetection) GetfreqCheckLow() float64 {
	return sd.freqCheckLow
}

func (sd *SlowDetection) GetlatestFreq() int64 {
	return sd.latestFreq
}

func (sd *SlowDetection) reset() {
	sd.values = make([]int64, 0)
	sd.ts = make([]int64, 0)
	sd.freq = make([]int64, 0)
	sd.historySlow = make([]bool, 0)
	sd.historyFreqState = make([]int, 0)
	sd.latestFreq = -1
	sd.instantFreq = -1
	sd.lastFreqCheck = -1
	sd.p25 = 10000000000
	sd.p50 = 10000000000
	sd.p75 = 10000000000
	sd.p90 = 10000000000
	sd.p95 = 10000000000
	sd.p99 = 10000000000
	sd.warnThresh = 10000000000
	sd.fatalThresh = 0
	sd.defaultWarnNs = 10000000000
	sd.freqCheckCV = 0
	sd.freqCheckUpp = 10000000
	sd.freqCheckLow = 0
	sd.statusValidLength = -1
	sd.alreadyFatal = false
}

func (sd *SlowDetection) IsFatal() bool {
	return sd.alreadyFatal
}

func (sd *SlowDetection) IsSlow(timeInNanos int64) bool {
	sd.CalculateStats()
	adaptiveThresh := sd.defaultWarnNs
	if len(sd.values) >= sd.maxCapacityTimes {
		adaptiveThresh = sd.p99
	}
	compareResult := timeInNanos > adaptiveThresh
	sd.CheckFreq()
	
	freqCode := 0
	if (sd.latestFreq > int64(sd.freqCheckUpp)) {
		if (sd.freqCheckCV > 0.5) {
			freqCode = -1
		}
	} else if (sd.latestFreq < int64(sd.freqCheckLow)) {
		if (sd.freqCheckCV > 0.5) {
			freqCode = 1
		}
	}
	msg := "normal"
	isSlowCont := sd.isSlowContinuous()
	if (freqCode > 0) {
		if (sd.isFreqStateContinuous(1)) {
			if (sd.alreadyFatal) {
				if (!isSlowCont) {
					sd.reset()
				}
			}
		} else {
			msg = "heavier"
		}
	} else if (freqCode < 0) {
		isLighterCont := sd.isFreqStateContinuous(-1)
		if (isLighterCont) {
			if (isSlowCont) {
				msg = "lighter-fatal"
			} else {
				if (sd.alreadyFatal) {
					sd.reset()
				}
			}
		} else {
			msg = "lighter"
		}
	}

	if (!sd.alreadyFatal && msg == "lighter-fatal") {
		sd.alreadyFatal = true
		sd.statusValidLength = sd.maxCapacity
		if (sd.instantFreq > 0) {
			sd.statusValidLength = int(math.Max(math.Min(float64(sd.maxCapacity), float64(1000/sd.instantFreq)), float64(1)))
		}
	}
	if (isSlowCont) {
		sd.alreadyFatal = true
	}

	if (sd.alreadyFatal) {
		sd.AddFreq()
		sd.updateFreqState(freqCode)
		sd.updateHistoricStates(compareResult)
		return true
	} else {
		sd.AddTime(timeInNanos)
		sd.AddFreq()
		sd.updateFreqState(freqCode)
		sd.updateHistoricStates(compareResult)
	}
	return compareResult
}

func (sd *SlowDetection) updateFreqState(state int) {
	if (len(sd.historyFreqState) >= sd.maxCapacity) {
		sd.historyFreqState = sd.historyFreqState[1:]
	}
	sd.historyFreqState = append(sd.historyFreqState, state)
}

func (sd *SlowDetection) updateHistoricStates(isThisSlow bool) {
	if len(sd.historySlow) >= sd.maxCapacity {
		sd.historySlow = sd.historySlow[1:]
	}
	sd.historySlow = append(sd.historySlow, isThisSlow)
}

// calculateStats method to calculate mean and standard deviation
func (sd *SlowDetection) CalculateStats() {
	if len(sd.values) >= sd.maxCapacityTimes {
		sd.p25 = sd.findPercentile(25)
		sd.p50 = sd.findPercentile(50)
		sd.p75 = sd.findPercentile(75)
		sd.p90 = sd.findPercentile(90)
		sd.p95 = sd.findPercentile(95)
		sd.p99 = sd.findPercentile(99)
	}
}

func (sd *SlowDetection) findPercentile(percentile float64) int64 {
	pos := int(percentile / 100 * float64(len(sd.values) + 1) - 1)
	if pos < 0 {
		pos = 0
	} 
	return sd.values[pos]
}

// isWarn method to determine if a given time is considered a warning
func (sd *SlowDetection) GetWarnThreshold(defaultNs int64) time.Duration {
	if len(sd.values) < sd.maxCapacity {
		sd.warnThresh = defaultNs
	} else {
		sd.warnThresh = sd.p99
	}
	return time.Duration(sd.warnThresh) * time.Nanosecond
}

// isFatal method to check if more than half of the entries are slow
func (sd *SlowDetection) isFatal() bool {
	trueCount := 0
	for _, value := range sd.historySlow {
		if value {
			trueCount++
		}
	}
	sd.fatalThresh = int64(trueCount)
	if len(sd.historySlow) == sd.maxCapacity {
		return trueCount > 10
	} else {
		return false
	}
}

func (sd *SlowDetection) isSlowContinuous() bool {
	trueCount := 0
	for _, value := range sd.historySlow {
		if value {
			trueCount++
		}
	}
	if len(sd.historySlow) == sd.maxCapacity {
		return trueCount > 10
	} else {
		return false
	}
}

func (sd *SlowDetection) isFreqStateContinuous(state int) bool {
	if (len(sd.historyFreqState) < sd.maxCapacity) {
		return false
	}
	validLength := sd.maxCapacity
	if (sd.instantFreq > 0) {
		validLength = int(math.Max(math.Min(float64(sd.maxCapacity), float64(1000/sd.instantFreq)), float64(1)))
	}
	if (sd.alreadyFatal) {
		validLength = sd.statusValidLength
	}
	startIndex := sd.maxCapacity - validLength
	index := 0
	trueCount := 0
	for _, value := range sd.historyFreqState {
		if (value == state && index >= startIndex) {
			trueCount++
		}
		index++
	}
	return trueCount > validLength / 2
}

func (sd *SlowDetection) GetFatalThreshold() int64 {
	return sd.fatalThresh
}


func (sd *SlowDetection) GetP25() int64 {
	return sd.p25
}

func (sd *SlowDetection) GetP50() int64 {
	return sd.p50
}

func (sd *SlowDetection) GetP75() int64 {
	return sd.p75
}

func (sd *SlowDetection) GetP90() int64 {
	return sd.p90
}

func (sd *SlowDetection) GetP95() int64 {
	return sd.p95
}

func (sd *SlowDetection) GetP99() int64 {
	return sd.p99
}

func (sd *SlowDetection) GetSlideLen() int {
	return len(sd.values)
}