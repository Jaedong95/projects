import torch
import torch.nn as nn


class C3D(nn.Module):
    """
    The C3D network.
    """

    def __init__(self, pretrained=None):
        super(C3D, self).__init__()

        self.pretrained = pretrained

        self.conv1a = nn.Conv3d(3, 64, kernel_size=(3, 3, 3), padding=(1, 1, 1))
        self.pool1 = nn.MaxPool3d(kernel_size=(1, 2, 2), stride=(1, 2, 2))

        self.conv2a = nn.Conv3d(64, 128, kernel_size=(3, 3, 3), padding=(1, 1, 1))
        self.pool2 = nn.MaxPool3d(kernel_size=(2, 2, 2), stride=(2, 2, 2))

        self.conv3a = nn.Conv3d(128, 256, kernel_size=(3, 3, 3), padding=(1, 1, 1))
        self.pool3 = nn.MaxPool3d(kernel_size=(2, 2, 2), stride=(2, 2, 2))

        self.conv4a = nn.Conv3d(256, 256, kernel_size=(3, 3, 3), padding=(1, 1, 1))
        self.pool4 = nn.MaxPool3d(kernel_size=(2, 2, 2), stride=(2, 2, 2))

        self.conv5a = nn.Conv3d(256, 256, kernel_size=(3, 3, 3), padding=(1, 1, 1))
        self.pool5 = nn.MaxPool3d(kernel_size=(2, 2, 2), stride=(2, 2, 2), padding=(0, 1, 1))

        self.fc6 = nn.Linear(4096, 2048)    
        self.fc7 = nn.Linear(2048, 2048)   # customizing 
        self.fc8 = nn.Linear(2048, 4)    # customizing 
        
        self.dropout = nn.Dropout(p=0.5)   # customizing 
        self.relu = nn.ReLU()
        self.softmax = nn.Softmax(dim=1)   # customizing 
        
        self.__init_weight()

        if pretrained:
            self.__load_pretrained_weights()

    def forward(self, x):
        x = self.relu(self.conv1a(x))
        x = self.pool1(x)
        x = self.relu(self.conv2a(x))
        x = self.pool2(x)
        x = self.relu(self.conv3a(x))
        x = self.pool3(x)
        x = self.relu(self.conv4a(x))
        x = self.pool4(x)
        x = self.relu(self.conv5a(x))
        x = self.pool5(x)
        x = x.view(-1, 4096)
        x = self.relu(self.fc6(x))
        x = self.dropout(x)
        x = self.relu(self.fc7(x))
        x = self.dropout(x)

        logits = self.fc8(x)
        probs = self.softmax(logits)

        return probs

    def __load_pretrained_weights(self):
        """Initialiaze network."""
        corresp_name = [
            # Conv1
            "conv1.weight",
            "conv1.bias",
            # Conv2
            "conv2.weight",
            "conv2.bias",
            # Conv3a
            "conv3a.weight",
            "conv3a.bias",
            # Conv3b
            "conv3b.weight",
            "conv3b.bias",
            # Conv4a
            "conv4a.weight",
            "conv4a.bias",
            # Conv4b
            "conv4b.weight",
            "conv4b.bias",
            # Conv5a
            "conv5a.weight",
            "conv5a.bias",
            # Conv5b
            "conv5b.weight",
            "conv5b.bias",
            # fc6
            "fc6.weight",
            "fc6.bias",
            # fc7
            "fc7.weight",
            "fc7.bias",
            # fc8
            "fc8.weight",
            "fc8.bias"
        ]

        ignored_weights = [f"{layer}.{type_}" for layer, type_ in itertools.product(['fc7', 'fc8'], ['bias', 'weight'])]

        p_dict = torch.load(self.pretrained)
        s_dict = self.state_dict()
        for name in p_dict:
            if name not in corresp_name:
                if name in ignored_weights:
                    continue
                print("no corresponding::", name)
                continue
            s_dict[name] = p_dict[name]
        self.load_state_dict(s_dict)


    def __init_weight(self):
        for m in self.modules():
            if isinstance(m, nn.Conv3d):
                # n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
                # m.weight.data.normal_(0, math.sqrt(2. / n))
                torch.nn.init.kaiming_normal_(m.weight)
            elif isinstance(m, nn.BatchNorm3d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()


if __name__ == "__main__":
    inputs = torch.ones((1, 3, 16, 112, 112))
    net = C3D(pretrained=False)

    outputs = net.forward(inputs)
    print(outputs.size())
	