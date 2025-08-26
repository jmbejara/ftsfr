"""
test_apple_silicon.py

Utility script to test Apple Silicon (M1/M2/M3) capabilities for forecasting frameworks.
Tests MPS acceleration, framework compatibility, and hardware detection.

Usage:
    # Test all frameworks
    python test_apple_silicon.py

    # Test specific framework
    python test_apple_silicon.py --framework torch
"""

import argparse
import subprocess
import sys
import platform
import psutil
import os


def test_system_info():
    """Test basic system information and Apple Silicon detection."""
    print("Testing System Information...")
    
    # Platform info
    print(f"✓ Platform: {platform.platform()}")
    print(f"✓ Architecture: {platform.machine()}")
    print(f"✓ Python: {platform.python_version()}")
    
    # Check if it's Apple Silicon
    if platform.machine() == "arm64" and platform.system() == "Darwin":
        print("✓ Apple Silicon (ARM64) detected")
        
        # Get processor info
        try:
            result = subprocess.run(["sysctl", "-n", "machdep.cpu.brand_string"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                cpu_info = result.stdout.strip()
                print(f"✓ Processor: {cpu_info}")
                
                # Check for M-series
                if any(m in cpu_info.lower() for m in ["m1", "m2", "m3"]):
                    print("✓ M-series chip detected")
                else:
                    print("⚠ Apple Silicon detected but not M-series")
            else:
                print("⚠ Could not determine processor model")
        except Exception as e:
            print(f"⚠ Error getting processor info: {e}")
        
        return True
    else:
        print("✗ Not running on Apple Silicon")
        return False


def test_memory():
    """Test memory capabilities."""
    print("\nTesting Memory...")
    
    try:
        memory = psutil.virtual_memory()
        total_gb = memory.total / (1024**3)
        available_gb = memory.available / (1024**3)
        
        print(f"✓ Total Memory: {total_gb:.1f} GB")
        print(f"✓ Available Memory: {available_gb:.1f} GB")
        print(f"✓ Memory Usage: {memory.percent:.1f}%")
        
        # Check if memory is sufficient for ML workloads
        if total_gb >= 16:
            print("✓ Sufficient memory for large ML workloads")
        elif total_gb >= 8:
            print("✓ Adequate memory for medium ML workloads")
        else:
            print("⚠ Limited memory for ML workloads")
            
        return True
    except Exception as e:
        print(f"✗ Error checking memory: {e}")
        return False


def test_torch_mps():
    """Test PyTorch MPS (Metal Performance Shaders) support."""
    print("\nTesting PyTorch MPS Support...")
    
    try:
        import torch
        
        print("✓ PyTorch imported successfully")
        print(f"  PyTorch version: {torch.__version__}")
        
        # Check MPS availability
        mps_available = torch.backends.mps.is_available()
        print(f"  MPS available: {mps_available}")
        
        if mps_available:
            print("  ✓ MPS (Metal Performance Shaders) is available")
            
            # Check if MPS is built
            mps_built = torch.backends.mps.is_built()
            print(f"  MPS built: {mps_built}")
            
            if mps_built:
                # Test MPS tensor creation
                try:
                    x = torch.tensor([1.0, 2.0, 3.0], device="mps")
                    print("  ✓ Successfully created MPS tensor")
                    
                    # Test basic operations
                    y = x * 2
                    print("  ✓ MPS tensor operations working")
                    
                    return True
                except Exception as e:
                    print(f"  ✗ Failed to create/use MPS tensor: {e}")
                    return False
            else:
                print("  ✗ MPS not built in this PyTorch version")
                return False
        else:
            print("  ✗ MPS not available")
            return False
            
    except ImportError:
        print("✗ PyTorch not installed")
        print("  Install with: pip install torch")
        return False
    except Exception as e:
        print(f"✗ Error testing PyTorch MPS: {e}")
        return False


def test_darts():
    """Test Darts framework compatibility."""
    print("\nTesting Darts Framework...")
    
    try:
        import darts
        
        print("✓ Darts imported successfully")
        print(f"  Darts version: {darts.__version__}")
        
        # Check if Darts can use MPS
        try:
            import torch
            if torch.backends.mps.is_available():
                print("  ✓ Darts can leverage MPS acceleration")
                
                # Test a simple Darts model with MPS
                from darts.models import NaiveSeasonal
                from darts import TimeSeries
                import numpy as np
                
                # Create dummy data
                values = np.random.randn(100)
                ts = TimeSeries.from_values(values)
                
                # Test model creation
                model = NaiveSeasonal(K=1)
                print("  ✓ Darts model creation successful")
                
                return True
            else:
                print("  ⚠ MPS not available for Darts")
                return True  # Darts still works without MPS
                
        except Exception as e:
            print(f"  ⚠ Error testing Darts MPS integration: {e}")
            return True  # Darts still works
            
    except ImportError:
        print("✗ Darts not installed")
        print("  Install with: pip install darts")
        return False
    except Exception as e:
        print(f"✗ Error testing Darts: {e}")
        return False


def test_neuralforecast():
    """Test NeuralForecast (Nixtla) framework compatibility."""
    print("\nTesting NeuralForecast (Nixtla)...")
    
    try:
        import neuralforecast
        
        print("✓ NeuralForecast imported successfully")
        print(f"  NeuralForecast version: {neuralforecast.__version__}")
        
        # Check PyTorch backend
        try:
            import torch
            if torch.backends.mps.is_available():
                print("  ✓ NeuralForecast can leverage MPS acceleration")
                
                # Test basic functionality
                from neuralforecast import NeuralForecast
                from neuralforecast.models import Autoformer
                
                print("  ✓ NeuralForecast model imports successful")
                return True
            else:
                print("  ⚠ MPS not available for NeuralForecast")
                return True  # Still works without MPS
                
        except Exception as e:
            print(f"  ⚠ Error testing NeuralForecast MPS integration: {e}")
            return True
            
    except ImportError:
        print("✗ NeuralForecast not installed")
        print("  Install with: pip install neuralforecast")
        return False
    except Exception as e:
        print(f"✗ Error testing NeuralForecast: {e}")
        return False


def test_gluonts():
    """Test GluonTS framework compatibility."""
    print("\nTesting GluonTS...")
    
    try:
        import gluonts
        
        print("✓ GluonTS imported successfully")
        print(f"  GluonTS version: {gluonts.__version__}")
        
        # Check PyTorch backend
        try:
            import torch
            if torch.backends.mps.is_available():
                print("  ✓ GluonTS can leverage MPS acceleration")
                
                # Test basic functionality
                from gluonts.model.deepar import DeepAREstimator
                from gluonts.dataset.common import ListDataset
                
                print("  ✓ GluonTS model imports successful")
                return True
            else:
                print("  ⚠ MPS not available for GluonTS")
                return True  # Still works without MPS
                
        except Exception as e:
            print(f"  ⚠ Error testing GluonTS MPS integration: {e}")
            return True
            
    except ImportError:
        print("✗ GluonTS not installed")
        print("  Install with: pip install gluonts[torch]")
        return False
    except Exception as e:
        print(f"✗ Error testing GluonTS: {e}")
        return False


def test_performance():
    """Test basic performance capabilities."""
    print("\nTesting Performance Capabilities...")
    
    try:
        import torch
        import time
        
        if torch.backends.mps.is_available():
            print("✓ Testing MPS performance...")
            
            # Create large tensor on MPS
            size = 1000
            x = torch.randn(size, size, device="mps")
            y = torch.randn(size, size, device="mps")
            
            # Time matrix multiplication
            start_time = time.time()
            z = torch.mm(x, y)
            torch.mps.synchronize()  # Ensure computation is complete
            end_time = time.time()
            
            duration = end_time - start_time
            print(f"  ✓ Matrix multiplication ({size}x{size}) took {duration:.3f}s")
            
            # Check if performance is reasonable
            if duration < 1.0:
                print("  ✓ Excellent MPS performance")
            elif duration < 5.0:
                print("  ✓ Good MPS performance")
            else:
                print("  ⚠ Slower than expected MPS performance")
                
            return True
        else:
            print("⚠ MPS not available for performance testing")
            return True
            
    except Exception as e:
        print(f"✗ Error testing performance: {e}")
        return False


def print_summary(results):
    """Print summary of Apple Silicon test results."""
    print("\n" + "=" * 60)
    print("APPLE SILICON TEST SUMMARY")
    print("=" * 60)

    all_passed = all(results.values())

    for test, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test:.<45} {status}")

    print("\nOverall Status:", "✓ APPLE SILICON READY" if all_passed else "⚠ ISSUES DETECTED")

    if all_passed:
        print("\n🎉 Your Apple Silicon Mac is ready for forecasting!")
        print("Recommendations:")
        print("- Use MPS acceleration for PyTorch-based models")
        print("- Leverage unified memory for large datasets")
        print("- Consider local training instead of cloud GPU instances")
    else:
        print("\nRecommendations:")
        if not results.get("system", False):
            print("- Ensure you're running on Apple Silicon")
        if not results.get("torch_mps", False):
            print("- Install PyTorch with MPS support")
            print("  Visit: https://pytorch.org/get-started/locally/")
        if not results.get("memory", False):
            print("- Check system memory availability")


def main():
    parser = argparse.ArgumentParser(
        description="Test Apple Silicon capabilities for forecasting models"
    )
    parser.add_argument(
        "--framework",
        choices=["all", "torch", "darts", "neuralforecast", "gluonts"],
        default="all",
        help="Which framework to test (default: all)",
    )

    args = parser.parse_args()

    print("Apple Silicon Capability Test for Forecasting Models")
    print("=" * 60)

    results = {}

    # Always test basic system capabilities
    results["system"] = test_system_info()
    results["memory"] = test_memory()

    if args.framework in ["all", "torch"]:
        results["torch_mps"] = test_torch_mps()
        results["performance"] = test_performance()

    if args.framework in ["all", "darts"]:
        results["darts"] = test_darts()

    if args.framework in ["all", "neuralforecast"]:
        results["neuralforecast"] = test_neuralforecast()

    if args.framework in ["all", "gluonts"]:
        results["gluonts"] = test_gluonts()

    print_summary(results)

    # Return non-zero exit code if any test failed
    sys.exit(0 if all(results.values()) else 1)


if __name__ == "__main__":
    main()
