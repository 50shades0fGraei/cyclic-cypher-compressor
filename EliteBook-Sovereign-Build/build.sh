#!/bin/bash
# ═══════════════════════════════════════════════════════════════════
#  CyberDNA: EliteBook Sovereign Build — Full Compile Pipeline
#  Target: HP EliteBook 6 G2q (Snapdragon / ARM64)
#  Run this script on a Linux machine (or WSL2) to build all artifacts.
#  Output artifacts go to: ./build-output/
# ═══════════════════════════════════════════════════════════════════

set -e  # Exit on any error

BUILD_DIR="$(dirname "$0")/build-output"
FIRMWARE_DIR="$(dirname "$0")/firmware-mod"
TESSERACT_DIR="$(dirname "$0")/tesseract-core"

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║   CyberDNA: Sovereign Compile Pipeline — Starting...    ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

mkdir -p "$BUILD_DIR"

# ─── STEP 1: Generate Sovereign RSA-4096 Keys ─────────────────────────────────
echo "[ STEP 1 ] Generating RSA-4096 Sovereign Keys..."
if [ ! -f "$BUILD_DIR/sovereign_private.key" ]; then
    openssl genrsa -out "$BUILD_DIR/sovereign_private.key" 4096
    openssl rsa -in "$BUILD_DIR/sovereign_private.key" -pubout -out "$BUILD_DIR/sovereign_public.key"
    openssl req -new -x509 \
        -key "$BUILD_DIR/sovereign_private.key" \
        -out "$BUILD_DIR/sovereign_root.crt" \
        -days 3650 \
        -subj "/C=UC/ST=CYBERDNA/L=TESSERACT/O=LUJAN_AGI/CN=Sovereign_Root"
    echo "[✓] Keys generated: sovereign_private.key + sovereign_root.crt"
else
    echo "[✓] Keys already exist. Skipping generation."
fi

# ─── STEP 2: Compile ACPI DSL → AML ───────────────────────────────────────────
echo ""
echo "[ STEP 2 ] Compiling ACPI efficiency table (DSL → AML)..."
if ! command -v iasl &>/dev/null; then
    echo "[!] iasl not found. Installing acpica-tools..."
    if command -v apt-get &>/dev/null; then
        sudo apt-get install -y acpica-tools
    elif command -v pacman &>/dev/null; then
        sudo pacman -S --noconfirm acpica
    else
        echo "[ERROR] Cannot install iasl. Install acpica-tools manually."
        exit 1
    fi
fi
iasl -p "$BUILD_DIR/efficiency" -oa "$FIRMWARE_DIR/acpi-efficiency.dsl"
echo "[✓] ACPI table compiled: efficiency.aml"

# ─── STEP 3: Compile EFI Bootloader (CubixOS-loader.c → .efi) ─────────────────
echo ""
echo "[ STEP 3 ] Compiling CubixOS-loader UEFI bootloader..."
if ! command -v aarch64-linux-gnu-gcc &>/dev/null; then
    echo "[!] ARM64 cross-compiler not found. Installing..."
    if command -v apt-get &>/dev/null; then
        sudo apt-get install -y gcc-aarch64-linux-gnu gnu-efi
    elif command -v pacman &>/dev/null; then
        sudo pacman -S --noconfirm aarch64-linux-gnu-gcc gnu-efi
    else
        echo "[ERROR] Install gcc-aarch64-linux-gnu and gnu-efi manually."
        exit 1
    fi
fi

# Auto-detect EFI include and library paths
EFI_INCLUDE=$(find /usr/include -name efi -type d 2>/dev/null | grep -v "aarch64" | head -1)
[ -z "$EFI_INCLUDE" ] && EFI_INCLUDE=$(find /usr/aarch64-linux-gnu/include -name efi -type d 2>/dev/null | head -1)
[ -z "$EFI_INCLUDE" ] && EFI_INCLUDE="/usr/include/efi"

EFI_LIB=$(find /usr/lib -name "crt0-efi-aarch64.o" 2>/dev/null -exec dirname {} \;)
[ -z "$EFI_LIB" ] && EFI_LIB="/usr/lib"

LDS_SCRIPT=$(find /usr/lib -name "elf_aarch64_efi.lds" 2>/dev/null | head -1)
[ -z "$LDS_SCRIPT" ] && LDS_SCRIPT="/usr/lib/elf_aarch64_efi.lds"

aarch64-linux-gnu-gcc \
    -I"$EFI_INCLUDE" \
    -I"$EFI_INCLUDE/aarch64" \
    -I"$EFI_INCLUDE/protocol" \
    -fno-stack-protector \
    -fpic \
    -fshort-wchar \
    -DEFI_FUNCTION_WRAPPER \
    -shared \
    -Wl,-Bsymbolic \
    -Wl,-znocombreloc \
    -T "$LDS_SCRIPT" \
    -o "$BUILD_DIR/CubixOS-loader.so" \
    "$FIRMWARE_DIR/CubixOS-loader.c" \
    "$EFI_LIB/crt0-efi-aarch64.o" \
    -L"$EFI_LIB" \
    -lefi -lgnuefi

