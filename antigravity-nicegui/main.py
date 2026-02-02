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
        ui.element('div').props('id=top')

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

        # Hero Section (Framer-inspired)
        ui.add_body_html('''
            <section class="hero">
              <div class="container">
                <div class="hero-grid">
                  <div class="profile-card">
                    <div class="profile-photo" aria-label="Profile photo placeholder"></div>
                    <div class="profile-name" style="text-align:center;">MockName Doe</div>
                    <div style="display:flex; justify-content:center;">
                      <div class="profile-icon" title="Featured">
                        <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" style="width:18px;height:18px;fill:#07070a;">
                          <path d="M12 2l2.4 6.6L21 9.3l-5 4.1 1.7 6.6L12 16.9 6.3 20l1.7-6.6-5-4.1 6.6-.7L12 2z"/>
                        </svg>
                      </div>
                    </div>
                    <div class="profile-bio">
                      A software engineer who loves shipping clean, high-polish products with Python—end to end.
                    </div>
                    <div class="signature-wrap" aria-label="Signature">
                      <div class="signature">MockName</div>
                      <div class="signature-meta mono">Signed • 2026</div>
                    </div>
                    <div class="socials" aria-label="Social links">
                      <a class="social-link" href="https://example.com" target="_blank" rel="noreferrer" aria-label="Website">
                        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 100 20 10 10 0 000-20zm6.9 9H16.8a15.7 15.7 0 00-1.2-5 8.03 8.03 0 013.3 5zM12 4c.9 1.3 1.7 3.4 2.2 7H9.8c.5-3.6 1.3-5.7 2.2-7zM5.1 13h2.1c.1 1.8.4 3.5.9 5A8.03 8.03 0 015.1 13zm2.1-2H5.1a8.03 8.03 0 013.3-5 15.7 15.7 0 00-1.2 5zm2.6 2h4.4c-.5 3.6-1.3 5.7-2.2 7-.9-1.3-1.7-3.4-2.2-7zm6.0 0h2.1a8.03 8.03 0 01-3.3 5c.5-1.5.8-3.2.9-5zm-.9-2H9.1c.1-1.8.4-3.5.9-5h5.0c.5 1.5.8 3.2.9 5z"/></svg>
                      </a>
                      <a class="social-link" href="https://github.com" target="_blank" rel="noreferrer" aria-label="GitHub">
                        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 .5a12 12 0 00-3.8 23.4c.6.1.8-.2.8-.6v-2.3c-3.3.7-4-1.4-4-1.4-.6-1.4-1.3-1.8-1.3-1.8-1.1-.7.1-.7.1-.7 1.2.1 1.9 1.2 1.9 1.2 1.1 1.9 2.9 1.4 3.6 1.1.1-.8.4-1.4.7-1.7-2.6-.3-5.3-1.3-5.3-5.9 0-1.3.5-2.4 1.2-3.2-.1-.3-.5-1.5.1-3.1 0 0 1-.3 3.3 1.2a11.3 11.3 0 016 0C17.5 4.7 18.5 5 18.5 5c.6 1.6.2 2.8.1 3.1.8.8 1.2 1.9 1.2 3.2 0 4.6-2.7 5.6-5.3 5.9.4.4.8 1.1.8 2.2v3.3c0 .4.2.7.8.6A12 12 0 0012 .5z"/></svg>
                      </a>
                      <a class="social-link" href="https://x.com" target="_blank" rel="noreferrer" aria-label="X">
                        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M18.9 2H22l-7.2 8.2L23.4 22h-7.2l-5.6-7.2L4.5 22H1.4l7.7-8.8L.9 2h7.4l5.1 6.6L18.9 2zm-1.3 18h1.7L6.3 4H4.5l13.1 16z"/></svg>
                      </a>
                      <a class="social-link" href="https://www.linkedin.com" target="_blank" rel="noreferrer" aria-label="LinkedIn">
                        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4.98 3.5A2.48 2.48 0 102.5 5.98 2.48 2.48 0 004.98 3.5zM2.9 21.5h4.1V8.2H2.9v13.3zM9.2 8.2h3.9v1.8h.1c.5-1 1.8-2.1 3.8-2.1 4.1 0 4.9 2.7 4.9 6.2v7.4h-4.1v-6.6c0-1.6 0-3.6-2.2-3.6s-2.5 1.7-2.5 3.5v6.7H9.2V8.2z"/></svg>
                      </a>
                    </div>
                  </div>
                  <div>
                    <div class="eyebrow">
                      <span style="width:8px;height:8px;border-radius:999px;background:rgba(34,211,238,0.95);box-shadow:0 0 0 6px rgba(34,211,238,0.12)"></span>
                      AVAILABLE FOR FREELANCE • 2026
                    </div>
                    <div class="headline">SOFTWARE ENGINEER</div>
                    <div class="headline headline-outline">SOFTWARE ENGINEER</div>
                    <p class="subhead">
                      I build clean, delightful web experiences and data-powered products.
                      Focused on Python, UI polish, and shipping fast without sacrificing quality.
                    </p>
                    <div style="display:flex; gap:12px; flex-wrap:wrap; align-items:center; margin-top: 10px;">
                      <a class="btn-primary" href="#projects" onclick="document.getElementById('projects')?.scrollIntoView({behavior:'smooth'}); return false;">View projects</a>
                      <a class="nav-link" style="background:rgba(255,255,255,0.05); border-color: rgba(255,255,255,0.10);" href="#contact" onclick="document.getElementById('contact')?.scrollIntoView({behavior:'smooth'}); return false;">Get in touch</a>
                      <span class="mono muted" style="font-size:12px; padding-left:4px;">Based in Anywhere • Remote-friendly</span>
                    </div>
                    <div class="stats">
                      <div class="stat">
                        <div class="stat-k">12+</div>
                        <div class="stat-l">Years experience</div>
                      </div>
                      <div class="stat">
                        <div class="stat-k">46+</div>
                        <div class="stat-l">Projects shipped</div>
                      </div>
                      <div class="stat">
                        <div class="stat-k">20+</div>
                        <div class="stat-l">Clients worldwide</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </section>
        ''')

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
