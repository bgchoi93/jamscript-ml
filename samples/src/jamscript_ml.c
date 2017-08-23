#include <unistd.h>
#include <stdlib.h>
#include <math.h>

int main() {
	int deviceId = getId();
	struct NEURON task;

	while(1) {
		if (task.deviceId == deviceId) {
			// compute task and log result
			OUTPUT = {
			    .problemId: task.problemId,
				.neuronId : task.neuronId,
				.value : computeTask(task)
			};
		}
	}
}

float computeTask(struct Neuron task) {
	// get corresponding weights and bias from neural network struct
	float weights[] = task.weights;
	float bias = task.bias;
	
	// get inputs from the task
	float inputs[] = task.inputs;

	// compute result
	float result = 1.0 / (1.0 + sumOfProducts(weights, inputs) - bias);
	return result;
}

float sumOfProducts(weights, inputs) {
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