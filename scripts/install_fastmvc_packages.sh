#!/usr/bin/env bash
#
# Install all fastmvc_* packages in editable mode from the sibling
# fastmvc_packages directory. Run from the FastMVC repo root.
#
# Prerequisite: clone or create ../fastmvc_packages with:
#   fastmvc_core, fastmvc_dashboards, fastmvc_channels,
#   fastmvc_notifications, fastmvc_kafka, fastmvc_webrtc
#
# Usage:
#   ./scripts/install_fastmvc_packages.sh
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PACKAGES_PARENT="$(cd "$REPO_ROOT/.." && pwd)"
PACKAGES_DIR="$PACKAGES_PARENT/fastmvc_packages"

if [ ! -d "$PACKAGES_DIR" ]; then
  echo "Directory not found: $PACKAGES_DIR"
  echo "Create it and add the fastmvc_* package repos, then run this script again."
  exit 1
fi

echo "Installing editable packages from $PACKAGES_DIR"
pip install -e "$PACKAGES_DIR/fastmvc_core" \
            -e "$PACKAGES_DIR/fastmvc_dashboards" \
            -e "$PACKAGES_DIR/fastmvc_channels" \
            -e "$PACKAGES_DIR/fastmvc_notifications" \
            -e "$PACKAGES_DIR/fastmvc_kafka" \
            -e "$PACKAGES_DIR/fastmvc_webrtc"

echo "Done. You can now use fastmvc_core, fastmvc_dashboards, etc. from this environment."
