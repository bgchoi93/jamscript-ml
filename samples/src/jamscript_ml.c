#include <unistd.h>
#include <stdlib.h>
#include <math.h>
int getId();

char* append(char *string1, char c) {
    char * result = NULL;
    asprintf(&result, "%s%c", string1, c);
    return result;
}

int getLength(char* arrayPointer) {
    int count = 0;

    if (*arrayPointer) {
        count++;
        while(*arrayPointer) {
            if (*arrayPointer == 44) {
                count++;
            }
            arrayPointer++;
        }
    }

    return count;
}

float* getFloatArray(char* arrayPointer) {

    int length = getLength(arrayPointer);
    int index = 0;
    char *floatString = "";

    float *floats = malloc(length * sizeof(float));

    if (length > 0) {
        // starts with [, initialize parsing
        if (*arrayPointer == 91) {
            arrayPointer++;
        }
        // parse comma-separated string to floats
        while (*arrayPointer) {
            if (*arrayPointer == 44) {
                floats[index] = atof(floatString);
                floatString = "";
                index++;
            }
            else if (*arrayPointer != 93) {
                floatString = append(floatString, *arrayPointer);
            }
            // add last element
            else if (*arrayPointer == 93) {
                floats[index] = atof(floatString);
                floatString = "";
                index++;
            }
            arrayPointer++;
        }
    }

    return floats;
}
float sumOfProducts(float* weights, float* inputs, int length) {
	float sum = 0.0;

	for (int i = 0; i < length; i++) {
		sum = sum + inputs[i] * weights[i];
	}

	return sum;
}


float computeTask(struct NEURON_TASK task) {
	// get corresponding weights and bias from neural network struct
	float *weights = getFloatArray(task.weights);
	float *inputs = getFloatArray(task.inputs);
	float bias = task.bias;

	// compute result
	float result = 1.0 / (1.0 + exp(-sumOfProducts(weights, inputs, getLength(task.weights)) - bias));
	return result;
}


int main() {
	int deviceId = getId();
	printf("Device ID: %d\n", deviceId);
	struct NEURON_TASK assignedTask;
	while(1) {
		assignedTask = NeuronTask;
		if (assignedTask.deviceId == deviceId) {
			printf("Task is assigned\n");
			// compute task and log result
			float result = computeTask(assignedTask);
			printf("Result for problem %d, neuron %d : %f\n", assignedTask.problemId, assignedTask.neuronId, result);
			printf("Weights: %s\n", assignedTask.weights);
			printf("Inputs: %s\n", assignedTask.inputs);
			printf("bias: %f\n", assignedTask.bias);
			NeuronResult = {
				.problemId: assignedTask.problemId,
				.neuronId : assignedTask.neuronId,
				.value : result
			};
		}
		sleep(1);
	}
}
