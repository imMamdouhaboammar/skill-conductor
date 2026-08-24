#!/usr/bin/env sh
# Skill Conductor Universal Installer for macOS and Linux
# Usage: curl -fsSL https://raw.githubusercontent.com/imMamdouhaboammar/skill-conductor/main/install.sh | sh

set -e

RESET='\033[0m'
BOLD='\033[1m'
GREEN='\033[32m'
BLUE='\033[34m'
YELLOW='\033[33m'
RED='\033[31m'

printf "${BOLD}${BLUE}"
cat << 'EOF'
  ____  _     _ _ _      ____                 _            _             
 / ___|| |__ (_) | |    / ___|___  _ __   __| |_   _  ___| |_ ___  _ __ 
 \___ \| '_ \| | | |   | |   / _ \| '_ \ / _` | | | |/ __| __/ _ \| '__|
  ___) | | | | | | |   | |__| (_) | | | | (_| | |_| | (__| || (_) | |   
 |____/|_| |_|_|_|_|    \____\___/|_| |_|\__,_|\__,_|\___|\__\___/|_|   
EOF
printf "${RESET}\n"
printf "${BOLD}Universal Multi-Agent Installation & Distribution Manager${RESET}\n\n"

# Detect Python
if command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_BIN="python"
else
    printf "${RED}[ERROR] Python 3 is required to install Skill Conductor.${RESET}\n"
    printf "Please install Python 3 (https://www.python.org/) or via Homebrew: brew install python\n"
    exit 1
fi

INSTALL_DIR="${HOME}/.skill-conductor"
BIN_DIR="${HOME}/.local/bin"

mkdir -p "${INSTALL_DIR}"
mkdir -p "${BIN_DIR}"

printf "${BLUE}==>${RESET} Downloading Skill Conductor into ${BOLD}${INSTALL_DIR}${RESET}...\n"

# Clone or update
if [ -d "${INSTALL_DIR}/.git" ]; then
    printf "Updating existing installation...\n"
    git -C "${INSTALL_DIR}" pull --quiet || true
else
    if command -v git >/dev/null 2>&1; then
        git clone --depth=1 --quiet https://github.com/imMamdouhaboammar/skill-conductor.git "${INSTALL_DIR}"
    else
        printf "Downloading tarball...\n"
        curl -fsSL https://github.com/imMamdouhaboammar/skill-conductor/archive/refs/heads/main.tar.gz | tar -xz -C "${INSTALL_DIR}" --strip-components=1
    fi
fi

chmod +x "${INSTALL_DIR}/bin/skill-conductor"

# Symlink to ~/.local/bin
ln -sf "${INSTALL_DIR}/bin/skill-conductor" "${BIN_DIR}/skill-conductor"

# Check if ~/.local/bin is in PATH
case ":${PATH}:" in
    *:"${BIN_DIR}":*) ;;
    *)
        printf "\n${YELLOW}[NOTE] ${BIN_DIR} is not currently in your PATH.${RESET}\n"
        printf "Add it to your shell configuration (~/.zshrc or ~/.bashrc):\n"
        printf "  ${BOLD}export PATH=\"\$HOME/.local/bin:\$PATH\"${RESET}\n\n"
        ;;
esac

printf "${GREEN}[OK] Skill Conductor successfully installed!${RESET}\n\n"

# Run doctor
"${INSTALL_DIR}/bin/skill-conductor" doctor || true

printf "${BOLD}Quick start commands:${RESET}\n"
printf "  • List all skills:       ${BLUE}skill-conductor list${RESET}\n"
printf "  • Install to all agents: ${BLUE}skill-conductor install --agent all${RESET}\n"
printf "  • Validate portability:  ${BLUE}skill-conductor validate skills/skill-conductor${RESET}\n"
printf "  • Inspect diagnostics:   ${BLUE}skill-conductor doctor${RESET}\n\n"
