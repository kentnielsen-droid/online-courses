from nicegui import ui
import theme
import asyncio
from projects import get_projects
from nicegui import ui
import theme
import asyncio
from projects import get_projects
from components import project_card, project_detail_dialog, skills_widget, timeline_widget, article_card, testimonial_card
from demos import sentiment_demo, churn_demo

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

            with ui.row().classes('gap-6'):
                ui.button('View Projects', on_click=lambda: ui.run_javascript('document.getElementById("projects").scrollIntoView({behavior: "smooth"})')).props('unelevated color=blue-9 text-color=white size=lg').classes('px-8 py-2 font-bold rounded-full shadow-[0_0_20px_rgba(56,189,248,0.3)] hover:shadow-[0_0_30px_rgba(56,189,248,0.5)] transition-shadow')
                ui.button('Download Resume', icon='download', on_click=lambda: ui.notify('Resume download started (mock)')).props('outline color=cyan-7 text-color=cyan-4 size=lg').classes('px-8 py-2 font-bold rounded-full border-2 hover:bg-cyan-900/20')

        # Skills Section
        with ui.column().classes('w-full max-w-6xl py-20 px-6 reveal') as skills_section:
            skills_section.props('id=skills')
            skills_widget()

        # Experience Section
        with ui.column().classes('w-full max-w-4xl py-20 px-6 reveal') as experience_section:
            experience_section.props('id=experience')
            ui.label('Professional Journey').classes('text-4xl font-bold text-slate-100 mb-12 text-center w-full')
            timeline_widget()

        # Projects Section
        with ui.column().classes('w-full max-w-6xl py-20 px-6 reveal') as projects_section:
            projects_section.props('id=projects')
            ui.label('Featured Projects').classes('text-4xl font-bold text-slate-100 mb-16 text-center w-full')
            
            projects = get_projects()
            with ui.grid(columns=3).classes('w-full gap-8'):
                for project in projects:
                    project_card(project, on_click=project_detail_dialog)

        # Articles Section
        with ui.column().classes('w-full max-w-6xl py-20 px-6 reveal') as articles_section:
            articles_section.props('id=articles')
            ui.label('Latest Thoughts').classes('text-4xl font-bold text-slate-100 mb-12 text-center w-full')
            with ui.grid(columns=2).classes('w-full gap-8'):
                article_card("The Future of LLMs in Production", "Exploring the challenges and opportunities of deploying Large Language Models in enterprise environments.", "Oct 24, 2024", "https://medium.com")
                article_card("Understanding Attention Mechanisms", "A deep dive into the mathematics behind the Transformer architecture.", "Sep 15, 2024", "https://medium.com")

        # Testimonials Section
        with ui.column().classes('w-full max-w-6xl py-20 px-6 reveal') as testimonials_section:
            testimonials_section.props('id=testimonials')
            ui.label('What People Say').classes('text-4xl font-bold text-slate-100 mb-12 text-center w-full')
            with ui.grid(columns=2).classes('w-full gap-8'):
                testimonial_card("One of the most talented data scientists I've worked with. Delivered exceptional results on our churn prediction model.", "Sarah Chen", "CTO at TechCorp")
                testimonial_card("Great communicator and technically brilliant. Transformed our data infrastructure.", "Michael Ross", "Product Manager")

        # About Section
        with ui.column().classes('w-full max-w-4xl py-32 px-6 items-center text-center reveal') as about_section:
            about_section.props('id=about')
            ui.label('About Me').classes('text-4xl font-bold text-slate-100 mb-8')
            ui.label('I am passionate about turning data into actionable insights. With a background in Computer Science and Statistics, I specialize in Machine Learning, NLP, and Computer Vision.').classes('text-xl text-slate-200 leading-relaxed')

        # Contact Section
        with ui.column().classes('w-full py-32 items-center reveal') as contact_section:
            contact_section.props('id=contact')
            with ui.card().classes('glass p-12 items-center text-center max-w-3xl w-full mx-6 border border-slate-700'):
                ui.label('Get In Touch').classes('text-4xl font-bold text-slate-100 mb-6')
                ui.label('Open for collaborations and new opportunities.').classes('text-lg text-slate-200 mb-10')
                ui.button('Email Me', icon='mail', on_click=lambda: ui.open('mailto:hello@example.com')).props('unelevated color=green-8 text-color=white size=xl').classes('px-10 py-3 rounded-full font-bold shadow-lg hover:scale-105 transition-transform')

@ui.page('/demo/{project_id}')
def project_demo(project_id: str):
    with theme.frame('Project Demo'):
        with ui.column().classes('w-full max-w-4xl mx-auto py-20 px-6'):
            if project_id == 'sentiment-analysis':
                ui.label('Sentiment Analysis Demo').classes('text-4xl font-bold text-slate-100 mb-4')
                ui.label('Enter text below to analyze its sentiment using our mock AI model.').classes('text-lg text-slate-300 mb-8')
                sentiment_demo()
            elif project_id == 'customer-churn':
                ui.label('Customer Churn Prediction').classes('text-4xl font-bold text-slate-100 mb-4')
                ui.label('Adjust the customer parameters to predict the likelihood of churn.').classes('text-lg text-slate-300 mb-8')
                churn_demo()
            else:
                ui.label('Demo not found').classes('text-2xl text-red-400')
            
            ui.button('Back to Portfolio', icon='arrow_back', on_click=lambda: ui.navigate.to('/')).props('outline color=slate-400').classes('mt-12 hover:bg-slate-800')

ui.run(title='My AI Portfolio')
