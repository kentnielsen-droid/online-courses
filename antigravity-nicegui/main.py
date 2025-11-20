from nicegui import ui
import theme
import asyncio
from projects import get_projects
from components import project_card, project_detail_dialog, skills_widget

# Page Layout
@ui.page('/')
async def index():
    with theme.frame('DK Portfolio'):
        # Scroll Reveal Script
        ui.add_body_html('''
            <script>
                const observer = new IntersectionObserver((entries) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            entry.target.classList.add('active');
                        }
                    });
                });
                // Wait for elements to exist
                setTimeout(() => {
                    document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));
                }, 100);
            </script>
        ''')

        # Hero Section
        with ui.column().classes('w-full max-w-5xl py-32 px-6 items-center text-center'):
            ui.label('Hello, I\'m a').classes('text-5xl md:text-7xl font-extrabold text-slate-100 mb-2')
            
            # Typing Effect
            typing_label = ui.label('Data Scientist').classes('text-5xl md:text-7xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-sky-400 to-emerald-400 mb-8 typing-cursor')
            
            async def type_effect():
                roles = ['Data Scientist', 'ML Engineer', 'AI Researcher', 'Python Dev']
                while True:
                    for role in roles:
                        for i in range(len(role) + 1):
                            typing_label.set_text(role[:i])
                            await asyncio.sleep(0.1)
                        await asyncio.sleep(2)
                        for i in range(len(role), -1, -1):
                            typing_label.set_text(role[:i])
                            await asyncio.sleep(0.05)
            
            ui.timer(0.1, type_effect, once=True)

            ui.label('I build intelligent systems and scalable AI solutions.').classes('text-xl text-slate-300 max-w-2xl leading-relaxed mb-10')
            with ui.row().classes('gap-6'):
                ui.button('View Projects', on_click=lambda: ui.run_javascript('document.getElementById("projects").scrollIntoView({behavior: "smooth"})')).props('unelevated color=sky text-color=slate-900 size=lg').classes('px-8 py-2 font-bold rounded-full shadow-[0_0_20px_rgba(56,189,248,0.3)] hover:shadow-[0_0_30px_rgba(56,189,248,0.5)] transition-shadow')
                ui.button('Contact Me', on_click=lambda: ui.run_javascript('document.getElementById("contact").scrollIntoView({behavior: "smooth"})')).props('outline color=sky size=lg').classes('px-8 py-2 font-bold rounded-full border-2 hover:bg-sky-400/10')

        # Skills Section
        with ui.column().classes('w-full max-w-6xl py-20 px-6 reveal') as skills_section:
            skills_section.props('id=skills')
            skills_widget()

        # Projects Section
        with ui.column().classes('w-full max-w-6xl py-20 px-6 reveal') as projects_section:
            projects_section.props('id=projects')
            ui.label('Featured Projects').classes('text-4xl font-bold text-slate-100 mb-16 text-center w-full')
            
            projects = get_projects()
            with ui.grid(columns=3).classes('w-full gap-8'):
                for project in projects:
                    project_card(project, on_click=project_detail_dialog)

        # About Section
        with ui.column().classes('w-full max-w-4xl py-32 px-6 items-center text-center reveal') as about_section:
            about_section.props('id=about')
            ui.label('About Me').classes('text-4xl font-bold text-slate-100 mb-8')
            ui.label('I am passionate about turning data into actionable insights. With a background in Computer Science and Statistics, I specialize in Machine Learning, NLP, and Computer Vision.').classes('text-xl text-slate-300 leading-relaxed')

        # Contact Section
        with ui.column().classes('w-full py-32 items-center reveal') as contact_section:
            contact_section.props('id=contact')
            with ui.card().classes('glass p-12 items-center text-center max-w-3xl w-full mx-6'):
                ui.label('Get In Touch').classes('text-4xl font-bold text-slate-100 mb-6')
                ui.label('Open for collaborations and new opportunities.').classes('text-lg text-slate-300 mb-10')
                ui.button('Email Me', icon='mail', on_click=lambda: ui.open('mailto:hello@example.com')).props('unelevated color=emerald text-color=slate-900 size=xl').classes('px-10 py-3 rounded-full font-bold shadow-lg hover:scale-105 transition-transform')

ui.run(title='My AI Portfolio')
