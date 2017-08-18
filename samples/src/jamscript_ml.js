jdata{
	struct Neuron {
		int id;
		int layer;
		int [] weights;
		int complete; //0 if not complete, 1 if complete
	} neuron as broadcaster;
	int [] layerInput as broadcaster;
	struct Output {
		int neuron;
		int value;
	} output as logger;
	int [] problemInput as logger;
}

var network = require('/network.json');

var problems = [],
	inputs = [],
	layer_num = 0;  

var outputListener = function(key,entry){
	console.log("key: " + key + " entry: " + entry);
	inputs[entry.neuron] = entry.value;
}

var problemListener = function(key,entry){
	problems.push(entry);
}

var layer_computation = function(layerNumber){
	input.broadcast(inputs)
	var nextLayer = network.network[layerNumber+1];
	inputs = new Array(network[nextLayer].length);
	return;
}

var compute_network = function(layer){
	var layerNumber = layer;
	var increment_layer = function(){
		layer_computation(layerNumber);
		layerNumber ++;
	}
}
