import torch
import numpy as np
from torch import nn
import torch.nn.functional as F
from tqdm import tqdm

def train(train_dataloader, model, optimizer, epoch, batch_size, device, scheduler=None, criterion=nn.CrossEntropyLoss()):
    print("Starting Epoch", epoch)

    bar = tqdm(enumerate(train_dataloader), total=len(train_dataloader))

    targets_img_gps = torch.Tensor([i for i in range(batch_size)]).long().to(device)

    total_loss = 0

    for i ,(imgs, gps) in bar:

        imgs = torch.from_numpy(np.asarray(imgs))
        # gps = torch.from_numpy(np.asarray(gps))
        # gps = torch.transpose( gps, 1,0)

        # Stack along dimension 0 (creates shape [2, N])
        gps_tensor = torch.stack(gps)
        # Transpose to get shape (N, 2)
        gps_tensor = gps_tensor.T  # or gps_tensor.transpose(0, 1)



        #print("before", imgs.dtype, gps_tensor.dtype)
        imgs = imgs.float()
        gps = gps_tensor.float()
        #print("after", imgs.dtype, gps.dtype)


        imgs = imgs.to(device)
        gps = gps.to(device)
        gps_queue = model.get_gps_queue()
        #print(gps.shape, gps_queue.shape)
        optimizer.zero_grad()

        # Append GPS Queue & Queue Update
        gps_all = torch.cat([gps, gps_queue], dim=0)
        model.dequeue_and_enqueue(gps)

        # Forward pass
        logits_img_gps = model(imgs, gps_all)

        # Compute the loss
        img_gps_loss = criterion(logits_img_gps, targets_img_gps)
        loss = img_gps_loss

        # Backpropagate
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

        bar.set_description("Epoch {} loss: {:.5f}".format(epoch, loss.item()))

    if scheduler is not None:
        scheduler.step()

    # Remove the return statement
    # return total_loss / len(train_dataloader)
