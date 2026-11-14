"""
Design Gallery - 37 UI design styles in one Streamlit app

Run with:  streamlit run designs.py

How it works (very simple):
    1. DESIGNS  -> a dictionary. Each design = a few colour/shadow settings.
    2. build_css() -> turns the chosen design into CSS.
    3. show_demo_page() -> ONE sample page (cards, buttons, inputs, bars)
       that looks different for every design because only the CSS changes.

Want to add your own design? Copy any block inside DESIGNS and change the values.
"""

import html

import streamlit as st


# =====================================================================
# 1. PAGE SETUP
# =====================================================================

st.set_page_config(page_title="Design Gallery", page_icon="🎨", layout="wide")


# =====================================================================
# 2. THE 37 DESIGNS
# =====================================================================
# Every design has:
#   icon / tagline / search  -> information shown on the page
#   tip                      -> the main CSS trick of that style
#   vars                     -> colours, shadows, radius... (used by the CSS)
#   extra                    -> extra CSS only this design needs (optional)

# Values used when a design does not set them
DEFAULTS = {
    "font": "'Segoe UI', system-ui, sans-serif",
    "head_font": "inherit",
    "card_border": "none",
    "card_shadow": "none",
    "blur": "none",
    "radius": "16px",
    "btn_border": "none",
    "btn_shadow": "none",
    "btn_hover": "none",
    "btn_radius": "12px",
    "btn_move": "none",
    "inset_bg": "transparent",
    "inset": "none",
    "input_border": "none",
    "sel_outline": "2px solid var(--accent)",
}

