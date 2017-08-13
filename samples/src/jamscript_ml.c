#include <unistd.h>
#include <stdlib.h>
#include <math.h>

int main() {
	struct NEURAL_NETWORK nn;
	struct TASK task;
	int isNetwork;
	struct result;

	if (isNetwork) {
		// construct neural network
		constructNN(nn);
	} 
	else {
		// compute task and log result
		computeTask(task);
	}

}

float computeTask(task) {
	// get corresponding weights and bias from neural network struct
	float weights[] = getWeights(task.id);
	float bias = getBias(task.id);
	
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

void constructNN(nn) {
}

