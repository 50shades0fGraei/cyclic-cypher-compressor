import tarfile
import os
import glob
from double_crunch_marketplace import double_crunch_compress

# Gather up to 6 PNG or JPEG assets
valid_extensions = ('.png', '.jpg', '.jpeg')
all_files = os.listdir('.')
files = [f for f in all_files if f.lower().endswith(valid_extensions)][:6]

if not files:
    print("No PNG or JPEG images found to bundle.")
else:
    print(f"Gathered {len(files)} image assets: {', '.join(files)}")
    total_size = sum(os.path.getsize(f) for f in files)
    print(f"Total Source Size: {total_size:,} bytes")

    print("\nBundling into tar archive...")
    bundle_name = "screenshot_bundle.tar"
    with tarfile.open(bundle_name, "w") as tar:
        for f in files:
            tar.add(f)
            
    bundle_size = os.path.getsize(bundle_name)
    print(f"Initial Tar Bundle Size: {bundle_size:,} bytes")

    print("\nExecuting Double Crunch...")
    double_crunch_compress(bundle_name, "screenshots.cdv6")
    if os.path.exists('screenshots.cdv6'):
        print(f"Final CDV6 Compressed Output: {os.path.getsize('screenshots.cdv6')} bytes!")
    else:
        print("Double crunch failed.")
