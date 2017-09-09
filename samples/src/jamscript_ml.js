jdata{
	struct NEURON_TASK {
      		int deviceId;
      		int problemId;
 		int neuronId;
		float bias;
 		char* weights;
 		char* inputs;
 	} NeuronTask as broadcaster;
 	struct NEURON_RESULT {
      		int problemId;
 		int neuronId;
 		float value;
 	} NeuronResult as logger;
 }

console.log("Initializing variables");
var problems = {};
var problemTasks = {};
var problemInputBuffer = {};
var problemTaskBuffer = {};
var deviceList = [];
var deviceIterator = 0;
var deviceId = 0;
var problemIdIterator = 0;

var problemExpectedOutput = {};
var problemCorrect = 0;
var problemExecuted = 0;

/*
*		Helper Functions
*/

// jsync function to assign id's to devices
jsync function getId() {
    console.log("GetId is called. Assigning device id: " + deviceId);
    deviceList.push(deviceId);
    deviceId++;
    return deviceId-1;
}

// Construct a task queue to carry out tasks
function constructTaskQueue(network) {
	var taskQueue = [];

	network["layers"].forEach(function(layer){
		var layerTask = [];
		layer["neurons"].forEach(function(neuron){
			neuron["completed"] = false;
			layerTask.push(neuron);
		});
		taskQueue.push(layerTask);
	});
	return taskQueue;
}

// stringfy list
function stringfyList(list) {
	return "[" + list + "]";
}

function getResult (outputLayer) {
	var maxOutput;
	var result;

	outputLayer.forEach(function(neuron){
		if (maxOutput === undefined) {
			maxOutput = neuron["output"];
			result = neuron["label"];
		}
		else if (maxOutput < neuron["output"]) {
			maxOutput = neuron["output"];
			result = neuron["label"];
		}
	})

	return result;
}

// Initialize computing the next layer
function computeNextLayer(problemId) {
    if (problemTasks[problemId].length > 0) {
        var layerTasks = problemTasks[problemId].shift();
        problemTaskBuffer[problemId] = layerTasks
        layerTasks.forEach(function(neuron){
            var targetDeviceId = getAvailableDevice();
            var inputs = problemInputBuffer[problemId];

            if (inputs.length !== neuron["weights"].length) {
                // throw an exception
            }
            // broadcast neuron task to a device
            inputBroadcaster({
                deviceId: targetDeviceId,
                problemId: problemId,
                neuronId: neuron["id"],
		bias: neuron["bias"],
                weights: stringfyList(neuron["weights"]),
                inputs: stringfyList(inputs)
            });
        });
    }
    else {
        // logic for output
				// logic for output
        var result = getResult(problemTaskBuffer[problemId]);
				var expectedOutput = problemExpectedOutput[problemId];
        console.log("------------------------");
        console.log("Problem : " + problemId);
				console.log("Expected: " + expectedOutput);
				console.log("Result: " + result);
				problemExecuted++;
				if (result === expectedOutput) {
					problemCorrect++;
				}
				console.log("Accuracy so far: " + problemCorrect/problemExecuted * 100 + "%");
				console.log("------------------------");
    }
}

// Get available device (simple implementation for now)
function getAvailableDevice() {
    var targetDeviceId = deviceList[deviceIterator];
    if (deviceList.length > deviceIterator) {
        deviceIterator = deviceIterator + 1;
    }
    else {
        deviceIterator = 0;
    }
    return targetDeviceId;
}

// Listener for new ML problem logger
var problemInputsListener = function (problemId, sourceDeviceId, inputs) {
	var network = require('../setup/network.json')["networks"];
	console.log(network);
	// add task to a problems dictionary - {problemId:sourceDeviceId}
	problems[problemId] = sourceDeviceId;
	// Construct a task queue and buffer
	problemTasks[problemId] = constructTaskQueue(network);
	problemInputBuffer[problemId] = inputs;
	computeNextLayer(problemId);
};

var neuronResultListener = function (key, entry, device) {
    var layerCompleted = true;
    problemTaskBuffer[entry.problemId].forEach(function(task){
        if (task["id"] === entry.neuronId) {
            task["output"] = entry.value;
            task["completed"] = true;
        }
        if (task["completed"] !== true) {
            layerCompleted = false;
        }
    });

    if (layerCompleted) {
        // initialize new input buffer for the next layer
        problemInputBuffer[entry.problemId] = [];
        problemTaskBuffer[entry.problemId].forEach(function(task){
            problemInputBuffer[entry.problemId].push(task["output"]);
        })

        computeNextLayer(entry.problemId);
    }
};

function inputBroadcaster (neuronTask) {
	NeuronTask.broadcast(neuronTask);
}

NeuronResult.subscribe(neuronResultListener);


function feedProblems() {
	var fs = require('fs');
	var arrayOfLines = fs.readFileSync('../setup/sensor_readings_2.data').toString().split("\n").slice(0,100);
	var testData = arrayOfLines.map(function(line){ return line.split(',') });

	var tempDeviceId = 101;
	var problemId = 0;
	testData.forEach(function(entry) {
		problemExpectedOutput[problemId] = entry[entry.length-1];
		problemInputsListener(problemId, tempDeviceId, entry.slice(0, entry.length-1));
	})
}

console.log("===============Fog Started===============");

var initialLoad = setInterval(function(){
    if (deviceList.length > 0) {
	clearInterval(initialLoad);
        console.log("Devices are available: " + deviceList);
        console.log("Starting simulation");
	feedProblems();
    }
    else {
        console.log("Device is not available yet");
    }
}, 10000);


