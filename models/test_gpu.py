"""
test_gpu.py

Utility script to test GPU availability for different frameworks used in the models.
Run this to verify GPU support before running models.

Usage:
    # Test all frameworks
    python test_gpu.py

    # Test specific framework
    python test_gpu.py --framework torch
"""

import argparse
import subprocess
import sys


def test_nvidia_smi():
    """Test if nvidia-smi is available (basic GPU check)."""
    print("Testing nvidia-smi...")
    try:
        result = subprocess.run(["nvidia-smi"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ nvidia-smi detected GPU(s)")
            # Parse output to show GPU info
            lines = result.stdout.split("\n")
            for line in lines:
                if "NVIDIA" in line and "Driver" in line:
                    print(f"  {line.strip()}")
            return True
        else:
            print("✗ nvidia-smi failed")
            return False
    except FileNotFoundError:
        print("✗ nvidia-smi not found (no NVIDIA driver installed)")
        return False
    except Exception as e:
        print(f"✗ Error running nvidia-smi: {e}")
        return False


def test_cuda():
    """Test CUDA availability."""
    print("\nTesting CUDA...")
    try:
        result = subprocess.run(["nvcc", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            # Extract CUDA version
            for line in result.stdout.split("\n"):
                if "release" in line:
                    print(f"✓ CUDA detected: {line.strip()}")
                    return True
        else:
            print("✗ nvcc failed")
            return False
    except FileNotFoundError:
        print("✗ nvcc not found (CUDA toolkit not installed)")
        return False
    except Exception as e:
        print(f"✗ Error checking CUDA: {e}")
        return False


def test_torch_gpu():
    """Test PyTorch GPU support."""
    print("\nTesting PyTorch GPU support...")
    try:
        import torch

        cuda_available = torch.cuda.is_available()
        print("✓ PyTorch imported successfully")
        print(f"  CUDA available: {cuda_available}")

        if cuda_available:
            print(f"  CUDA device count: {torch.cuda.device_count()}")
            for i in range(torch.cuda.device_count()):
                print(f"  GPU {i}: {torch.cuda.get_device_name(i)}")
            print(f"  Current CUDA device: {torch.cuda.current_device()}")

            # Test tensor creation
            try:
                x = torch.tensor([1.0, 2.0, 3.0]).cuda()
                print("  ✓ Successfully created CUDA tensor")
                return True
            except Exception as e:
                print(f"  ✗ Failed to create CUDA tensor: {e}")
                return False
        else:
            print("  ✗ CUDA not available in PyTorch")
            return False

    except ImportError:
        print("✗ PyTorch not installed")
        print("  Install with: pip install torch")
        return False
    except Exception as e:
        print(f"✗ Error testing PyTorch: {e}")
        return False


def test_lightning_gpu():
    """Test PyTorch Lightning GPU support."""
    print("\nTesting PyTorch Lightning GPU support...")
    try:
        import lightning.pytorch as pl
        from lightning.pytorch.accelerators import find_usable_cuda_devices

        print("✓ PyTorch Lightning imported successfully")
        print(f"  Lightning version: {pl.__version__}")

        # Check if CUDA is available through Lightning
        try:
            # Try to find usable CUDA devices
            devices = find_usable_cuda_devices(1)
            if devices:
                print(f"  Usable CUDA devices: {devices}")

                # Test creating a simple trainer with GPU
                trainer = pl.Trainer(accelerator="gpu", devices=1)
                print("  ✓ Successfully created GPU trainer")
                return True
            else:
                print("  ✗ No usable CUDA devices found")
                return False
        except Exception as e:
            print(f"  ✗ Error finding/using CUDA devices: {e}")
            return False

    except ImportError:
        print("✗ PyTorch Lightning not installed")
        print("  Install with: pip install lightning")
        return False
    except Exception as e:
        print(f"✗ Error testing PyTorch Lightning: {e}")
        return False


def test_tensorflow_gpu():
    """Test TensorFlow GPU support (for GluonTS/TimesFM)."""
    print("\nTesting TensorFlow GPU support...")
    try:
        import tensorflow as tf

        print("✓ TensorFlow imported successfully")
        print(f"  TensorFlow version: {tf.__version__}")

        # List physical devices
        gpus = tf.config.list_physical_devices("GPU")
        print(f"  GPU devices found: {len(gpus)}")

        if gpus:
            for i, gpu in enumerate(gpus):
                print(f"  GPU {i}: {gpu}")

            # Test tensor creation
            try:
                with tf.device("/GPU:0"):
                    a = tf.constant([[1.0, 2.0], [3.0, 4.0]])
                    b = tf.constant([[1.0, 1.0], [0.0, 1.0]])
                    c = tf.matmul(a, b)
                print("  ✓ Successfully performed GPU computation")
                return True
            except Exception as e:
                print(f"  ✗ Failed to perform GPU computation: {e}")
                return False
        else:
            print("  ✗ No GPU devices found")
            return False

    except ImportError:
        print("✗ TensorFlow not installed")
        print("  Install with: pip install tensorflow")
        return False
    except Exception as e:
        print(f"✗ Error testing TensorFlow: {e}")
        return False


def print_summary(results):
    """Print summary of GPU test results."""
    print("\n" + "=" * 60)
    print("GPU TEST SUMMARY")
    print("=" * 60)

    all_passed = all(results.values())

    for test, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test:.<45} {status}")

    print("\nOverall Status:", "✓ GPU READY" if all_passed else "⚠ GPU ISSUES DETECTED")

    if not all_passed:
        print("\nRecommendations:")
        if not results.get("nvidia-smi", False):
            print("- Install NVIDIA drivers")
        if not results.get("cuda", False):
            print("- Install CUDA toolkit")
        if not results.get("torch", False):
            print("- Install PyTorch with CUDA support")
            print("  Visit: https://pytorch.org/get-started/locally/")
        if not results.get("lightning", False) and results.get("torch", False):
            print("- Install PyTorch Lightning: pip install lightning")
        if not results.get("tensorflow", False):
            print("- Install TensorFlow with GPU support if using GluonTS/TimesFM")


def main():
    parser = argparse.ArgumentParser(
        description="Test GPU availability for forecasting models"
    )
    parser.add_argument(
        "--framework",
        choices=["all", "torch", "tensorflow", "cuda"],
        default="all",
        help="Which framework to test (default: all)",
    )

    args = parser.parse_args()

    print("GPU Availability Test for Forecasting Models")
    print("=" * 60)

    results = {}

    # Always test basic GPU availability
    results["nvidia-smi"] = test_nvidia_smi()
    results["cuda"] = test_cuda()

    if args.framework in ["all", "torch"]:
        results["torch"] = test_torch_gpu()
        results["lightning"] = test_lightning_gpu()

    if args.framework in ["all", "tensorflow"]:
        results["tensorflow"] = test_tensorflow_gpu()

    print_summary(results)

    # Return non-zero exit code if any test failed
    sys.exit(0 if all(results.values()) else 1)


if __name__ == "__main__":
    main()
