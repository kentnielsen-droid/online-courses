from nicegui import ui
from contextlib import contextmanager

@contextmanager
def frame(nav_title: str):
    """
    Standard layout frame for the portfolio.
    Includes a header, a drawer (optional, maybe for later), and a footer.
    """
    # Global Style (Framer-like portfolio theme)
    ui.add_head_html('''
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@600;700&display=swap');
            
            body {
                font-family: 'Outfit', sans-serif;
                background-color: #07070a;
                color: #f8fafc;
                overflow-x: hidden;
            }
            
            :root {
                --bg: #07070a;
                --panel: rgba(255, 255, 255, 0.06);
                --panel-strong: rgba(255, 255, 255, 0.10);
                --border: rgba(255, 255, 255, 0.10);
                --border-strong: rgba(255, 255, 255, 0.16);
                --text: #f8fafc;
                --muted: rgba(248, 250, 252, 0.70);
                --muted2: rgba(248, 250, 252, 0.55);
                --accent: #7c3aed;
                --accent2: #22d3ee;
            }

            /* Animated Background Gradient */
            .gradient-bg {
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                z-index: -1;
                background:
                    radial-gradient(circle at 10% 10%, rgba(124, 58, 237, 0.22), transparent 45%),
                    radial-gradient(circle at 90% 15%, rgba(34, 211, 238, 0.14), transparent 40%),
                    radial-gradient(circle at 50% 110%, rgba(16, 185, 129, 0.10), transparent 55%);
                filter: blur(70px);
                animation: pulse 12s infinite alternate;
            }
            
            @keyframes pulse {
                0% { transform: scale(1); opacity: 0.8; }
                100% { transform: scale(1.1); opacity: 1; }
            }

            /* Glassmorphism Utilities */
            .glass {
                background: var(--panel);
                backdrop-filter: blur(16px);
                -webkit-backdrop-filter: blur(16px);
                border: 1px solid var(--border);
            }
            
            .glass-card {
                background: rgba(255, 255, 255, 0.06);
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
                border: 1px solid var(--border);
                box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            }
            
            .glass-card:hover {
                transform: translateY(-5px) scale(1.01);
                background: rgba(255, 255, 255, 0.10);
                border-color: rgba(124, 58, 237, 0.45);
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
            }

            /* Typography & Links */
            .nicegui-content {
                padding: 0;
                margin: 0;
                max-width: 100%;
            }
            a {
                color: rgba(248, 250, 252, 0.80);
                text-decoration: none;
                transition: all 0.2s;
                font-weight: 600; /* Bolder links */
            }
            a:hover {
                color: rgba(248, 250, 252, 1.0);
            }

            /* Header */
            .portfolio-header {
                position: sticky;
                top: 0;
                z-index: 60;
                padding: 14px 20px;
                background: rgba(7, 7, 10, 0.55);
                backdrop-filter: blur(18px);
                -webkit-backdrop-filter: blur(18px);
                border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            }
            .header-inner {
                width: 100%;
                max-width: 1120px;
                margin: 0 auto;
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 12px;
            }
            .brand {
                display: inline-flex;
                align-items: center;
                gap: 10px;
                color: var(--text);
                font-weight: 800;
                letter-spacing: -0.02em;
                font-size: 18px;
            }
            .brand-dot {
                width: 10px;
                height: 10px;
                border-radius: 999px;
                background: linear-gradient(135deg, var(--accent), var(--accent2));
                box-shadow: 0 0 0 6px rgba(124, 58, 237, 0.16);
            }
            .nav {
                display: flex;
                align-items: center;
                gap: 18px;
            }
            .nav-link {
                font-weight: 600;
                font-size: 13px;
                color: rgba(248, 250, 252, 0.72);
                padding: 8px 10px;
                border-radius: 10px;
                border: 1px solid transparent;
                transition: background 160ms ease, border-color 160ms ease, color 160ms ease;
            }
            .nav-link:hover {
                background: rgba(255, 255, 255, 0.06);
                border-color: rgba(255, 255, 255, 0.10);
                color: rgba(248, 250, 252, 0.95);
            }
            .btn-primary {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                gap: 8px;
                border-radius: 999px;
                padding: 10px 14px;
                font-weight: 700;
                font-size: 13px;
                color: #07070a;
                background: linear-gradient(135deg, var(--accent), var(--accent2));
                border: 1px solid rgba(255, 255, 255, 0.10);
                box-shadow: 0 16px 40px rgba(124, 58, 237, 0.18);
                transition: transform 160ms ease, box-shadow 160ms ease, filter 160ms ease;
            }
            .btn-primary:hover { transform: translateY(-1px); filter: brightness(1.02); }
            .btn-primary:active { transform: translateY(0px); }

            /* Hero */
            .container {
                width: 100%;
                max-width: 1120px;
                margin: 0 auto;
                padding: 0 20px;
            }
            .hero {
                padding: 84px 0 56px;
            }
            .hero-grid {
                display: grid;
                grid-template-columns: 0.75fr 1.25fr;
                gap: 28px;
                align-items: start;
            }
            @media (max-width: 980px) {
                .hero-grid { grid-template-columns: 1fr; }
            }
            .eyebrow {
                display: inline-flex;
                align-items: center;
                gap: 8px;
                font-size: 12px;
                font-weight: 700;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                color: rgba(248, 250, 252, 0.70);
                padding: 10px 12px;
                border-radius: 999px;
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.10);
                width: fit-content;
            }
            .headline {
                font-size: clamp(48px, 7vw, 92px);
                line-height: 0.92;
                letter-spacing: -0.05em;
                font-weight: 800;
                margin: 18px 0 12px;
                color: rgba(248, 250, 252, 0.96);
            }
            .headline-outline {
                color: transparent;
                -webkit-text-stroke: 1px rgba(248, 250, 252, 0.35);
                text-stroke: 1px rgba(248, 250, 252, 0.35);
            }
            .subhead {
                font-size: 18px;
                line-height: 1.55;
                color: rgba(248, 250, 252, 0.72);
                max-width: 64ch;
                margin: 0 0 20px;
            }
            .stats {
                display: grid;
                grid-template-columns: repeat(3, minmax(0, 1fr));
                gap: 12px;
                margin-top: 18px;
            }
            @media (max-width: 700px) {
                .stats { grid-template-columns: 1fr; }
            }
            .stat {
                padding: 14px 14px;
                border-radius: 16px;
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.10);
            }
            .stat-k {
                font-size: 26px;
                font-weight: 800;
                letter-spacing: -0.03em;
                color: rgba(248, 250, 252, 0.96);
            }
            .stat-l {
                font-size: 12px;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                font-weight: 700;
                color: rgba(248, 250, 252, 0.55);
                margin-top: 3px;
            }
            .side-card {
                border-radius: 22px;
                padding: 16px;
                background: rgba(255, 255, 255, 0.06);
                border: 1px solid rgba(255, 255, 255, 0.12);
            }

            /* Profile card (hero left card) */
            .profile-card {
                border-radius: 26px;
                padding: 18px;
                background: rgba(255, 255, 255, 0.06);
                border: 1px solid rgba(255, 255, 255, 0.12);
                box-shadow: 0 22px 70px rgba(0, 0, 0, 0.45);
            }
            .profile-photo {
                width: 100%;
                aspect-ratio: 1 / 1;
                border-radius: 22px;
                border: 1px solid rgba(255, 255, 255, 0.14);
                overflow: hidden;
                background:
                    radial-gradient(circle at 30% 25%, rgba(34, 211, 238, 0.35), transparent 45%),
                    radial-gradient(circle at 70% 80%, rgba(124, 58, 237, 0.35), transparent 55%),
                    linear-gradient(135deg, rgba(255, 255, 255, 0.12), rgba(255, 255, 255, 0.02));
                position: relative;
            }
            .profile-photo::after {
                content: "";
                position: absolute;
                inset: 0;
                background:
                    radial-gradient(circle at 55% 35%, rgba(0, 0, 0, 0.50), transparent 55%),
                    radial-gradient(circle at 50% 120%, rgba(0, 0, 0, 0.65), transparent 55%);
                mix-blend-mode: overlay;
                pointer-events: none;
            }
            .profile-name {
                margin-top: 16px;
                font-size: 34px;
                line-height: 1.05;
                font-weight: 800;
                letter-spacing: -0.04em;
                color: rgba(248, 250, 252, 0.96);
            }
            .profile-icon {
                width: 36px;
                height: 36px;
                border-radius: 999px;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                background: linear-gradient(135deg, var(--accent), var(--accent2));
                border: 1px solid rgba(255, 255, 255, 0.14);
                box-shadow: 0 18px 35px rgba(124, 58, 237, 0.22);
                margin: 14px auto 0;
            }
            .profile-bio {
                margin-top: 14px;
                text-align: center;
                font-size: 15px;
                line-height: 1.45;
                color: rgba(248, 250, 252, 0.66);
                padding: 0 10px;
            }
            .socials {
                display: flex;
                justify-content: center;
                gap: 14px;
                margin-top: 18px;
                padding-top: 14px;
                border-top: 1px solid rgba(255, 255, 255, 0.10);
            }
            .social-link {
                width: 38px;
                height: 38px;
                border-radius: 999px;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.10);
                transition: transform 160ms ease, background 160ms ease, border-color 160ms ease;
            }
            .social-link:hover {
                transform: translateY(-1px);
                background: rgba(255, 255, 255, 0.08);
                border-color: rgba(124, 58, 237, 0.35);
            }
            .social-link svg {
                width: 18px;
                height: 18px;
                fill: rgba(248, 250, 252, 0.75);
            }
            .social-link:hover svg {
                fill: rgba(248, 250, 252, 0.92);
            }

            /* Signature */
            .signature-wrap {
                margin-top: 14px;
                padding-top: 14px;
                border-top: 1px dashed rgba(255, 255, 255, 0.12);
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 12px;
            }
            .signature {
                font-family: 'Dancing Script', 'Outfit', sans-serif;
                font-size: 26px;
                line-height: 1;
                color: rgba(248, 250, 252, 0.82);
                letter-spacing: -0.01em;
                transform: rotate(-1deg);
                white-space: nowrap;
            }
            .signature-meta {
                font-size: 11px;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                font-weight: 700;
                color: rgba(248, 250, 252, 0.55);
            }

            /* Skills marquee */
            .skills-card {
                border-radius: 22px;
                padding: 18px;
                background: rgba(255, 255, 255, 0.06);
                border: 1px solid rgba(255, 255, 255, 0.12);
                width: 100%;
            }
            .skills-title {
                font-size: 22px;
                font-weight: 800;
                letter-spacing: -0.02em;
                margin-bottom: 10px;
                background: linear-gradient(90deg, rgba(34,211,238,0.95), rgba(124,58,237,0.95));
                -webkit-background-clip: text;
                background-clip: text;
                color: transparent;
            }
            .skills-subtitle {
                color: rgba(248, 250, 252, 0.62);
                font-size: 14px;
                margin-bottom: 14px;
            }
            .marquee {
                position: relative;
                overflow: hidden;
                border-radius: 18px;
                background: rgba(255, 255, 255, 0.04);
                border: 1px solid rgba(255, 255, 255, 0.10);
            }
            .marquee::before,
            .marquee::after {
                content: "";
                position: absolute;
                top: 0;
                bottom: 0;
                width: 56px;
                pointer-events: none;
                z-index: 2;
            }
            .marquee::before {
                left: 0;
                background: linear-gradient(90deg, rgba(7,7,10,0.85), rgba(7,7,10,0.0));
            }
            .marquee::after {
                right: 0;
                background: linear-gradient(270deg, rgba(7,7,10,0.85), rgba(7,7,10,0.0));
            }
            .marquee-track {
                display: flex;
                width: max-content;
                gap: 10px;
                padding: 12px;
                animation: marquee-scroll 26s linear infinite;
            }
            .marquee.marquee-slow .marquee-track { animation-duration: 34s; }
            .marquee:hover .marquee-track { animation-play-state: paused; }
            @media (prefers-reduced-motion: reduce) {
                .marquee-track { animation: none; }
            }
            @keyframes marquee-scroll {
                from { transform: translateX(0); }
                to { transform: translateX(-50%); }
            }
            .pill {
                display: inline-flex;
                align-items: center;
                gap: 8px;
                padding: 10px 12px;
                border-radius: 999px;
                background: rgba(255, 255, 255, 0.06);
                border: 1px solid rgba(255, 255, 255, 0.10);
                color: rgba(248, 250, 252, 0.82);
                font-weight: 700;
                font-size: 13px;
                white-space: nowrap;
                transition: transform 160ms ease, border-color 160ms ease, background 160ms ease;
            }
            .pill:hover {
                transform: translateY(-1px);
                background: rgba(255, 255, 255, 0.09);
                border-color: rgba(124, 58, 237, 0.35);
            }
            .pill-dot {
                width: 8px;
                height: 8px;
                border-radius: 999px;
                background: linear-gradient(135deg, var(--accent), var(--accent2));
                box-shadow: 0 0 0 6px rgba(124, 58, 237, 0.12);
            }
            .mono {
                font-family: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
            }
            .badge {
                display: inline-flex;
                align-items: center;
                gap: 8px;
                font-size: 12px;
                font-weight: 700;
                padding: 10px 12px;
                border-radius: 999px;
                background: rgba(124, 58, 237, 0.14);
                border: 1px solid rgba(124, 58, 237, 0.35);
                color: rgba(248, 250, 252, 0.92);
                width: fit-content;
            }
            .avatar {
                width: 72px;
                height: 72px;
                border-radius: 20px;
                background: linear-gradient(135deg, rgba(124, 58, 237, 0.9), rgba(34, 211, 238, 0.8));
                border: 1px solid rgba(255, 255, 255, 0.16);
                box-shadow: 0 22px 55px rgba(0, 0, 0, 0.45);
            }
            .muted { color: rgba(248, 250, 252, 0.62); }
            
            /* Scroll Reveal Animation Class */
            .reveal {
                opacity: 0;
                transform: translateY(30px);
                transition: all 0.8s ease-out;
            }
            .reveal.active {
                opacity: 1;
                transform: translateY(0);
            }
            
            /* Typing Cursor */
            .typing-cursor::after {
                content: '|';
                animation: blink 1s step-start infinite;
            }
            @keyframes blink {
                50% { opacity: 0; }
            }
        </style>
    ''')

    # Background Element
    ui.element('div').classes('gradient-bg')

    # Header
    ui.add_body_html('''
        <header class="portfolio-header">
          <div class="header-inner">
            <a class="brand" href="#top" onclick="window.scrollTo({top: 0, behavior: 'smooth'}); return false;">
              <span class="brand-dot"></span>
              <span>MockName</span>
            </a>
            <nav class="nav">
              <a class="nav-link" href="#projects" onclick="document.getElementById('projects')?.scrollIntoView({behavior:'smooth'}); return false;">Projects</a>
              <a class="nav-link" href="#experience" onclick="document.getElementById('experience')?.scrollIntoView({behavior:'smooth'}); return false;">Experience</a>
              <a class="nav-link" href="#about" onclick="document.getElementById('about')?.scrollIntoView({behavior:'smooth'}); return false;">About</a>
              <a class="nav-link" href="#contact" onclick="document.getElementById('contact')?.scrollIntoView({behavior:'smooth'}); return false;">Contact</a>
              <a class="btn-primary" href="#contact" onclick="document.getElementById('contact')?.scrollIntoView({behavior:'smooth'}); return false;">Let’s work</a>
            </nav>
          </div>
        </header>
    ''')

    # Main Content Container
    with ui.column().classes('w-full min-h-screen items-center'):
        yield

    with ui.footer().classes('bg-slate-900 text-slate-400 justify-center py-6 border-t border-slate-800'):
        ui.label('© 2024 AI/ML Portfolio. Built with NiceGUI.')
