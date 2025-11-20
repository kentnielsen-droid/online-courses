from nicegui import ui
import random

def sentiment_demo():
    with ui.column().classes('w-full gap-4 p-4 bg-slate-800/50 rounded-lg border border-slate-700'):
        ui.label('Try the Model').classes('text-lg font-bold text-slate-200')
        
        text_input = ui.textarea(placeholder='Type something here... (e.g., "I love this product!")').classes('w-full bg-slate-900 text-slate-200 rounded-md border-slate-600').props('outlined input-class=text-slate-200')
        result_label = ui.label().classes('text-xl font-bold')
        
        def analyze():
            text = text_input.value.lower()
            if not text:
                result_label.set_text('')
                return
            
            # Mock Logic
            if any(word in text for word in ['love', 'great', 'amazing', 'good', 'happy']):
                sentiment = 'Positive'
                color = 'text-green-400'
            elif any(word in text for word in ['hate', 'bad', 'terrible', 'sad', 'awful']):
                sentiment = 'Negative'
                color = 'text-red-400'
            else:
                sentiment = 'Neutral'
                color = 'text-slate-400'
                
            result_label.set_text(f'Prediction: {sentiment}')
            result_label.classes(remove='text-green-400 text-red-400 text-slate-400', add=color)

        ui.button('Analyze Sentiment', on_click=analyze).props('unelevated color=blue-9 text-color=white').classes('w-full')
        result_label

def churn_demo():
    with ui.column().classes('w-full gap-4 p-4 bg-slate-800/50 rounded-lg border border-slate-700'):
        ui.label('Customer Churn Predictor').classes('text-lg font-bold text-slate-200')
        
        with ui.grid(columns=2).classes('w-full gap-4'):
            tenure = ui.number(label='Tenure (Months)', value=12, min=0, max=72).props('outlined dark')
            monthly_charges = ui.number(label='Monthly Charges ($)', value=50, min=0, max=200).props('outlined dark')
            contract = ui.select(['Month-to-month', 'One year', 'Two year'], value='Month-to-month', label='Contract Type').props('outlined dark')
            tech_support = ui.checkbox('Has Tech Support').props('dark')

        result_bar = ui.linear_progress(value=0).props('color=red-5 track-color=slate-700 size=20px show-value rounded').classes('mt-4')
        result_label = ui.label().classes('text-center w-full text-slate-300 text-sm')

        def predict():
            # Mock Logic
            score = 0.5
            if contract.value == 'Month-to-month': score += 0.3
            if contract.value == 'Two year': score -= 0.3
            if tenure.value < 12: score += 0.2
            if tenure.value > 48: score -= 0.2
            if monthly_charges.value > 100: score += 0.1
            if tech_support.value: score -= 0.2
            
            score = max(0.0, min(1.0, score + random.uniform(-0.05, 0.05)))
            
            result_bar.set_value(score)
            result_label.set_text(f'Churn Probability: {score:.1%}')
            
            if score > 0.7:
                result_bar.props('color=red-5')
            elif score > 0.3:
                result_bar.props('color=orange-5')
            else:
                result_bar.props('color=green-5')

        ui.button('Predict Churn Risk', on_click=predict).props('unelevated color=blue-9 text-color=white').classes('w-full mt-2')
        result_bar
        result_label
