# This is for training the classifier (AI) This doesn't matter for the game to run

import torch # type: ignore
import torch.nn as nn # type: ignore
import torch.optim as optim # type: ignore
from torch.utils.data import Dataset, DataLoader # type: ignore
import os
import numpy as np
from preprocess import preprocess_image

# Classes
classes = ["rock", "paper", "scissors"]

# Custom dataset class
class RPSDataset(Dataset):
    def __init__(self, data_dir):
        self.images = []
        self.labels = []
        for idx, label in enumerate(classes):
            folder = os.path.join(data_dir, label)
            for fname in os.listdir(folder):
                if fname.endswith(".png"):
                    path = os.path.join(folder, fname)
                    img = preprocess_image(path)   # shape: (64, 64, 1)
                    img = np.transpose(img, (2, 0, 1))  # to (1, 64, 64)
                    self.images.append(img)
                    self.labels.append(idx)

        self.images = torch.tensor(self.images, dtype=torch.float32)
        self.labels = torch.tensor(self.labels, dtype=torch.long)

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        return self.images[idx], self.labels[idx]

# CNN model
class RPScnn(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(1, 16, 3, padding=1), nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(16, 32, 3, padding=1), nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Flatten(),
            nn.Linear(32 * 16 * 16, 32), nn.ReLU(),
            nn.Linear(32, 3)
        )

    def forward(self, x):
        return self.net(x)

# Load data
dataset = RPSDataset("data/")
loader = DataLoader(dataset, batch_size=8, shuffle=True)

# Model, loss, optimizer
model = RPScnn()
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
for epoch in range(15):
    for imgs, labels in loader:
        optimizer.zero_grad()
        output = model(imgs)
        loss = criterion(output, labels)
        loss.backward()
        optimizer.step()
    print(f"Epoch {epoch+1}/15, Loss: {loss.item():.4f}")

# Save model
torch.save(model.state_dict(), "rps_model.pt")
print("Saved model: rps_model.pt")