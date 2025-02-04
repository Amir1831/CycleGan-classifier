import torch
import torch.nn as nn


class ConvBlock(nn.Module):
    def  __init__ (self , in_channel , out_channel , down = True , use_act = True , **kwargs):
        super().__init__()
        if down : 
            self.model = nn.Sequential(
                nn.Conv2d(in_channel , out_channel , padding_mode = "reflect" , **kwargs),
                nn.InstanceNorm2d(out_channel),
                nn.ReLU(inplace=True) if use_act else nn.Identity())
        else: 
            self.model = nn.Sequential(
            nn.ConvTranspose2d(in_channel , out_channel , **kwargs),
            nn.InstanceNorm2d(out_channel),
            nn.ReLU(inplace=True) if use_act else nn.Identity()
            )

    def forward(self ,x):
       return self.model(x)


class ResidualBlock(nn.Module):
    def __init__(self , channels):
        super().__init__()
        self.block = nn.Sequential(
            ConvBlock(channels , channels , kernel_size = 3 , padding = 1),
            ConvBlock(channels , channels , kernel_size = 3 , use_act = False , padding = 1)
        )

    def forward(self , x):
        return x + self.block(x)


class Generator(nn.Module):
    def __init__(self, img_channels ,num_features = 64, num_residuals = 9):
        super().__init__()
        self.initial = nn.Sequential(
            nn.Conv2d(img_channels , num_features , kernel_size=7 , stride = 1 , padding = 3 ,padding_mode = "reflect"),
            nn.ReLU(inplace = True )
        )
        self.down_blocks = nn.ModuleList(
            [
                ConvBlock(num_features , num_features *2  ,kernel_size=3 , padding= 1 , stride = 2 ),
                ConvBlock(num_features*2 , num_features *4  ,kernel_size=3 , padding= 1 , stride = 2 )
            ]
        )

        self.residual_blocks = nn.Sequential(
            *[ResidualBlock(num_features*4) for _ in range(num_residuals)]
        )
        self.up_blocks = nn.ModuleList(
            [
                ConvBlock(num_features * 4 , num_features * 2 , down = False , kernel_size=3 , stride =2 , padding =1 , output_padding = 1),
                ConvBlock(num_features * 2 , num_features  , down = False , kernel_size=3 , stride =2 , padding =1 , output_padding = 1)
            ]
        )
        self.last = nn.Conv2d(num_features*1 , img_channels , kernel_size = 7 , stride = 1 , padding = 3 , padding_mode = "reflect")

    def forward(self , x):
        x = self.initial(x)
        # print(f"initial : {x.shape}")
        for layer in self.down_blocks:
            x = layer(x)
        # print(f"down_blocks : {x.shape}")
        x = self.residual_blocks(x)
        # print(f"residual : {x.shape}")
        for layer in self.up_blocks :
            x = layer(x)
        # print(f"up block : {x.shape}")
        return torch.tanh(self.last(x))

def test():

    img_channels = 3
    img_size = 256
    x = torch.randn((2 , img_channels , img_size , img_size))
    gen = Generator(img_channels , 9)
    print(gen)
    print(f"input : {x.shape}")
    print(gen(x).shape)

if __name__ == "__main__":
    test()