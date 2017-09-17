jdata{
	struct NEURON_TASK {
      	int deviceId;
      	char* problemId;
 		int neuronId;
		float bias;
 		char* weights;
 		char* inputs;
 	} NeuronTask as broadcaster;
 	struct NEURON_RESULT {
      	char* problemId;
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

var problemExpectedOutput = {};
var problemCorrect = 0;
var problemExecuted = 0;
var numberOfProblems = 100;
var minNumberOfDevices = 4;

/*
*		Helper Functions
*/

// jsync function to assign id's to devices
jsync function getId() {
    deviceList.push(deviceId);
    deviceId++;
    return deviceId-1;
}

function S4() {
    return (((1+Math.random())*0x10000)|0).toString(16).substring(1);
}

function getGuid() {
	guid = (S4() + S4() + "-" + S4() + "-4" + S4().substr(0,3) + "-" + S4() + "-" + S4() + S4() + S4()).toLowerCase();
	return guid;
}

// Construct a task queue to carry out tasks
function constructTaskQueue() {
	var network = require('../setup/network.json')["networks"];

	var taskQueue = [];
	network["layers"].forEach(function(layer){
		var layerTask = [];
		layer["neurons"].forEach(function(neuron){
			var neuronTask = {};
			neuronTask["id"] = neuron["id"];
			neuronTask["bias"] = neuron["bias"];
			neuronTask["weights"] = neuron["weights"];
			neuronTask["label"] = neuron["label"];
			neuronTask["completed"] = false;
			layerTask.push(neuronTask);
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
	// check if problem is already solved
	if (problemTasks[problemId]) {
		// assign neurons tasks from the next layer
		if (problemTasks[problemId].length > 0) {

			problemTaskBuffer[problemId] = [];
			problemTaskBuffer[problemId] = problemTasks[problemId].shift();

			problemTaskBuffer[problemId].forEach(function(neuron){
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
			handleCompletedProblem(problemId);
		}
	}

}

function handleCompletedProblem(problemId){
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
	console.log("Problems simulated: " + problemExecuted);
	console.log("Accuracy: " + problemCorrect/problemExecuted * 100 + "%");
	console.log("------------------------");

	delete problemTaskBuffer[problemId];
	delete problemInputBuffer[problemId];
	delete problemTasks[problemId];

	if (problemExecuted === numberOfProblems) {
		console.log("===============End of Simulation===============")
		console.log("Problems simulated: " + numberOfProblems);
		console.log("Accuracy: " + problemCorrect/problemExecuted * 100 + "%");
	}
}

// Get available device (simple implementation for now)
function getAvailableDevice() {
    return deviceList[Math.floor(Math.random() * deviceList.length)];
}

// Listener for new ML problem logger
var problemInputsListener = function (problemId, sourceDeviceId, inputs) {
	// add task to a problems dictionary - {problemId:sourceDeviceId}
	problems[problemId] = sourceDeviceId;
	// Construct a task queue and buffer
	problemTasks[problemId] = constructTaskQueue();
	problemInputBuffer[problemId] = inputs;
	computeNextLayer(problemId);
};

var neuronResultListener = function (key, entry, device) {
	// check if problem is solved already
	if (problemTasks[entry.log.problemId]) {
		var layerCompleted = true;

		// flag neuron as completed
	    problemTaskBuffer[entry.log.problemId].forEach(function(task){
			if (task["id"] === entry.log.neuronId) {
				task["output"] = entry.log.value;
				task["completed"] = true;
			}
			if (task["completed"] !== true) {
			   layerCompleted = false;
			}
		});

		// if layer is completed, move on to the next layer
	    if (layerCompleted) {
	        // initialize new input buffer for the next layer
	        problemInputBuffer[entry.log.problemId] = [];
	        problemTaskBuffer[entry.log.problemId].forEach(function(task){
	            problemInputBuffer[entry.log.problemId].push(task["output"]);
	        })

	        computeNextLayer(entry.log.problemId);
	    }
	}
};

function inputBroadcaster (neuronTask) {
	NeuronTask.broadcast(neuronTask);
}

NeuronResult.subscribe(neuronResultListener);


function feedProblems() {
	var fs = require('fs');
	var arrayOfLines = fs.readFileSync('../setup/sensor_readings_2.data').toString().split("\n").slice(0,numberOfProblems);
	var testData = arrayOfLines.map(function(line){ return line.split(',') });

	var tempDeviceId = 101;
	testData.forEach(function(entry) {
		var problemId = getGuid();
		problemExpectedOutput[problemId] = entry[entry.length-1];
		problemInputsListener(problemId, tempDeviceId, entry.slice(0, entry.length-1));
	})
}

console.log("===============Fog Started===============");

var initialLoad = setInterval(function(){
    if (deviceList.length >= minNumberOfDevices) {
	clearInterval(initialLoad);
        console.log("Devices are available: " + deviceList);
        console.log("Starting simulation");
		feedProblems();
    }
    else {
        console.log("Device is not available yet");
    }
}, 10000);
