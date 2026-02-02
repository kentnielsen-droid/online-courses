from nicegui import ui
from projects import Project
from demos import sentiment_demo, churn_demo

def project_card(project: Project, on_click):
    with ui.card().classes('glass-card w-full max-w-sm cursor-pointer no-shadow') as card:
        card.on('click', lambda: on_click(project))
        ui.image(project.image_url).classes('h-48 w-full object-cover rounded-t-lg opacity-90 hover:opacity-100 transition-opacity duration-300')
        with ui.card_section():
            ui.label(project.title).classes('text-xl font-bold text-slate-100 mb-2')
            ui.label(project.description).classes('text-sm text-slate-300 mb-4 line-clamp-3')
            with ui.row().classes('gap-2 flex-wrap mb-4'):
                for tag in project.tags:
                    ui.label(tag).classes('text-xs px-2 py-1 rounded-full bg-slate-700/80 text-sky-300 border border-slate-600')

def _pill_html(label: str) -> str:
    return f'<span class="pill"><span class="pill-dot"></span>{label}</span>'


def skills_widget():
    """Framer-style sliding 'Technical Arsenal' marquee."""
    skills_row_1 = [
        # Data + APIs
        "Python", "SQL", "Pandas", "Polars", "PyArrow", "Requests", "HTTPX", "BeautifulSoup",
        "FastAPI", "Pydantic", "OpenAPI", "gRPC",
        # ML / DL
        "NumPy", "Scikit-learn", "PyTorch", "TorchVision", "XGBoost", "LightGBM",
        "Transformers", "LangChain", "Sentence Transformers",
    ]
    skills_row_2 = [
        # Data eng + orchestration
        "Postgres", "SQLite", "Redis", "Kafka", "Spark", "Airflow", "dbt",
        # MLOps / deployment
        "Docker", "Kubernetes", "CI/CD", "GitHub Actions", "MLflow", "ONNX", "BentoML",
        # Serving / monitoring
        "Model Serving", "A/B Testing", "Prometheus", "Grafana", "Evidently", "Data Drift", "Feature Store",
        # Cloud
        "AWS", "S3", "Lambda", "CloudWatch",
    ]

    def row_markup(items: list[str]) -> str:
        # Duplicate content so CSS can scroll -50% for seamless loop.
        base = ''.join(_pill_html(x) for x in items)
        return base + base

    with ui.element('div').classes('skills-card'):
        ui.html('<div class="skills-title">Technical Arsenal</div>', sanitize=False)
        ui.html('<div class="skills-subtitle">Full-stack AI/ML engineering: data → models → deployment → monitoring.</div>', sanitize=False)

        ui.html(f'''
            <div class="marquee">
              <div class="marquee-track">
                {row_markup(skills_row_1)}
              </div>
            </div>
        ''', sanitize=False)
        ui.html('<div style="height:10px"></div>', sanitize=False)
        ui.html(f'''
            <div class="marquee marquee-slow">
              <div class="marquee-track">
                {row_markup(skills_row_2)}
              </div>
            </div>
        ''', sanitize=False)

def timeline_widget():
    experience = [
        {"role": "Senior Data Scientist", "company": "TechCorp AI", "date": "2022 - Present", "desc": "Leading a team of 5 ML engineers building LLM-based customer support agents."},
        {"role": "Machine Learning Engineer", "company": "DataFlow Systems", "date": "2020 - 2022", "desc": "Deployed computer vision models for manufacturing defect detection. Optimized inference time by 40%."},
        {"role": "Data Analyst", "company": "FinTech Solutions", "date": "2018 - 2020", "desc": "Built automated reporting dashboards and predictive models for credit risk assessment."}
    ]
    
    with ui.column().classes('w-full gap-8 border-l-2 border-slate-700 ml-4 pl-8 relative'):
        for job in experience:
            with ui.column().classes('relative'):
                # Dot on the timeline
                ui.element('div').classes('absolute -left-[41px] top-1 w-5 h-5 rounded-full bg-sky-500 border-4 border-slate-900 shadow-[0_0_10px_rgba(14,165,233,0.5)]')
                
                ui.label(job['date']).classes('text-sm text-sky-400 font-mono mb-1 font-bold')
                ui.label(job['role']).classes('text-xl font-bold text-slate-100')
                ui.label(job['company']).classes('text-md text-slate-300 mb-2')
                ui.label(job['desc']).classes('text-slate-200 leading-relaxed')

def article_card(title, summary, date, link):
    with ui.card().classes('glass-card w-full p-6 hover:border-sky-500 cursor-pointer group') as card:
        card.on('click', lambda: ui.open(link, new_tab=True))
        with ui.row().classes('justify-between items-start w-full mb-4'):
            ui.icon('article', size='sm', color='sky-400').classes('opacity-100')
            ui.label(date).classes('text-xs text-slate-400 font-mono')
        
        ui.label(title).classes('text-lg font-bold text-slate-100 mb-2 group-hover:text-sky-400 transition-colors')
        ui.label(summary).classes('text-sm text-slate-300 line-clamp-2')

def testimonial_card(quote, author, role):
    with ui.card().classes('glass p-8 relative border border-slate-700/50'):
        ui.icon('format_quote', size='lg', color='slate-600').classes('absolute top-4 right-4 opacity-50')
        ui.label(quote).classes('text-lg text-slate-200 italic mb-6 leading-relaxed')
        with ui.row().classes('items-center gap-3'):
            ui.avatar(icon='person', color='slate-800', text_color='slate-300').classes('border border-slate-600')
            with ui.column().classes('gap-0'):
                ui.label(author).classes('font-bold text-slate-100')
                ui.label(role).classes('text-xs text-sky-400')

def project_detail_dialog(project: Project):
    with ui.dialog() as dialog, ui.card().classes('w-full max-w-2xl bg-slate-900 border border-slate-700'):
        with ui.row().classes('w-full justify-between items-start'):
            ui.label(project.title).classes('text-2xl font-bold text-sky-400')
            ui.button(icon='close', on_click=dialog.close).props('flat round dense color=grey')
        
        ui.image(project.image_url).classes('h-64 w-full object-cover rounded-lg my-4')
        
        with ui.row().classes('gap-2 mb-4'):
            for tag in project.tags:
                ui.label(tag).classes('text-xs px-2 py-1 rounded-full bg-slate-800 text-sky-300 border border-slate-700')

        ui.markdown(project.long_description).classes('text-slate-300 text-base leading-relaxed mb-6')
        
        with ui.row().classes('w-full justify-end gap-4 mt-6'):
            if project.github_url:
                ui.button('View Code', icon='code', on_click=lambda: ui.open(project.github_url, new_tab=True)).props('outline color=sky')
            if project.demo_url:
                # Check if it's an internal demo
                if project.id in ['sentiment-analysis', 'customer-churn']:
                    ui.button('Live Demo', icon='launch', on_click=lambda: ui.navigate.to(f'/demo/{project.id}')).props('unelevated color=cyan-6 text-color=slate-900 font-bold')
                else:
                    ui.button('Live Demo', icon='launch', on_click=lambda: ui.open(project.demo_url, new_tab=True)).props('unelevated color=cyan-6 text-color=slate-900 font-bold')
    
    dialog.open()
