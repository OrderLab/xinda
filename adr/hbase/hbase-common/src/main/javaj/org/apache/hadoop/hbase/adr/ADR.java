package org.apache.hadoop.hbase.adr;

import org.apache.yetus.audience.InterfaceAudience;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.ArrayList;
import java.util.Queue;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentLinkedQueue;
import org.apache.hadoop.hbase.util.EnvironmentEdgeManager;
import java.text.MessageFormat;
import java.util.Random;

@InterfaceAudience.Private
public class ADR {
    private static final Logger LOG = LoggerFactory.getLogger(ADR.class);
    private int maxHistoricStateCapacity = 100;
    private int maxFreqCapacity = 100;
    private int maxCapacityForAdaptive = 1000;
    private int maxEntryCountBeforeReset = Integer.MAX_VALUE;
    private Map<String, Long> adaptiveThresholds;
    private Map<String, Queue<Long>> metricValuesMap;
    private Map<String, Queue<Boolean>> metricHistoricStateMap;
    private Map<String, Queue<Integer>> metricHistoricFreqStateMap;
    private Map<String, Queue<Long>> metricTsMap;
    private Map<String, Queue<Long>> metricFreqMap;
    private boolean isFutureTaskRunning = false;
    private boolean isFutureTaskRunning2 = false;
    private ExecutorService executorService;
    private ExecutorService executorService2;
    private ExecutorService freqCheckService;
    private int entryCounter = 0;
    private int p99Counter = 0;
    private int fatalCounter = 0;
    private int slowCount = 0;
    private long lastAdaptiveTimeMs = EnvironmentEdgeManager.currentTime();
    private long lastAdaptiveDuration = 0;
    private long latestFreq = -1;
    private long instantFreq = -1;
    private long lastFreqCheck = -1;
    private boolean alreadyFatal = false;
    private long statusValidLength = -1;
    private long lastResetTimeMs = EnvironmentEdgeManager.currentTime();
    private boolean isFutureFreqCheckRunning = false;
    private double freqCheckUpp = 100000;
    private double freqCheckLow = -1;
    private double freqCheckCV = 0;
    private long lastFreqCheckDuration = 0;
    private long lastFreqCheckTime = EnvironmentEdgeManager.currentTime();
    private long executorMaxDuration = 300;
    private final int MAX_FUTURES = 100;
    private final List<CompletableFuture<Boolean>> futureResults;
    private ExecutorService es;
    private int lastCompletedIndex = 0; 
    // private boolean isSlowAndLight = false;

    public ADR() {
        this.metricValuesMap = new LinkedHashMap<>();
        this.metricTsMap = new LinkedHashMap<>();
        this.metricFreqMap = new LinkedHashMap<>();
        this.metricHistoricStateMap = new ConcurrentHashMap<>();
        this.metricHistoricFreqStateMap = new ConcurrentHashMap<>();
        this.adaptiveThresholds = new LinkedHashMap<>();
        this.executorService = Executors.newFixedThreadPool(1); 
        this.executorService2 = Executors.newFixedThreadPool(1); 
        this.freqCheckService = Executors.newFixedThreadPool(1); 
        this.futureResults = new ArrayList<>();
        this.es = Executors.newFixedThreadPool(10); // Or adjust thread pool size
        for (int i = 0; i < MAX_FUTURES; i++) {
            futureResults.add(null); // Initialize with null
        }
    }

