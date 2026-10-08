#!/usr/bin/env bash
# ==============================================================================
# Captura de tela de área selecionada (Ctrl + P)
# ==============================================================================

DIR="$HOME/Imagens/Screenshots"
mkdir -p "$DIR"

FILENAME="$DIR/Screenshot_$(date +%Y-%m-%d_%H-%M-%S).png"

# Seleção de área interativa com slurp (estilo branco e escuro combinando com o tema)
GEOMETRY=$(slurp -b "#1e1f2280" -c "#ffffff" -w 2 -d)

# Se o usuário cancelou (pressionou Esc), encerra
if [ -z "$GEOMETRY" ]; then
    exit 0
fi

# Captura a área selecionada
grim -g "$GEOMETRY" "$FILENAME"

# Copia para o clipboard e notifica
if [ -f "$FILENAME" ]; then
    wl-copy --type image/png < "$FILENAME"
    notify-send -a "Screenshot" "Captura de tela salva!" "Copiada para a área de transferência e salva em Screenshots." -i "$FILENAME"
fi