DESIGNS = {
    # ------------------------------------------------------------ 1
    "Neumorphism": {
        "icon": "🫧",
        "tagline": "Soft, pushed-out shapes made from the same colour as the background.",
        "search": ["neumorphism", "soft UI", "neumorphic design CSS", "neumorphism.io"],
        "tip": "box-shadow: 9px 9px 18px #a3b1c6,\n            -9px -9px 18px #ffffff;   /* raised */\n"
               "box-shadow: inset 6px 6px 12px #a3b1c6,\n            inset -6px -6px 12px #ffffff; /* pressed */",
        "vars": {
            "page_bg": "#e0e5ec", "side_bg": "#e0e5ec", "card_bg": "#e0e5ec",
            "card_shadow": "9px 9px 18px #a3b1c6, -9px -9px 18px #ffffff",
            "radius": "24px", "text": "#3d4468", "muted": "#7b84a3",
            "accent": "#5b7cfa", "accent2": "#8f6bff",
            "btn_bg": "#e0e5ec", "btn_text": "#5b7cfa", "btn_radius": "16px",
            "btn_shadow": "5px 5px 10px #a3b1c6, -5px -5px 10px #ffffff",
            "btn_hover": "inset 4px 4px 8px #a3b1c6, inset -4px -4px 8px #ffffff",
            "inset_bg": "#e0e5ec",
            "inset": "inset 5px 5px 10px #a3b1c6, inset -5px -5px 10px #ffffff",
            "sel_outline": "none",
        },
    },
    # ------------------------------------------------------------ 2
    "Glassmorphism": {
        "icon": "🪟",
        "tagline": "Frosted-glass panels floating over a colourful background.",
        "search": ["glassmorphism", "frosted glass UI", "backdrop-filter blur CSS", "css.glass"],
        "tip": "background: rgba(255, 255, 255, 0.18);\nbackdrop-filter: blur(14px);\n"
               "border: 1px solid rgba(255, 255, 255, 0.4);",
        "vars": {
            "page_bg": "linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%)",
            "side_bg": "rgba(255,255,255,0.12)", "card_bg": "rgba(255,255,255,0.18)",
            "card_border": "1px solid rgba(255,255,255,0.45)",
            "card_shadow": "0 8px 32px rgba(31,38,135,0.25)", "blur": "blur(14px)",
            "radius": "22px", "text": "#ffffff", "muted": "rgba(255,255,255,0.78)",
            "accent": "#ffffff", "accent2": "#ffd6ff",
            "btn_bg": "rgba(255,255,255,0.22)", "btn_text": "#ffffff",
            "btn_border": "1px solid rgba(255,255,255,0.55)",
            "btn_hover": "0 6px 20px rgba(255,255,255,0.35)", "btn_move": "translateY(-2px)",
            "inset_bg": "rgba(255,255,255,0.2)", "input_border": "1px solid rgba(255,255,255,0.45)",
        },
    },
    # ------------------------------------------------------------ 3
    "Claymorphism": {
        "icon": "🧸",
        "tagline": "Puffy, rounded 3D shapes that look like soft clay.",
        "search": ["claymorphism", "clay UI design", "3D soft UI CSS", "clay style buttons"],
        "tip": "border-radius: 32px;\nbox-shadow: inset -8px -8px 16px rgba(0,0,0,0.08),\n"
               "            inset 8px 8px 16px rgba(255,255,255,0.7),\n"
               "            10px 10px 24px rgba(214,130,170,0.45);",
        "vars": {
            "page_bg": "#ffeef6", "side_bg": "#ffe0ee", "card_bg": "#ffd9ea",
            "card_shadow": "inset -8px -8px 16px rgba(0,0,0,0.07), inset 8px 8px 16px rgba(255,255,255,0.7), 10px 10px 24px rgba(214,130,170,0.45)",
            "radius": "34px", "text": "#5a2a45", "muted": "#9a6a85",
            "accent": "#ff5fa2", "accent2": "#ffa24d", "head_font": "'Nunito', sans-serif",
            "btn_bg": "#ffb3d4", "btn_text": "#5a2a45", "btn_radius": "22px",
            "btn_shadow": "inset -4px -4px 8px rgba(0,0,0,0.08), inset 4px 4px 8px rgba(255,255,255,0.7), 5px 5px 12px rgba(214,130,170,0.5)",
            "btn_hover": "inset -4px -4px 8px rgba(0,0,0,0.08), inset 4px 4px 8px rgba(255,255,255,0.7), 8px 10px 18px rgba(214,130,170,0.6)",
            "btn_move": "translateY(-2px)", "inset_bg": "#ffe6f1",
            "inset": "inset 4px 4px 8px rgba(214,130,170,0.35), inset -4px -4px 8px rgba(255,255,255,0.8)",
        },
    },
    # ------------------------------------------------------------ 4
    "Neobrutalism": {
        "icon": "🧱",
        "tagline": "Bold black outlines, hard shadows and loud flat colours.",
        "search": ["neobrutalism", "neo brutalism web design", "brutalist UI CSS", "neubrutalism components"],
        "tip": "border: 3px solid #000;\nbox-shadow: 6px 6px 0 #000;   /* hard shadow, NO blur */\n"
               "border-radius: 6px;",
        "vars": {
            "page_bg": "#fff4d6", "side_bg": "#ffd400", "card_bg": "#ffffff",
            "card_border": "3px solid #000", "card_shadow": "6px 6px 0 #000",
            "radius": "6px", "text": "#000000", "muted": "#444444",
            "accent": "#ff3d71", "accent2": "#ffd400",
            "font": "'Space Grotesk', sans-serif",
            "btn_bg": "#ffd400", "btn_text": "#000000", "btn_border": "3px solid #000",
            "btn_shadow": "4px 4px 0 #000", "btn_hover": "0 0 0 #000",
            "btn_move": "translate(4px, 4px)", "btn_radius": "6px",
            "inset_bg": "#ffffff", "input_border": "3px solid #000",
        },
    },
    # ------------------------------------------------------------ 5
    "Cyberpunk Neon": {
        "icon": "🌃",
        "tagline": "Dark background with glowing cyan and pink neon edges.",
        "search": ["cyberpunk UI", "neon glow CSS", "dark neon website design", "futuristic HUD UI"],
        "tip": "border: 1px solid #00f0ff;\nbox-shadow: 0 0 18px #00f0ff55;   /* glow */\n"
               "text-shadow: 0 0 8px #00f0ff;",
        "vars": {
            "page_bg": "#0b0f1a", "side_bg": "#070a12", "card_bg": "#121a2e",
            "card_border": "1px solid rgba(0,240,255,0.45)",
            "card_shadow": "0 0 18px rgba(0,240,255,0.2)", "radius": "12px",
            "text": "#e6f7ff", "muted": "#7fa4b8", "accent": "#00f0ff", "accent2": "#ff2bd6",
            "font": "'Rajdhani', sans-serif", "head_font": "'Orbitron', sans-serif",
            "btn_bg": "transparent", "btn_text": "#00f0ff", "btn_border": "1px solid #00f0ff",
            "btn_shadow": "0 0 10px rgba(0,240,255,0.5)",
            "btn_hover": "0 0 24px rgba(0,240,255,0.9)", "btn_radius": "8px",
            "inset_bg": "#0b1324", "input_border": "1px solid rgba(0,240,255,0.4)",
        },
        "extra": ".stApp .hero h1 { text-shadow: 0 0 14px #00f0ff; }",
    },
    # ------------------------------------------------------------ 6
    "Minimal Swiss": {
        "icon": "⬜",
        "tagline": "Lots of white space, thin lines and one strong accent.",
        "search": ["minimalist web design", "Swiss design style", "International Typographic Style", "minimal UI"],
        "tip": "background: #fff;\nborder: 1px solid #e5e5e5;   /* thin line, no shadow */\n"
               "color: #111;",
        "vars": {
            "page_bg": "#ffffff", "side_bg": "#fafafa", "card_bg": "#ffffff",
            "card_border": "1px solid #e5e5e5", "radius": "4px",
            "text": "#111111", "muted": "#777777", "accent": "#e63946", "accent2": "#111111",
            "font": "'Inter', sans-serif",
            "btn_bg": "#111111", "btn_text": "#ffffff", "btn_radius": "2px",
            "btn_hover": "0 0 0 3px #e63946", "inset_bg": "#f5f5f5",
            "input_border": "1px solid #dddddd",
        },
    },
    # ------------------------------------------------------------ 7
    "Aurora Gradient": {
        "icon": "🌌",
        "tagline": "Dark page with soft glowing colour clouds (mesh gradient).",
        "search": ["aurora UI", "mesh gradient background", "gradient glow website design", "aurora gradient CSS"],
        "tip": "background:\n  radial-gradient(at 20% 10%, #7c3aed55, transparent 50%),\n"
               "  radial-gradient(at 80% 20%, #06b6d455, transparent 50%),\n  #0f1020;",
        "vars": {
            "page_bg": "radial-gradient(at 15% 10%, rgba(124,58,237,0.55), transparent 50%), radial-gradient(at 85% 15%, rgba(6,182,212,0.45), transparent 50%), radial-gradient(at 50% 95%, rgba(244,114,182,0.4), transparent 50%), #0f1020",
            "side_bg": "rgba(15,16,32,0.7)", "card_bg": "rgba(255,255,255,0.06)",
            "card_border": "1px solid rgba(255,255,255,0.14)", "blur": "blur(10px)",
            "radius": "20px", "text": "#f1f0ff", "muted": "#a9a8c8",
            "accent": "#a78bfa", "accent2": "#22d3ee",
            "btn_bg": "linear-gradient(90deg, #7c3aed, #06b6d4)", "btn_text": "#ffffff",
            "btn_hover": "0 8px 24px rgba(124,58,237,0.55)", "btn_move": "translateY(-2px)",
            "btn_radius": "14px", "inset_bg": "rgba(255,255,255,0.07)",
            "input_border": "1px solid rgba(255,255,255,0.18)",
        },
    },
    # ------------------------------------------------------------ 8
    "Retro Windows 98": {
        "icon": "💾",
        "tagline": "Grey 3D buttons, teal desktop and a blue title bar - 90s computer look.",
        "search": ["Windows 98 UI CSS", "98.css", "retro operating system design", "y2k web design"],
        "tip": "border-radius: 0;\nbox-shadow: inset -1px -1px #0a0a0a, inset 1px 1px #ffffff,\n"
               "            inset -2px -2px #808080, inset 2px 2px #dfdfdf;",
        "vars": {
            "page_bg": "#008080", "side_bg": "#c0c0c0", "card_bg": "#c0c0c0",
            "card_shadow": "inset -1px -1px #0a0a0a, inset 1px 1px #ffffff, inset -2px -2px #808080, inset 2px 2px #dfdfdf",
            "radius": "0px", "text": "#000000", "muted": "#404040",
            "accent": "#000080", "accent2": "#1084d0", "font": "Tahoma, 'MS Sans Serif', sans-serif",
            "btn_bg": "#c0c0c0", "btn_text": "#000000", "btn_radius": "0px",
            "btn_shadow": "inset -1px -1px #0a0a0a, inset 1px 1px #ffffff, inset -2px -2px #808080, inset 2px 2px #dfdfdf",
            "btn_hover": "inset -1px -1px #ffffff, inset 1px 1px #0a0a0a, inset -2px -2px #dfdfdf, inset 2px 2px #808080",
            "inset_bg": "#ffffff",
            "inset": "inset -1px -1px #ffffff, inset 1px 1px #808080, inset -2px -2px #dfdfdf, inset 2px 2px #0a0a0a",
        },
        "extra": ".stApp .hero { background: linear-gradient(90deg, #000080, #1084d0); }"
                 ".stApp .hero h1, .stApp .hero p, .stApp .hero .muted { color: #ffffff; }",
    },
    # ------------------------------------------------------------ 9
    "Material Design": {
        "icon": "📱",
        "tagline": "Google style: clean white cards, layered shadows, colourful buttons.",
        "search": ["Material Design", "Material 3", "material.io", "elevation shadows UI"],
        "tip": "box-shadow: 0 2px 6px rgba(0,0,0,0.12),\n            0 8px 24px rgba(0,0,0,0.08);   /* elevation */\n"
               "border-radius: 12px;",
        "vars": {
            "page_bg": "#f4f6fb", "side_bg": "#ffffff", "card_bg": "#ffffff",
            "card_shadow": "0 2px 6px rgba(0,0,0,0.12), 0 8px 24px rgba(0,0,0,0.08)",
            "radius": "14px", "text": "#1f2430", "muted": "#6b7280",
            "accent": "#6750a4", "accent2": "#b69df8", "font": "'Inter', sans-serif",
            "btn_bg": "#6750a4", "btn_text": "#ffffff", "btn_radius": "22px",
            "btn_shadow": "0 2px 4px rgba(0,0,0,0.3)",
            "btn_hover": "0 6px 14px rgba(103,80,164,0.45)", "btn_move": "translateY(-1px)",
            "inset_bg": "#eceaf4", "input_border": "1px solid #cfc9e0",
        },
    },
    # ------------------------------------------------------------ 10
    "Skeuomorphism": {
        "icon": "🎛️",
        "tagline": "Realistic look: brushed metal, glossy buttons, real-world textures.",
        "search": ["skeuomorphism", "skeuomorphic UI", "iOS 6 design", "realistic UI buttons CSS"],
        "tip": "background: linear-gradient(#6fb1ff, #2b7de9);   /* gloss */\n"
               "box-shadow: 0 3px 0 #1c5fb8,\n            0 6px 10px rgba(0,0,0,0.4);   /* thick 3D button */",
        "vars": {
            "page_bg": "linear-gradient(180deg, #3a3f47, #23262b)", "side_bg": "#1c1f24",
            "side_text": "#e8ebf0",
            "card_bg": "linear-gradient(180deg, #f2f4f7, #cfd4db)",
            "card_border": "1px solid #9aa1ab",
            "card_shadow": "0 8px 18px rgba(0,0,0,0.5), inset 0 1px 0 #ffffff",
            "radius": "16px", "text": "#20242a", "muted": "#5a6270",
            "accent": "#2b7de9", "accent2": "#6fb1ff",
            "btn_bg": "linear-gradient(180deg, #6fb1ff, #2b7de9)", "btn_text": "#ffffff",
            "btn_border": "1px solid #1c5fb8",
            "btn_shadow": "0 3px 0 #1c5fb8, 0 6px 10px rgba(0,0,0,0.4)",
            "btn_hover": "0 1px 0 #1c5fb8, 0 2px 4px rgba(0,0,0,0.4)", "btn_move": "translateY(2px)",
            "inset_bg": "#d9dde3", "inset": "inset 0 2px 5px rgba(0,0,0,0.35)",
            "input_border": "1px solid #9aa1ab",
        },
        "extra": ".stApp > header, [data-testid='stHeader'] * { color: #e8ebf0 !important; }"
                 ".stApp .page-title { color: #e8ebf0; }",
    },
    # ------------------------------------------------------------ 11
    "Bento Grid": {
        "icon": "🍱",
        "tagline": "Apple-style tiles of different colours packed in a tidy grid.",
        "search": ["bento grid UI", "bento box layout design", "apple style tiles", "bento grid CSS"],
        "tip": "display: grid;\ngrid-template-columns: repeat(4, 1fr);\ngap: 16px;\n"
               "border-radius: 28px;   /* every tile = big rounded box */",
        "vars": {
            "page_bg": "#f2f2f7", "side_bg": "#ffffff", "card_bg": "#ffffff",
            "card_border": "1px solid #e8e8ee", "radius": "28px",
            "text": "#1d1d1f", "muted": "#6e6e73", "accent": "#0071e3", "accent2": "#5ac8fa",
            "btn_bg": "#1d1d1f", "btn_text": "#ffffff", "btn_radius": "999px",
            "btn_hover": "0 6px 16px rgba(0,0,0,0.25)", "btn_move": "translateY(-1px)",
            "inset_bg": "#ececf1", "input_border": "1px solid #dcdce3",
        },
        "extra": ".stat:nth-child(1) { background: #dbeafe; } .stat:nth-child(2) { background: #fde68a; }"
                 ".stat:nth-child(3) { background: #fbcfe8; } .stat:nth-child(4) { background: #bbf7d0; }",
    },
    # ------------------------------------------------------------ 12
    "Candy Pastel": {
        "icon": "🍬",
        "tagline": "Cute pastel colours, dashed borders and chunky pill buttons.",
        "search": ["kawaii UI", "pastel web design", "cute website design", "playful UI design"],
        "tip": "border: 3px dashed #f8bbd0;\nborder-radius: 28px;\nbox-shadow: 0 6px 0 #f8bbd0;   /* chunky bottom edge */",
        "vars": {
            "page_bg": "linear-gradient(160deg, #e0f7fa, #f3e5f5 60%, #ffe0ec)",
            "side_bg": "#fff0f6", "card_bg": "#ffffff",
            "card_border": "3px dashed #f8bbd0", "card_shadow": "0 6px 0 #f8bbd0",
            "radius": "28px", "text": "#6a4c93", "muted": "#9b83b8",
            "accent": "#ff6f91", "accent2": "#845ec2", "font": "'Nunito', sans-serif",
            "btn_bg": "#ffc2d4", "btn_text": "#6a4c93", "btn_border": "3px solid #ffffff",
            "btn_shadow": "0 4px 0 #ff9ebb", "btn_hover": "0 1px 0 #ff9ebb",
            "btn_move": "translateY(3px)", "btn_radius": "999px",
            "inset_bg": "#fdf1f6", "input_border": "2px dashed #f8bbd0",
        },
    },
    # ------------------------------------------------------------ 13
    "Terminal Hacker": {
        "icon": "👨‍💻",
        "tagline": "Black screen, green monospace text - like a hacker's command line.",
        "search": ["terminal UI design", "hacker theme website", "monospace retro CRT CSS", "matrix green UI"],
        "tip": "background: #000;\ncolor: #00ff41;\nfont-family: 'Courier New', monospace;\n"
               "border: 1px solid #00ff41;",
        "vars": {
            "page_bg": "#000000", "side_bg": "#020a02", "card_bg": "#030c03",
            "card_border": "1px solid #00ff41", "card_shadow": "0 0 10px rgba(0,255,65,0.3)",
            "radius": "0px", "text": "#00ff41", "muted": "#1fa83a",
            "accent": "#00ff41", "accent2": "#b6ff00",
            "font": "'Share Tech Mono', 'Courier New', monospace",
            "btn_bg": "transparent", "btn_text": "#00ff41", "btn_border": "1px solid #00ff41",
            "btn_hover": "0 0 18px rgba(0,255,65,0.9)", "btn_radius": "0px",
            "inset_bg": "#000000", "input_border": "1px solid #00ff41",
        },
        "extra": "@keyframes blink { 50% { opacity: 0; } }"
                 ".stApp .hero h1::after { content: '_'; animation: blink 1s steps(1) infinite; }",
    },
    # ------------------------------------------------------------ 14
    "Vaporwave": {
        "icon": "🌴",
        "tagline": "80s synthwave sunset: purple sky, hot pink and cyan glow.",
        "search": ["vaporwave aesthetic", "synthwave UI", "retrowave website design", "80s neon CSS"],
        "tip": "background: linear-gradient(180deg, #1a0536, #3b0a6b, #ff3cac);\n"
               "border: 2px solid #ff71ce;\nbox-shadow: 0 0 20px #ff71ce88;",
        "vars": {
            "page_bg": "linear-gradient(180deg, #1a0536 0%, #3b0a6b 55%, #ff3cac 130%)",
            "side_bg": "rgba(20,0,40,0.85)", "card_bg": "rgba(20,0,40,0.55)",
            "card_border": "2px solid #ff71ce",
            "card_shadow": "0 0 20px rgba(255,113,206,0.5), inset 0 0 12px rgba(1,205,254,0.25)",
            "radius": "6px", "text": "#fdf6ff", "muted": "#d6b8ff",
            "accent": "#01cdfe", "accent2": "#ff71ce", "font": "'Trebuchet MS', sans-serif",
            "btn_bg": "linear-gradient(90deg, #ff71ce, #b967ff)", "btn_text": "#ffffff",
            "btn_border": "2px solid #01cdfe", "btn_shadow": "0 0 12px rgba(1,205,254,0.6)",
            "btn_hover": "0 0 26px rgba(1,205,254,1)", "btn_radius": "6px",
            "inset_bg": "rgba(255,255,255,0.08)", "input_border": "2px solid #b967ff",
        },
        "extra": ".stApp .hero h1 { text-shadow: 3px 3px 0 #01cdfe; letter-spacing: 3px; text-transform: uppercase; }",
    },
    # ------------------------------------------------------------ 15
    "Editorial Paper": {
        "icon": "📰",
        "tagline": "Newspaper / magazine feel: serif fonts, warm paper, thin black rules.",
        "search": ["editorial web design", "newspaper style website", "serif typography UI", "magazine layout CSS"],
        "tip": "font-family: Georgia, serif;\nbackground: #fffdf7;\nborder-top: 4px double #222;   /* newspaper rule */",
        "vars": {
            "page_bg": "#f5f0e6", "side_bg": "#ece5d6", "card_bg": "#fffdf7",
            "card_border": "1px solid #2b2b2b", "card_shadow": "4px 4px 0 rgba(0,0,0,0.15)",
            "radius": "2px", "text": "#222222", "muted": "#6b6253",
            "accent": "#8b1e1e", "accent2": "#c19a6b",
            "font": "Georgia, 'Times New Roman', serif", "head_font": "'Playfair Display', Georgia, serif",
            "btn_bg": "transparent", "btn_text": "#222222", "btn_border": "1px solid #222222",
            "btn_hover": "inset 0 -4px 0 #8b1e1e", "btn_radius": "2px",
            "inset_bg": "#f1ebdc", "input_border": "1px solid #2b2b2b",
        },
        "extra": ".stApp .hero { border-top: 5px double #222; border-bottom: 5px double #222; }",
    },
    # ------------------------------------------------------------ 16
    "Holographic Iridescent": {
        "icon": "🌈",
        "tagline": "Oil-slick iridescent surface that slowly cycles through every hue.",
        "search": ["holographic CSS", "iridescent web design", "conic gradient shimmer", "hue-rotate animation"],
        "tip": "background: conic-gradient(from 0deg, #ff0080, #ff8c00, #ffd700, #00ff7f, #00bfff, #8a2be2, #ff0080);\n"
               "animation: hueShift 12s linear infinite;\n@keyframes hueShift { to { filter: hue-rotate(360deg); } }",
        "vars": {
            "page_bg": "#08080f", "side_bg": "rgba(15,15,25,0.85)", "card_bg": "rgba(20,20,35,0.55)",
            "card_border": "1px solid rgba(255,255,255,0.18)",
            "card_shadow": "0 8px 32px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.15)",
            "blur": "blur(16px)",
            "radius": "22px", "text": "#ffffff", "muted": "#a8a8c8",
            "accent": "#ff00ff", "accent2": "#00ffff",
            "font": "'Inter', sans-serif",
            "btn_bg": "conic-gradient(from 0deg, #ff0080, #ff8c00, #ffd700, #00ff7f, #00bfff, #8a2be2, #ff0080)",
            "btn_text": "#ffffff", "btn_border": "1px solid rgba(255,255,255,0.4)",
            "btn_hover": "0 6px 24px rgba(255,0,255,0.5)", "btn_move": "translateY(-2px)",
            "btn_radius": "14px", "inset_bg": "rgba(255,255,255,0.06)",
            "input_border": "1px solid rgba(255,255,255,0.2)",
        },
        "extra": "@keyframes hueShift { to { filter: hue-rotate(360deg); } }"
                 ".stApp .hero, .stApp .stat, .stButton > button { animation: hueShift 14s linear infinite; }"
                 ".stApp .hero h1 { background: linear-gradient(90deg, #ff0080, #ff8c00, #ffd700, #00ff7f, #00bfff, #8a2be2, #ff0080); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; animation: hueShift 14s linear infinite; }",
    },
    # ------------------------------------------------------------ 17
    "Sticky Note Corkboard": {
        "icon": "📌",
        "tagline": "Yellow paper notes pinned to a corkboard with tape and slight rotation.",
        "search": ["sticky note UI", "post-it design CSS", "corkboard web design", "paper note card style"],
        "tip": "background: #fff9c4;\ntransform: rotate(-2deg);\nbox-shadow: 3px 3px 8px rgba(0,0,0,0.3);   /* paper drop shadow */",
        "vars": {
            "page_bg": "#b8895c repeating-linear-gradient(45deg, transparent, transparent 20px, rgba(0,0,0,0.04) 20px, rgba(0,0,0,0.04) 22px)",
            "side_bg": "#a67a4f", "card_bg": "#fff9c4",
            "card_border": "1px solid #e6d97a",
            "card_shadow": "3px 4px 10px rgba(0,0,0,0.35)",
            "radius": "2px", "text": "#3d3d1d", "muted": "#7a7a4a",
            "accent": "#d32f2f", "accent2": "#1565c0",
            "font": "'Caveat', cursive", "head_font": "'Caveat', cursive",
            "btn_bg": "#fff59d", "btn_text": "#3d3d1d", "btn_border": "1px solid #c0a040",
            "btn_hover": "2px 2px 5px rgba(0,0,0,0.3)", "btn_move": "translateY(-1px)",
            "btn_radius": "2px", "inset_bg": "#fff9c4", "input_border": "1px solid #c0a040",
        },
        "extra": ".stApp .card { transform: rotate(-1.2deg); }"
                 ".stApp .card:nth-of-type(even) { transform: rotate(1.5deg); }"
                 ".stApp .card:nth-of-type(3n) { transform: rotate(-0.5deg); }"
                 ".stApp .hero h1 { font-size: 3rem; }"
                 ".stApp .hero::before, .stApp .hero::after { content: ''; position: absolute; width: 60px; height: 18px; background: rgba(255,255,255,0.55); top: -8px; }"
                 ".stApp .hero::before { left: 30%; transform: rotate(-3deg); } .stApp .hero::after { right: 30%; transform: rotate(3deg); }"
                 ".stApp .hero { position: relative; overflow: visible; }",
    },
    # ------------------------------------------------------------ 18
    "8-bit Pixel": {
        "icon": "👾",
        "tagline": "Retro game UI - blocky pixel font, chunky stepped shadows, no anti-aliasing.",
        "search": ["8-bit UI design", "pixel art web design", "Press Start 2P font", "retro game CSS"],
        "tip": "font-family: 'Press Start 2P', monospace;\nbox-shadow: 4px 4px 0 #000, 8px 8px 0 #555;   /* stepped chunky shadow */\n"
               "border: 3px solid #000; image-rendering: pixelated;",
        "vars": {
            "page_bg": "#1a1c2c", "side_bg": "#29366f", "card_bg": "#41a6f6",
            "card_border": "4px solid #1a1c2c",
            "card_shadow": "6px 6px 0 #1a1c2c, 12px 12px 0 #b13e53",
            "radius": "0px", "text": "#1a1c2c", "muted": "#29366f",
            "accent": "#ffcd75", "accent2": "#94b0c2",
            "font": "'Press Start 2P', monospace", "head_font": "'Press Start 2P', monospace",
            "btn_bg": "#38b764", "btn_text": "#1a1c2c", "btn_border": "3px solid #1a1c2c",
            "btn_shadow": "4px 4px 0 #1a1c2c",
            "btn_hover": "0 0 0 #1a1c2c", "btn_move": "translate(4px, 4px)", "btn_radius": "0px",
            "inset_bg": "#29366f", "input_border": "3px solid #1a1c2c",
        },
        "extra": ".stApp .hero h1 { letter-spacing: 2px; font-size: 1.4rem; }"
                 ".stApp h3 { font-size: 0.85rem; letter-spacing: 1px; }"
                 ".stApp p, .stApp li { font-size: 0.65rem; line-height: 1.8; }"
                 ".stApp .stat .num { font-size: 1.1rem; }"
                 ".stApp .stat .label { font-size: 0.55rem; }",
    },
    # ------------------------------------------------------------ 19
    "Hand-drawn Sketchy": {
        "icon": "✏️",
        "tagline": "Wobbly hand-drawn borders, marker headlines and a handwriting font.",
        "search": ["sketchy UI design", "hand drawn CSS borders", "rough notation style", "Roughjs hand drawn"],
        "tip": "font-family: 'Caveat', cursive;\nborder: 2px solid #2d2d2d;\nborder-radius: 255px 15px 225px 15px / 15px 225px 15px 255px;   /* wobbly hand-drawn corners */",
        "vars": {
            "page_bg": "#fdfbf7", "side_bg": "#f5f0e6", "card_bg": "#ffffff",
            "card_border": "2px solid #2d2d2d",
            "card_shadow": "3px 3px 0 rgba(45,45,45,0.2)",
            "radius": "255px 15px 225px 15px / 15px 225px 15px 255px",
            "text": "#2d2d2d", "muted": "#7a7a7a",
            "accent": "#e63946", "accent2": "#1d3557",
            "font": "'Caveat', cursive", "head_font": "'Permanent Marker', cursive",
            "btn_bg": "#ffe66d", "btn_text": "#2d2d2d", "btn_border": "2px solid #2d2d2d",
            "btn_shadow": "2px 2px 0 #2d2d2d",
            "btn_hover": "0 0 0 #2d2d2d", "btn_move": "translate(2px, 2px)",
            "btn_radius": "255px 15px 225px 15px / 15px 225px 15px 255px",
            "inset_bg": "#fdfbf7", "input_border": "2px solid #2d2d2d",
        },
        "extra": ".stApp .hero h1 { font-size: 3.4rem; }"
                 ".stApp h3 { font-size: 1.6rem; }"
                 ".stApp p, .stApp li { font-size: 1.25rem; line-height: 1.4; }"
                 ".stApp .stat .num { font-size: 2.4rem; }"
                 ".stApp .hero { position: relative; }"
                 ".stApp .hero h3 { display: inline-block; background: linear-gradient(transparent 60%, #ffe66d 60%); padding: 0 6px; }",
    },
    # ------------------------------------------------------------ 20
    "Blueprint Wireframe": {
        "icon": "📐",
        "tagline": "Engineering blueprint - blue grid background, thin white outlines, NO fills.",
        "search": ["blueprint design CSS", "wireframe UI style", "grid background blueprint", "engineering blueprint web"],
        "tip": "background:\n  linear-gradient(rgba(255,255,255,0.15) 1px, transparent 1px),\n"
               "  linear-gradient(90deg, rgba(255,255,255,0.15) 1px, transparent 1px),\n  #0d3a5c;\nbackground-size: 20px 20px;\nborder: 1px solid #ffffff;   /* thin outline, NO fill */",
        "vars": {
            "page_bg": "linear-gradient(rgba(255,255,255,0.12) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.12) 1px, transparent 1px), #0d3a5c",
            "side_bg": "#0a2e4a", "card_bg": "transparent",
            "card_border": "1px solid rgba(255,255,255,0.85)",
            "card_shadow": "none",
            "radius": "0px", "text": "#ffffff", "muted": "#8eb4d4",
            "accent": "#ffeb3b", "accent2": "#4fc3f7",
            "font": "'Space Mono', 'Courier New', monospace",
            "btn_bg": "transparent", "btn_text": "#ffffff", "btn_border": "1px solid #ffffff",
            "btn_hover": "inset 0 0 0 1px #ffeb3b, 0 0 0 1px #ffeb3b",
            "btn_radius": "0px", "inset_bg": "transparent", "input_border": "1px dashed rgba(255,255,255,0.7)",
        },
        "extra": ".stApp { background-size: 24px 24px; }"
                 ".stApp .hero h1 { letter-spacing: 4px; text-transform: uppercase; font-size: 1.8rem; }"
                 ".stApp h3 { text-transform: uppercase; letter-spacing: 2px; font-size: 1rem; }"
                 ".stApp p, .stApp li { font-size: 0.9rem; }"
                 ".stApp .stat .num { font-family: 'Space Mono', monospace; }",
    },
    # ------------------------------------------------------------ 21
    "Letterpress Debossed": {
        "icon": "🗞️",
        "tagline": "Text appears pressed INTO cream paper - debossed, ink-stamped look.",
        "search": ["letterpress CSS", "debossed text effect", "inset text shadow", "pressed paper design"],
        "tip": "background: #f5ecd9;\ncolor: #2a1f10;\ntext-shadow: 0 1px 0 rgba(255,255,255,0.6), 0 -1px 1px rgba(0,0,0,0.4);   /* pressed-in look */",
        "vars": {
            "page_bg": "#f5ecd9", "side_bg": "#ede0c0", "card_bg": "#f5ecd9",
            "card_border": "1px solid #d4c4a0",
            "card_shadow": "inset 0 1px 0 rgba(255,255,255,0.5), inset 0 -2px 4px rgba(0,0,0,0.1), 0 2px 8px rgba(0,0,0,0.05)",
            "radius": "4px", "text": "#2a1f10", "muted": "#7a6845",
            "accent": "#8b2a2a", "accent2": "#3d5a3d",
            "font": "Georgia, serif", "head_font": "'Playfair Display', Georgia, serif",
            "btn_bg": "#2a1f10", "btn_text": "#f5ecd9", "btn_border": "1px solid #1a1208",
            "btn_shadow": "inset 0 1px 0 rgba(255,255,255,0.15), 0 2px 4px rgba(0,0,0,0.3)",
            "btn_hover": "inset 0 2px 6px rgba(0,0,0,0.5)", "btn_move": "translateY(1px)",
            "btn_radius": "4px", "inset_bg": "#ede0c0", "inset": "inset 0 2px 4px rgba(0,0,0,0.2)",
            "input_border": "1px solid #d4c4a0",
        },
        "extra": ".stApp h1, .stApp h2, .stApp h3 { text-shadow: 0 1px 0 rgba(255,255,255,0.7), 0 -1px 1px rgba(0,0,0,0.45); }"
                 ".stApp .stat .num { text-shadow: 0 1px 0 rgba(255,255,255,0.6), 0 -1px 2px rgba(0,0,0,0.55); }"
                 ".stApp .hero h1 { letter-spacing: 2px; font-weight: 700; }",
    },
    # ------------------------------------------------------------ 22
    "Raw HTML 1995": {
        "icon": "🌐",
        "tagline": "Pure 1995 web - Times New Roman, blue underlined links, grey background, no styling.",
        "search": ["old web 1995 design", "retro HTML website", "Web 1.0 aesthetic", "unstyled HTML look"],
        "tip": "font-family: 'Times New Roman', serif;\nbackground: #c0c0c0;\ncolor: #000000;\na { color: #0000ee; text-decoration: underline; }   /* classic blue link */",
        "vars": {
            "page_bg": "#c0c0c0", "side_bg": "#c0c0c0", "card_bg": "#ffffff",
            "card_border": "1px solid #808080",
            "card_shadow": "none",
            "radius": "0px", "text": "#000000", "muted": "#404040",
            "accent": "#0000ee", "accent2": "#800080",
            "font": "'Times New Roman', Times, serif",
            "btn_bg": "#c0c0c0", "btn_text": "#000000", "btn_border": "1px outset #ffffff",
            "btn_shadow": "1px 1px 0 #808080",
            "btn_hover": "1px 1px 0 #808080 inset", "btn_radius": "0px",
            "inset_bg": "#ffffff", "input_border": "2px inset #808080",
        },
        "extra": ".stApp .hero h1 { font-size: 2rem; font-weight: bold; text-align: center; }"
                 ".stApp .hero { border: 1px solid #808080; background: #ffffff; }"
                 ".stApp .stButton > button { color: #0000ee; text-decoration: underline; font-family: 'Times New Roman', serif; font-weight: normal; font-size: 1rem; }"
                 ".stApp .stButton > button:hover { color: #0000ee; text-decoration: underline; }"
                 ".stApp h3 { font-size: 1.2rem; }",
    },
    # ------------------------------------------------------------ 23
    "Gradient Border Mask": {
        "icon": "🌈",
        "tagline": "Rainbow gradient borders around solid dark cards - uses the padding-box/border-box trick.",
        "search": ["gradient border CSS", "rainbow border design", "border-image gradient", "padding-box border-box trick"],
        "tip": "border: 3px solid transparent;\nbackground: linear-gradient(#1a1a2e, #1a1a2e) padding-box,\n"
               "            linear-gradient(135deg, #ff0080, #ff8c00, #ffd700, #00ff7f, #00bfff, #8a2be2) border-box;   /* gradient border trick */",
        "vars": {
            "page_bg": "#0d0d1a", "side_bg": "#14141f", "card_bg": "#1a1a2e",
            "card_border": "2px solid transparent",
            "card_shadow": "0 4px 20px rgba(0,0,0,0.4)",
            "radius": "14px", "text": "#f0f0f5", "muted": "#8a8aa0",
            "accent": "#ff0080", "accent2": "#00bfff",
            "font": "'Inter', sans-serif",
            "btn_bg": "linear-gradient(135deg, #ff0080, #ff8c00, #ffd700, #00ff7f, #00bfff, #8a2be2)",
            "btn_text": "#ffffff", "btn_border": "none",
            "btn_hover": "0 6px 24px rgba(255,0,128,0.5)", "btn_move": "translateY(-2px)",
            "btn_radius": "10px", "inset_bg": "#14141f", "input_border": "2px solid transparent",
        },
        "extra": ".stApp .card, .stApp .stat, .stApp .hero {"
                 "  background: linear-gradient(#1a1a2e, #1a1a2e) padding-box, linear-gradient(135deg, #ff0080, #ff8c00, #ffd700, #00ff7f, #00bfff, #8a2be2) border-box;"
                 "  border: 2px solid transparent;"
                 "}"
                 ".stApp .hero h1 { background: linear-gradient(135deg, #ff0080, #ff8c00, #ffd700, #00ff7f, #00bfff, #8a2be2); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; }"
                 "[data-testid='stTextInputRootElement'] { background: linear-gradient(#14141f, #14141f) padding-box, linear-gradient(135deg, #ff0080, #00bfff, #8a2be2) border-box !important; border: 2px solid transparent !important; }",
    },
    # ------------------------------------------------------------ 24
    "Halftone Comic": {
        "icon": "💥",
        "tagline": "Comic-book halftone dot overlay, thick black outlines and Bangers display font.",
        "search": ["halftone CSS", "comic book design", "Bangers font comic", "halftone dot pattern"],
        "tip": "background: radial-gradient(circle, #000 20%, transparent 21%) 0 0 / 8px 8px;   /* halftone dots */\n"
               "border: 4px solid #000;\nfont-family: 'Bangers', cursive;",
        "vars": {
            "page_bg": "#fef3c7", "side_bg": "#fde68a", "card_bg": "#ffffff",
            "card_border": "4px solid #000000",
            "card_shadow": "6px 6px 0 #000000",
            "radius": "8px", "text": "#1a1a1a", "muted": "#6b7280",
            "accent": "#dc2626", "accent2": "#2563eb",
            "font": "'Bangers', cursive", "head_font": "'Bangers', cursive",
            "btn_bg": "#fbbf24", "btn_text": "#1a1a1a", "btn_border": "3px solid #000000",
            "btn_shadow": "4px 4px 0 #000000",
            "btn_hover": "0 0 0 #000000", "btn_move": "translate(4px, 4px)", "btn_radius": "6px",
            "inset_bg": "#fef3c7", "input_border": "3px solid #000000",
        },
        "extra": ".stApp .card, .stApp .stat, .stApp .hero { position: relative; overflow: hidden; }"
                 ".stApp .card::after, .stApp .stat::after { content: ''; position: absolute; inset: 0; background: radial-gradient(circle, rgba(0,0,0,0.18) 20%, transparent 21%); background-size: 8px 8px; pointer-events: none; opacity: 0.6; }"
                 ".stApp .hero h1 { font-size: 3rem; letter-spacing: 2px; -webkit-text-stroke: 2px #000; text-shadow: 4px 4px 0 #dc2626; }"
                 ".stApp h3 { letter-spacing: 1px; font-size: 1.6rem; }"
                 ".stApp p, .stApp li { font-family: 'Comic Sans MS', cursive; font-size: 1rem; }",
    },
    # ------------------------------------------------------------ 25
    "CRT Monitor": {
        "icon": "🖥️",
        "tagline": "Old CRT monitor - scanlines, screen curvature and RGB-split ghost text.",
        "search": ["CRT effect CSS", "scanline overlay", "retro monitor design", "RGB split text shadow"],
        "tip": "background: #0a0a0a;\nbackground-image: repeating-linear-gradient(0deg, rgba(0,0,0,0.3) 0px, rgba(0,0,0,0.3) 1px, transparent 1px, transparent 3px);   /* scanlines */\n"
               "text-shadow: 2px 0 #ff0000, -2px 0 #00ffff;   /* RGB split */",
        "vars": {
            "page_bg": "#0a0a0a", "side_bg": "#0d0d0d", "card_bg": "#101010",
            "card_border": "1px solid #1a3a1a",
            "card_shadow": "0 0 30px rgba(0,255,65,0.15), inset 0 0 60px rgba(0,255,65,0.05)",
            "radius": "20px", "text": "#33ff33", "muted": "#1a8a1a",
            "accent": "#33ff33", "accent2": "#ffff33",
            "font": "'VT323', 'Courier New', monospace", "head_font": "'VT323', monospace",
            "btn_bg": "transparent", "btn_text": "#33ff33", "btn_border": "1px solid #33ff33",
            "btn_hover": "0 0 16px rgba(51,255,51,0.7)", "btn_radius": "4px",
            "inset_bg": "#050505", "input_border": "1px solid #1a3a1a",
        },
        "extra": ".stApp { background-image: repeating-linear-gradient(0deg, rgba(0,0,0,0.4) 0px, rgba(0,0,0,0.4) 1px, transparent 1px, transparent 3px); }"
                 ".stApp .hero h1, .stApp h3, .stApp .stat .num { text-shadow: 2px 0 rgba(255,0,0,0.7), -2px 0 rgba(0,255,255,0.7); }"
                 ".stApp .hero, .stApp .card, .stApp .stat { border-radius: 30px / 20px; }"
                 ".stApp .hero h1 { font-size: 2.4rem; letter-spacing: 2px; }"
                 "@keyframes flicker { 0%, 100% { opacity: 1; } 50% { opacity: 0.97; } 92% { opacity: 0.93; } }"
                 ".stApp { animation: flicker 0.15s infinite; }",
    },
    # ------------------------------------------------------------ 26
    "Isometric 2.5D": {
        "icon": "📦",
        "tagline": "Cards tilted in 3D space - isometric 2.5D look with perspective transform.",
        "search": ["isometric CSS design", "2.5D UI cards", "3D transform cards", "perspective tilt UI"],
        "tip": "transform: perspective(1200px) rotateX(8deg) rotateY(-8deg);\nbox-shadow: 12px 12px 30px rgba(0,0,0,0.3);",
        "vars": {
            "page_bg": "linear-gradient(135deg, #e0e7ff 0%, #f0f9ff 100%)",
            "side_bg": "#ffffff", "card_bg": "#ffffff",
            "card_border": "1px solid #e0e7ff",
            "card_shadow": "12px 12px 30px rgba(99,102,241,0.2), 0 4px 8px rgba(0,0,0,0.05)",
            "radius": "16px", "text": "#1e293b", "muted": "#64748b",
            "accent": "#6366f1", "accent2": "#ec4899",
            "font": "'Inter', sans-serif",
            "btn_bg": "#6366f1", "btn_text": "#ffffff", "btn_radius": "10px",
            "btn_hover": "0 8px 20px rgba(99,102,241,0.4)", "btn_move": "translateY(-2px)",
            "inset_bg": "#f8fafc", "input_border": "1px solid #e0e7ff",
        },
        "extra": ".stApp { perspective: 1500px; }"
                 ".stApp .card { transform: perspective(1200px) rotateX(6deg) rotateY(-6deg); transform-style: preserve-3d; transition: transform 0.3s ease; }"
                 ".stApp .card:hover { transform: perspective(1200px) rotateX(0deg) rotateY(0deg); }"
                 ".stApp .stat { transform: perspective(1000px) rotateX(10deg) rotateY(-10deg); transition: transform 0.3s ease; }"
                 ".stApp .stat:hover { transform: perspective(1000px) rotateX(0deg) rotateY(0deg); }"
                 ".stApp .hero { transform: perspective(1200px) rotateX(4deg); }",
    },
    # ------------------------------------------------------------ 27
    "Neon Outline Hollow": {
        "icon": "🌀",
        "tagline": "Pure line-art - transparent fills, ONLY glowing outlines. Like neon signs.",
        "search": ["neon outline CSS", "hollow line art UI", "glowing wireframe design", "neon sign effect"],
        "tip": "background: transparent;\nborder: 1px solid #ff00ff;\nbox-shadow: 0 0 8px #ff00ff, inset 0 0 8px #ff00ff44;   /* outline glow, NO fill */",
        "vars": {
            "page_bg": "#050008", "side_bg": "transparent", "card_bg": "transparent",
            "card_border": "1px solid #ff00ff",
            "card_shadow": "0 0 10px rgba(255,0,255,0.6), inset 0 0 10px rgba(255,0,255,0.15)",
            "radius": "4px", "text": "#ff00ff", "muted": "#a040a0",
            "accent": "#00ffff", "accent2": "#ffff00",
            "font": "'Share Tech Mono', monospace", "head_font": "'Orbitron', sans-serif",
            "btn_bg": "transparent", "btn_text": "#00ffff", "btn_border": "1px solid #00ffff",
            "btn_shadow": "0 0 8px rgba(0,255,255,0.6)",
            "btn_hover": "0 0 16px rgba(0,255,255,1), inset 0 0 12px rgba(0,255,255,0.3)",
            "btn_radius": "4px", "inset_bg": "transparent", "input_border": "1px solid #ff00ff",
        },
        "extra": ".stApp .hero h1 { text-shadow: 0 0 8px #ff00ff, 0 0 16px #ff00ff, 0 0 24px #ff00ff; letter-spacing: 3px; }"
                 ".stApp .stat, .stApp .card { backdrop-filter: none; }"
                 ".stApp .stat .num { color: #00ffff; text-shadow: 0 0 8px #00ffff, 0 0 16px #00ffff; }"
                 ".stApp .bar-fill { background: transparent; box-shadow: 0 0 8px #00ffff; border: 1px solid #00ffff; }",
    },
    # ------------------------------------------------------------ 28
    "Patchwork Stitched": {
        "icon": "🧵",
        "tagline": "Quilted fabric patches with visible stitching - warm, tactile, handcrafted.",
        "search": ["stitched border CSS", "patchwork fabric UI", "quilt design web", "sewn stitching effect"],
        "tip": "border: 3px dashed #5a3a1a;\nbox-shadow: 0 4px 0 #d4a574, inset 0 0 0 6px #f4d8a8;   /* layered stitching look */",
        "vars": {
            "page_bg": "#d4a574", "side_bg": "#c89868", "card_bg": "#f4d8a8",
            "card_border": "3px dashed #5a3a1a",
            "card_shadow": "0 4px 0 #b8895c, inset 0 0 0 6px #f4d8a8, inset 0 0 0 9px #5a3a1a",
            "radius": "8px", "text": "#3d2410", "muted": "#7a4a2a",
            "accent": "#c0392b", "accent2": "#5d8a3a",
            "font": "'Inter', sans-serif",
            "btn_bg": "#c0392b", "btn_text": "#f4d8a8", "btn_border": "2px dashed #f4d8a8",
            "btn_shadow": "0 3px 0 #7a1f15",
            "btn_hover": "0 1px 0 #7a1f15", "btn_move": "translateY(2px)", "btn_radius": "6px",
            "inset_bg": "#e8c890", "inset": "inset 0 0 0 4px #f4d8a8",
            "input_border": "2px dashed #5a3a1a",
        },
        "extra": ".stApp .stat:nth-child(1) { background: #f4d8a8; } .stApp .stat:nth-child(2) { background: #e8b4a0; }"
                 ".stApp .stat:nth-child(3) { background: #c8d8a0; } .stApp .stat:nth-child(4) { background: #d8c0d8; }"
                 ".stApp .hero h3 { font-family: 'Caveat', cursive; }",
    },
    # ------------------------------------------------------------ 29
    "Polaroid Photo": {
        "icon": "📷",
        "tagline": "Thick white frame, bottom-heavy, slight rotation - like a stack of polaroid photos.",
        "search": ["polaroid CSS design", "photo frame UI", "polaroid card style", "instant camera web design"],
        "tip": "background: #ffffff;\npadding: 12px 12px 50px 12px;   /* thick bottom border = polaroid look */\n"
               "transform: rotate(-2deg);\nbox-shadow: 4px 6px 14px rgba(0,0,0,0.25);",
        "vars": {
            "page_bg": "#2a2a2a", "side_bg": "#1f1f1f", "card_bg": "#ffffff",
            "card_border": "none",
            "card_shadow": "4px 6px 14px rgba(0,0,0,0.35)",
            "radius": "2px", "text": "#1a1a1a", "muted": "#7a7a7a",
            "accent": "#d32f2f", "accent2": "#1976d2",
            "font": "'Caveat', cursive", "head_font": "'Caveat', cursive",
            "btn_bg": "#ffffff", "btn_text": "#1a1a1a", "btn_border": "1px solid #cccccc",
            "btn_shadow": "2px 3px 8px rgba(0,0,0,0.3)",
            "btn_hover": "0 1px 3px rgba(0,0,0,0.3)", "btn_move": "translateY(1px)",
            "btn_radius": "2px", "inset_bg": "#f5f5f5", "input_border": "1px solid #cccccc",
        },
        "extra": ".stApp .card { padding: 18px 18px 50px 18px; transform: rotate(-1.5deg); }"
                 ".stApp .card:nth-of-type(even) { transform: rotate(1.8deg); }"
                 ".stApp .card:nth-of-type(3n) { transform: rotate(-0.8deg); }"
                 ".stApp .hero h1 { font-size: 2.6rem; }"
                 ".stApp .stat { padding: 14px 10px 36px 10px; transform: rotate(-2deg); }"
                 ".stApp .stat:nth-of-type(even) { transform: rotate(2deg); }"
                 ".stApp h3, .stApp .stat .label { font-family: 'Caveat', cursive; }"
                 ".stApp p, .stApp li { font-family: 'Caveat', cursive; font-size: 1.15rem; }",
    },
    # ------------------------------------------------------------ 30
    "Card Deck Stack": {
        "icon": "🃏",
        "tagline": "Each card has a visible stacked duplicate behind it - like a deck of playing cards.",
        "search": ["stacked card CSS", "card deck design", "playing card UI", "stacked paper effect"],
        "tip": "position: relative;\n/* the visible card */\n.card { background: #fff; }\n/* the duplicate behind, peeking out */\n"
               ".card::before { content: ''; position: absolute; top: 8px; left: 8px; right: -8px; bottom: -8px;"
               "  background: #f0f0f0; border: 1px solid #ccc; border-radius: inherit; z-index: -1; }",
        "vars": {
            "page_bg": "#0d4f2c", "side_bg": "#0a3d22", "card_bg": "#ffffff",
            "card_border": "1px solid #1a1a1a",
            "card_shadow": "0 2px 4px rgba(0,0,0,0.3)",
            "radius": "10px", "text": "#1a1a1a", "muted": "#6b6b6b",
            "accent": "#d32f2f", "accent2": "#1a1a1a",
            "font": "'Inter', sans-serif", "head_font": "'Playfair Display', serif",
            "btn_bg": "#ffffff", "btn_text": "#1a1a1a", "btn_border": "1px solid #1a1a1a",
            "btn_shadow": "2px 2px 0 #1a1a1a",
            "btn_hover": "0 0 0 #1a1a1a", "btn_move": "translate(2px, 2px)", "btn_radius": "6px",
            "inset_bg": "#f5f5f5", "input_border": "1px solid #1a1a1a",
        },
        "extra": ".stApp .card, .stApp .stat, .stApp .hero { position: relative; }"
                 ".stApp .card::before, .stApp .stat::before, .stApp .hero::before {"
                 "  content: ''; position: absolute; top: 8px; left: 8px; right: -8px; bottom: -8px;"
                 "  background: #f0f0f0; border: 1px solid #cccccc; border-radius: inherit; z-index: -1;"
                 "  box-shadow: 0 2px 4px rgba(0,0,0,0.15);"
                 "}"
                 ".stApp .hero h1 { font-family: 'Playfair Display', serif; letter-spacing: 1px; }",
    },
    # ------------------------------------------------------------ 31
    "Origami Folded Corner": {
        "icon": "📄",
        "tagline": "Clean paper cards with a folded triangular corner - origami/paper-fold effect.",
        "search": ["origami CSS design", "folded corner card", "paper fold effect CSS", "dog-eared card UI"],
        "tip": "/* folded corner using clip-path */\nclip-path: polygon(0 0, calc(100% - 30px) 0, 100% 30px, 100% 100%, 0 100%);\n"
               "/* the fold shadow triangle */\nbox-shadow: -3px 3px 6px rgba(0,0,0,0.1) inset;",
        "vars": {
            "page_bg": "#e8e4dc", "side_bg": "#d8d2c4", "card_bg": "#ffffff",
            "card_border": "1px solid #c4bdb0",
            "card_shadow": "0 4px 12px rgba(0,0,0,0.1)",
            "radius": "2px", "text": "#2a2a2a", "muted": "#7a7a7a",
            "accent": "#c0392b", "accent2": "#2c3e50",
            "font": "'Inter', sans-serif",
            "btn_bg": "#c0392b", "btn_text": "#ffffff", "btn_border": "none",
            "btn_hover": "0 4px 10px rgba(192,57,43,0.4)", "btn_move": "translateY(-1px)",
            "btn_radius": "2px", "inset_bg": "#f5f2ec", "input_border": "1px solid #c4bdb0",
        },
        "extra": ".stApp .card, .stApp .stat, .stApp .hero {"
                 "  clip-path: polygon(0 0, calc(100% - 28px) 0, 100% 28px, 100% 100%, 0 100%);"
                 "  position: relative;"
                 "}"
                 ".stApp .card::after, .stApp .stat::after, .stApp .hero::after {"
                 "  content: ''; position: absolute; top: 0; right: 0;"
                 "  width: 28px; height: 28px;"
                 "  background: linear-gradient(225deg, transparent 50%, #d4cec0 50%, #b8b0a0);"
                 "  box-shadow: -2px 2px 4px rgba(0,0,0,0.1);"
                 "}"
                 ".stApp .hero h1 { letter-spacing: 1px; }",
    },
    # ------------------------------------------------------------ 32
    "Blackletter Manuscript": {
        "icon": "📜",
        "tagline": "Medieval manuscript - blackletter font, vellum parchment, illuminated red initials.",
        "search": ["blackletter font CSS", "medieval manuscript design", "UnifrakturCook font", "illuminated manuscript UI"],
        "tip": "font-family: 'UnifrakturCook', serif;\nbackground: #f4e8d0;   /* vellum */\ncolor: #2a1a0a;\n"
               "/* illuminated drop cap */\nh1::first-letter { color: #c41e3a; font-size: 1.4em; }",
        "vars": {
            "page_bg": "#f4e8d0", "side_bg": "#e8dcc0", "card_bg": "#fbf2dc",
            "card_border": "2px double #8b6914",
            "card_shadow": "0 4px 12px rgba(139,105,20,0.2)",
            "radius": "4px", "text": "#2a1a0a", "muted": "#6b5020",
            "accent": "#c41e3a", "accent2": "#8b6914",
            "font": "'UnifrakturCook', serif", "head_font": "'UnifrakturCook', serif",
            "btn_bg": "transparent", "btn_text": "#c41e3a", "btn_border": "2px double #8b6914",
            "btn_hover": "inset 0 0 0 1px #c41e3a", "btn_radius": "2px",
            "inset_bg": "#e8dcc0", "input_border": "2px double #8b6914",
        },
        "extra": ".stApp .hero h1 { font-size: 3rem; }"
                 ".stApp .hero h1::first-letter { color: #c41e3a; font-size: 1.5em; }"
                 ".stApp h3 { font-size: 1.6rem; }"
                 ".stApp h3::first-letter { color: #c41e3a; font-size: 1.3em; }"
                 ".stApp p, .stApp li { font-family: Georgia, serif; font-size: 1.05rem; line-height: 1.7; }"
                 ".stApp .hero { border: 3px double #8b6914; }",
    },
    # ------------------------------------------------------------ 33
    "Brutalist Concrete": {
        "icon": "🏗️",
        "tagline": "Raw concrete brutalism - grey textures, harsh monospace, exposed structure.",
        "search": ["brutalist web design", "concrete texture CSS", "raw brutalism UI", "harsh architecture design"],
        "tip": "background: #9a9a9a;\nfont-family: 'Courier New', monospace;\nborder: 2px solid #1a1a1a;   /* harsh heavy border */\n"
               "box-shadow: 8px 8px 0 #1a1a1a;   /* hard, no blur, no softness */",
        "vars": {
            "page_bg": "#8a8a8a", "side_bg": "#6e6e6e", "card_bg": "#a8a8a8",
            "card_border": "2px solid #1a1a1a",
            "card_shadow": "8px 8px 0 #1a1a1a",
            "radius": "0px", "text": "#1a1a1a", "muted": "#3a3a3a",
            "accent": "#c41e3a", "accent2": "#1a1a1a",
            "font": "'Space Mono', 'Courier New', monospace",
            "btn_bg": "#1a1a1a", "btn_text": "#ffffff", "btn_border": "2px solid #1a1a1a",
            "btn_shadow": "4px 4px 0 #4a4a4a",
            "btn_hover": "0 0 0 #4a4a4a", "btn_move": "translate(4px, 4px)", "btn_radius": "0px",
            "inset_bg": "#7a7a7a", "input_border": "2px solid #1a1a1a",
        },
        "extra": ".stApp { background-image: radial-gradient(circle at 20% 30%, rgba(0,0,0,0.1) 0%, transparent 50%), radial-gradient(circle at 80% 70%, rgba(255,255,255,0.1) 0%, transparent 50%); }"
                 ".stApp .hero h1 { text-transform: uppercase; letter-spacing: 2px; font-size: 1.8rem; }"
                 ".stApp h3 { text-transform: uppercase; letter-spacing: 1px; font-size: 1rem; }"
                 ".stApp p, .stApp li { font-size: 0.9rem; }",
    },
    # ------------------------------------------------------------ 34
    "Sticker Bombed": {
        "icon": "🏷️",
        "tagline": "Overlapping sticker labels with random rotations and washi-tape strips on top.",
        "search": ["sticker design CSS", "washi tape UI", "sticker bomb aesthetic", "scrapbook web design"],
        "tip": "transform: rotate(-3deg);\nborder: 2px solid #1a1a1a;\nbox-shadow: 3px 3px 0 rgba(0,0,0,0.2);\n"
               "/* washi tape on top via ::before */",
        "vars": {
            "page_bg": "#fef3e2", "side_bg": "#fde8c8", "card_bg": "#ffffff",
            "card_border": "2px solid #1a1a1a",
            "card_shadow": "3px 4px 8px rgba(0,0,0,0.2)",
            "radius": "4px", "text": "#1a1a1a", "muted": "#6b6b6b",
            "accent": "#ec4899", "accent2": "#10b981",
            "font": "'Permanent Marker', cursive", "head_font": "'Permanent Marker', cursive",
            "btn_bg": "#fef08a", "btn_text": "#1a1a1a", "btn_border": "2px solid #1a1a1a",
            "btn_shadow": "3px 3px 0 #1a1a1a",
            "btn_hover": "0 0 0 #1a1a1a", "btn_move": "translate(3px, 3px)", "btn_radius": "4px",
            "inset_bg": "#fffbeb", "input_border": "2px solid #1a1a1a",
        },
        "extra": ".stApp .card { transform: rotate(-1.5deg); position: relative; }"
                 ".stApp .card:nth-of-type(even) { transform: rotate(2deg); }"
                 ".stApp .card:nth-of-type(3n) { transform: rotate(-0.5deg); }"
                 ".stApp .card::before { content: ''; position: absolute; top: -10px; left: 20%; width: 60px; height: 20px; background: rgba(236,72,153,0.6); transform: rotate(-4deg); z-index: 1; }"
                 ".stApp .card:nth-of-type(even)::before { background: rgba(16,185,129,0.6); left: 60%; transform: rotate(5deg); }"
                 ".stApp .hero h1 { font-size: 2.8rem; }"
                 ".stApp p, .stApp li { font-family: 'Caveat', cursive; font-size: 1.2rem; }",
    },
    # ------------------------------------------------------------ 35

    
    # ------------------------------------------------------------ 36
    "Torn Paper Edge": {
        "icon": "📰",
        "tagline": "Cards look ripped from paper - rough torn edges using a many-point clip-path polygon.",
        "search": ["torn paper CSS", "ripped edge effect", "torn paper clip-path", "rough paper edge design"],
        "tip": "/* torn edge using a many-point polygon */\nclip-path: polygon(0% 5%, 3% 0%, 8% 4%, 12% 0%, 18% 3%, 25% 0%, ... 100% 5%, 100% 95%, ... 0% 100%);",
        "vars": {
            "page_bg": "#2a2a2a", "side_bg": "#1f1f1f", "card_bg": "#f5ebd6",
            "card_border": "none",
            "card_shadow": "0 6px 16px rgba(0,0,0,0.4)",
            "radius": "0px", "text": "#2a1f10", "muted": "#7a6845",
            "accent": "#8b2a2a", "accent2": "#3d5a3d",
            "font": "'Special Elite', 'Courier New', monospace",
            "btn_bg": "#2a1f10", "btn_text": "#f5ebd6", "btn_border": "none",
            "btn_hover": "0 4px 10px rgba(0,0,0,0.4)", "btn_move": "translateY(-1px)",
            "btn_radius": "0px", "inset_bg": "#e8dcc0", "input_border": "2px dashed #2a1f10",
        },
        "extra": ".stApp .card, .stApp .stat, .stApp .hero {"
                 "  clip-path: polygon(0% 4%, 5% 0%, 12% 5%, 20% 0%, 30% 4%, 40% 0%, 50% 5%, 60% 0%, 70% 4%, 80% 0%, 90% 5%, 100% 0%, 100% 95%, 95% 100%, 85% 96%, 75% 100%, 65% 95%, 55% 100%, 45% 96%, 35% 100%, 25% 95%, 15% 100%, 5% 96%, 0% 100%);"
                 "  border-radius: 0;"
                 "}"
                 ".stApp .hero h1 { letter-spacing: 1px; }"
                 ".stApp p, .stApp li { font-family: 'Special Elite', monospace; }",
    },
    # ------------------------------------------------------------ 37
    "Etched Frosted Lines": {
        "icon": "❄️",
        "tagline": "Frosted glass with horizontal etched lines - like cut crystal or frosted glass panels.",
        "search": ["etched glass CSS", "frosted glass lines", "etched pattern overlay", "cut crystal UI"],
        "tip": "background: rgba(255,255,255,0.15);\nbackdrop-filter: blur(16px);\n"
               "/* etched horizontal lines overlay */\nbackground-image: repeating-linear-gradient(0deg, transparent, transparent 6px, rgba(255,255,255,0.08) 6px, rgba(255,255,255,0.08) 7px);",
        "vars": {
            "page_bg": "linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%)",
            "side_bg": "rgba(255,255,255,0.1)", "card_bg": "rgba(255,255,255,0.15)",
            "card_border": "1px solid rgba(255,255,255,0.3)",
            "card_shadow": "0 8px 32px rgba(0,0,0,0.3)",
            "blur": "blur(16px)",
            "radius": "4px", "text": "#ffffff", "muted": "rgba(255,255,255,0.7)",
            "accent": "#5eead4", "accent2": "#fbbf24",
            "font": "'Inter', sans-serif",
            "btn_bg": "rgba(255,255,255,0.2)", "btn_text": "#ffffff",
            "btn_border": "1px solid rgba(255,255,255,0.4)",
            "btn_hover": "0 4px 16px rgba(94,234,212,0.4)", "btn_move": "translateY(-2px)",
            "btn_radius": "4px", "inset_bg": "rgba(255,255,255,0.1)",
            "input_border": "1px solid rgba(255,255,255,0.3)",
        },
        "extra": ".stApp .card, .stApp .stat, .stApp .hero {"
                 "  background-image: repeating-linear-gradient(0deg, transparent, transparent 6px, rgba(255,255,255,0.06) 6px, rgba(255,255,255,0.06) 7px);"
                 "}"
                 ".stApp .hero h1 { letter-spacing: 2px; text-shadow: 0 1px 0 rgba(0,0,0,0.3); }"
                 ".stApp .stat .num { text-shadow: 0 1px 0 rgba(0,0,0,0.3); }",
    },
}


