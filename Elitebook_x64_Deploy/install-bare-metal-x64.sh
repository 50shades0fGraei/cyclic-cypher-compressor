#!/bin/bash
# (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.
# PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.
# This software is proprietary and subject to the terms of a specific License Agreement.

# ═══════════════════════════════════════════════════════════════════════
#  CyberDNA: Bare-Metal EFI Stub Installer
#  Target: HP EliteBook (x86_64 / amd64 architecture)
#
#  What this does:
#  BIOS → vmlinuz.efi (kernel IS the bootloader) → Tesseract-OS
#  No GRUB. No Windows. Nothing in the way.
#
#  REQUIREMENTS (run on the EliteBook itself under a live Linux USB):
#   - x86_64 Linux live environment (e.g. Ubuntu x86_64 live USB)
#   - Target NVMe/SATA drive with partitions already set up
#   - Internet connection for package installs
#
#  PARTITION LAYOUT (use fdisk/gdisk on the EliteBook's drive):
#   /dev/nvme0n1p1 or sda1  →  512MB   EFI System Partition (ESP)  vfat
#   /dev/nvme0n1p2 or sda2  →  50GB+   Tesseract Root (/)          ext4 or btrfs
#   /dev/nvme0n1p3 or sda3  →  rest    Sovereign DNA Vault          ext4
# ═══════════════════════════════════════════════════════════════════════

set -e

ESP_DEVICE="${1:-/dev/sda1}"
ROOT_DEVICE="${2:-/dev/sda2}"
VAULT_DEVICE="${3:-/dev/sda3}"
MOUNT_ROOT="/mnt/tesseract"
MOUNT_ESP="$MOUNT_ROOT/boot/efi"
SOVEREIGN_LABEL="CyberDNA-Tesseract-OS-x64"

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║   CyberDNA: Bare-Metal EFI Stub Installer (x64)             ║"
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
mkfs.ext4 -L "SOVEREIGN_VAULT" "$VAULT_DEVICE"
echo "[✓] Partitions formatted."

# ─── STEP 2: Mount ────────────────────────────────────────────────────────────
echo ""
echo "[ STEP 2 ] Mounting..."
mkdir -p "$MOUNT_ROOT" "$MOUNT_ESP"
mount "$ROOT_DEVICE" "$MOUNT_ROOT"
mount "$ESP_DEVICE" "$MOUNT_ESP"
echo "[✓] Mounted at $MOUNT_ROOT"

# ─── STEP 3: Install Minimal x86_64 Linux Base ─────────────────────────────────
echo ""
echo "[ STEP 3 ] Installing minimal x86_64 base system with XFCE desktop..."
if command -v pacstrap &>/dev/null; then
    # Arch Linux x86_64 route
    pacstrap "$MOUNT_ROOT" base linux linux-firmware networkmanager python xorg-server xorg-xinit xdg-utils chromium xfce4 xfce4-terminal thunar
elif command -v debootstrap &>/dev/null; then
    # Ubuntu/Debian AMD64 route
    debootstrap --arch=amd64 noble "$MOUNT_ROOT" http://archive.ubuntu.com/ubuntu/
    arch-chroot "$MOUNT_ROOT" env DEBIAN_FRONTEND=noninteractive apt-get install -y linux-image-generic python3 networkmanager xorg xinit x11-xserver-utils xfce4 xfce4-terminal thunar chromium-browser
else
    echo "[ERROR] Neither pacstrap nor debootstrap found. Boot a proper x86_64 live USB."
    exit 1
fi
echo "[✓] Base system installed."

# ─── STEP 4: Copy Tesseract-OS Stack & Setup Identity ────────────────────────
echo ""
echo "[ STEP 4 ] Deploying CyberDNA / Tesseract-OS stack & Initializing Sovereign User..."

if command -v arch-chroot &>/dev/null; then
    arch-chroot "$MOUNT_ROOT" useradd -m -u 1000 -G wheel,video,audio -s /bin/bash sovereign 2>/dev/null || true
    arch-chroot "$MOUNT_ROOT" passwd -d sovereign 2>/dev/null || true
else
    chroot "$MOUNT_ROOT" useradd -m -u 1000 -G sudo,video,audio -s /bin/bash sovereign 2>/dev/null || true
    chroot "$MOUNT_ROOT" passwd -d sovereign 2>/dev/null || true
fi

SOVEREIGN_HOME="$MOUNT_ROOT/home/sovereign"
mkdir -p "$SOVEREIGN_HOME"

PROJECT_SRC="$(dirname "$0")/.."
cp -r "$PROJECT_SRC" "$SOVEREIGN_HOME/cyclic-cypher-compressor"
chown -R 1000:1000 "$SOVEREIGN_HOME"

