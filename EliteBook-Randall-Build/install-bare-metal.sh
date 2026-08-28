#!/bin/bash
# (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.
# PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.
# This software is proprietary and subject to the terms of a specific License Agreement.

# ═══════════════════════════════════════════════════════════════════════
#  CyberDNA: Bare-Metal EFI Stub Installer
#  Target: HP EliteBook 6 G2q (Snapdragon X Elite / ARM64)
#
#  What this does:
#  BIOS → vmlinuz.efi (kernel IS the bootloader) → Tesseract-OS
#  No GRUB. No Windows. Nothing in the way.
#
#  REQUIREMENTS (run on the EliteBook itself under a live Linux USB):
#   - ARM64 Linux live environment (e.g. Fedora ARM / Ubuntu ARM live USB)
#   - Target NVMe drive with partitions already set up (see PARTITION GUIDE)
#   - Internet connection for package installs
#
#  PARTITION LAYOUT (use fdisk/gdisk on the EliteBook's NVMe):
#   /dev/nvme0n1p1  →  512MB   EFI System Partition (ESP)  vfat
#   /dev/nvme0n1p2  →  50GB+   Tesseract Root (/)          ext4 or btrfs
#   /dev/nvme0n1p3  →  rest    Randall DNA Vault          ext4
# ═══════════════════════════════════════════════════════════════════════

set -e

ESP_DEVICE="${1:-/dev/nvme0n1p1}"
ROOT_DEVICE="${2:-/dev/nvme0n1p2}"
VAULT_DEVICE="${3:-/dev/nvme0n1p3}"
MOUNT_ROOT="/mnt/tesseract"
MOUNT_ESP="$MOUNT_ROOT/boot/efi"
RANDALL_LABEL="CyberDNA-Tesseract-OS"

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║   CyberDNA: Bare-Metal EFI Stub Installer                   ║"
echo "║   BIOS → Kernel (No GRUB. No Windows. Nothing in the way.)  ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "ESP:   $ESP_DEVICE"
echo "ROOT:  $ROOT_DEVICE"
echo "VAULT: $VAULT_DEVICE"
echo ""
read -p "Continue? This will format and install. [y/N] " confirm
[[ "$confirm" =~ ^[Yy]$ ]] || exit 0

# ─── STEP 1: Format Partitions ────────────────────────────────────────────────
echo ""
echo "[ STEP 1 ] Formatting partitions..."
mkfs.vfat -F32 -n "ESP" "$ESP_DEVICE"
mkfs.ext4 -L "TESSERACT_ROOT" "$ROOT_DEVICE"
mkfs.ext4 -L "RANDALL_VAULT" "$VAULT_DEVICE"
echo "[✓] Partitions formatted."

# ─── STEP 2: Mount ────────────────────────────────────────────────────────────
echo ""
echo "[ STEP 2 ] Mounting..."
mkdir -p "$MOUNT_ROOT" "$MOUNT_ESP"
mount "$ROOT_DEVICE" "$MOUNT_ROOT"
mount "$ESP_DEVICE" "$MOUNT_ESP"
echo "[✓] Mounted at $MOUNT_ROOT"

# ─── STEP 3: Install Minimal ARM64 Linux Base ─────────────────────────────────
echo ""
echo "[ STEP 3 ] Installing minimal ARM64 base system..."
# Using Arch Linux ARM (lightest randall base)
# Alternative: debootstrap ubuntu-arm64
if command -v pacstrap &>/dev/null; then
    # Arch Linux ARM route
    pacstrap "$MOUNT_ROOT" base linux linux-firmware networkmanager python xorg-server xorg-xinit xdg-utils chromium
elif command -v debootstrap &>/dev/null; then
    # Ubuntu/Debian ARM64 route
    debootstrap --arch=arm64 noble "$MOUNT_ROOT" http://ports.ubuntu.com/ubuntu-ports
    # Install kernel, python, and graphical UI engine inside chroot
    arch-chroot "$MOUNT_ROOT" apt-get install -y linux-image-generic-arm64 python3 networkmanager xorg xinit x11-xserver-utils chromium-browser