# =====================================================================
# 3. THE CSS (shared by all designs)
# =====================================================================
# This CSS only uses variables like var(--accent).
# Each design just gives different values, so the SAME page looks different.

FONTS = (
    "@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800"
    "&family=Space+Grotesk:wght@500;700&family=Orbitron:wght@600;800&family=Rajdhani:wght@500;700"
    "&family=Nunito:wght@600;800&family=Share+Tech+Mono&family=Playfair+Display:wght@700;900"
    "&family=Press+Start+2P&family=Caveat:wght@500;700&family=Permanent+Marker"
    "&family=Bangers&family=UnifrakturCook:wght@700&family=VT323"
    "&family=Space+Mono:wght@400;700&family=Special+Elite&display=swap');"
)

BASE_CSS = """
.stApp { background: var(--page-bg); background-attachment: fixed; color: var(--text); font-family: var(--font); }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stHeader"] * { color: var(--text); }
.block-container { max-width: 1100px; padding-top: 2.2rem; }

/* text colours */
.stApp h1, .stApp h2, .stApp h3, .stApp h4 { color: var(--text); font-family: var(--head-font); }
.stApp p, .stApp li, .stApp label { color: var(--text); }
.stApp .muted { color: var(--muted); }

/* sidebar */
[data-testid="stSidebar"] { background: var(--side-bg); backdrop-filter: var(--blur); }
[data-testid="stSidebar"] h3, [data-testid="stSidebar"] .stCaption, [data-testid="stSidebar"] p { color: var(--side-text); }
[data-testid="stSidebar"] [role="radiogroup"] { gap: 10px; }
[data-testid="stSidebar"] [role="radiogroup"] label {
    background: var(--btn-bg); border: var(--btn-border); border-radius: var(--btn-radius);
    box-shadow: var(--btn-shadow); padding: 8px 14px; cursor: pointer; transition: all .18s ease;
}
[data-testid="stSidebar"] [role="radiogroup"] label * { color: var(--btn-text); }
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    box-shadow: var(--btn-hover); outline: var(--sel-outline); outline-offset: 2px; font-weight: 700;
}
[data-testid="stSidebar"] [data-baseweb="radio"] > div:first-child { display: none; }

/* cards (HTML cards AND the st.container that has key="widgets_card") */
.card, .st-key-widgets_card {
    background: var(--card-bg); border: var(--card-border); border-radius: var(--radius);
    box-shadow: var(--card-shadow); backdrop-filter: var(--blur);
    padding: 22px 26px; margin-bottom: 22px;
}
.card h3 { margin: 0 0 10px 0; font-size: 1.2rem; }
.hero { text-align: center; padding: 34px 20px; }
.hero h1 { font-size: 2.6rem; margin: 8px 0; font-weight: 800; }

/* small pieces */
.stApp .badge {
    display: inline-block; padding: 6px 14px; margin: 4px; font-size: .8rem; font-weight: 600;
    background: var(--btn-bg); color: var(--btn-text); border: var(--btn-border);
    border-radius: var(--btn-radius); box-shadow: var(--btn-shadow);
}
.stat-row { display: flex; gap: 18px; flex-wrap: wrap; margin-bottom: 22px; }
.stat {
    flex: 1; min-width: 150px; text-align: center; padding: 20px 10px;
    background: var(--card-bg); border: var(--card-border); border-radius: var(--radius);
    box-shadow: var(--card-shadow); backdrop-filter: var(--blur);
}
.stApp .stat .num { font-size: 1.9rem; font-weight: 800; color: var(--accent); }
.stApp .stat .label { font-size: .85rem; color: var(--muted); }

.bar-row { display: flex; align-items: center; gap: 12px; margin: 12px 0; }
.bar-name { width: 80px; font-weight: 600; font-size: .9rem; }
.bar-track {
    flex: 1; height: 14px; overflow: hidden; background: var(--inset-bg);
    border: var(--input-border); border-radius: var(--btn-radius); box-shadow: var(--inset);
}
.bar-fill { height: 100%; background: linear-gradient(90deg, var(--accent), var(--accent2)); }
.bar-value { width: 48px; text-align: right; font-size: .85rem; color: var(--muted); }

.nm-table { width: 100%; border-collapse: collapse; margin-top: 8px; }
.nm-table th { text-align: left; font-size: .8rem; color: var(--muted); padding: 8px 6px; }
.nm-table td { padding: 8px 6px; font-size: .92rem; border-top: 1px dashed var(--muted); }

.code {
    background: var(--inset-bg); box-shadow: var(--inset); border: var(--input-border);
    border-radius: var(--btn-radius); padding: 14px 18px; white-space: pre-wrap;
    font-family: 'Courier New', monospace; font-size: .85rem; color: var(--text);
}
.footer { text-align: center; color: var(--muted); font-size: .85rem; margin: 26px 0 8px 0; }

/* Streamlit buttons */
.stButton > button {
    background: var(--btn-bg); color: var(--btn-text); border: var(--btn-border);
    border-radius: var(--btn-radius); box-shadow: var(--btn-shadow);
    font-weight: 700; padding: 10px 12px; font-family: inherit; transition: all .18s ease; white-space: nowrap;
}
.stApp .stButton > button p { color: var(--btn-text); }
.stButton > button:hover, .stButton > button:active, .stButton > button:focus {
    background: var(--btn-bg); color: var(--btn-text); border: var(--btn-border);
    box-shadow: var(--btn-hover); transform: var(--btn-move);
}

/* Streamlit text input */
[data-testid="stTextInputRootElement"] {
    background: var(--inset-bg) !important; border: var(--input-border) !important;
    border-radius: var(--btn-radius) !important; box-shadow: var(--inset);
}
[data-baseweb="input"], [data-baseweb="input"] > div, [data-baseweb="base-input"] { background: transparent !important; border: none !important; }
[data-baseweb="input"] input { background: transparent !important; color: var(--text) !important; -webkit-text-fill-color: var(--text); }
[data-baseweb="input"] input::placeholder { color: var(--muted); -webkit-text-fill-color: var(--muted); }
"""


