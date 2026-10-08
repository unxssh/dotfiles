#!/usr/bin/env bash
# ==============================================================================
#  Dotfiles Installer - Hyprland Desktop Environment
#  Suporta execução local (./install.sh) ou remota via curl:
#  bash <(curl -fsSL <URL_DO_RAW_INSTALL_SH>)
# ==============================================================================

set -e

# Cores para saída no terminal
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Repositório padrão (pode ser sobrescrito por variável de ambiente DOTFILES_REPO)
DOTFILES_REPO="${DOTFILES_REPO:-https://github.com/unxssh/dotfiles.git}"
TARGET_DIR="${HOME}/.dotfiles"

echo -e "${CYAN}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║             Instalador de Dotfiles Hyprland                ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Detectar diretório de execução
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" 2>/dev/null && pwd || echo "")"

# Se executado via pipe (curl | bash), clona ou atualiza o repositório em ~/.dotfiles
if [ -z "$SCRIPT_DIR" ] || [ ! -d "$SCRIPT_DIR/.config" ]; then
    echo -e "${BLUE}[*] Execução remota detectada. Preparando ambiente...${NC}"
    
    if ! command -v git &>/dev/null; then
        echo -e "${YELLOW}[!] Git não encontrado. Instalando git...${NC}"
        sudo pacman -S --needed --noconfirm git
    fi

    if [ -d "$TARGET_DIR/.git" ]; then
        echo -e "${BLUE}[*] Atualizando repositório existente em $TARGET_DIR...${NC}"
        cd "$TARGET_DIR"
        git pull origin main || git pull
    else
        echo -e "${BLUE}[*] Clonando dotfiles para $TARGET_DIR...${NC}"
        rm -rf "$TARGET_DIR"
        git clone "$DOTFILES_REPO" "$TARGET_DIR"
    fi

    cd "$TARGET_DIR"
    exec bash "$TARGET_DIR/install.sh" "$@"
fi

DOTFILES_PATH="$SCRIPT_DIR"

# Flags
AUTO_YES=false
for arg in "$@"; do
    if [ "$arg" == "-y" ] || [ "$arg" == "--noconfirm" ]; then
        AUTO_YES=true
    fi
done

prompt_user() {
    if [ "$AUTO_YES" = true ]; then
        return 0
    fi
    local message="$1"
    read -rp "$message [S/n]: " response
    case "$response" in
        [nN][aA][oO]|[nN]) return 1 ;;
        *) return 0 ;;
    esac
}

# 1. Instalação de dependências (se em Arch Linux)
if [ -f /etc/arch-release ]; then
    if prompt_user "$(echo -e "${YELLOW}[?] Deseja instalar os pacotes e dependências necessários?${NC}")"; then
        echo -e "${BLUE}[*] Atualizando banco de pacotes e instalando dependências oficiais...${NC}"
        if [ -f "$DOTFILES_PATH/packages.txt" ]; then
            # Filtra comentários e linhas vazias
            PKG_LIST=$(grep -v '^#' "$DOTFILES_PATH/packages.txt" | grep -v '^[[:space:]]*$' | tr '\n' ' ')
            # shellcheck disable=SC2086
            sudo pacman -S --needed --noconfirm $PKG_LIST || echo -e "${YELLOW}[!] Alguns pacotes não puderam ser instalados pelo pacman.${NC}"
        fi

        # Instalação de pacotes AUR se yay estiver disponível
        if command -v yay &>/dev/null && [ -f "$DOTFILES_PATH/packages-aur.txt" ]; then
            echo -e "${BLUE}[*] Instalando pacotes do AUR via yay...${NC}"
            AUR_LIST=$(grep -v '^#' "$DOTFILES_PATH/packages-aur.txt" | grep -v '^[[:space:]]*$' | tr '\n' ' ')
            # shellcheck disable=SC2086
            yay -S --needed --noconfirm $AUR_LIST || echo -e "${YELLOW}[!] Aviso na instalação de pacotes AUR.${NC}"
        else
            echo -e "${YELLOW}[!] yay não detectado. Pulando pacotes AUR.${NC}"
        fi
    fi
fi

# 2. Backup de configurações existentes
echo -e "${BLUE}[*] Criando backup de segurança das configurações existentes...${NC}"
BACKUP_DIR="${HOME}/.config_backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

for item in hypr waybar wofi dunst gtk-3.0 gtk-4.0 nwg-look qt5ct qt6ct xsettingsd spicetify; do
    if [ -d "${HOME}/.config/$item" ]; then
        cp -r "${HOME}/.config/$item" "$BACKUP_DIR/"
    fi
done
for file in kdeglobals dolphinrc arkrc pavucontrol.ini mimeapps.list; do
    if [ -f "${HOME}/.config/$file" ]; then
        cp "${HOME}/.config/$file" "$BACKUP_DIR/"
    fi
