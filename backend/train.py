import torch
import pandas as pd
# loading and preprocessing the data
csv_file = r"C:/Users/Lenovo/Downloads/Make_A_Ton6.0/final2.csv"
df = pd.read_csv(csv_file)
Norms = df.iloc[7]
Norms[15] = 1
Norm = []

# Creating the dataset
class Food_Quantity_Data(torch.utils.data.Dataset):
    def __init__(self,df):
        self.dataframe = df
        print(df)
        super().__init__()
    def __getitem__(self,id):
        id = id + 2
        data = self.dataframe.iloc[id]
        labels = [data[0]/7,data[1]/Norms[1]]
        Norm_people =float(data[1]/Norms[1])
        targets = []
        for i in range(2,self.dataframe.shape[1],2):
            targets.append((float(data[i])/(float(Norms[i])) - float(data[i+1])/(float(Norms[i+1])))*Norm_people)
            Norm.append(Norms[i])
        return labels,targets
    def __len__(self):
        return self.dataframe.shape[0]-2

# Creating the data Module
from pytorch_lightning import LightningDataModule
class Food_loader_Module(LightningDataModule):
    def __init__(self,dataset,num_workers = 0,batch_size = 128):
        self.dataset = dataset
        self.num_workers = num_workers
        self.batch_size = batch_size
        super().__init__()
    def train_dataset(self,df = df):
        return Food_Quantity_Data(df)
    def train_dataloader(self):
        train_dataset = self.train_dataset()
        train_loader = torch.utils.data.DataLoader(
            train_dataset,
            batch_size = self.batch_size,
            shuffle = True,
            pin_memory=True,
            drop_last=True,
            num_workers=self.num_workers,
            collate_fn=self.collate_fn
        )
        return train_loader
    def val_dataloader(self):
        valid_dataset = self.train_dataset()
        valid_loader = torch.utils.data.DataLoader(
            valid_dataset,
            batch_size = self.batch_size,
            shuffle = True,
            pin_memory=True,
            drop_last=True,
            num_workers=self.num_workers,
            collate_fn=self.collate_fn
        )
        return valid_loader
    @staticmethod
    def collate_fn(batch):
        labels,targets = tuple(zip(*batch))
        labels = torch.tensor(labels)
        targets = torch.tensor(targets)
        return labels,targets

class Model(torch.nn.Module):
    def __init__(self,n_inputs,n_outputs):
        super(Model,self).__init__()
        self.n_inputs = n_inputs
        self.n_outputs = n_outputs
        self.hidden_layer_1 = torch.nn.Linear(n_inputs,n_outputs*2)
        self.hidden_layer_2 = torch.nn.Linear(n_outputs*2,n_outputs*4)
        self.hidden_layer_3 = torch.nn.Linear(n_outputs*4,n_outputs*2)
        self.final_layer = torch.nn.Linear(n_outputs*2,n_outputs)
    def forward(self,x):
        x = x.float()
        x = self.hidden_layer_1(x)
        x = self.hidden_layer_2(x)
        x = self.hidden_layer_3(x)
        x = self.final_layer(x)
        return x

from pytorch_lightning import LightningModule
class FNN_Model(LightningModule):
    def __init__(self,lr = 0.1):
        super().__init__()
        self.model = Model(2,21)
        self.lr = lr
        self.loss_fn = torch.nn.MSELoss()
        self.Norms = Norms
    def forward(self, label, targets):
        return self.model(label, targets)
    def configure_optimizers(self):
        return torch.optim.AdamW(self.model.parameters(), lr=self.lr)
    def loss(self,output,target):
        self.loss_fn(output,target)

    def training_step(self, batch, batch_idx):
        torch.cuda.empty_cache()
        labels,targets = batch    
        outputs = self.model(labels)
        loss = self.loss_fn(outputs,targets)
        self.log("train_loss", loss, on_step=True, on_epoch=True, prog_bar=True,logger=True)
        return loss

from pytorch_lightning import Trainer
def main():
    FNN = FNN_Model()
    trainer = Trainer(max_epochs=500, num_sanity_val_steps=0,accelerator="cpu",devices = [0])
    dm = Food_loader_Module(df)
    trainer.fit(FNN,dm)
    torch.save(FNN.state_dict(), f'data_test')

if __name__ == "__main__":
    main()

