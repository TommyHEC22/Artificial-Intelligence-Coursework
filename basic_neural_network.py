import csv
import random
import numpy as np
import pandas as pd

def parameters():
    num_inputs = 2
    num_hidden_units = 2
    num_outputs = 1
    num_epochs = 20
    learning_rate = 0.1
    activation_function = "sigmoid"

    return num_inputs, num_hidden_units, num_outputs, num_epochs, learning_rate, activation_function

def input_data():
    choose = input("Type 0 if you want to enter data manually, type 1 to upload a file (note the file must have 3 columns with the third column containing only 0's and 1's)...")

    if choose == "0":

        with open('data.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Input1', 'Input2', 'Result'])

        rows = input("how many rows do you want to enter? ")
        for i in range(0, int(rows)):
            input_value = float(input("Enter input value 1: "))
            input_value2 = float(input("Enter input value 2: "))
            result = int(input("Enter the result (1 or 0):"))

            with open('data.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([input_value, input_value2, result])
        filename = 'data.csv'

    if choose == "1":
        filename = input("Enter the filename (with .csv extension): ")   
    data = pd.read_csv(filename)
        
    return data

def structure(num_inputs, num_hidden_units, num_outputs):

    input_to_hidden_unit = num_inputs * num_hidden_units
    hidden_to_output_unit = num_hidden_units * num_outputs
    weights_needed = input_to_hidden_unit + hidden_to_output_unit

    return {
        "num_inputs": num_inputs,
        "num_hidden": num_hidden_units,
        "num_outputs": num_outputs,
        "weights_needed": weights_needed, }  

def initialise(weights_needed):
    weights = []
    for i in range(weights_needed):
        weights.append(random.uniform(0, 1))
    
    return weights
         
def introduced(data, weights, num_epochs, learning_rate): 
    for epoch in range(num_epochs):
        rows = list(range(len(data)))
        random.shuffle(rows)

        for row in rows:
            x11, x12, h1, h2, result = output(data, weights, row)
            target = data.iloc[row, 2]
            weights = weightUpdate(weights, result, target, learning_rate, x11, x12, h1, h2)
        
        print("epoch:", epoch + 1, "complete")
            
    return weights

def sigmoid(x):
        return 1 / (1 + np.exp(-x))

def output(data, weights, row):
    
    x11 = data.iloc[row, 0]
    x12 = data.iloc[row, 1]
    x21 = x11*weights[0] + x12*weights[1]
    x22 = x11*weights[2] + x12*weights[3]
    h1 = sigmoid(x21)
    h2 = sigmoid(x22)
    y = weights[4]*h1 + weights[5]*h2
    result = sigmoid(y)

    return x11, x12, h1, h2, result

def weightUpdate(weights, result, target, learning_rate, x11, x12, h1, h2):
    w = weights
    error = float(target - result)
    lr = float(learning_rate)
    x11 = float(x11)
    x12 = float(x12)
    h1 = float(h1)
    h2 = float(h2)

    w[0] = w[0] + lr * error * x11
    w[1] = w[1] + lr * error * x12
    w[2] = w[2] + lr * error * x11
    w[3] = w[3] + lr * error * x12
    w[4] = w[4] + lr * error * h1
    w[5] = w[5] + lr * error * h2

    return list(w)

def print_weights(weights):
    print("Final weights after training:")
    print("weight 1 = input 1 to hidden unit 1", weights[0])
    print("weight 2 = input 2 to hidden unit 1", weights[1])
    print("weight 3 = input 1 to hidden unit 2", weights[2])
    print("weight 4 = input 2 to hidden unit 2", weights[3])
    print("weight 5 = hidden unit 1 to output", weights[4])
    print("weight 6 = hidden unit 2 to output", weights[5])

num_inputs, num_hidden_units, num_outputs, num_epochs, learning_rate, activation_function = parameters() 
struct = structure(num_inputs, num_hidden_units, num_outputs)
weights_needed = struct["weights_needed"]

parameters()
data = input_data()
weights = initialise(weights_needed)
introduced(data, weights, num_epochs, learning_rate)
print_weights(weights)
