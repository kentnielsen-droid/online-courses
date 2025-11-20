from nicegui import ui
from projects import Project

def project_card(project: Project, on_click):
    with ui.card().classes('glass-card w-full max-w-sm cursor-pointer no-shadow') as card:
        card.on('click', lambda: on_click(project))
        ui.image(project.image_url).classes('h-48 w-full object-cover rounded-t-lg opacity-80 hover:opacity-100 transition-opacity duration-300')
        with ui.card_section():
            ui.label(project.title).classes('text-xl font-bold text-slate-100 mb-2')
            ui.label(project.description).classes('text-sm text-slate-300 mb-4 line-clamp-3')
            with ui.row().classes('gap-2 flex-wrap'):
                for tag in project.tags:
                    ui.label(tag).classes('text-xs px-2 py-1 rounded-full bg-slate-700/50 text-sky-300 border border-slate-600/50')

def skills_widget():
    skills = {
        "Languages": ["Python", "SQL", "R", "C++"],
        "Machine Learning": ["PyTorch", "TensorFlow", "Scikit-learn", "XGBoost"],
        "Data Engineering": ["Spark", "Kafka", "Airflow", "Docker"],
        "Tools": ["Git", "AWS", "FastAPI", "NiceGUI"]
    }
    
    with ui.card().classes('glass w-full p-6'):
        ui.label('Technical Arsenal').classes('text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-cyan-400 mb-6')
        with ui.grid(columns=2).classes('w-full gap-8'):
            for category, items in skills.items():
                with ui.column().classes('gap-2'):
                    ui.label(category).classes('text-lg font-semibold text-slate-200')
                    with ui.row().classes('gap-2 flex-wrap'):
                        for item in items:
                            ui.label(item).classes('text-sm px-3 py-1 rounded-md bg-slate-800/50 text-slate-300 border border-slate-700/50 hover:border-sky-500/50 hover:text-sky-300 transition-colors cursor-default')

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
        
        with ui.row().classes('w-full justify-end gap-4'):
            if project.github_url:
                ui.button('View Code', icon='code', on_click=lambda: ui.open(project.github_url, new_tab=True)).props('outline color=sky')
            if project.demo_url:
                ui.button('Live Demo', icon='launch', on_click=lambda: ui.open(project.demo_url, new_tab=True)).props('unelevated color=sky text-color=slate-900')
    
    dialog.open()