done
[ -f "${HOME}/.bashrc" ] && cp "${HOME}/.bashrc" "$BACKUP_DIR/"
[ -f "${HOME}/.gtkrc-2.0" ] && cp "${HOME}/.gtkrc-2.0" "$BACKUP_DIR/"

echo -e "${GREEN}[✓] Backup salvo com sucesso em: $BACKUP_DIR${NC}"

# 3. Aplicando os arquivos de configuração
echo -e "${BLUE}[*] Copiando arquivos de configuração para ~/.config...${NC}"
mkdir -p "${HOME}/.config"
cp -r "$DOTFILES_PATH/.config/"* "${HOME}/.config/"

# Ajustar permissões dos scripts
echo -e "${BLUE}[*] Configurando permissões de execução nos scripts...${NC}"
chmod +x "${HOME}/.config/hypr/scripts/"* 2>/dev/null || true
[ -f "${HOME}/.config/waybar/weather.py" ] && chmod +x "${HOME}/.config/waybar/weather.py"

# Copiando dotfiles da pasta home
if [ -d "$DOTFILES_PATH/home" ]; then
    echo -e "${BLUE}[*] Copiando arquivos para $HOME...${NC}"
    [ -f "$DOTFILES_PATH/home/.gtkrc-2.0" ] && cp "$DOTFILES_PATH/home/.gtkrc-2.0" "${HOME}/"
    [ -f "$DOTFILES_PATH/home/.bash_profile" ] && cp "$DOTFILES_PATH/home/.bash_profile" "${HOME}/"
    # Se o usuário quiser sobrescrever o .bashrc
    if prompt_user "$(echo -e "${YELLOW}[?] Deseja atualizar o ~/.bashrc?${NC}")"; then
        cp "$DOTFILES_PATH/home/.bashrc" "${HOME}/"
    fi
fi

# Copiando gsettings nwg-look
if [ -d "$DOTFILES_PATH/local_share/nwg-look" ]; then
    mkdir -p "${HOME}/.local/share/nwg-look"
    cp -r "$DOTFILES_PATH/local_share/nwg-look/"* "${HOME}/.local/share/nwg-look/"
fi

# 4. Wallpapers padrão
WP_DIR="${HOME}/Imagens/Wallpaper/walpaper v2"
mkdir -p "$WP_DIR"
if [ -d "$DOTFILES_PATH/wallpapers" ]; then
    echo -e "${BLUE}[*] Instalando papéis de parede padrão em $WP_DIR...${NC}"
    cp -r "$DOTFILES_PATH/wallpapers/"* "$WP_DIR/"
fi

# 5. Ajustar caminhos dinâmicos para o usuário atual
echo -e "${BLUE}[*] Normalizando caminhos para o usuário atual ($USER)...${NC}"
DEFAULT_WP="${WP_DIR}/0RJJV1S4DVZ5.png"
FALLBACK_WP="${WP_DIR}/WEPAP9J3DE7U.jpg"

echo "$DEFAULT_WP" > "${HOME}/.config/hypr/current_wallpaper"

if [ -f "${HOME}/.config/hypr/hyprpaper.conf" ]; then
    cat <<EOF > "${HOME}/.config/hypr/hyprpaper.conf"
preload = ${FALLBACK_WP}
wallpaper = ,${FALLBACK_WP}
EOF
fi

if [ -f "${HOME}/.config/spicetify/config-xpui.ini" ]; then
    sed -i "s|prefs_path.*=.*|prefs_path = ${HOME}/.config/spotify/prefs|g" "${HOME}/.config/spicetify/config-xpui.ini"
fi

# 6. Aplicar temas via gsettings
if command -v gsettings &>/dev/null; then
    echo -e "${BLUE}[*] Aplicando temas GTK e ícones via gsettings...${NC}"
    gsettings set org.gnome.desktop.interface gtk-theme "Breeze-Dark" 2>/dev/null || true
    gsettings set org.gnome.desktop.interface icon-theme "Papirus-Dark" 2>/dev/null || true
    gsettings set org.gnome.desktop.interface font-name "JetBrainsMono Nerd Font Mono Medium 10" 2>/dev/null || true
    gsettings set org.gnome.desktop.interface cursor-theme "breeze_cursors" 2>/dev/null || true
    gsettings set org.gnome.desktop.interface cursor-size 24 2>/dev/null || true
    gsettings set org.gnome.desktop.interface color-scheme "prefer-dark" 2>/dev/null || true
fi

echo -e "\n${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║         Instalação concluída com sucesso! 🎉              ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo -e "\n${CYAN}Dica:${NC} Se você já estiver em uma sessão Hyprland, execute:"
echo -e "  ${YELLOW}hyprctl reload${NC}  e reinicie a waybar (${YELLOW}killall waybar && waybar &${NC})"
echo -e "Caso contrário, basta iniciar a sessão normalmente com ${YELLOW}Hyprland${NC}.\n"