    public boolean isSlowAsync(String metricName, Number rawValue, String operator, Number rawThreshold) {
        // Start searching from the next available future, wrapping around if needed
        int startIndex = lastCompletedIndex;
        for (int i = 0; i < MAX_FUTURES; i++) {
            int currentIndex = (startIndex + i) % MAX_FUTURES;  // Wrapping around
            LOG.info("Index: {}", currentIndex);
            CompletableFuture<Boolean> future = futureResults.get(currentIndex);

            // Check if the future is either null or completed
            if (future == null || future.isDone()) {
                if (future != null && future.isDone()) {
                    try {
                        // Get the result of the completed future and return immediately
                        boolean result = future.get();
                         LOG.info("Stopped at: {}, result: {}", currentIndex, result);
                        lastCompletedIndex = currentIndex; // Store the index of the completed future
                        return result; // Return the result
                    } catch (InterruptedException | ExecutionException e) {
                        return false;
                    }
                }

                // If future is null or completed, run isSlow asynchronously and store the new future
                CompletableFuture<Boolean> newFuture = CompletableFuture.supplyAsync(() -> {
                    return isSlow(metricName, rawValue, operator, rawThreshold);
                }, es);

                futureResults.set(currentIndex, newFuture);
                lastCompletedIndex = currentIndex; // Update the last completed index
                return false;
            }
        }

        // If all slots are full, reset the index and return a completed future with false (or default)
        lastCompletedIndex = 0;
        return false;
    }

    private void reset(String metricName, long defaultThresh) {
        long curTime = EnvironmentEdgeManager.currentTime();
        if (curTime - lastResetTimeMs <= 1000) {
            return;
        }
        metricValuesMap.put(metricName, new LinkedList<>());
        metricTsMap.put(metricName, new LinkedList<>());
        metricFreqMap.put(metricName, new LinkedList<>());
        metricHistoricStateMap.put(metricName, new ConcurrentLinkedQueue<>());
        metricHistoricFreqStateMap.put(metricName, new ConcurrentLinkedQueue<>());
        adaptiveThresholds.put(metricName, defaultThresh);
        lastAdaptiveTimeMs = EnvironmentEdgeManager.currentTime();
        lastAdaptiveDuration = 0;
        latestFreq = -1;
        lastFreqCheck = -1;
        alreadyFatal = false;
        statusValidLength = - 1;
        lastResetTimeMs = EnvironmentEdgeManager.currentTime();
        isFutureFreqCheckRunning = false;
        freqCheckUpp = 100000;
        freqCheckLow = -1;
        freqCheckCV = 0;
        lastFreqCheckDuration = 0;
        lastFreqCheckTime = EnvironmentEdgeManager.currentTime();
    }

    private boolean adaptiveReady() {
        if (alreadyFatal) return false;
        long currentTimeMs = EnvironmentEdgeManager.currentTime();
        lastAdaptiveDuration = currentTimeMs - lastAdaptiveTimeMs;
        if (lastAdaptiveDuration > executorMaxDuration) {
            lastAdaptiveTimeMs = currentTimeMs;
            return true;
        }
        return false;
    }

    private boolean freqCheckReady() {
        long currentTimeMs = EnvironmentEdgeManager.currentTime();
        lastFreqCheckDuration = currentTimeMs - lastFreqCheckTime;
        if (lastFreqCheckDuration > executorMaxDuration) {
            lastFreqCheckTime = currentTimeMs;
            return true;
        }
        return false;
    }

    private boolean compare(long metricValue, String operator, long threshold) {
        switch (operator) {
            case ">":
                return metricValue > threshold;
            case ">=":
                return metricValue >= threshold;
            case "<":
                return metricValue < threshold;
            case "<=":
                return metricValue <= threshold;
            default:
                throw new IllegalArgumentException("Invalid operator");
        }
    }

    private boolean logicalCompare(boolean conditionA, String logicalOperator, boolean conditionB) {
        switch (logicalOperator) {
            case "&&":
                return conditionA && conditionB;
            case "||":
                return conditionA || conditionB;
            default:
                throw new IllegalArgumentException("Invalid logical operator");
        }
    }

    private String getStats(Queue<Long> q) {
        long sum = 0;
        long queueSize = q.size();
        for (long v : q) {
            sum += v;
        }

        double mean = (double) sum / queueSize;

        double varianceSum = 0;
        for (long v : q) {
            varianceSum += (v - mean) * (v - mean);
        }

        double stdev = Math.sqrt(varianceSum / queueSize);
        return MessageFormat.format("mean: {0}, stdev: {1}, 2sigma: {2}, 3sigma: {3}, CV: {4}", mean, stdev, mean +2*stdev , mean + 3*stdev , stdev / mean);
    }

