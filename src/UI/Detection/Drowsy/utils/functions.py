import torch

def extract_class_name(p):
    return p.split('/')[-2]

def train_epoch(model, train_loader, criterion, optimizer, device, epoch, num_epochs, total_step):
    
    model.train()
    running_loss = 0.0

    for i, (images, labels) in enumerate(train_loader):  
        # Move tensors to the configured device
        images = images.to(device)
        labels = labels.to(device)
        
        # Forward pass
        outputs = model(images)
        if isinstance(outputs, tuple):
            outputs = outputs[0]
        
        loss = criterion(outputs, labels)
        running_loss += loss.item()
        
        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # Print training statistics
        if (i+1) % 100 == 0 or (i+1) == len(train_loader):
            print ('Epoch [{}/{}], Step [{}/{}], Train Loss: {:.4f}' 
                   .format(epoch+1, num_epochs, i+1, total_step, running_loss / (i+1)))
    
    avg_loss = running_loss / total_step
    return avg_loss

def load_best_model(model, path='best_model.pth'):
    model.load_state_dict(torch.load(path))
    print("Best model loaded from", path)