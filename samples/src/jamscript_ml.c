#include <unistd.h>
#include <stdlib.h>
#include <math.h>
int getId();

float sumOfProducts(float* weights, float* inputs) {
	if (sizeof(weights) == sizeof(inputs)) {
		
		float sum = 0.0;

		for (int i = 0; i < sizeof(weights); i++) {
			sum = sum + inputs[i] * weights[i];
		}

		return sum;

	} else {
		// throw an error
	}
}


float computeTask(struct NEURON_TASK task) {
	// get corresponding weights and bias from neural network struct
	//float weights[getLength(task.weights)];
	//weights = parseToFloatArray(task.weights);
	float weights[] = {0.1, 0.2, 0.3};
	float inputs [] = {0.3, 0.2, 0.1};
	float bias = task.bias;
	
	// get inputs from the task
	//float inputs[10]
	//inputs = parseToFloatArray(task.inputs);

	// compute result
	float result = 1.0 / (1.0 + sumOfProducts(weights, inputs) - bias);
	return result;
}


int main() {
	int deviceId = getId();
	struct NEURON_TASK task;

	while(1) {
		if (task.deviceId == deviceId) {
			// compute task and log result
			NEURON_RESULT = {
			    .problemId: task.problemId,
				.neuronId : task.neuronId,
				.value : computeTask(task)
			};
		}
	}
}
