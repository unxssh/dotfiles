# 🌌 Hyprland Dotfiles & Desktop Environment

Configurações personalizadas para Arch Linux com **Hyprland**, **Waybar**, **Wofi**, **Dunst**, scripts utilitários e tema escuro integrado.

---

## ⚡ Instalação Rápida (Através de um Link)

Para instalar em qualquer máquina Arch Linux com um único comando:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/unxssh/dotfiles/main/install.sh)
```



---

## 📦 Instalação Manual

Se preferir clonar manualmente:

```bash
git clone https://github.com/unxssh/dotfiles.git ~/.dotfiles
cd ~/.dotfiles
chmod +x install.sh
./install.sh
```

---

## 🛠️ O que está incluído

- **Hyprland** (`~/.config/hypr`): Gerenciador de janelas Wayland com animações, layouts e atalhos customizados.
- **Waybar** (`~/.config/waybar`): Barra de status com previsão do tempo, workspaces dinâmicos, monitor de sistema e áudio.
- **Wofi** (`~/.config/wofi`): Menu de aplicativos estilizado e rápido.
- **Dunst** (`~/.config/dunst`): Notificações elegantes.
- **Kitty**: Terminal configurado.
- **Scripts Utilitários** (`~/.config/hypr/scripts/`):
  - `clipboard.sh`: Gerenciador de histórico da área de transferência com suporte a texto e imagens (`Super + V`).
  - `screenshot.sh`: Captura de área selecionada para a área de transferência e arquivo (`Ctrl + P` ou `Print`).
  - `wallpaper.sh`: Seletor interativo de wallpapers com transição suave via `awww` (`Super + W`).
  - `wsp.py`: Compactador inteligente de workspaces do Hyprland.
  - `init-keyring.sh`: Inicializador do `gnome-keyring` para senhas seguras.
- **Tema & Visual**:
  - Tema GTK: **Breeze-Dark**
  - Tema de Ícones: **Papirus-Dark**
  - Fontes: **JetBrainsMono Nerd Font**
  - Wallpapers padrão pré-instalados em `~/Imagens/Wallpaper/walpaper v2/`
- **Spicetify**:
  - Temas e extensões para Spotify com estilo iOS-Glass / LiquidMusic.

---

## ⌨️ Principais Atalhos de Teclado

| Atalho | Ação |
| :--- | :--- |
| `Super + Q` | Abrir terminal (**Kitty**) |
| `Super + E` | Abrir gerenciador de arquivos (**Dolphin**) |
| `Super + R` | Abrir menu de aplicativos (**Wofi**) |
| `Super + C` | Fechar janela ativa |
| `Super + V` | Histórico da área de transferência (**Cliphist + Wofi**) |
| `Super + W` | Seletor visual de papéis de parede |
| `Ctrl + P` ou `Print` | Captura de tela interativa (**Grim + Slurp**) |
| `Super + M` | Sair do Hyprland |

---

## 🔒 Segurança

Antes de qualquer instalação ou sobrescrita, o script `install.sh` gera automaticamente um backup timestamped de segurança em `~/.config_backup_YYYYMMDD_HHMMSS/`.