else
    echo "[ERROR] Neither pacstrap nor debootstrap found. Boot a proper ARM64 live USB."
    exit 1
fi
echo "[✓] Base system installed."

# ─── STEP 4: Copy Tesseract-OS Stack & Setup Identity ────────────────────────
echo ""
echo "[ STEP 4 ] Deploying CyberDNA / Tesseract-OS stack & Initializing Randall User..."

# Create user randall in the chroot environment so they actually exist in the OS user database
if command -v arch-chroot &>/dev/null; then
    arch-chroot "$MOUNT_ROOT" useradd -m -u 1000 -G wheel,video,audio -s /bin/bash randall 2>/dev/null || true
    arch-chroot "$MOUNT_ROOT" passwd -d randall 2>/dev/null || true
else
    chroot "$MOUNT_ROOT" useradd -m -u 1000 -G sudo,video,audio -s /bin/bash randall 2>/dev/null || true
    chroot "$MOUNT_ROOT" passwd -d randall 2>/dev/null || true
fi

RANDALL_HOME="$MOUNT_ROOT__HOME_RANDALL_PLACEHOLDER__"
mkdir -p "$RANDALL_HOME"

# Copy the entire project from USB (adjust path as needed)
PROJECT_SRC="$(dirname "$0")/../.."
cp -r "$PROJECT_SRC" "$RANDALL_HOME/cyclic-cypher-compressor"
chown -R 1000:1000 "$RANDALL_HOME"

echo "[✓] Tesseract-OS stack deployed to $RANDALL_HOME"

# ─── STEP 5: Configure EFI Stub — KERNEL AS BOOTLOADER ───────────────────────
echo ""
echo "[ STEP 5 ] Configuring EFI Stub (kernel = bootloader, nothing in the way)..."

# Find the kernel in the installed system
VMLINUZ=$(find "$MOUNT_ROOT/boot" -name "vmlinuz*" | head -1)
INITRD=$(find "$MOUNT_ROOT/boot" -name "initramfs*" -o -name "initrd*" | head -1)

if [ -z "$VMLINUZ" ]; then
    echo "[ERROR] Kernel not found in $MOUNT_ROOT/boot"
    exit 1
fi

# Copy kernel + initrd into ESP so UEFI can see them directly
EFI_CYBERDNA="$MOUNT_ESP/EFI/CyberDNA"
mkdir -p "$EFI_CYBERDNA"
cp "$VMLINUZ" "$EFI_CYBERDNA/vmlinuz.efi"
[ -n "$INITRD" ] && cp "$INITRD" "$EFI_CYBERDNA/initramfs.img"

echo "[✓] Kernel installed to ESP: $EFI_CYBERDNA/vmlinuz.efi"

# ─── STEP 6: Register UEFI Boot Entry via efibootmgr ─────────────────────────
echo ""
echo "[ STEP 6 ] Registering CyberDNA as primary UEFI boot entry..."

# Get disk device (strip partition number)
DISK=$(echo "$ESP_DEVICE" | sed 's/p[0-9]*$//' | sed 's/[0-9]*$//')
PART_NUM=$(echo "$ESP_DEVICE" | grep -o '[0-9]*$')
ROOT_UUID=$(blkid -s UUID -o value "$ROOT_DEVICE")

# Build kernel command line
KERNEL_PARAMS="root=UUID=$ROOT_UUID rw console=tty0 quiet splash \
    rootfstype=ext4 \
    cyberdna.randall=1 \
    cyberdna.vault=$VAULT_DEVICE \
    cyberdna.identity=LUJAN_AGI_PRIME"

# Register EFI boot entry — this is the "nothing in the way" line
efibootmgr \
    --create \
    --disk "$DISK" \
    --part "$PART_NUM" \
    --label "$RANDALL_LABEL" \
    --loader "\\EFI\\CyberDNA\\vmlinuz.efi" \
    --unicode "$KERNEL_PARAMS initrd=\\EFI\\CyberDNA\\initramfs.img" \
    --verbose

echo "[✓] '$RANDALL_LABEL' registered as UEFI boot entry."

