
"""
Design Gallery - 35 UI design styles in one Streamlit app

Run with:  streamlit run designs.py

How it works (very simple):
    1. DESIGNS  -> a dictionary. Each design = a few colour/shadow settings.
    2. build_css() -> turns the chosen design into CSS.
    3. show_demo_page() -> ONE sample page (cards, buttons, inputs, bars)
       that looks different for every design because only the CSS changes.

Want to add your own design? Copy any block inside DESIGNS and change the values.

Styles 1-15 are the classic set. Styles 16-35 are the "professional" set:
modern SaaS, design systems, and cultural/art movements - each one is a real,
recognisable look you can build an actual product with.
"""

import html

import streamlit as st


# =====================================================================
# 1. PAGE SETUP
# =====================================================================

st.set_page_config(page_title="Design Gallery", page_icon="🎨", layout="wide")


# =====================================================================
# 2. THE 35 DESIGNS
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
    "Dark SaaS": {
        "icon": "🌑",
        "tagline": "The modern developer-tool look: near-black surfaces, hairline borders, one electric accent.",
        "search": ["dark saas dashboard", "linear app design", "vercel developer tool UI", "modern dark mode interface"],
        "tip": "background: #0a0a0c;\nborder: 1px solid rgba(255,255,255,0.08);\n"
               "box-shadow: inset 0 1px 0 rgba(255,255,255,0.04);   /* hairline edge */",
        "vars": {
            "page_bg": "#0a0a0c", "side_bg": "#0d0d10", "card_bg": "#131316",
            "card_border": "1px solid rgba(255,255,255,0.08)",
            "card_shadow": "0 8px 24px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.04)",
            "radius": "14px", "text": "#f4f4f5", "muted": "#8e8e96",
            "accent": "#7c8cf8", "accent2": "#c084fc", "font": "'Inter', sans-serif",
            "btn_bg": "#1c1c21", "btn_text": "#f4f4f5", "btn_border": "1px solid rgba(255,255,255,0.1)",
            "btn_radius": "10px", "btn_hover": "0 0 0 2px #7c8cf8",
            "inset_bg": "rgba(255,255,255,0.04)", "input_border": "1px solid rgba(255,255,255,0.12)",
        },
    },
    # ------------------------------------------------------------ 17
    "Stripe Fresh": {
        "icon": "💳",
        "tagline": "Enterprise-clean: white surfaces, a soft pastel ribbon and one confident indigo.",
        "search": ["stripe website design", "modern enterprise landing page", "pastel gradient saas", "saas website 2026"],
        "tip": "background: #ffffff;\nbox-shadow: 0 8px 24px rgba(50,50,93,0.10);   /* Stripe's soft signature shadow */\n"
               "color: #32325d;",
        "vars": {
            "page_bg": "#f6f9fc", "side_bg": "#ffffff", "card_bg": "#ffffff",
            "card_border": "1px solid #e6ebf1",
            "card_shadow": "0 8px 24px rgba(50,50,93,0.10)",
            "radius": "12px", "text": "#32325d", "muted": "#6b7c93",
            "accent": "#635bff", "accent2": "#00d4ff", "font": "'Inter', sans-serif",
            "btn_bg": "linear-gradient(90deg, #635bff, #8f7bff)", "btn_text": "#ffffff",
            "btn_radius": "22px", "btn_shadow": "0 4px 12px rgba(99,91,255,0.3)",
            "btn_hover": "0 8px 22px rgba(99,91,255,0.45)", "btn_move": "translateY(-1px)",
            "inset_bg": "#f2f5f9", "input_border": "1px solid #d8e0ea",
        },
        "extra": ".stApp .hero { background: linear-gradient(120deg, rgba(163,184,255,0.25), rgba(255,214,224,0.3), rgba(179,240,255,0.25)); }",
    },
    # ------------------------------------------------------------ 18
    "Apple HIG": {
        "icon": "🍎",
        "tagline": "iOS-clean: soft grey canvas, pure white cards, one system-blue accent.",
        "search": ["iOS design language", "apple human interface guidelines", "ios app UI design", "sf pro design system"],
        "tip": "background: #f2f2f7;   /* iOS systemGroupedBackground */\n"
               "background: #ffffff;   /* grouped card */\nborder-radius: 18px;",
        "vars": {
            "page_bg": "#f2f2f7", "side_bg": "#fbfbfd", "card_bg": "#ffffff",
            "card_border": "none", "card_shadow": "0 1px 3px rgba(0,0,0,0.06)",
            "radius": "18px", "text": "#1d1d1f", "muted": "#6e6e73",
            "accent": "#007aff", "accent2": "#5ac8fa",
            "font": "'SF Pro Display', -apple-system, 'Segoe UI', sans-serif",
            "btn_bg": "#007aff", "btn_text": "#ffffff", "btn_radius": "12px",
            "btn_hover": "0 6px 16px rgba(0,122,255,0.4)", "inset_bg": "#e4e4ea",
            "input_border": "1px solid #d1d1d6",
        },
    },
    # ------------------------------------------------------------ 19
    "Fluent Design": {
        "icon": "🔷",
        "tagline": "Microsoft acrylic: blurred translucency, soft depth layers, Segoe blue.",
        "search": ["microsoft fluent design", "acrylic material UI", "windows 11 design style", "fluent ui components"],
        "tip": "background: rgba(255,255,255,0.75);\nbackdrop-filter: blur(30px) saturate(160%);   /* acrylic */\n"
               "box-shadow: 0 8px 40px rgba(0,0,0,0.12);",
        "vars": {
            "page_bg": "linear-gradient(135deg, #e8f0fe 0%, #fde7f9 50%, #e9fff5 100%)",
            "side_bg": "rgba(255,255,255,0.7)", "card_bg": "rgba(255,255,255,0.72)",
            "card_border": "1px solid rgba(255,255,255,0.85)", "blur": "blur(30px) saturate(160%)",
            "card_shadow": "0 8px 40px rgba(32,60,120,0.12)",
            "radius": "8px", "text": "#1b1b1b", "muted": "#5c5c5c",
            "accent": "#0078d4", "accent2": "#4f6bed", "font": "'Segoe UI', system-ui, sans-serif",
            "btn_bg": "#0078d4", "btn_text": "#ffffff", "btn_radius": "4px",
            "btn_hover": "0 4px 14px rgba(0,120,212,0.4)", "inset_bg": "rgba(255,255,255,0.65)",
            "input_border": "1px solid rgba(0,0,0,0.12)",
        },
    },
    # ------------------------------------------------------------ 20
    "Enterprise Admin": {
        "icon": "📊",
        "tagline": "Ant-Design workhorse: compact tables, dense data, trustworthy blue.",
        "search": ["ant design pro", "enterprise admin dashboard", "data dense UI design", "antd dashboard template"],
        "tip": "background: #f0f2f5;\nborder-radius: 8px;\ncolor: rgba(0,0,0,0.88);   /* Ant Design body text */",
        "vars": {
            "page_bg": "#f0f2f5", "side_bg": "#001529", "side_text": "#ffffff",
            "card_bg": "#ffffff", "card_shadow": "0 1px 4px rgba(0,21,41,0.08)",
            "radius": "8px", "text": "rgba(0,0,0,0.88)", "muted": "rgba(0,0,0,0.45)",
            "accent": "#1677ff", "accent2": "#69b1ff", "font": "'Inter', sans-serif",
            "btn_bg": "#1677ff", "btn_text": "#ffffff", "btn_radius": "6px",
            "btn_hover": "0 4px 12px rgba(22,119,255,0.4)", "inset_bg": "#f5f5f5",
            "input_border": "1px solid #d9d9d9",
        },
    },
    # ------------------------------------------------------------ 21
    "Notion Minimal": {
        "icon": "📝",
        "tagline": "Workspace-minimal: warm off-white, hairline grey borders, zero decoration.",
        "search": ["notion design style", "minimal workspace UI", "notion clone design", "warm neutral interface"],
        "tip": "background: #f7f6f3;   /* Notion's warm paper */\nborder: 1px solid #e9e9e7;\n"
               "color: #37352f;",
        "vars": {
            "page_bg": "#f7f6f3", "side_bg": "#f1f0ed", "card_bg": "#ffffff",
            "card_border": "1px solid #e9e9e7", "card_shadow": "none",
            "radius": "6px", "text": "#37352f", "muted": "#9f9e9b",
            "accent": "#2383e2", "accent2": "#0f7b6c", "font": "'Inter', sans-serif",
            "btn_bg": "#f0efed", "btn_text": "#37352f", "btn_border": "1px solid #d3d1cb",
            "btn_radius": "6px", "btn_hover": "0 2px 6px rgba(0,0,0,0.08)",
            "inset_bg": "#fbfbfa", "input_border": "1px solid #e0deda",
        },
    },
    # ------------------------------------------------------------ 22
    "Duotone": {
        "icon": "🎧",
        "tagline": "Spotify-dark: charcoal surfaces, one electric green, duotone gradient art.",
        "search": ["duotone design", "spotify dark UI", "music app interface", "duotone gradient images"],
        "tip": "filter: grayscale(100%) contrast(1.2);   /* then blend a gradient over it */\n"
               "background: linear-gradient(45deg, #1db954, #1ed760);",
        "vars": {
            "page_bg": "#121212", "side_bg": "#000000", "card_bg": "#1a1a1a",
            "card_border": "1px solid #2a2a2a", "card_shadow": "none",
            "radius": "10px", "text": "#ffffff", "muted": "#a7a7a7",
            "accent": "#1db954", "accent2": "#1ed760", "font": "'Inter', sans-serif",
            "btn_bg": "#1db954", "btn_text": "#000000", "btn_radius": "999px",
            "btn_hover": "0 6px 18px rgba(29,185,84,0.45)", "inset_bg": "#2a2a2a",
            "input_border": "1px solid #3a3a3a",
        },
        "extra": ".stApp .stat { background: linear-gradient(135deg, rgba(29,185,84,0.14), #1a1a1a); border: 1px solid #2a2a2a; }",
    },
    # ------------------------------------------------------------ 23
    "Luxury Noir": {
        "icon": "🖤",
        "tagline": "Black-tie premium: deep black, brushed gold hairlines, serif headlines.",
        "search": ["luxury website design", "black and gold UI", "premium brand design", "dark luxury interface"],
        "tip": "background: #0b0a08;\ncolor: #e8dfc8;\nborder: 1px solid #c9a22755;\n"
               "letter-spacing: 0.12em;   /* spacious, confident type */",
        "vars": {
            "page_bg": "#0b0a08", "side_bg": "#12100c", "card_bg": "#14110c",
            "card_border": "1px solid rgba(201,162,39,0.35)",
            "card_shadow": "0 10px 40px rgba(0,0,0,0.6)",
            "radius": "4px", "text": "#ece5d0", "muted": "#8f8672",
            "accent": "#c9a227", "accent2": "#e8d48b",
            "font": "'Inter', sans-serif", "head_font": "'Playfair Display', Georgia, serif",
            "btn_bg": "transparent", "btn_text": "#c9a227", "btn_border": "1px solid #c9a227",
            "btn_hover": "inset 0 -3px 0 #c9a227", "btn_radius": "2px",
            "inset_bg": "#1a1611", "input_border": "1px solid rgba(201,162,39,0.4)",
        },
        "extra": ".stApp .hero h1 { letter-spacing: 0.06em; }",
    },
    # ------------------------------------------------------------ 24
    "Scandinavian": {
        "icon": "🪑",
        "tagline": "Nordic calm: bright whites, pale wood tones, and one honest accent.",
        "search": ["scandinavian web design", "nordic minimalism UI", "danish design style", "hygge website aesthetic"],
        "tip": "background: #faf9f6;\ncolor: #2b2b2b;\naccent: #d95d39;   /* Danish red-orange */\n"
               "border-radius: 2px;",
        "vars": {
            "page_bg": "#faf9f6", "side_bg": "#f0ede6", "card_bg": "#ffffff",
            "card_border": "none", "card_shadow": "0 2px 10px rgba(60,50,40,0.06)",
            "radius": "6px", "text": "#2b2b2b", "muted": "#8a8578",
            "accent": "#d95d39", "accent2": "#7a9e7e", "font": "'Inter', sans-serif",
            "btn_bg": "#2b2b2b", "btn_text": "#ffffff", "btn_radius": "2px",
            "btn_hover": "0 4px 12px rgba(0,0,0,0.18)", "inset_bg": "#f1efe9",
            "input_border": "1px solid #d9d4c8",
        },
    },
    # ------------------------------------------------------------ 25
    "Japanese Zen": {
        "icon": "⛩️",
        "tagline": "Washi-paper quiet: warm cream, ink black, and a single red seal.",
        "search": ["japanese minimal web design", "wabi sabi aesthetic", "zen ui design", "japan style website"],
        "tip": "background: #f5f0e8;   /* washi paper */\nfont-family: Georgia, serif;\n"
               "border: 1px solid #d8cfc0;",
        "vars": {
            "page_bg": "#f5f0e8", "side_bg": "#efe8dc", "card_bg": "#fdfbf5",
            "card_border": "1px solid #d8cfc0", "card_shadow": "none",
            "radius": "2px", "text": "#2f2a24", "muted": "#8a7f6d",
            "accent": "#b3392e", "accent2": "#6b7f59",
            "font": "Georgia, 'Times New Roman', serif",
            "btn_bg": "transparent", "btn_text": "#2f2a24", "btn_border": "1px solid #2f2a24",
            "btn_hover": "0 0 0 1px #b3392e", "btn_radius": "2px",
            "inset_bg": "#f0e9db", "input_border": "1px solid #cbbfa9",
        },
        "extra": ".stApp .hero h1 { font-weight: 400; }",
    },
    # ------------------------------------------------------------ 26
    "Bauhaus": {
        "icon": "🔴",
        "tagline": "Form follows function: geometry, primary colours, and bold grotesk type.",
        "search": ["bauhaus web design", "geometric abstract UI", "primary colors design", "modernist poster style"],
        "tip": "background: #f0ede6;\nborder: 3px solid #1a1a1a;\nborder-radius: 0;\n"
               "accent: #e30613, #1d5fbf, #f2c400;   /* red, blue, yellow */",
        "vars": {
            "page_bg": "#f0ede6", "side_bg": "#e7e2d8", "card_bg": "#fbfaf7",
            "card_border": "3px solid #1a1a1a", "card_shadow": "8px 8px 0 #1a1a1a",
            "radius": "0px", "text": "#1a1a1a", "muted": "#6a655c",
            "accent": "#e30613", "accent2": "#1d5fbf",
            "font": "'Space Grotesk', sans-serif", "head_font": "'Space Grotesk', sans-serif",
            "btn_bg": "#1d5fbf", "btn_text": "#ffffff", "btn_border": "3px solid #1a1a1a",
            "btn_shadow": "4px 4px 0 #1a1a1a", "btn_hover": "0 0 0 #1a1a1a",
            "btn_move": "translate(4px, 4px)", "btn_radius": "0px",
            "inset_bg": "#ffffff", "input_border": "3px solid #1a1a1a",
        },
        "extra": ".stApp .hero h1 { text-transform: uppercase; letter-spacing: 2px; }"
                 ".stat:nth-child(2) { background: #f2c400; } .stat:nth-child(3) { background: #1d5fbf; }"
                 ".stat:nth-child(3) .num, .stat:nth-child(3) .label { color: #ffffff; }",
    },
    # ------------------------------------------------------------ 27
    "Memphis Milano": {
        "icon": "🌀",
        "tagline": "80s Italian postmodern: pastel shapes, squiggles, and playful black outlines.",
        "search": ["memphis design style", "80s pattern UI", "postmodern graphic design", "memphis milano aesthetic"],
        "tip": "background: #fff4e8;\nborder: 3px solid #000;\n"
               "/* layer a repeating SVG/radial pattern behind everything */",
        "vars": {
            "page_bg": "#fff4e8", "side_bg": "#ffe8d6", "card_bg": "#ffffff",
            "card_border": "3px solid #181818", "card_shadow": "6px 6px 0 #181818",
            "radius": "18px", "text": "#181818", "muted": "#6b5d4f",
            "accent": "#ff5d8f", "accent2": "#00c2a8",
            "font": "'Nunito', sans-serif", "head_font": "'Space Grotesk', sans-serif",
            "btn_bg": "#ffd23f", "btn_text": "#181818", "btn_border": "3px solid #181818",
            "btn_shadow": "4px 4px 0 #181818", "btn_hover": "0 0 0 #181818",
            "btn_move": "translate(3px, 3px)", "btn_radius": "18px",
            "inset_bg": "#fff0df", "input_border": "3px solid #181818",
        },
        "extra": ".stApp { background-image: radial-gradient(rgba(24,24,24,0.07) 2px, transparent 2.5px); background-size: 26px 26px; }",
    },
    # ------------------------------------------------------------ 28
    "Art Deco": {
        "icon": "🥂",
        "tagline": "Gatsby-era glamour: navy and gold, sunburst geometry, high-contrast serifs.",
        "search": ["art deco web design", "gatsby style website", "1920s design aesthetic", "great gatsby ui"],
        "tip": "background: #0f1b2d;\ncolor: #e9c46a;\nborder: 2px solid #c9a227;\n"
               "font-family: 'Playfair Display', serif;",
        "vars": {
            "page_bg": "#0f1b2d", "side_bg": "#0b1524", "card_bg": "#13233a",
            "card_border": "2px solid rgba(201,162,39,0.5)",
            "card_shadow": "0 12px 40px rgba(0,0,0,0.5)",
            "radius": "2px", "text": "#f0e6c8", "muted": "#a3906e",
            "accent": "#d4af37", "accent2": "#f4e3b2",
            "font": "Georgia, serif", "head_font": "'Playfair Display', Georgia, serif",
            "btn_bg": "#d4af37", "btn_text": "#0f1b2d", "btn_radius": "0px",
            "btn_hover": "0 6px 18px rgba(212,175,55,0.5)", "inset_bg": "#1a2c47",
            "input_border": "1px solid #3a4a63",
        },
        "extra": ".stApp .hero { border-top: 3px double #d4af37; border-bottom: 3px double #d4af37; }",
    },
    # ------------------------------------------------------------ 29
    "Blueprint": {
        "icon": "📐",
        "tagline": "Technical drawing: grid paper, dashed dimension lines, annotation-white type.",
        "search": ["blueprint design style", "technical drawing UI", "grid paper interface", "engineering schematic aesthetic"],
        "tip": "background:\n  linear-gradient(rgba(255,255,255,0.07) 1px, transparent 1px),\n"
               "  linear-gradient(90deg, rgba(255,255,255,0.07) 1px, transparent 1px),\n  #1e3a5f;\n"
               "background-size: 24px 24px;",
        "vars": {
            "page_bg": "linear-gradient(rgba(255,255,255,0.07) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.07) 1px, transparent 1px), #1e3a5f",
            "side_bg": "#182f4d", "card_bg": "rgba(255,255,255,0.04)",
            "card_border": "1px solid rgba(255,255,255,0.6)", "card_shadow": "none",
            "radius": "2px", "text": "#eaf2fa", "muted": "#9db8d2",
            "accent": "#ffd23f", "accent2": "#7fd4ff",
            "font": "'IBM Plex Mono', 'Courier New', monospace",
            "btn_bg": "transparent", "btn_text": "#eaf2fa", "btn_border": "1px solid #eaf2fa",
            "btn_hover": "0 0 0 2px #7fd4ff", "btn_radius": "2px",
            "inset_bg": "rgba(0,0,0,0.2)", "input_border": "1px dashed rgba(255,255,255,0.7)",
        },
        "extra": ".stApp .hero { border: 1px dashed rgba(255,255,255,0.7); }",
    },
    # ------------------------------------------------------------ 30
    "Aqua Gloss": {
        "icon": "💧",
        "tagline": "Mac OS X 2000s: pinstripes and candy gel buttons you want to lick.",
        "search": ["mac os x aqua design", "skeuomorphic mac interface", "2000s apple UI", "gel buttons CSS"],
        "tip": "background: linear-gradient(#8fd3ff, #3d95e3);\n"
               "box-shadow: inset 0 2px 3px rgba(255,255,255,0.8), 0 3px 6px rgba(0,0,0,0.3);   /* candy gloss */",
        "vars": {
            "page_bg": "repeating-linear-gradient(180deg, #e3eeff 0px, #e3eeff 1px, #d3e4fa 1px, #d3e4fa 3px)",
            "side_bg": "#dbe9fa",
            "card_bg": "linear-gradient(180deg, #fdfefe, #eef4fb)",
            "card_border": "1px solid #8b98a8", "card_shadow": "0 4px 12px rgba(30,60,110,0.25)",
            "radius": "10px", "text": "#17202b", "muted": "#5a6a7d",
            "accent": "#3d95e3", "accent2": "#7fd4ff",
            "font": "'Lucida Grande', 'Segoe UI', sans-serif",
            "btn_bg": "linear-gradient(180deg, #bfe6ff 0%, #4a9be6 50%, #2a7fd4 100%)",
            "btn_text": "#ffffff", "btn_border": "1px solid #0f4e96",
            "btn_shadow": "inset 0 2px 3px rgba(255,255,255,0.8), 0 3px 6px rgba(0,0,0,0.3)",
            "btn_hover": "inset 0 2px 3px rgba(255,255,255,0.95), 0 5px 12px rgba(0,0,0,0.35)",
            "btn_radius": "999px", "inset_bg": "#ffffff", "inset": "inset 0 2px 4px rgba(0,0,0,0.15)",
            "input_border": "1px solid #8b98a8",
        },
    },
    # ------------------------------------------------------------ 31
    "Frutiger Aero": {
        "icon": "🌊",
        "tagline": "Mid-2000s optimism: glossy glass, water bubbles, lush greens and blues.",
        "search": ["frutiger aero aesthetic", "y2k glossy ui", "windows vista design", "2000s tech optimism design"],
        "tip": "background: linear-gradient(180deg, #bfe6f5, #e8f9ee);\n"
               "box-shadow: inset 0 4px 20px rgba(255,255,255,0.7);   /* underwater glass */",
        "vars": {
            "page_bg": "linear-gradient(180deg, #a8dcf0 0%, #c9efdb 55%, #e9f9d8 100%)",
            "side_bg": "rgba(255,255,255,0.55)", "card_bg": "rgba(255,255,255,0.6)",
            "card_border": "1px solid rgba(255,255,255,0.9)", "blur": "blur(18px)",
            "card_shadow": "0 10px 30px rgba(60,140,180,0.25)",
            "radius": "18px", "text": "#123c2e", "muted": "#4d7a68",
            "accent": "#00a8c6", "accent2": "#7ae0b8", "font": "'Segoe UI', sans-serif",
            "btn_bg": "linear-gradient(180deg, rgba(255,255,255,0.95), rgba(79,195,232,0.9))",
            "btn_text": "#07537a", "btn_border": "1px solid rgba(255,255,255,0.95)",
            "btn_shadow": "0 3px 8px rgba(0,90,130,0.3), inset 0 1px 0 #ffffff",
            "btn_hover": "0 6px 16px rgba(0,90,130,0.4)", "btn_move": "translateY(-2px)",
            "inset_bg": "rgba(255,255,255,0.55)", "input_border": "1px solid rgba(255,255,255,0.9)",
        },
    },
    # ------------------------------------------------------------ 32
    "Long Shadow Flat": {
        "icon": "🔲",
        "tagline": "2013 flat design with dramatic 45-degree long shadows.",
        "search": ["long shadow flat design", "flat design trend 2013", "material long shadow", "flat ui colors"],
        "tip": "box-shadow: 14px 14px 0 rgba(38,50,56,0.12);   /* long shadow, no blur, 45 degrees */",
        "vars": {
            "page_bg": "#eceff1", "side_bg": "#e2e6e9", "card_bg": "#ffffff",
            "card_border": "none", "card_shadow": "14px 14px 0 rgba(38,50,56,0.12)",
            "radius": "4px", "text": "#263238", "muted": "#78909c",
            "accent": "#26a69a", "accent2": "#7e57c2", "font": "'Inter', sans-serif",
            "btn_bg": "#26a69a", "btn_text": "#ffffff", "btn_radius": "4px",
            "btn_shadow": "6px 6px 0 rgba(38,50,56,0.25)",
            "btn_hover": "2px 2px 0 rgba(38,50,56,0.25)", "btn_move": "translate(4px, 4px)",
            "inset_bg": "#eceff1", "input_border": "1px solid #b0bec5",
        },
    },
    # ------------------------------------------------------------ 33
    "Pop Art Comic": {
        "icon": "💥",
        "tagline": "Lichtenstein loud: Ben-Day dots, action words, thick ink outlines.",
        "search": ["pop art web design", "comic book UI style", "benday dots css", "retro comic aesthetic"],
        "tip": "background-image: radial-gradient(#00000022 2px, transparent 2.5px);\n"
               "background-size: 18px 18px;   /* Ben-Day dots */",
        "vars": {
            "page_bg": "#ffde03", "side_bg": "#ffd100", "card_bg": "#ffffff",
            "card_border": "4px solid #111111", "card_shadow": "8px 8px 0 #111111",
            "radius": "2px", "text": "#111111", "muted": "#555555",
            "accent": "#e3000f", "accent2": "#1d5fbf",
            "font": "'Space Grotesk', sans-serif", "head_font": "'Space Grotesk', sans-serif",
            "btn_bg": "#e3000f", "btn_text": "#ffffff", "btn_border": "4px solid #111111",
            "btn_shadow": "6px 6px 0 #111111", "btn_hover": "0 0 0 #111111",
            "btn_move": "translate(5px, 5px)", "btn_radius": "2px",
            "inset_bg": "#fff7c2", "input_border": "3px solid #111111",
        },
        "extra": ".stApp { background-image: radial-gradient(rgba(0,0,0,0.08) 2px, transparent 2.5px); background-size: 18px 18px; }",
    },
    # ------------------------------------------------------------ 34
    "Eco Organic": {
        "icon": "🌿",
        "tagline": "Sustainability-first: recycled-paper tones, moss greens, soft rounded everything.",
        "search": ["eco friendly web design", "sustainability website style", "organic natural UI", "earth tone design"],
        "tip": "background: #f4f1e8;   /* recycled paper */\ncolor: #33402e;\n"
               "border-radius: 24px;\naccent: #5b7553;   /* moss green */",
        "vars": {
            "page_bg": "#f4f1e8", "side_bg": "#eae6d8", "card_bg": "#fbf9f3",
            "card_border": "1px solid #ddd6c3", "card_shadow": "0 4px 14px rgba(90,110,80,0.12)",
            "radius": "24px", "text": "#33402e", "muted": "#7d8a72",
            "accent": "#5b7553", "accent2": "#a3b18a", "font": "'Nunito', sans-serif",
            "btn_bg": "#5b7553", "btn_text": "#ffffff", "btn_radius": "999px",
            "btn_hover": "0 6px 16px rgba(91,117,83,0.4)", "inset_bg": "#ece8da",
            "input_border": "1px solid #c9c2ac",
        },
    },
    # ------------------------------------------------------------ 35
    "Dark Neumorphism": {
        "icon": "🌒",
        "tagline": "Neumorphism after sunset: soft extrusions rising out of a charcoal surface.",
        "search": ["dark neumorphism", "dark mode soft ui", "black neumorphic design", "soft shadows dark theme"],
        "tip": "background: #1b1e26;\nbox-shadow: 8px 8px 16px #0d0f14,\n            -8px -8px 16px #2a3040;",
        "vars": {
            "page_bg": "#1b1e26", "side_bg": "#1b1e26", "card_bg": "#1b1e26",
            "card_shadow": "9px 9px 18px #0d0f14, -9px -9px 18px #2a3040",
            "radius": "22px", "text": "#d8dee9", "muted": "#7b8494",
            "accent": "#5b8cff", "accent2": "#9a6bff",
            "btn_bg": "#1b1e26", "btn_text": "#5b8cff", "btn_radius": "14px",
            "btn_shadow": "5px 5px 10px #0d0f14, -5px -5px 10px #2a3040",
            "btn_hover": "inset 4px 4px 8px #0d0f14, inset -4px -4px 8px #2a3040",
            "inset_bg": "#1b1e26", "sel_outline": "none",
            "inset": "inset 5px 5px 10px #0d0f14, inset -5px -5px 10px #2a3040",
        },
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
    "&family=IBM+Plex+Mono:wght@400;600&display=swap');"
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
# 6. MAIN - sidebar with 35 designs
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
        st.caption("35 styles · one Streamlit file")

    design = DESIGNS[choice]
    st.markdown(build_css(design), unsafe_allow_html=True)

    show_demo_page(choice, design)
    show_html('<div class="footer">Design Gallery · Built with Streamlit and pure CSS</div>')


main()
