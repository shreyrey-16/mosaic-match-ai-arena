# ai_player.py - the AI opponent
# Uses a ResNet18 that was already trained on ImageNet (transfer learning, module 2).
# We cut off the last classification layer, so the network just gives us a feature
# vector for each image. Then the AI picks whichever choice has the most similar vector.
import torch
from torchvision import models


class AIPlayer:
    def __init__(self):
        weights = models.ResNet18_Weights.DEFAULT
        self.model = models.resnet18(weights=weights)
        self.model.fc = torch.nn.Identity()  # throw away the 1000-class layer
        self.model.eval()
        self.prep = weights.transforms()  # resize + normalise like ImageNet

    def embed(self, img):
        with torch.no_grad():
            x = self.prep(img).unsqueeze(0)
            v = self.model(x)[0]
        return torch.nn.functional.normalize(v, dim=0)

    def guess(self, target, choices):
        """returns (index of best match, list of similarity scores)"""
        t = self.embed(target)
        sims = [float(t @ self.embed(c)) for c in choices]
        best = max(range(len(sims)), key=lambda i: sims[i])
        return best, sims
