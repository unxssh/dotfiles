#!/bin/bash

# Atualiza as variáveis de ambiente no DBus e systemd para a sessão Wayland
dbus-update-activation-environment --systemd WAYLAND_DISPLAY XDG_CURRENT_DESKTOP --all 2>/dev/null || true

# Inicializa ou conecta ao daemon do gnome-keyring
if ! pgrep -u "$USER" gnome-keyring-daemon >/dev/null 2>&1; then
    gnome-keyring-daemon --daemonize --components=secrets
else
    gnome-keyring-daemon --start --components=secrets
fi