def build_css(design):
    """Make the full CSS text for one design."""
    settings = {**DEFAULTS, **design["vars"]}
    settings.setdefault("side_text", settings["text"])

    # turn the dictionary into CSS variables:  page_bg -> --page-bg: ...;
    variables = ""
    for key, value in settings.items():
        variables += f"--{key.replace('_', '-')}: {value};\n"

    return f"<style>{FONTS}\n:root {{\n{variables}}}\n{BASE_CSS}\n{design.get('extra', '')}</style>"


# =====================================================================
# 4. SMALL HTML HELPERS
# =====================================================================

def show_html(text):
    """Show HTML on the page (blank lines removed so Streamlit does not break it)."""
    lines = [line.strip() for line in text.strip().splitlines()]
    st.markdown("\n".join(line for line in lines if line), unsafe_allow_html=True)


def badges(words):
    return "".join(f'<span class="badge">{word}</span>' for word in words)


def stat_tiles(items):
    """items = [(number, label), ...]"""
    tiles = ""
    for number, label in items:
        tiles += f'<div class="stat"><div class="num">{number}</div><div class="label">{label}</div></div>'
    show_html(f'<div class="stat-row">{tiles}</div>')


def bars(items):
    """items = [(name, percent), ...]"""
    rows = ""
    for name, value in items:
        rows += (
            f'<div class="bar-row"><div class="bar-name">{name}</div>'
            f'<div class="bar-track"><div class="bar-fill" style="width:{value}%"></div></div>'
            f'<div class="bar-value">{value}%</div></div>'
        )
    return rows


