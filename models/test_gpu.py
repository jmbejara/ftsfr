# Source: https://lightning.ai/docs/pytorch/stable/accelerators/gpu_basic.html
from lightning.pytorch.accelerators import find_usable_cuda_devices

# Find two GPUs on the system that are not already occupied
print(find_usable_cuda_devices(1))

# Found this function in traceback's path to the file in the lightning
from pytorch_lightning.accelerators.cuda import CUDAAccelerator

print(CUDAAccelerator.is_available())