    private void updateMetricValues(String metricName, long value) {
        Queue<Long> valuesQueue = metricValuesMap.getOrDefault(metricName, new LinkedList<>());
        if (entryCounter >= maxEntryCountBeforeReset) {
            valuesQueue = new LinkedList<>();
        }
        if (valuesQueue.size() >= maxCapacityForAdaptive) {
            valuesQueue.poll();
        }
        valuesQueue.add(value);
        metricValuesMap.put(metricName, valuesQueue);
        entryCounter = entryCounter + 1;
    }

    private void updateMetricFreqs(String metricName) {
        Queue<Long> tsQueue = metricTsMap.getOrDefault(metricName, new LinkedList<>());
        Queue<Long> freqQueue = metricFreqMap.getOrDefault(metricName, new LinkedList<>());
        long curTime = EnvironmentEdgeManager.currentTime();
        if (entryCounter >= maxEntryCountBeforeReset) {
            tsQueue = new LinkedList<>();
            entryCounter = 0;
            adaptiveThresholds = new LinkedHashMap<>();
        }
        if (freqQueue.size() >= maxFreqCapacity) {
            freqQueue.poll();
        }
        if (tsQueue.size() >= maxFreqCapacity) {
            latestFreq = curTime - tsQueue.poll();
            instantFreq = curTime - lastFreqCheck;
            lastFreqCheck = curTime;
            freqQueue.add(latestFreq);
        }
        tsQueue.add(curTime);
        metricTsMap.put(metricName, tsQueue);
        metricFreqMap.put(metricName, freqQueue);
    }

    private void updateHistoricStates(String metricName, boolean compareResult) {
        Queue<Boolean> historicStateQueue = metricHistoricStateMap.getOrDefault(metricName, new ConcurrentLinkedQueue<>());
        while (historicStateQueue.size() >= maxHistoricStateCapacity) {
            historicStateQueue.poll();
        }
        historicStateQueue.add(compareResult);
        metricHistoricStateMap.put(metricName, historicStateQueue);
    }

    private void updateHistoricFreqStates(String metricName, int freqCode) {
        Queue<Integer> historicFreqStateQueue = metricHistoricFreqStateMap.getOrDefault(metricName, new ConcurrentLinkedQueue<>());
        while (historicFreqStateQueue.size() >= maxHistoricStateCapacity) {
            historicFreqStateQueue.poll();
        }
        historicFreqStateQueue.add(freqCode);
        metricHistoricFreqStateMap.put(metricName, historicFreqStateQueue);
    }

    private void checkFreq(String metricName) {
        Queue<Long> q = metricFreqMap.get(metricName);
        if (latestFreq == -1 || q.size() < maxFreqCapacity) {
            return;
        }
        long sum = 0;
        long queueSize = q.size();
        for (long v : q) {
            sum += v;
        }

        double mean = (double) sum / queueSize;

        double varianceSum = 0;
        for (long v : q) {
            varianceSum += (v - mean) * (v - mean);
        }

        double stdev = Math.sqrt(varianceSum / queueSize);
        freqCheckCV = stdev / mean;
        freqCheckUpp = mean + stdev;
        freqCheckLow = mean - stdev;
    }

    
    