# ─── STEP 7: Set Boot Order (put CyberDNA FIRST) ─────────────────────────────
echo ""
echo "[ STEP 7 ] Setting CyberDNA as boot priority #1..."
NEW_ENTRY=$(efibootmgr | grep "$RANDALL_LABEL" | grep -o 'Boot[0-9A-F]*' | sed 's/Boot//')
CURRENT_ORDER=$(efibootmgr | grep BootOrder | awk '{print $2}')
efibootmgr --bootorder "$NEW_ENTRY,$CURRENT_ORDER"
echo "[✓] Boot order: CyberDNA first."

# ─── STEP 8: Disable Windows Boot Manager (optional but randall) ────────────
echo ""
read -p "[ STEP 8 ] Remove Windows Boot Manager from UEFI entries? [y/N] " rm_windows
if [[ "$rm_windows" =~ ^[Yy]$ ]]; then
    WIN_ENTRY=$(efibootmgr | grep -i "windows" | grep -o 'Boot[0-9A-F]*' | sed 's/Boot//')
    if [ -n "$WIN_ENTRY" ]; then
        efibootmgr --bootnum "$WIN_ENTRY" --delete-bootnum
        echo "[✓] Windows Boot Manager removed from UEFI."
    else
        echo "[!] No Windows entry found."
    fi
fi

# ─── STEP 9: Install NPU Retention Driver ─────────────────────────────────────
echo ""
echo "[ STEP 9 ] Installing NPU retention driver into initramfs..."
DRIVER_SRC="$(dirname "$0")/../../EliteBook-Randall-Build/build-output/npu-retention-driver.ko"
if [ -f "$DRIVER_SRC" ]; then
    KVER=$(basename "$VMLINUZ" | sed 's/vmlinuz-//')
    DRIVER_DEST="$MOUNT_ROOT/lib/modules/$KVER/kernel/drivers/misc/"
    mkdir -p "$DRIVER_DEST"
    cp "$DRIVER_SRC" "$DRIVER_DEST"
    # Register with depmod inside chroot
    arch-chroot "$MOUNT_ROOT" depmod "$KVER"
    # Add to modules-load
    echo "npu-retention-driver" >> "$MOUNT_ROOT/etc/modules-load.d/cyberdna.conf"
    echo "[✓] NPU driver installed and registered."
else
    echo "[!] NPU driver .ko not found — run build.sh first to compile it."
fi

# ─── STEP 10: Deploy Randall Autostart ─────────────────────────────────────
echo ""
echo "[ STEP 10 ] Configuring Tesseract-OS autostart on login..."
cat > "$MOUNT_ROOT/etc/profile.d/cyberdna-launch.sh" << 'AUTOSTART'
#!/bin/bash
# Auto-launch Tesseract-OS interface after randall login
if [ "$(tty)" = "/dev/tty1" ] && [ "$USER" = "randall" ] && [ -z "$DISPLAY" ]; then
    echo ""
    echo "  CyberDNA Tesseract-OS — Randall Boot Complete"
    echo "  Identity: Randall Lujan / LUJAN_AGI_PRIME"
    echo "  Initializing Visual Logic..."
    echo ""
    cd __HOME_RANDALL_PLACEHOLDER__/cyclic-cypher-compressor
    
    # Start the local engine quietly
    python3 -m http.server 8080 >/dev/null 2>&1 &
    
    # Configure graphical boot
    echo "exec chromium --kiosk --no-sandbox http://localhost:8080/cubix_os.html" > ~/.xinitrc
    
    # Launch graphics
    startx
fi
AUTOSTART
chmod +x "$MOUNT_ROOT/etc/profile.d/cyberdna-launch.sh"
echo "[✓] Autostart configured."

# ─── CLEANUP ──────────────────────────────────────────────────────────────────
echo ""
echo "[ CLEANUP ] Unmounting..."
sync
umount "$MOUNT_ESP"
umount "$MOUNT_ROOT"

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║   BARE-METAL INSTALL COMPLETE                               ║"
echo "╠══════════════════════════════════════════════════════════════╣"
echo "║   Power off → Remove live USB → Power on EliteBook          ║"
echo "║   BIOS will boot directly to: CyberDNA-Tesseract-OS         ║"
echo "║   No GRUB. No Windows. Nothing in the way.                  ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
