from lightning.pytorch.accelerators import find_usable_cuda_devices

# Find two GPUs on the system that are not already occupied
print(find_usable_cuda_devices(1))

from pytorch_lightning.accelerators.cuda import CUDAAccelerator

print(CUDAAccelerator.is_available())