#!/usr/bin/env python3
import os
import subprocess
import base64

HYPR_WP_FILE = os.path.expanduser("~/.config/hypr/current_wallpaper")
FALLBACK_WP = os.path.expanduser("~/Imagens/Wallpaper/walpaper v2/0RJJV1S4DVZ5.png")
THEME_DIR = os.path.expanduser("~/.config/spicetify/Themes/iOS-Glass")
USER_CSS = os.path.join(THEME_DIR, "user.css")
TMP_JPG = "/tmp/spotify_wp_optimized.jpg"

wp_path = FALLBACK_WP
if os.path.exists(HYPR_WP_FILE):
    with open(HYPR_WP_FILE, "r") as f:
        line = f.read().strip()
        if os.path.exists(line):
            wp_path = line

print(f"Using wallpaper: {wp_path}")

subprocess.run(["magick", "convert", wp_path, "-quality", "85", TMP_JPG], check=True)

with open(TMP_JPG, "rb") as f:
    b64_data = base64.b64encode(f.read()).decode("utf-8")
data_uri = f"data:image/jpeg;base64,{b64_data}"

custom_css = f"""/* ========================================================================== */
/* iOS Glass Theme - Frosted Glass (Desfoque) com Wallpaper e UI Limpa        */
/* ========================================================================== */

/* Fundo transparente nas raízes para exibir o wallpaper */
html,
body,
#main,
.Root,
.Root__top-container,
.main-view-container,
.main-view-container__scroll-node,
.main-view-container__scroll-node-child,
main {{
    background: transparent !important;
    background-color: transparent !important;
}}

/* Wallpaper de Fundo Fixo */
body::before {{
    content: "";
    position: fixed;
    inset: 0;
    z-index: -9999;
    background-image: url("{data_uri}") !important;
    background-size: cover !important;
    background-position: center !important;
    background-repeat: no-repeat !important;
    pointer-events: none !important;
}}

/* Película escura sutil sobre o wallpaper para garantir contraste e leitura */
body::after {{
    content: "";
    position: fixed;
    inset: 0;
    z-index: -9998;
    background: rgba(10, 10, 14, 0.40) !important;
    pointer-events: none !important;
}}

/* Espaçamento e layout elegante */
.Root__top-container {{
    padding: 10px !important;
    gap: 10px !important;
}}

/* ========================================================================== */
/* PAINÉIS EM VIDRO COM DESFOQUE (Frosted Glass / Backdrop Filter)            */
/* ========================================================================== */

/* Painel Central (Home / Playlist / Browse) */
.Root__main-view {{
    background: rgba(18, 18, 24, 0.52) !important;
    backdrop-filter: blur(28px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(28px) saturate(180%) !important;
    border-radius: 18px !important;
    border: 1px solid rgba(255, 255, 255, 0.10) !important;
    overflow: hidden !important;
}}

/* Barra Lateral Esquerda (Sua Biblioteca) */
.Root__nav-bar {{
    background: rgba(14, 14, 18, 0.58) !important;
    backdrop-filter: blur(32px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(32px) saturate(180%) !important;
    border-radius: 18px !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    overflow: hidden !important;
}}

.Root__nav-bar .main-yourLibraryX-entryPoints {{
    background: transparent !important;
}}

/* Barra Lateral Direita (Now Playing View / Painel de Amigos) */
.Root__right-sidebar,
.Root__right-sidebar-peek {{
    background: rgba(14, 14, 18, 0.58) !important;
    backdrop-filter: blur(32px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(32px) saturate(180%) !important;
    border-radius: 18px !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    overflow: hidden !important;
}}

/* Top Navigation / Barra Superior */
.Root__globalNav,
.main-topBar-container {{
    background: transparent !important;
}}

.main-topBar-background {{
    background: rgba(18, 18, 24, 0.45) !important;
    backdrop-filter: blur(20px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
}}

.main-globalNav-historyButtons,
.main-globalNav-searchInputContainer {{
    background: rgba(28, 28, 36, 0.65) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 9999px !important;
}}

/* Player Inferior - Pílula Flutuante em Vidro */
.Root__now-playing-bar {{
    background: transparent !important;
}}

.main-nowPlayingBar-container {{
    background: rgba(20, 20, 26, 0.70) !important;
    backdrop-filter: blur(35px) saturate(200%) !important;
    -webkit-backdrop-filter: blur(35px) saturate(200%) !important;
    border: 1px solid rgba(255, 255, 255, 0.14) !important;
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.45) !important;
    border-radius: 20px !important;
    padding: 0 16px !important;
}}

/* Cards com visual translúcido suave */
.main-card-card {{
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    border-radius: 12px !important;
    transition: background 0.2s ease, transform 0.2s ease !important;
}}

.main-card-card:hover {{
    background: rgba(255, 255, 255, 0.10) !important;
    transform: translateY(-2px) !important;
}}

/* ========================================================================== */
/* CORREÇÃO DO LAYOUT DA HOME: REMOVE "GETTING STARTED" E EVITA SOBREPOSIÇÃO  */
/* ========================================================================== */

/* Remove a seção "Getting started" (banner de dicas que sobrepõe "Jump back in") */
[data-shelf-collapsable],
section:has([aria-label*="Getting started"]),
section:has([aria-label*="Comece a ouvir"]),
section:has(button[aria-label*="Show more tips"]),
section:has(button[aria-label*="Mais dicas"]),
section:has(a[href*="genre/getting-started"]) {{
    display: none !important;
}}

/* Garante que as prateleiras fiquem em colunas independentes e nunca colidam */
.main-home-content {{
    flex-direction: column !important;
    gap: 24px !important;
}}

.main-home-content > [data-shelf] {{
    width: 100% !important;
    max-width: 100% !important;
    min-width: 100% !important;
    flex: 1 1 100% !important;
}}

/* ========================================================================== */
/* LIMPEZA DE TELA: REMOVE ITENS DESNECESSÁRIOS E SCROLLBAR                   */
/* ========================================================================== */

/* Oculta scrollbars */
::-webkit-scrollbar {{
    width: 0 !important;
    height: 0 !important;
    display: none !important;
}}

* {{
    scrollbar-width: none !important;
}}

/* Tipografia moderna */
* {{
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Inter", "Segoe UI", Roboto, sans-serif !important;
}}

/* Remove botões de Upgrade, Baixar App e banners */
[data-testid="upgrade-button"],
button[data-testid="upgrade-button"],
.main-topBar-UpgradeButton,
button[title*="Upgrade"],
button[title*="Atualizar"],
button[title*="Melhorar"],
[data-testid="download-desktop-client-button"],
button[aria-label*="Download"],
button[aria-label*="Baixar"],
button[data-testid="whats-new-feed-button"],
.desktop-banner-container,
#banner-container,
.main-leaderboardComponent-container,
.main-billboardComponent-container,
.main-connectToDevice-button[aria-expanded="false"] + .main-connectToDevice-tooltip {{
    display: none !important;
}}

/* ========================================================================== */
/* OCULTA PLAYLIST "MÚSICAS CURTIDAS" DOS ATALHOS E DA BARRA LATERAL          */
/* ========================================================================== */
li:has(a[href*="/collection/tracks"]),
[data-testid="your-library-item"]:has(a[href*="/collection/tracks"]),
.view-homeShortcutsGrid-shortcut:has(a[href*="/collection/tracks"]),
a[href*="/collection/tracks"],
.main-collectionLinkButton-collectionLinkButton[href*="/collection/tracks"],
.collection-collectionEntityHeroCard-likedSongs,
button[aria-label*="Músicas Curtidas"],
button[aria-label*="Liked Songs"] {{
    display: none !important;
}}
"""

with open(USER_CSS, "w") as f:
    f.write(custom_css)

print("iOS-Glass user.css generated successfully!")