    public boolean isSlow(String metricName, Number rawValue, String operator, Number rawThreshold) {
        long metricValue = rawValue.longValue();
        long defaultThreshold = rawThreshold.longValue();

        
        Queue<Long> valuesQueue = metricValuesMap.getOrDefault(metricName, new LinkedList<>());
        if (valuesQueue.size() >= maxCapacityForAdaptive && adaptiveReady()) {
            if (!isFutureTaskRunning) {
                isFutureTaskRunning = true;
                executorService.submit(() -> {
                    calculateAndStoreAdaptiveThreshold(metricName);
                    isFutureTaskRunning = false;
                });
            } else {
                if (lastAdaptiveDuration > executorMaxDuration) {
                    executorService.shutdownNow();
                    executorService = Executors.newFixedThreadPool(1);
                    isFutureTaskRunning = false;
                }
            }
        }
        long adaptiveThresh = adaptiveThresholds.getOrDefault(metricName, defaultThreshold);
        boolean compareResult = compare(metricValue, operator, adaptiveThresh);

        if (freqCheckReady()) {
            if (!isFutureFreqCheckRunning) {
                isFutureFreqCheckRunning = true;
                freqCheckService.submit(() -> {
                    checkFreq(metricName);
                    isFutureFreqCheckRunning = false;
                });
            } else {
                if (lastFreqCheckDuration > executorMaxDuration) {
                    freqCheckService.shutdownNow();
                    freqCheckService = Executors.newFixedThreadPool(1);
                    isFutureFreqCheckRunning = false;
                }
            }
        }

        int freqCode = 0;

        if (latestFreq > freqCheckUpp) {
            if (freqCheckCV > 0.5) {
                freqCode = -1;
            }
            // return -1;
        } else if (latestFreq < freqCheckLow) {
            if (freqCheckCV > 0.5) {
                freqCode = 1;
            }
        } 
        
        
        
        String msg = "normal";
        if (freqCode > 0) {
            if (isFreqStateContinuous(metricName, 1)) {
                if (alreadyFatal) {
                    // If it is fatal right now + workload heavier + slow not continuous = turning normal
                    boolean isSlowCont = isSlowContinuous(metricName);
                    if (!isSlowCont) {
                        LOG.info("WORKLOAD Metric {} not fatal anymore, reset due to heavier (but not slow) workload", metricName);
                        reset(metricName, defaultThreshold);
                        msg = "heavier-reset";
                    }
                }
            } else msg = "heavier";
        } else if (freqCode < 0) {
            boolean isLighterCont = isFreqStateContinuous(metricName, -1);
            if (isLighterCont) {
                boolean isSlowCont = isSlowContinuous(metricName);
                if (isSlowCont) {
                    msg = "lighter-fatal";
                } else {
                    if (alreadyFatal) {
                        // If it is fatal right now + workload lighter + slow not continuous = turning normal
                        LOG.info("WORKLOAD Metric {} not fatal anymore, reset due to lighter (but not slow) workload", metricName);
                        reset(metricName, defaultThreshold);
                        msg = "lighter-reset";
                    }
                }
            } else msg = "lighter";
        }
        if (!alreadyFatal && msg == "lighter-fatal") {
            alreadyFatal = true;
            statusValidLength = maxHistoricStateCapacity;
            if (instantFreq > 0) statusValidLength = Math.max(Math.min(maxHistoricStateCapacity, 1000 / instantFreq), 1);
            LOG.info("Metric {} just became fatal, use {} as valid length", metricName, statusValidLength);
        }
        if (alreadyFatal) {
            updateMetricFreqs(metricName);
            updateHistoricStates(metricName, compareResult);
            updateHistoricFreqStates(metricName, freqCode);
        } else {
            updateMetricFreqs(metricName);
            updateMetricValues(metricName, metricValue);
            updateHistoricStates(metricName, compareResult);
            updateHistoricFreqStates(metricName, freqCode);

            if (msg == "normal" || msg == "heavier" || msg == "heavier-reset" || msg == "lighter-reset") return false;

            if (compareResult) {
                LOG.info("Metric {} is slow ({} {} {}), reason: {}", metricName, metricValue, operator, adaptiveThresh, msg);
            }
        }
        
        
        return compareResult;
    }



