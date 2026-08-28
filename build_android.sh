#!/bin/bash
# Lujan Randall Vault: Native Android APK Compiler

echo "=========================================================="
echo "LUJAN RANDALL VAULT: INITIATING ANDROID (APK) BUILD"
echo "=========================================================="

BUILD_TYPE=$1
APP_TITLE="Randall Vault"
PKG_NAME="randallvault"

if [ "$BUILD_TYPE" == "media" ]; then
    APP_TITLE="Randall Media Vault"
    PKG_NAME="mediavault"
elif [ "$BUILD_TYPE" == "docs" ]; then
    APP_TITLE="Randall Document Vault"
    PKG_NAME="documentvault"
else
    echo "Usage: ./build_android.sh [media|docs]"
    echo "Building default universal vault..."
fi

echo "Initializing Buildozer & Cython dependencies..."
./.venv/bin/pip install buildozer cython

# Initialize a base buildozer configuration dynamically
if [ ! -f "buildozer.spec" ]; then
    ./.venv/bin/buildozer init
fi

echo "Configuring buildozer.spec for Double Crunch parameters..."
sed -i "s/^title = .*/title = $APP_TITLE/g" buildozer.spec
sed -i "s/^package.name = .*/package.name = $PKG_NAME/g" buildozer.spec
sed -i 's/^package.domain = org.test/package.domain = com.lujan.vault/g' buildozer.spec
# Inject all python dependencies needed for the backend logic
sed -i 's/^requirements = python3,kivy/requirements = python3,kivy,flask,werkzeug/g' buildozer.spec

echo "=========================================================="
echo "Kicking off Android Compilation (Requires Java/Android SDK)"
echo "Standby: This build bridges Python logic directly to an APK format."
echo "=========================================================="

export PATH="$PWD/.venv/bin:$PATH"
./.venv/bin/buildozer android debug

echo "=========================================================="
echo "COMPILATION SUCCESSFUL."
echo "Android APK generated inside the ./bin/ directory!"
echo "=========================================================="
