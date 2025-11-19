# This is for training the classifier (AI)

import torch  # type: ignore
import torch.nn as nn  # type: ignore
import torch.optim as optim  # type: ignore
from torch.utils.data import Dataset, DataLoader  # type: ignore
import os
import numpy as np
from preprocess import preprocess_image

# Classes
classes = ["rock", "paper", "scissors"]

# ================================ Classes definitions ==================================

class RPSDataset(Dataset):
    def __init__(self, data_dir, size=64):
        self.images = []
        self.labels = []
        for idx, label in enumerate(classes):
            folder = os.path.join(data_dir, label)
            if not os.path.isdir(folder):
                continue
            for fname in os.listdir(folder):
                if fname.lower().endswith(".png") or fname.lower().endswith(".jpg"):
                    path = os.path.join(folder, fname)
                    img = preprocess_image(path, size=size, save_debug=False)   # shape: (64, 64, 1)
                    img = np.transpose(img, (2, 0, 1))  # to (1, 64, 64) for PyTorch
                    self.images.append(img)
                    self.labels.append(idx)

        if len(self.images) == 0:
            raise RuntimeError(f"No images found under {data_dir}. Make sure data/rock etc. exist.")

        self.images = torch.tensor(np.array(self.images), dtype=torch.float32)
        self.labels = torch.tensor(self.labels, dtype=torch.long)

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        return self.images[idx], self.labels[idx]


class RPScnn(nn.Module):
    def __init__(self, in_channels=1):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(in_channels, 16, 3, padding=1), nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(16, 32, 3, padding=1), nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Flatten(),
            nn.Linear(32 * 16 * 16, 32), nn.ReLU(),
            nn.Linear(32, len(classes))
        )

    def forward(self, x):
        return self.net(x)


# ================================ Training ==================================

def train(data_dir="data/", epochs=20, batch_size=8, lr=1e-3, size=64):
    dataset = RPSDataset(data_dir, size=size)
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    model = RPScnn(in_channels=1)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    best_loss = float("inf")
    for epoch in range(epochs):
        running_loss = 0.0
        for imgs, labels in loader:
            optimizer.zero_grad()
            output = model(imgs)
            loss = criterion(output, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item() * imgs.size(0)

        epoch_loss = running_loss / len(dataset)
        print(f"Epoch {epoch+1}/{epochs}: loss={epoch_loss:.4f}")

        # save every epoch
        torch.save(model.state_dict(), "rps_model.pt")

    print("Training finished. Model saved to rps_model.pt")


if __name__ == "__main__":
    # default training run if executed directly
    train(data_dir="data/", epochs=15, batch_size=8, lr=0.001, size=64)