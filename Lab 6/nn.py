import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
# 设备配置，部署GPU加速
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# Hyper-parameters，定义各层规模及其他超参数
input_size = 784
hidden_size = 500
num_classes = 10
num_epochs = 5
batch_size = 100
learning_rate = 0.001
# MNIST dataset，准备数据集，转换为Tensor数据格式
train_dataset = torchvision.datasets.MNIST(root='data',train=True,transform=transforms.ToTensor(),download=True)
test_dataset = torchvision.datasets.MNIST(root='data',train=False,transform=transforms.ToTensor())
# DataLoader类，进行batch_size(每个batch的大小),
# shuffle(是否进行shuffle操作),
# num_workers(加载数据的时候使用几个子进程)等操作
train_loader = torch.utils.data.DataLoader(dataset=train_dataset,batch_size=batch_size,shuffle=True)
test_loader = torch.utils.data.DataLoader(dataset=test_dataset,batch_size=batch_size,shuffle=False)
# 定义网络结构，Fully connected neural network with one hidden layer
class NeuralNet(nn.Module): 
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, num_classes)
    def forward(self, x):
        # 向前传播，模型的计算流程
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out
    
model = NeuralNet(input_size, hidden_size, num_classes)
# Loss and optimizer
# 定义损失函数，使用的是交叉熵函数
criterion = nn.CrossEntropyLoss()
# 定义迭代优化算法，使用的是Adam (Adaptive Moment Estimation)
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
# Train the model 迭代训练
def train_model(model, train_loader):
    total_step = len(train_loader)
    for epoch in range(num_epochs):
        for i, (images, labels) in enumerate(train_loader):
            # Move tensors to the configured device
            images = images.reshape(-1, 28 * 28).to(device)
            labels = labels.to(device)

            # Forward pass，前向传播计算网络结构的输出结果
            outputs = model(images)
            # 计算损失函数
            loss = criterion(outputs, labels)
            # Backward and optimize 反向传播更新参数
            # 将上次迭代计算的梯度值清0
            optimizer.zero_grad()
            # 反向传播，计算梯度值
            loss.backward()
            # 更新权值参数
            optimizer.step()
            # 打印训练信息
            if (i + 1) % 100 == 0:
                print('Epoch [{}/{}], Step [{}/{}], loss: {:.4f}'.format(epoch + 1, num_epochs, i + 1, total_step, loss.item()))
    # 保存训练好的模型
    torch.save(model.state_dict(), 'model.ckpt')
    
# Test the model 测试模型
def test_model(model, test_loader, device):
    model.load_state_dict(torch.load('model.ckpt', map_location=device))
    with torch.no_grad():
        correct = 0
        total = 0
        for images, labels in test_loader:
            images = images.reshape(-1, 28 * 28).to(device)
            labels = labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
        print('Accuracy is: {}%'.format(100 * correct / total))
train_model(model, train_loader)
test_model(model, test_loader, device)
