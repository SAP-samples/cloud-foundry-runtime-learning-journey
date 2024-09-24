/**
 * This worker thread simulates a CPU-intensive task, for Application Autoscaler service
 * It receives the CPU utilization and duration from the main thread.
 * It then runs a busy loop for the specified duration
 **/
const {parentPort, workerData} = require('worker_threads');
const os = require('process');

console.log("Worker thread started with data from main thread:", workerData);

let duration = workerData.duration;

const busyLoop = () => {

    let result = []
    const startTime = Date.now();
    let usage;
    let totalUsage = 0;
    while (Date.now() - startTime < duration) { // in milliseconds
        usage = process.cpuUsage();
        totalUsage = usage.user + usage.system;
        totalUsage = (totalUsage / (1000 * 1000)) * 100;
        result.unshift(new Date().toUTCString() + " CPU Usage (%): " + totalUsage);
    }
    setTimeout(() => {
        busyLoop();
    }, 100000); // delay 100 seconds
    return {
        result,
        totalExecutionTime: `${(Date.now() - startTime) / 1000} seconds`,
    };
}


// Perform the time-consuming task
const result = busyLoop();

// Send the result back to the main thread
parentPort.postMessage(result);

console.log("Worker thread finished.");

