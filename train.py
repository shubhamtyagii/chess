from torch.utils.data import Dataset
import numpy as np
class ChessValueDataset(Dataset):
    def __init__(self):
        data=np.load('./processed/dataset.npz')
        self.X=data['arr_0']
        self.Y=data['arr_1']
        print('loaded data shapes= ',self.X.shape,self.Y.shape)


    def __len__(self):
        return self.X.shape[0]

    def __getitem__(self,idx):
        return {'X':self.X[idx],'Y':self.Y[idx]}

chess_dataset=ChessValueDataset()