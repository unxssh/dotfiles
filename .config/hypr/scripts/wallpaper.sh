#!/usr/bin/env bash
# ==============================================================================
# Gerenciador de Wallpapers com Wofi para Hyprland
# ==============================================================================

WALLPAPER_DIR="${WALLPAPER_DIR:-$HOME/Imagens/Wallpaper/walpaper v2}"
FALLBACK_DIR="$HOME/Imagens/Wallpaper"
CURRENT_WP_FILE="$HOME/.config/hypr/current_wallpaper"

# Se o diretório padrão não existir, tenta o fallback
if [ ! -d "$WALLPAPER_DIR" ]; then
    if [ -d "$FALLBACK_DIR" ]; then
        WALLPAPER_DIR="$FALLBACK_DIR"
    else
        notify-send "Erro" "Nenhum diretório de wallpapers encontrado" -u critical
        exit 1
    fi
fi

# Garante que o daemon awww está em execução
if ! pgrep -x "awww-daemon" > /dev/null; then
    awww-daemon &
    sleep 0.4
fi

# Função para aplicar wallpaper com transição suave
set_wallpaper() {
    local wp="$1"
    if [ -f "$wp" ]; then
        awww img "$wp" \
            --transition-type wipe \
            --transition-angle 30 \
            --transition-step 90 \
            --transition-fps 60

        echo "$wp" > "$CURRENT_WP_FILE"
        notify-send -a "Wallpaper" "Papel de parede aplicado" "$(basename "$wp")" -i "$wp"

        # Atualiza o tema do Spotify com o novo wallpaper em segundo plano
        if [ -f "$HOME/.config/spicetify/apply_custom_theme.py" ]; then
            (python3 "$HOME/.config/spicetify/apply_custom_theme.py" >/dev/null 2>&1 && ~/.spicetify/spicetify apply >/dev/null 2>&1) &
        fi
    fi
}

# Suporte ao modo aleatório via argumento de terminal (ex: wallpaper.sh random)
if [ "$1" = "random" ]; then
    random_wp=$(find "$WALLPAPER_DIR" -type f \( -iname "*.jpg" -o -iname "*.png" -o -iname "*.webp" -o -iname "*.jpeg" \) | shuf -n 1)
    if [ -n "$random_wp" ]; then
        set_wallpaper "$random_wp"
    fi
    exit 0
fi

# Abre diretamente o Wofi com a lista de todos os wallpapers
selected_name=$(find "$WALLPAPER_DIR" -maxdepth 1 -type f \( -iname "*.jpg" -o -iname "*.png" -o -iname "*.webp" -o -iname "*.jpeg" \) -printf "%f\n" | sort -V | wofi --show dmenu --prompt "Escolher Wallpaper...")

if [ -n "$selected_name" ]; then
    full_path="$WALLPAPER_DIR/$selected_name"
    if [ -f "$full_path" ]; then
        set_wallpaper "$full_path"
    fi
fi