    public boolean isSlow(Number rawValue1, String operator1, Number rawThreshold1, String logicalOperator, Number rawValue2, String operator2, Number rawThreshold2, String metricName2) {
        long metricValue1 = rawValue1.longValue();
        long defaultThreshold1 = rawThreshold1.longValue();

        long metricValue2 = rawValue2.longValue();
        long defaultThreshold2 = rawThreshold2.longValue();
        
        if (metricName2 != "retain" && (operator2 == "<" || operator2 == "<=")) {
            metricValue2 = -metricValue2;
            defaultThreshold2 = -defaultThreshold2;
            if (operator2 == "<") operator2 = ">";
            else operator2 = ">=";
        }

        boolean compareResult1 = compare(metricValue1, operator1, defaultThreshold1);
        boolean compareResult2;
        long adaptiveThresh2 = defaultThreshold2;
        if (metricName2 == "retain") {
            compareResult2 = compare(metricValue2, operator2, defaultThreshold2);
        } else {
            updateMetricValues(metricName2, metricValue2);
            Queue<Long> valuesQueue2 = metricValuesMap.getOrDefault(metricName2, new LinkedList<>());
            if (valuesQueue2.size() >= maxCapacityForAdaptive && adaptiveReady()) {
                if (!isFutureTaskRunning2) {
                    isFutureTaskRunning2 = true;
                    executorService2.submit(() -> {
                        calculateAndStoreAdaptiveThreshold(metricName2);
                        isFutureTaskRunning2 = false;
                    });
                } else {
                    if (lastAdaptiveDuration > 1000) {
                        executorService2.shutdownNow();
                        executorService2 = Executors.newFixedThreadPool(1);
                        isFutureTaskRunning2 = false;
                        LOG.warn("Adaptive calculation task is reset due to timeout in {}", metricName2);
                    }
                }
            }
            adaptiveThresh2 = adaptiveThresholds.getOrDefault(metricName2, defaultThreshold2);
            compareResult2 = compare(metricValue2, operator2, adaptiveThresh2);
        }
        boolean compareResult = logicalCompare(compareResult1, logicalOperator, compareResult2);
        updateHistoricStates(metricName2, compareResult);
        if (compareResult) {
            handleSlowMetric(metricValue1, operator1, defaultThreshold1, logicalOperator, metricValue2, operator2, adaptiveThresh2, metricName2);
        }
        return compareResult;
    }

    public boolean isFatal(String metricName, Number rawValue, String operator, Number rawThreshold) {
        long metricValue = rawValue.longValue();
        long defaultThreshold = rawThreshold.longValue();
        if (alreadyFatal) {
            LOG.info("Metric {} is fatal (continuous slowdown + lower frequency)", metricName);
            fatalCounter = fatalCounter + 1;
        } else if (compare(metricValue, operator, defaultThreshold)) {
            LOG.info("Metric {} is fatal ({} {} {})", metricName, metricValue, operator, defaultThreshold);
            fatalCounter = fatalCounter + 1;
        }
        return alreadyFatal || compare(metricValue, operator, defaultThreshold);
    }

    public boolean isFatal(Number rawValue1, String operator1, Number rawThreshold1, String logicalOperator, Number rawValue2, String operator2, Number rawThreshold2, String metricName) {
        long metricValue1 = rawValue1.longValue();
        long defaultThreshold1 = rawThreshold1.longValue();

        long metricValue2 = rawValue2.longValue();
        long defaultThreshold2 = rawThreshold2.longValue();
        boolean isFatal = isSlowContinuous(metricName) || 
            logicalCompare(compare(metricValue1, operator1, defaultThreshold1), logicalOperator, compare(metricValue2, operator2, defaultThreshold2));
        if (isFatal) {
            handleFatalMetric(metricName);
        }
        fatalCounter = fatalCounter + 1;
        return isFatal;
    }

    public boolean isSlowContinuous(String metricName) {
        Queue<Boolean> historicStateQueue = metricHistoricStateMap.getOrDefault(metricName, new ConcurrentLinkedQueue<>());
        if (historicStateQueue == null || historicStateQueue.size() < maxHistoricStateCapacity) {
            return false;
        }
        slowCount = 0;
        long validLength = maxHistoricStateCapacity;
        if (instantFreq > 0) validLength = Math.max(Math.min(maxHistoricStateCapacity, 1000 / instantFreq), 1);
        if (alreadyFatal) validLength = statusValidLength;
        long startIndex = historicStateQueue.size() - validLength;
        int index = 0;
        for (boolean historicState : historicStateQueue) {
            if (index >= startIndex && historicState) {
                slowCount++;
            }
            index++;
        }
        return slowCount > validLength / 2;
    }

