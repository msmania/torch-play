# https://lightning.ai/docs/pytorch/stable/model/train_model_basic.html

import os
import torch
from torch import nn
import torch.nn.functional as F
from torchvision import transforms
from torchvision.datasets import MNIST
from torch.utils.data import DataLoader
import lightning as L

class Encoder(nn.Module):
  def __init__(self):
    super().__init__()
    self.l1 = nn.Sequential(nn.Linear(28 * 28, 64), nn.ReLU(), nn.Linear(64, 3))

  def forward(self, x):
    return self.l1(x)

class Decoder(nn.Module):
  def __init__(self):
    super().__init__()
    self.l1 = nn.Sequential(nn.Linear(3, 64), nn.ReLU(), nn.Linear(64, 28 * 28))

  def forward(self, x):
    return self.l1(x)

class LitAutoEncoder(L.LightningModule):
  def __init__(self, encoder, decoder):
    super().__init__()
    self.encoder = encoder
    self.decoder = decoder

  def training_step(self, batch, batch_idx):
    # training_step defines the train loop.
    x, _ = batch
    x = x.view(x.size(0), -1)
    z = self.encoder(x)
    x_hat = self.decoder(z)
    loss = F.mse_loss(x_hat, x)
    return loss

  def configure_optimizers(self):
    optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)
    return optimizer

def main():
  dataset = MNIST(os.getcwd(), download=True, transform=transforms.ToTensor())
  train_loader = DataLoader(dataset, num_workers=3)

  # model
  autoencoder = LitAutoEncoder(Encoder(), Decoder())

  # train model
  trainer = L.Trainer(fast_dev_run=1000)
  trainer.fit(model=autoencoder, train_dataloaders=train_loader)

if __name__ == "__main__":
  main()
