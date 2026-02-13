import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import io


class CNNFigureEncoder:
    def __init__(self, device=None):
        print("Loading ResNet18 for Visual Analysis...")

        # Device handling (CPU / GPU)
        self.device = device if device else (
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        # Load pretrained ResNet18 (new style)
        weights = models.ResNet18_Weights.DEFAULT
        self.model = models.resnet18(weights=weights)

        # Remove final classification layer → get feature extractor
        self.model = torch.nn.Sequential(*list(self.model.children())[:-1])

        self.model.eval()
        self.model.to(self.device)

        # Standard ImageNet preprocessing
        self.preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            ),
        ])

    def analyze_image_stream(self, image_bytes):
        """
        Extracts feature embedding from an image.
        Returns:
            (success_flag, embedding_vector or error_message)
        """
        try:
            # Load image
            input_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

            # Preprocess
            input_tensor = self.preprocess(input_image)
            input_batch = input_tensor.unsqueeze(0).to(self.device)

            # Inference
            with torch.no_grad():
                features = self.model(input_batch)

            # Flatten (1, 512, 1, 1) → (512,)
            embedding = features.squeeze().cpu().numpy()

            return True, embedding

        except Exception as e:
            return False, str(e)