# =====================================================================
# 5. THE SAMPLE PAGE (same page for every design)
# =====================================================================

def show_demo_page(name, design):
    # ----- Top banner -----
    show_html(f"""
    <div class="card hero">
        <div>{badges(["UI Design", "Streamlit", "CSS"])}</div>
        <h1>{design['icon']} {name}</h1>
        <p class="muted">{design['tagline']}</p>
    </div>
    """)

    # ----- Four stat tiles -----
    stat_tiles([("12.4K", "Happy users"), ("$48K", "Revenue"), ("4.9 ★", "Rating"), ("99.9%", "Uptime")])

    # ----- Two columns: widgets (left) and progress + table (right) -----
    left, right = st.columns(2, gap="large")

    with left:
        with st.container(key="widgets_card"):
            st.markdown("### Buttons and inputs")
            col1, col2, col3 = st.columns(3)
            if col1.button("Primary"):
                st.toast(f"Primary button clicked in {name}!", icon="🎉")
            if col2.button("Cancel"):
                st.toast("Cancel button clicked", icon="👍")
            if col3.button("Delete"):
                st.toast("Delete button clicked", icon="⚠️")

            st.text_input("Your name", placeholder="Type something here...", key=f"name_{name}")
            st.toggle("Enable notifications", value=True, key=f"toggle_{name}")

    with right:
        card("Progress bars", bars([("Design", 92), ("Code", 78), ("Speed", 64), ("Fun", 100)]))

    # ----- Table card -----
    card("Sample table", """
        <table class="nm-table">
            <tr><th>Page</th><th>Visits</th><th>Status</th></tr>
            <tr><td>Home</td><td>8,420</td><td>Live</td></tr>
            <tr><td>Pricing</td><td>3,115</td><td>Live</td></tr>
            <tr><td>Blog</td><td>1,870</td><td>Draft</td></tr>
        </table>
    """)

    # ----- Info card: what to search + the main CSS trick -----
    tip = html.escape(design["tip"])
    card("What is this design? How to learn more?", f"""
        <p>{design['tagline']}</p>
        <p><b>Search on Google / YouTube / Dribbble:</b></p>
        <div>{badges(design['search'])}</div>
        <p style="margin-top:16px"><b>Main CSS trick:</b></p>
        <div class="code">{tip}</div>
    """)


def card(title, body):
    """A card with a title and some HTML inside."""
    show_html(f'<div class="card"><h3>{title}</h3>{body}</div>')


# =====================================================================
# 6. MAIN - sidebar with all designs
# =====================================================================

def main():
    names = list(DESIGNS.keys())

    # Sidebar menu (each item shows icon + name)
    with st.sidebar:
        st.markdown("### 🎨 Design Gallery")
        st.caption("Pick a design - the whole page changes")
        choice = st.radio(
            "Designs",
            names,
            format_func=lambda n: f"{DESIGNS[n]['icon']}  {n}",
            label_visibility="collapsed",
        )
        st.caption(f"{len(DESIGNS)} styles · one Streamlit file")

    design = DESIGNS[choice]
    st.markdown(build_css(design), unsafe_allow_html=True)

    show_demo_page(choice, design)
    show_html('<div class="footer">Design Gallery · Built with Streamlit and pure CSS</div>')


main()
