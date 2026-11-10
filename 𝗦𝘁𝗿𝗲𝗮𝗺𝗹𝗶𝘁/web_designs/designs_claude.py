"""
Design Gallery - 35 UI design styles in one Streamlit app

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

    # =================================================================
    # NEW DESIGNS 16 - 35
    # =================================================================
    # ------------------------------------------------------------ 16
    "Dark SaaS": {
        "icon": "🌑",
        "tagline": "Linear / Vercel style: near-black surfaces, hairline borders, one calm accent.",
        "search": ["dark SaaS UI", "Linear app design", "Vercel dashboard design", "dark mode dashboard"],
        "tip": "background: #101114;\nborder: 1px solid #23252a;   /* hairline border */\n"
               "box-shadow: 0 0 0 3px rgba(113,112,255,0.35);   /* focus ring */",
        "vars": {
            "page_bg": "#08090a", "side_bg": "#0d0e10", "card_bg": "#101114",
            "card_border": "1px solid #23252a",
            "card_shadow": "inset 0 1px 0 rgba(255,255,255,0.04), 0 8px 24px rgba(0,0,0,0.4)",
            "radius": "12px", "text": "#ededef", "muted": "#8a8f98",
            "accent": "#7170ff", "accent2": "#5e6ad2", "font": "'Inter', sans-serif",
            "btn_bg": "#5e6ad2", "btn_text": "#ffffff", "btn_border": "1px solid rgba(255,255,255,0.12)",
            "btn_shadow": "0 1px 2px rgba(0,0,0,0.4)",
            "btn_hover": "0 0 0 3px rgba(113,112,255,0.35)", "btn_radius": "8px",
            "inset_bg": "#16181c", "input_border": "1px solid #2a2d34",
        },
        "extra": ".stApp .hero { background: radial-gradient(ellipse at 50% 0%, rgba(113,112,255,0.22), transparent 70%), var(--card-bg); }",
    },
    # ------------------------------------------------------------ 17
    "Corporate Blue": {
        "icon": "🏢",
        "tagline": "Trustworthy enterprise look: navy sidebar, white cards, solid blue buttons.",
        "search": ["enterprise UI design", "IBM Carbon design system", "corporate website design", "B2B dashboard UI"],
        "tip": "background: #0b2545;   /* navy navigation */\nborder-top: 4px solid #0f62fe;   /* accent strip */\n"
               "border-radius: 4px;   /* small, serious corners */",
        "vars": {
            "page_bg": "#f3f6fb", "side_bg": "#0b2545", "side_text": "#e6eefb", "card_bg": "#ffffff",
            "card_border": "1px solid #dbe3ef", "card_shadow": "0 1px 3px rgba(11,37,69,0.08)",
            "radius": "8px", "text": "#13294b", "muted": "#5b6b86",
            "accent": "#0f62fe", "accent2": "#4589ff", "font": "'Inter', sans-serif",
            "btn_bg": "#0f62fe", "btn_text": "#ffffff", "btn_radius": "4px",
            "btn_hover": "0 4px 12px rgba(15,98,254,0.4)", "btn_move": "translateY(-1px)",
            "inset_bg": "#eaf0f9", "input_border": "1px solid #c5d1e3",
        },
        "extra": ".stApp .hero { border-top: 4px solid var(--accent); }",
    },
    # ------------------------------------------------------------ 18
    "Fintech Emerald": {
        "icon": "💳",
        "tagline": "Fresh money-app style: deep green, clean white cards, soft green glow.",
        "search": ["fintech UI design", "banking app design", "finance dashboard UI", "payment app design"],
        "tip": "background: linear-gradient(135deg, #10b981, #047857);   /* brand gradient */\n"
               "box-shadow: 0 10px 30px rgba(6,95,70,0.08);   /* soft green shadow */\nborder-radius: 18px;",
        "vars": {
            "page_bg": "#f6fbf9", "side_bg": "#06382c", "side_text": "#d6f5ea", "card_bg": "#ffffff",
            "card_border": "1px solid #d9efe6", "card_shadow": "0 10px 30px rgba(6,95,70,0.08)",
            "radius": "18px", "text": "#0b2e25", "muted": "#5f7f74",
            "accent": "#10b981", "accent2": "#047857", "font": "'Inter', sans-serif",
            "btn_bg": "linear-gradient(135deg, #10b981, #047857)", "btn_text": "#ffffff",
            "btn_hover": "0 8px 20px rgba(16,185,129,0.45)", "btn_move": "translateY(-2px)",
            "btn_radius": "12px", "inset_bg": "#e8f6f0", "input_border": "1px solid #bfe3d4",
        },
    },
    # ------------------------------------------------------------ 19
    "Notion Soft Docs": {
        "icon": "📝",
        "tagline": "Calm productivity-app look: warm greys, light buttons, tiny rounded corners.",
        "search": ["Notion style UI", "document app design", "minimal productivity UI", "soft grey UI"],
        "tip": "background: #fbfbfa;\nborder: 1px solid #e9e9e7;\ncolor: #37352f;   /* warm dark grey, never pure black */",
        "vars": {
            "page_bg": "#fbfbfa", "side_bg": "#f7f6f3", "card_bg": "#ffffff",
            "card_border": "1px solid #e9e9e7", "card_shadow": "0 1px 2px rgba(55,53,47,0.05)",
            "radius": "6px", "text": "#37352f", "muted": "#787774",
            "accent": "#2383e2", "accent2": "#e16259", "font": "'Inter', sans-serif",
            "btn_bg": "#f1f1ef", "btn_text": "#37352f", "btn_border": "1px solid #e0dfdc",
            "btn_hover": "0 0 0 2px rgba(35,131,226,0.35)", "btn_radius": "6px",
            "inset_bg": "#f7f6f3", "input_border": "1px solid #e0dfdc",
        },
    },
    # ------------------------------------------------------------ 20
    "Luxury Noir": {
        "icon": "👑",
        "tagline": "Premium brand feel: black surfaces, thin gold lines, elegant serif headings.",
        "search": ["luxury website design", "black and gold UI", "premium brand web design", "high-end fashion website"],
        "tip": "background: #121212;\nborder: 1px solid rgba(212,175,55,0.35);   /* thin gold line */\n"
               "background: linear-gradient(90deg,#d4af37,#f5e1a4,#d4af37);\n-webkit-background-clip: text;   /* gold text */",
        "vars": {
            "page_bg": "#0a0a0a", "side_bg": "#050505", "card_bg": "#121212",
            "card_border": "1px solid rgba(212,175,55,0.35)", "card_shadow": "0 10px 40px rgba(0,0,0,0.6)",
            "radius": "2px", "text": "#f3ead7", "muted": "#a89b7d",
            "accent": "#d4af37", "accent2": "#f5e1a4", "font": "'Inter', sans-serif",
            "head_font": "'Cormorant Garamond', Georgia, serif",
            "btn_bg": "transparent", "btn_text": "#d4af37", "btn_border": "1px solid #d4af37",
            "btn_hover": "0 0 0 1px #d4af37, 0 8px 24px rgba(212,175,55,0.25)", "btn_radius": "0px",
            "inset_bg": "#0c0c0c", "input_border": "1px solid rgba(212,175,55,0.4)",
        },
        "extra": ".stApp .hero h1 { letter-spacing: 4px; text-transform: uppercase; "
                 "background: linear-gradient(90deg,#d4af37,#f5e1a4,#d4af37); "
                 "-webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; }",
    },
    # ------------------------------------------------------------ 21
    "Art Deco": {
        "icon": "🏛️",
        "tagline": "1920s glamour: deep teal, gold double borders, geometric uppercase type.",
        "search": ["art deco web design", "gatsby style UI", "geometric gold design", "art deco CSS"],
        "tip": "border: 3px double #c9a227;   /* double gold frame */\ntext-transform: uppercase;\n"
               "letter-spacing: 3px;\nbackground: repeating-linear-gradient(45deg, #c9a22710 0 2px, transparent 2px 22px);",
        "vars": {
            "page_bg": "repeating-linear-gradient(45deg, rgba(201,162,39,0.05) 0 2px, transparent 2px 22px), #0f2a2a",
            "side_bg": "#0a1f1f", "card_bg": "#133535",
            "card_border": "3px double #c9a227", "card_shadow": "0 10px 30px rgba(0,0,0,0.4)",
            "radius": "0px", "text": "#f4ecd2", "muted": "#b8ad85",
            "accent": "#c9a227", "accent2": "#e8d28a", "font": "'Josefin Sans', sans-serif",
            "btn_bg": "transparent", "btn_text": "#c9a227", "btn_border": "2px solid #c9a227",
            "btn_hover": "inset 0 0 0 2px #0f2a2a, inset 0 0 0 4px #c9a227", "btn_radius": "0px",
            "inset_bg": "#0c2424", "input_border": "1px solid #c9a227",
        },
        "extra": ".stApp h1, .stApp .card h3 { text-transform: uppercase; letter-spacing: 3px; }",
    },
    # ------------------------------------------------------------ 22
    "Organic Earth": {
        "icon": "🌿",
        "tagline": "Natural and warm: olive green, terracotta, sand colours and soft round shapes.",
        "search": ["organic web design", "earthy colour palette UI", "wellness brand website", "natural eco website design"],
        "tip": "background: #f1ede4;   /* sand */\nborder-radius: 26px;\n"
               "color: #5f7a3a;   /* olive */\naccent: #c97b4a;   /* terracotta */",
        "vars": {
            "page_bg": "#f1ede4", "side_bg": "#e3dccb", "card_bg": "#faf7f0",
            "card_border": "1px solid #d8cfbb", "card_shadow": "0 6px 18px rgba(92,74,50,0.12)",
            "radius": "26px", "text": "#3b3a2a", "muted": "#7a7660",
            "accent": "#5f7a3a", "accent2": "#c97b4a", "font": "'Nunito', sans-serif",
            "head_font": "'Fraunces', Georgia, serif",
            "btn_bg": "#5f7a3a", "btn_text": "#faf7f0", "btn_radius": "999px",
            "btn_hover": "0 6px 14px rgba(95,122,58,0.4)", "btn_move": "translateY(-1px)",
            "inset_bg": "#ebe5d6", "input_border": "1px solid #cfc5ac",
        },
    },
    # ------------------------------------------------------------ 23
    "Sunset Warm": {
        "icon": "🌅",
        "tagline": "Light and friendly: peach-to-coral gradient, frosted cards, orange buttons.",
        "search": ["warm gradient UI", "sunset gradient website", "peach coral color palette", "friendly app landing page"],
        "tip": "background: linear-gradient(160deg, #fff1e6, #ffd9c2 45%, #ffb199);\n"
               "background: linear-gradient(90deg, #ff5e3a, #ff9a3c);   /* button */",
        "vars": {
            "page_bg": "linear-gradient(160deg, #fff1e6 0%, #ffd9c2 45%, #ffb199 100%)",
            "side_bg": "rgba(255,255,255,0.55)", "card_bg": "rgba(255,255,255,0.7)",
            "card_border": "1px solid rgba(255,255,255,0.85)", "card_shadow": "0 10px 30px rgba(220,90,60,0.18)",
            "blur": "blur(8px)", "radius": "22px", "text": "#4a1f1a", "muted": "#8a5a50",
            "accent": "#ff5e3a", "accent2": "#ff9a3c", "font": "'Poppins', sans-serif",
            "btn_bg": "linear-gradient(90deg, #ff5e3a, #ff9a3c)", "btn_text": "#ffffff",
            "btn_hover": "0 8px 22px rgba(255,94,58,0.5)", "btn_move": "translateY(-2px)",
            "btn_radius": "14px", "inset_bg": "rgba(255,255,255,0.6)",
            "input_border": "1px solid rgba(255,140,100,0.5)",
        },
    },
    # ------------------------------------------------------------ 24
    "Frutiger Aero": {
        "icon": "🫧",
        "tagline": "2000s optimism: sky-blue gradients, glossy bubble buttons, fresh green.",
        "search": ["Frutiger Aero", "Aero glass UI", "Windows Vista design", "glossy web 2.0 UI"],
        "tip": "background: linear-gradient(180deg, #7fd6ff, #1aa3e8 55%, #0f86c8);   /* gloss */\n"
               "box-shadow: 0 3px 8px rgba(11,110,168,0.45),\n            inset 0 1px 0 rgba(255,255,255,0.8);   /* shine */",
        "vars": {
            "page_bg": "linear-gradient(180deg, #bfe9ff 0%, #e8fbff 45%, #c8f5d0 100%)",
            "side_bg": "rgba(255,255,255,0.45)",
            "card_bg": "linear-gradient(180deg, rgba(255,255,255,0.88), rgba(255,255,255,0.5))",
            "card_border": "1px solid rgba(255,255,255,0.9)",
            "card_shadow": "0 8px 24px rgba(30,120,180,0.25), inset 0 1px 0 #ffffff", "blur": "blur(6px)",
            "radius": "20px", "text": "#0b3d5c", "muted": "#3f7191",
            "accent": "#1aa3e8", "accent2": "#42d17b",
            "btn_bg": "linear-gradient(180deg, #7fd6ff, #1aa3e8 55%, #0f86c8)", "btn_text": "#ffffff",
            "btn_border": "1px solid #0b6ea8",
            "btn_shadow": "0 3px 8px rgba(11,110,168,0.45), inset 0 1px 0 rgba(255,255,255,0.8)",
            "btn_hover": "0 5px 14px rgba(11,110,168,0.6), inset 0 1px 0 #ffffff", "btn_radius": "999px",
            "inset_bg": "rgba(255,255,255,0.7)", "inset": "inset 0 2px 5px rgba(30,120,180,0.25)",
            "input_border": "1px solid #9fd8f3",
        },
    },
    # ------------------------------------------------------------ 25
    "Liquid Glass": {
        "icon": "💧",
        "tagline": "Modern Apple-style glass: very blurry, bright edges, soft pastel light behind.",
        "search": ["liquid glass UI", "Apple liquid glass design", "iOS 26 design", "backdrop-filter saturate CSS"],
        "tip": "backdrop-filter: blur(24px) saturate(180%);\nbackground: rgba(255,255,255,0.45);\n"
               "box-shadow: inset 0 1px 1px rgba(255,255,255,0.9);   /* bright top edge */",
        "vars": {
            "page_bg": "radial-gradient(at 20% 15%, #a5d8ff 0, transparent 45%), radial-gradient(at 85% 20%, #ffd6e8 0, transparent 45%), radial-gradient(at 50% 90%, #d4c1ff 0, transparent 50%), #f4f6ff",
            "side_bg": "rgba(255,255,255,0.45)", "card_bg": "rgba(255,255,255,0.45)",
            "card_border": "1px solid rgba(255,255,255,0.7)",
            "card_shadow": "0 10px 40px rgba(80,90,150,0.18), inset 0 1px 1px rgba(255,255,255,0.9), inset 0 -1px 1px rgba(255,255,255,0.4)",
            "blur": "blur(24px) saturate(180%)", "radius": "28px", "text": "#1c1c2b", "muted": "#5f6078",
            "accent": "#007aff", "accent2": "#af52de", "font": "'Inter', sans-serif",
            "btn_bg": "rgba(255,255,255,0.55)", "btn_text": "#1c1c2b", "btn_border": "1px solid rgba(255,255,255,0.8)",
            "btn_shadow": "0 4px 14px rgba(80,90,150,0.18), inset 0 1px 1px #ffffff",
            "btn_hover": "0 8px 24px rgba(0,122,255,0.3), inset 0 1px 1px #ffffff", "btn_move": "translateY(-1px)",
            "btn_radius": "999px", "inset_bg": "rgba(255,255,255,0.5)",
            "input_border": "1px solid rgba(255,255,255,0.8)",
        },
    },
    # ------------------------------------------------------------ 26
    "Holographic": {
        "icon": "🔮",
        "tagline": "Iridescent rainbow borders and pastel foil gradients on a light page.",
        "search": ["holographic UI design", "iridescent gradient CSS", "gradient border CSS", "foil gradient web design"],
        "tip": "border: 2px solid transparent;\nbackground:\n  linear-gradient(white, white) padding-box,\n"
               "  linear-gradient(120deg,#7df9ff,#c9a0ff,#ff9ed8) border-box;   /* gradient border */",
        "vars": {
            "page_bg": "linear-gradient(135deg, #e0f7ff, #f3e0ff 35%, #ffe0f0 65%, #e0ffe9)",
            "side_bg": "rgba(255,255,255,0.6)", "card_bg": "rgba(255,255,255,0.85)",
            "card_border": "2px solid transparent", "card_shadow": "0 8px 28px rgba(138,92,246,0.15)",
            "radius": "20px", "text": "#2a2340", "muted": "#6e6590",
            "accent": "#8a5cf6", "accent2": "#22d3ee", "font": "'Poppins', sans-serif",
            "btn_bg": "linear-gradient(120deg, #7df9ff, #c9a0ff, #ff9ed8)", "btn_text": "#2a2340",
            "btn_hover": "0 6px 20px rgba(201,160,255,0.6)", "btn_move": "translateY(-2px)",
            "btn_radius": "14px", "inset_bg": "rgba(255,255,255,0.7)", "input_border": "1px solid #d9c8ff",
        },
        "extra": ".card, .stat, .st-key-widgets_card { background: linear-gradient(rgba(255,255,255,0.85), rgba(255,255,255,0.85)) padding-box, "
                 "linear-gradient(120deg, #7df9ff, #c9a0ff, #ff9ed8, #fff59d, #7df9ff) border-box; }"
                 ".stApp .hero h1 { background: linear-gradient(90deg, #22d3ee, #8a5cf6, #ff6fb5); "
                 "-webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; }",
    },
    # ------------------------------------------------------------ 27
    "Blueprint": {
        "icon": "📐",
        "tagline": "Engineer's drawing: blue grid paper, white dashed lines, monospace labels.",
        "search": ["blueprint UI design", "technical drawing website", "grid paper CSS background", "engineering style web design"],
        "tip": "background:\n  linear-gradient(rgba(255,255,255,.08) 1px, transparent 1px) 0 0 / 32px 32px,\n"
               "  linear-gradient(90deg, rgba(255,255,255,.08) 1px, transparent 1px) 0 0 / 32px 32px,\n  #1b4f9c;\n"
               "border: 1px dashed rgba(255,255,255,.65);",
        "vars": {
            "page_bg": "linear-gradient(rgba(255,255,255,0.08) 1px, transparent 1px) 0 0 / 32px 32px, linear-gradient(90deg, rgba(255,255,255,0.08) 1px, transparent 1px) 0 0 / 32px 32px, #1b4f9c",
            "side_bg": "#133a75", "card_bg": "rgba(255,255,255,0.05)",
            "card_border": "1px dashed rgba(255,255,255,0.65)", "radius": "2px",
            "text": "#eaf3ff", "muted": "#a9c6ee", "accent": "#ffffff", "accent2": "#7fd0ff",
            "font": "'Share Tech Mono', 'Courier New', monospace",
            "btn_bg": "transparent", "btn_text": "#ffffff", "btn_border": "1px solid #ffffff",
            "btn_hover": "0 0 0 3px rgba(255,255,255,0.25)", "btn_radius": "2px",
            "inset_bg": "rgba(255,255,255,0.08)", "input_border": "1px dashed rgba(255,255,255,0.6)",
        },
    },
    # ------------------------------------------------------------ 28
    "Dracula Dev": {
        "icon": "🧛",
        "tagline": "Popular code-editor theme: purple and pink on charcoal, monospace everywhere.",
        "search": ["Dracula theme", "developer portfolio dark theme", "code editor UI design", "dark purple dev website"],
        "tip": "background: #282a36;\ncolor: #f8f8f2;\naccent: #bd93f9;   /* purple */\n"
               "accent2: #ff79c6;   /* pink */\nfont-family: 'JetBrains Mono', monospace;",
        "vars": {
            "page_bg": "#282a36", "side_bg": "#21222c", "card_bg": "#2d2f3d",
            "card_border": "1px solid #44475a", "card_shadow": "0 6px 18px rgba(0,0,0,0.35)",
            "radius": "10px", "text": "#f8f8f2", "muted": "#9aa3d0",
            "accent": "#bd93f9", "accent2": "#ff79c6", "font": "'JetBrains Mono', monospace",
            "btn_bg": "#44475a", "btn_text": "#50fa7b", "btn_border": "1px solid #6272a4",
            "btn_hover": "0 0 0 2px #bd93f9", "btn_radius": "6px",
            "inset_bg": "#1e1f29", "input_border": "1px solid #44475a",
        },
        "extra": ".stApp .hero h1 { color: #bd93f9; }",
    },
    # ------------------------------------------------------------ 29
    "Gruvbox Retro": {
        "icon": "📟",
        "tagline": "Warm retro-dev palette: cream text, mustard yellow and brick red on brown-black.",
        "search": ["Gruvbox theme", "retro dark warm UI", "vintage terminal website", "gruvbox colors"],
        "tip": "background: #282828;\ncolor: #ebdbb2;   /* cream */\naccent: #fabd2f;   /* mustard */\n"
               "box-shadow: 0 3px 0 #b57614;   /* chunky button edge */",
        "vars": {
            "page_bg": "#282828", "side_bg": "#1d2021", "card_bg": "#32302f",
            "card_border": "1px solid #504945", "card_shadow": "4px 4px 0 #1d2021",
            "radius": "4px", "text": "#ebdbb2", "muted": "#a89984",
            "accent": "#fabd2f", "accent2": "#fb4934", "font": "'JetBrains Mono', monospace",
            "btn_bg": "#d79921", "btn_text": "#1d2021", "btn_border": "1px solid #b57614",
            "btn_shadow": "0 3px 0 #b57614", "btn_hover": "0 1px 0 #b57614", "btn_move": "translateY(2px)",
            "btn_radius": "4px", "inset_bg": "#1d2021", "input_border": "1px solid #665c54",
        },
    },
    # ------------------------------------------------------------ 30
    "Pixel Arcade": {
        "icon": "👾",
        "tagline": "8-bit game look: chunky pixel borders, scanlines and blocky fonts.",
        "search": ["pixel art UI", "8-bit website design", "retro game UI CSS", "NES.css"],
        "tip": "border: 4px solid #f5f5f5;\nborder-radius: 0;\nbox-shadow: 6px 6px 0 #000;   /* hard pixel shadow */\n"
               "font-family: 'Press Start 2P', monospace;",
        "vars": {
            "page_bg": "repeating-linear-gradient(0deg, rgba(255,255,255,0.03) 0 2px, transparent 2px 4px), #1a1a2e",
            "side_bg": "#10101e", "card_bg": "#16213e",
            "card_border": "4px solid #f5f5f5",
            "card_shadow": "inset -4px -4px 0 rgba(0,0,0,0.35), 6px 6px 0 #000000",
            "radius": "0px", "text": "#f5f5f5", "muted": "#9fb0d6",
            "accent": "#ffe66d", "accent2": "#4ecdc4",
            "font": "'VT323', monospace", "head_font": "'Press Start 2P', monospace",
            "btn_bg": "#e94560", "btn_text": "#ffffff", "btn_border": "4px solid #000000",
            "btn_shadow": "4px 4px 0 #000000", "btn_hover": "0 0 0 #000000", "btn_move": "translate(4px, 4px)",
            "btn_radius": "0px", "inset_bg": "#0f3460", "input_border": "4px solid #000000",
        },
        "extra": ".stApp p, .stApp li, .stApp label, .stApp .nm-table td, .stApp .stat .label { font-size: 1.2rem; }"
                 ".stApp .hero h1 { font-size: 1.6rem; line-height: 1.6; }"
                 ".stApp .card h3 { font-size: .85rem; line-height: 1.6; }"
                 ".stApp .stat .num { font-family: 'Press Start 2P', monospace; font-size: 1.1rem; }",
    },
    # ------------------------------------------------------------ 31
    "Comic Pop Art": {
        "icon": "💥",
        "tagline": "Comic-book style: halftone dots, thick ink lines, red and blue pop colours.",
        "search": ["comic book UI design", "pop art website", "halftone CSS background", "retro comic web design"],
        "tip": "background: radial-gradient(rgba(0,0,0,.12) 1.5px, transparent 1.6px) 0 0 / 14px 14px, #ffe14d;   /* halftone dots */\n"
               "border: 3px solid #111;\nbox-shadow: 6px 6px 0 #111;",
        "vars": {
            "page_bg": "radial-gradient(rgba(0,0,0,0.12) 1.5px, transparent 1.6px) 0 0 / 14px 14px, #ffe14d",
            "side_bg": "#0057d9", "side_text": "#ffffff", "card_bg": "#ffffff",
            "card_border": "3px solid #111111", "card_shadow": "6px 6px 0 #111111",
            "radius": "10px", "text": "#111111", "muted": "#444444",
            "accent": "#e3002b", "accent2": "#0057d9",
            "font": "'Comic Neue', 'Comic Sans MS', cursive", "head_font": "'Bangers', cursive",
            "btn_bg": "#e3002b", "btn_text": "#ffffff", "btn_border": "3px solid #111111",
            "btn_shadow": "4px 4px 0 #111111", "btn_hover": "0 0 0 #111111", "btn_move": "translate(4px, 4px)",
            "btn_radius": "8px", "inset_bg": "#fff6c9", "input_border": "3px solid #111111",
        },
        "extra": ".stApp .hero h1 { font-size: 3.4rem; letter-spacing: 3px; text-shadow: 3px 3px 0 #ffe14d, 5px 5px 0 #e3002b; }",
    },
    # ------------------------------------------------------------ 32
    "Hand-drawn Sketch": {
        "icon": "✏️",
        "tagline": "Doodle notebook feel: wobbly pencil borders, grid paper and handwriting fonts.",
        "search": ["hand drawn UI design", "sketch style website", "wobbly border CSS", "notebook paper web design"],
        "tip": "border: 2.5px solid #2b2b2b;\nborder-radius: 28px 6px 24px 8px / 8px 24px 6px 28px;   /* wobbly corners */\n"
               "box-shadow: 3px 4px 0 #2b2b2b;",
        "vars": {
            "page_bg": "linear-gradient(rgba(120,140,200,0.15) 1px, transparent 1px) 0 0 / 28px 28px, #fdfbf5",
            "side_bg": "#f6f1e3", "card_bg": "#fffef9",
            "card_border": "2.5px solid #2b2b2b", "card_shadow": "3px 4px 0 #2b2b2b",
            "radius": "28px 6px 24px 8px / 8px 24px 6px 28px", "text": "#2b2b2b", "muted": "#6d6d6d",
            "accent": "#e8590c", "accent2": "#1c7ed6",
            "font": "'Patrick Hand', cursive", "head_font": "'Caveat', cursive",
            "btn_bg": "#ffec99", "btn_text": "#2b2b2b", "btn_border": "2.5px solid #2b2b2b",
            "btn_shadow": "3px 3px 0 #2b2b2b", "btn_hover": "1px 1px 0 #2b2b2b", "btn_move": "translate(2px, 2px)",
            "btn_radius": "14px 4px 12px 6px", "inset_bg": "#fff8dc", "input_border": "2px solid #2b2b2b",
        },
        "extra": ".stApp p, .stApp li, .stApp label, .stApp .nm-table td { font-size: 1.1rem; }"
                 ".stApp h1, .stApp .card h3 { font-weight: 700; }"
                 ".stApp .hero h1 { font-size: 3.2rem; }",
    },
    # ------------------------------------------------------------ 33
    "Playful Edu": {
        "icon": "🦉",
        "tagline": "Duolingo-style learning app: white cards, chunky green buttons, friendly rounded type.",
        "search": ["Duolingo UI design", "gamified learning app design", "edtech UI design", "chunky button CSS"],
        "tip": "background: #58cc02;\nbox-shadow: 0 4px 0 #58a700;   /* chunky bottom edge */\n"
               "border: 2px solid #e5e5e5;   /* card outline */\nborder-radius: 16px;",
        "vars": {
            "page_bg": "#ffffff", "side_bg": "#f7f7f7", "card_bg": "#ffffff",
            "card_border": "2px solid #e5e5e5", "card_shadow": "0 4px 0 #e5e5e5",
            "radius": "18px", "text": "#3c3c3c", "muted": "#777777",
            "accent": "#58cc02", "accent2": "#1cb0f6", "font": "'Nunito', sans-serif",
            "btn_bg": "#58cc02", "btn_text": "#ffffff", "btn_shadow": "0 4px 0 #58a700",
            "btn_hover": "0 1px 0 #58a700", "btn_move": "translateY(3px)", "btn_radius": "16px",
            "inset_bg": "#f0f0f0", "input_border": "2px solid #e5e5e5",
        },
    },
    # ------------------------------------------------------------ 34
    "Nord Arctic": {
        "icon": "🧊",
        "tagline": "Cool, calm dark theme: slate backgrounds with icy blue accents.",
        "search": ["Nord theme", "arctic blue dark UI", "calm dark mode design", "nordtheme.com"],
        "tip": "background: #2e3440;\ncolor: #eceff4;\naccent: #88c0d0;   /* frost blue */\n"
               "border: 1px solid #4c566a;",
        "vars": {
            "page_bg": "#2e3440", "side_bg": "#272c36", "card_bg": "#3b4252",
            "card_border": "1px solid #4c566a", "card_shadow": "0 6px 18px rgba(0,0,0,0.25)",
            "radius": "10px", "text": "#eceff4", "muted": "#a7b1c4",
            "accent": "#88c0d0", "accent2": "#81a1c1", "font": "'Inter', sans-serif",
            "btn_bg": "#5e81ac", "btn_text": "#eceff4", "btn_hover": "0 0 0 3px rgba(136,192,208,0.4)",
            "btn_radius": "8px", "inset_bg": "#2e3440", "input_border": "1px solid #4c566a",
        },
    },
    # ------------------------------------------------------------ 35
    "Esports Lime": {
        "icon": "🎮",
        "tagline": "Gaming / esports energy: near-black panels, electric lime accent, sharp edges.",
        "search": ["esports website design", "gaming UI design", "neon lime dark UI", "game dashboard design"],
        "tip": "background: #14161d;\nborder-left: 4px solid #c6ff00;   /* lime edge */\n"
               "text-transform: uppercase;\nborder-radius: 4px;   /* sharp corners */",
        "vars": {
            "page_bg": "#0b0c10", "side_bg": "#07080b", "card_bg": "#14161d",
            "card_border": "1px solid #262a35", "radius": "4px",
            "text": "#f2f4f8", "muted": "#8b93a7", "accent": "#c6ff00", "accent2": "#7cff6b",
            "font": "'Chakra Petch', sans-serif",
            "btn_bg": "#c6ff00", "btn_text": "#0b0c10", "btn_hover": "0 0 22px rgba(198,255,0,0.6)",
            "btn_move": "translateY(-2px)", "btn_radius": "2px",
            "inset_bg": "#0b0c10", "input_border": "1px solid #2f3442",
        },
        "extra": ".card, .stat, .st-key-widgets_card { border-left: 4px solid var(--accent); }"
                 ".stApp h1, .stApp .card h3 { text-transform: uppercase; letter-spacing: 1.5px; }",
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
    "&family=JetBrains+Mono:wght@400;700&family=Press+Start+2P&family=VT323&family=Bangers"
    "&family=Comic+Neue:wght@400;700&family=Caveat:wght@600;700&family=Patrick+Hand"
    "&family=Poppins:wght@400;600;700&family=Fraunces:wght@600;800&family=Cormorant+Garamond:wght@600;700"
    "&family=Josefin+Sans:wght@400;600;700&family=Chakra+Petch:wght@500;700&display=swap');"
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
# 6. MAIN - sidebar with all designs (+ a small search box)
# =====================================================================

def main():
    all_names = list(DESIGNS.keys())

    # Sidebar menu (each item shows icon + name)
    with st.sidebar:
        st.markdown("### 🎨 Design Gallery")
        st.caption("Pick a design - the whole page changes")

        # Search box: type "dark", "glass", "retro"... to filter the list
        query = st.text_input(
            "Search designs", placeholder="Search: dark, glass, retro...",
            label_visibility="collapsed", key="design_search",
        ).strip().lower()
        names = [
            n for n in all_names
            if query in " ".join([n, DESIGNS[n]["tagline"], *DESIGNS[n]["search"]]).lower()
        ]
        if not names:
            st.caption("No match - showing all designs")
            names = all_names

        choice = st.radio(
            "Designs",
            names,
            format_func=lambda n: f"{DESIGNS[n]['icon']}  {n}",
            label_visibility="collapsed",
        )
        st.caption(f"{len(all_names)} styles · one Streamlit file")

    design = DESIGNS[choice]
    st.markdown(build_css(design), unsafe_allow_html=True)

    show_demo_page(choice, design)
    show_html('<div class="footer">Design Gallery · Built with Streamlit and pure CSS</div>')


main()
