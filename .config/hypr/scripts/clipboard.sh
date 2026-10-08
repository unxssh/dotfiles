#!/usr/bin/env bash
# ==============================================================================
# Gerenciador de Área de Transferência com Wofi e Cliphist (Super + V)
# Suporta textos, links e imagens/prints
# ==============================================================================

# Garante que os watchers do cliphist estão ativos em segundo plano
if ! pgrep -f "cliphist store" > /dev/null; then
    wl-paste --type text --watch cliphist store &
    wl-paste --type image --watch cliphist store &
fi

# Abre o Wofi com o histórico de cópias
selected=$(cliphist list | wofi --show dmenu --prompt "Área de Transferência...")

if [ -n "$selected" ]; then
    # Decodifica e envia de volta ao clipboard
    cliphist decode "$selected" | wl-copy

    # Notificação informativa
    if echo "$selected" | grep -q '\[\[ binary data'; then
        notify-send -a "Área de Transferência" "Print/Imagem copiada!" "Pronta para colar com Ctrl + V." -i image-x-generic
    else
        text_content=$(echo "$selected" | cut -f2-)
        notify-send -a "Área de Transferência" "Item copiado!" "$text_content" -i edit-copy
    fi
fi