echo "[✓] Tesseract-OS stack deployed to $SOVEREIGN_HOME"

# ─── STEP 5: Configure EFI Stub — KERNEL AS BOOTLOADER ───────────────────────
echo ""
echo "[ STEP 5 ] Configuring EFI Stub (kernel = bootloader, nothing in the way)..."

VMLINUZ=$(find "$MOUNT_ROOT/boot" -name "vmlinuz*" | head -1)
INITRD=$(find "$MOUNT_ROOT/boot" -name "initramfs*" -o -name "initrd*" | head -1)

if [ -z "$VMLINUZ" ]; then
    echo "[ERROR] Kernel not found in $MOUNT_ROOT/boot"
    exit 1
fi

EFI_CYBERDNA="$MOUNT_ESP/EFI/CyberDNA"
mkdir -p "$EFI_CYBERDNA"
cp "$VMLINUZ" "$EFI_CYBERDNA/vmlinuz.efi"
[ -n "$INITRD" ] && cp "$INITRD" "$EFI_CYBERDNA/initramfs.img"

echo "[✓] Kernel installed to ESP: $EFI_CYBERDNA/vmlinuz.efi"

# ─── STEP 6: Register UEFI Boot Entry via efibootmgr ─────────────────────────
echo ""
echo "[ STEP 6 ] Registering CyberDNA as primary UEFI boot entry..."

DISK=$(echo "$ESP_DEVICE" | sed 's/p[0-9]*$//' | sed 's/[0-9]*$//')
PART_NUM=$(echo "$ESP_DEVICE" | grep -o '[0-9]*$')
ROOT_UUID=$(blkid -s UUID -o value "$ROOT_DEVICE")

KERNEL_PARAMS="root=UUID=$ROOT_UUID rw console=tty0 quiet splash \
    rootfstype=ext4 \
    cyberdna.sovereign=1 \
    cyberdna.vault=$VAULT_DEVICE \
    cyberdna.identity=LUJAN_AGI_PRIME"

efibootmgr \
    --create \
    --disk "$DISK" \
    --part "$PART_NUM" \
    --label "$SOVEREIGN_LABEL" \
    --loader "\\EFI\\CyberDNA\\vmlinuz.efi" \
    --unicode "$KERNEL_PARAMS initrd=\\EFI\\CyberDNA\\initramfs.img" \
    --verbose

echo "[✓] '$SOVEREIGN_LABEL' registered as UEFI boot entry."

# ─── STEP 7: Set Boot Order & Cleanup ─────────────────────────────────────────
echo ""
echo "[ STEP 7 ] Setting CyberDNA as boot priority #1..."
NEW_ENTRY=$(efibootmgr | grep "$SOVEREIGN_LABEL" | grep -o 'Boot[0-9A-F]*' | sed 's/Boot//')
CURRENT_ORDER=$(efibootmgr | grep BootOrder | awk '{print $2}')
efibootmgr --bootorder "$NEW_ENTRY,$CURRENT_ORDER"
echo "[✓] Boot order updated."

echo ""
echo "[ STEP 8 ] Configuring Tesseract-OS autostart on login..."
cat > "$MOUNT_ROOT/etc/profile.d/cyberdna-launch.sh" << 'AUTOSTART'
#!/bin/bash
if [ "$(tty)" = "/dev/tty1" ] && [ "$USER" = "sovereign" ] && [ -z "$DISPLAY" ]; then
    echo "  CyberDNA Tesseract-OS — Sovereign Boot Complete"
    
    # Configure XFCE start, launching background python server and Chromium
    echo "cd /home/sovereign/cyclic-cypher-compressor/Elitebook_x64_Deploy" > ~/.xinitrc
    echo "python3 -m http.server 8080 >/dev/null 2>&1 &" >> ~/.xinitrc
    echo "(chromium-browser --no-sandbox http://localhost:8080/cubix_os.html || chromium --no-sandbox http://localhost:8080/cubix_os.html) &" >> ~/.xinitrc
    echo "exec startxfce4" >> ~/.xinitrc
    
    startx
fi
AUTOSTART
chmod +x "$MOUNT_ROOT/etc/profile.d/cyberdna-launch.sh"
echo "[✓] Autostart configured."

echo ""
echo "[ CLEANUP ] Unmounting..."
sync
umount "$MOUNT_ESP"
umount "$MOUNT_ROOT"

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║   x64 BARE-METAL INSTALL COMPLETE                           ║"
echo "╚══════════════════════════════════════════════════════════════╝"
