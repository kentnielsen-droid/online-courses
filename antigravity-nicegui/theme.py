from nicegui import ui
from contextlib import contextmanager

@contextmanager
def frame(nav_title: str):
    """
    Standard layout frame for the portfolio.
    Includes a header, a drawer (optional, maybe for later), and a footer.
    """
    # Global Style
    ui.add_head_html('''
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
            
            body {
                font-family: 'Outfit', sans-serif;
                background-color: #0f172a;
                color: #e2e8f0;
                overflow-x: hidden;
            }
            
            /* Animated Background Gradient */
            .gradient-bg {
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                z-index: -1;
                background: radial-gradient(circle at 50% 50%, rgba(14, 165, 233, 0.15), transparent 50%),
                            radial-gradient(circle at 0% 0%, rgba(16, 185, 129, 0.1), transparent 40%),
                            radial-gradient(circle at 100% 100%, rgba(139, 92, 246, 0.1), transparent 40%);
                filter: blur(60px);
                animation: pulse 10s infinite alternate;
            }
            
            @keyframes pulse {
                0% { transform: scale(1); opacity: 0.8; }
                100% { transform: scale(1.1); opacity: 1; }
            }

            /* Glassmorphism Utilities */
            .glass {
                background: rgba(30, 41, 59, 0.4);
                backdrop-filter: blur(12px);
                -webkit-backdrop-filter: blur(12px);
                border: 1px solid rgba(255, 255, 255, 0.05);
            }
            
            .glass-card {
                background: rgba(30, 41, 59, 0.6);
                backdrop-filter: blur(16px);
                -webkit-backdrop-filter: blur(16px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            }
            
            .glass-card:hover {
                transform: translateY(-5px) scale(1.02);
                background: rgba(30, 41, 59, 0.8);
                border-color: rgba(56, 189, 248, 0.3);
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
            }

            /* Typography & Links */
            .nicegui-content {
                padding: 0;
                margin: 0;
                max-width: 100%;
            }
            a {
                color: #38bdf8;
                text-decoration: none;
                transition: color 0.2s;
            }
            a:hover {
                color: #7dd3fc;
            }
            
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

    with ui.header().classes('items-center justify-between glass text-white px-8 py-4 sticky top-0 z-50'):
        ui.label(nav_title).classes('text-2xl font-bold tracking-tight text-sky-400')
        with ui.row().classes('gap-6'):
            ui.link('Projects', '#projects').classes('text-slate-300 hover:text-white transition-colors')
            ui.link('About', '#about').classes('text-slate-300 hover:text-white transition-colors')
            ui.link('Contact', '#contact').classes('text-slate-300 hover:text-white transition-colors')

    # Main Content Container
    with ui.column().classes('w-full min-h-screen items-center'):
        yield

    with ui.footer().classes('bg-slate-900 text-slate-400 justify-center py-6 border-t border-slate-800'):
        ui.label('© 2024 AI/ML Portfolio. Built with NiceGUI.')