objcopy \
    -j .text -j .sdata -j .data -j .dynamic -j .dynsym \
    -j .rel -j .rela -j .reloc \
    --target=efi-app-aarch64 \
    "$BUILD_DIR/CubixOS-loader.so" \
    "$BUILD_DIR/CubixOS-loader.efi"

echo "[✓] Bootloader compiled: CubixOS-loader.efi"

# ─── STEP 4: Sign the EFI Bootloader ──────────────────────────────────────────
echo ""
echo "[ STEP 4 ] Signing CubixOS-loader.efi with Sovereign Root..."
if ! command -v sbsign &>/dev/null; then
    echo "[!] sbsigntools not found. Installing..."
    if command -v apt-get &>/dev/null; then
        sudo apt-get install -y sbsigntools
    elif command -v pacman &>/dev/null; then
        sudo pacman -S --noconfirm sbsigntools
    fi
fi

sbsign \
    --key  "$BUILD_DIR/sovereign_private.key" \
    --cert "$BUILD_DIR/sovereign_root.crt" \
    --output "$BUILD_DIR/CubixOS-loader-signed.efi" \
    "$BUILD_DIR/CubixOS-loader.efi"

echo "[✓] Signed bootloader: CubixOS-loader-signed.efi"

# ─── STEP 5: Build NPU Retention Kernel Module ────────────────────────────────
echo ""
echo "[ STEP 5 ] Building NPU retention driver kernel module..."
KERNEL_VERSION=$(uname -r)
if [ ! -d "/lib/modules/$KERNEL_VERSION/build" ]; then
    echo "[!] Kernel headers not found for $KERNEL_VERSION. Installing..."
    sudo apt-get install -y linux-headers-"$KERNEL_VERSION" 2>/dev/null || \
    sudo pacman -S --noconfirm linux-headers 2>/dev/null || \
    echo "[WARNING] Install kernel headers manually: linux-headers-$(uname -r)"
fi

cat > "$TESSERACT_DIR/Makefile" << 'EOF'
obj-m += npu-retention-driver.o

KDIR := /lib/modules/$(shell uname -r)/build

all:
	make -C $(KDIR) M=$(PWD) modules ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu-

clean:
	make -C $(KDIR) M=$(PWD) clean
EOF

make -C "$TESSERACT_DIR" && \
    cp "$TESSERACT_DIR/npu-retention-driver.ko" "$BUILD_DIR/" && \
    echo "[✓] Kernel module built: npu-retention-driver.ko" || \
    echo "[WARNING] NPU driver build skipped (needs matching kernel headers on EliteBook)."

# ─── STEP 6: Package EFI Deployment Bundle ────────────────────────────────────
echo ""
echo "[ STEP 6 ] Packaging EFI deployment bundle..."
EFI_BUNDLE="$BUILD_DIR/EFI-Deploy"
mkdir -p "$EFI_BUNDLE/EFI/CyberDNA"

cp "$BUILD_DIR/CubixOS-loader-signed.efi" "$EFI_BUNDLE/EFI/CyberDNA/bootaa64.efi"
cp "$BUILD_DIR/efficiency.aml"            "$EFI_BUNDLE/EFI/CyberDNA/"
cp "$BUILD_DIR/sovereign_root.crt"        "$EFI_BUNDLE/EFI/CyberDNA/"
[ -f "$BUILD_DIR/npu-retention-driver.ko" ] && \
    cp "$BUILD_DIR/npu-retention-driver.ko" "$EFI_BUNDLE/EFI/CyberDNA/"

echo "[✓] EFI bundle ready at: $EFI_BUNDLE"

# ─── DONE ─────────────────────────────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║          SOVEREIGN BUILD COMPLETE                        ║"
echo "╠══════════════════════════════════════════════════════════╣"
echo "║  Artifacts in: ./build-output/                          ║"
echo "║  • sovereign_private.key  (KEEP SECRET)                 ║"
echo "║  • sovereign_root.crt     (Enroll in EliteBook BIOS db) ║"
echo "║  • CubixOS-loader-signed.efi                            ║"
echo "║  • efficiency.aml                                       ║"
echo "║  • npu-retention-driver.ko (if built)                   ║"
echo "║  • EFI-Deploy/            (copy to USB ESP partition)   ║"
echo "╠══════════════════════════════════════════════════════════╣"
echo "║  NEXT: Copy EFI-Deploy/ to USB → Enroll cert in BIOS   ║"
echo "║        → Boot from CyberDNA entry → Sovereignty achieved║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
