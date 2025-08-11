import os


def main() -> None:
    try:
        import torch
    except Exception as exc:
        print("PyTorch not installed in this environment.")
        print(f"Import error: {exc}")
        return

    use_mps = os.environ.get("PYTORCH_ENABLE_MPS_FALLBACK", "0") == "1"

    cuda_available = torch.cuda.is_available()
    mps_available = (
        getattr(torch.backends, "mps", None) is not None
        and torch.backends.mps.is_available()
    )

    print(f"CUDA available: {cuda_available}")
    print(f"MPS available:  {mps_available}")

    if cuda_available:
        device = torch.device("cuda")
        name = torch.cuda.get_device_name(0)
    elif mps_available and use_mps:
        device = torch.device("mps")
        name = "Apple MPS"
    else:
        print("No GPU/MPS device available. CPU-only.")
        return

    # Tiny matmul on the selected device
    a = torch.randn(256, 256, device=device)
    b = torch.randn(256, 256, device=device)
    c = a @ b
    print(f"Device: {name}, result shape: {tuple(c.shape)}")


if __name__ == "__main__":
    main()