    public Boolean isFreqStateContinuous(String metricName, int state) {
        Queue<Integer> historicFreqStateQueue = metricHistoricFreqStateMap.getOrDefault(metricName, new ConcurrentLinkedQueue<>());
        if (historicFreqStateQueue == null || historicFreqStateQueue.size() < maxHistoricStateCapacity) {
            return false;
        }
        int count = 0;
        long validLength = maxHistoricStateCapacity;
        if (instantFreq > 0) validLength = Math.max(Math.min(maxHistoricStateCapacity, 1000 / instantFreq), 1);
        if (alreadyFatal) validLength = statusValidLength;
        long startIndex = historicFreqStateQueue.size() - validLength;
        int index = 0;
        for (int historicState : historicFreqStateQueue) {
            if (index >= startIndex && historicState == state) {
                count++;
            }
            index++;
        }
        return count > validLength / 2;
    }


    public boolean isSlowAndFatal(Number rawValue1, String operator1, Number rawThreshold1, String logicalOperator, Number rawValue2, String operator2, Number rawThreshold2, String metricName) {
        boolean slow = isSlow(rawValue1, operator1, rawThreshold1, logicalOperator, rawValue2, operator2, rawThreshold2, metricName);
        if (slow) {
            return isFatal(rawValue1, operator1, rawThreshold1, logicalOperator, rawValue2, operator2, rawThreshold2, metricName);
        }
        return false;
    }

    private void calculateAndStoreAdaptiveThreshold(String metricName) {
        Queue<Long> valuesQueue = metricValuesMap.get(metricName);
        if (valuesQueue != null && !valuesQueue.isEmpty()) {
            List<Long> sortedValues = new LinkedList<>(valuesQueue);
            Collections.sort(sortedValues);
            int index = (int) Math.ceil(0.99 * sortedValues.size()) - 1;
            long p99Value = sortedValues.get(index);
            adaptiveThresholds.put(metricName, p99Value);
        }
        p99Counter = p99Counter + 1;
    }

    private void handleSlowMetric(String metricName, long value, long threshold) {
        LOG.info("Metric {} is slow: {} (threshold: {})", metricName, value, threshold);
    }

    private void handleSlowMetric(long value1, String operator1, long threshold1, String logicalOperator, long value2, String operator2, long threshold2, String metricName) {
        LOG.info("Metric {} is slow: {} {} {} {} {} {} {}", metricName, value1, operator1, threshold1, logicalOperator, value2, operator2, threshold2);
    }

    private void handleFatalMetric(String metricName, long metricValue, long defaultThreshold) {
        // Log or handle the slow metric as needed
        LOG.warn("Metric {} is fatal: {} out of {} slow OR metricValue {} > {} (default)", metricName, slowCount, maxHistoricStateCapacity, metricValue, defaultThreshold);
        printCounterInfo();
    }

    private void handleFatalMetric(String metricName) {
        // Log or handle the slow metric as needed
        LOG.warn("Metric {} is fatal: {} out of {} slow", metricName, slowCount, maxHistoricStateCapacity);
        printCounterInfo();
    }

    private void printCounterInfo() {
        LOG.info("Summary of counters: {} / {} / {} -> fatal / p99 / #entry", fatalCounter, p99Counter, entryCounter);
    }

    public void printEverything(String metricName, long metricValue) {
        long adaptiveThreshold = adaptiveThresholds.getOrDefault(metricName, Long.MAX_VALUE);
        LOG.info("Adaptive thresh: {}; Raw value: {}; Summary of counters: {} / {} / {} -> fatal / p99 / #entry", adaptiveThreshold, metricValue, fatalCounter, p99Counter, entryCounter);
    }
}