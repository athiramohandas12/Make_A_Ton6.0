from train import *
import torch

trained_file_dir = r"C:/Users/Lenovo/Downloads/Make_A_Ton6.0/data_test_new"



FNN = FNN_Model()
FNN.load_state_dict(torch.load(trained_file_dir))

def get_inference(day,people):
    tp = people
    day = day/10
    people = people/273
    input = torch.Tensor([day,people])
    output_tensor = FNN.model(input)
    out = []
    for i in range(2,len(FNN.Norms),2):
        output = round(float(float(FNN.Norms[i])-float(FNN.Norms[i+1])*output_tensor[(i//2)-1]),2)
        output = round(output*people,2)
        if output < 0:
            output = output * -1
        out.append(output)
    return(out)