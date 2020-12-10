import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
from sklearn import datasets
# 设备配置，部署GPU加速
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# Hyper-parameters，定义各层规模及其他超参数
input_size = 64
hidden_size = 500
num_classes = 10
num_epochs = 5
batch_size = 100
learning_rate = 0.001
# sklearn dataset，准备数据集，转换为Tensor数据格式
digits = datasets.load_digits()
images_and_labels = list(zip(torch.from_numpy(digits.images/16).float(), torch.from_numpy(digits.target).long()))
n_samples = len(digits.images)

train_loader = images_and_labels[:n_samples//2]
test_loader = images_and_labels[n_samples//2:]
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
            images = images.reshape(-1, 8 * 8).to(device)
            labels = labels.reshape(1).to(device)

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
    torch.save(model.state_dict(), 'model_skl.ckpt')
    
# Test the model 测试模型
def test_model(model, test_loader, device):
    model.load_state_dict(torch.load('model_skl.ckpt', map_location=device))
    with torch.no_grad():
        correct = 0
        total = 0
        for images, labels in test_loader:
            images = images.reshape(-1, 8 * 8).to(device)
            labels = labels.reshape(1).to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
        print('Accuracy is: {}%'.format(100 * correct / total))
        
train_model(model, train_loader)
test_model(model, test_loader, device)
