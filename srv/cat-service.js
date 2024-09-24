const cds = require('@sap/cds');
const {Worker, isMainThread} = require("worker_threads");
module.exports = class CatalogService extends cds.ApplicationService {
    init() {

        let worker
        const books = [{
            "ID": 1, "title": "Wuthering Heights", "stock": 100
        }, {
            "ID": 2, "title": "Jane Eyre", "stock": 500
        }];

        const {Books} = this.entities;

        this.on("READ", Books, (req) => {
            return books
        });

        /**
         * Custom action to exhaust CPU for Application Autoscaler for metric 'cpuUtil'
         * usage: http://localhost:4004/odata/v4/catalog/useCPU(action='stop',duration='2')
         * payload: { "action": "start | stop"
         *             duration: minutes for cpu load (default is 5 minutes)
         *            }
         */
        this.on('useCPU', async (req) => {

            let status = 'unknown';
            if (req.data.action === 'start') {
                status = 'started';
                const durationParam = req.data.duration || "5"; // default duration is 5 minutes
                const minutes = parseInt(durationParam, 10);
                const duration = minutes * 60 * 1000; // in milliseconds

                if (isMainThread) {
                    console.log("Main thread started.");
                    // Create a new worker thread
                    const workerPayload = {workerData: {duration}};
                    this.worker = new Worker("./srv/autoscaler/autoscaler-cpu-worker.js", workerPayload);

                    // Listen for messages from the worker thread
                    this.worker.on("message", (result) => {
                        console.log("Result from worker" + this.worker.threadId + " :", result);
                        // Terminate the worker thread
                        this.worker.terminate();
                        console.log("Main thread finished.");
                    });
                }

            } else if (req.data.action === 'stop') {
                status = 'stopped';
                if (this.worker) {
                    console.log("Stopping worker thread" + this.worker.threadId);
                    await this.worker.terminate();
                }

            }
            return {
                "metric": "cpuutil",
                "service": "Application Autoscaler",
                "status": status,
                "startTimeUTC ": new Date().toUTCString()
            };
        });

    }
}



