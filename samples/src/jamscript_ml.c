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
	float result = 1.0 / (1.0 + sumOfProducts(weights, inputs, getLength(weights)) - bias);
	return result;
}


int main() {
	int deviceId = getId();
	struct NEURON_TASK assignedTask;

	while(1) {
		if (task.deviceId == deviceId) {
			assignedTask = task;
			// compute task and log result
			NeuronResult = {
			  .problemId: task.problemId,
				.neuronId : task.neuronId,
				.value : computeTask(task)
			};
		}
		sleep(1);
	}
}
