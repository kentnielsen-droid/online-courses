from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Project:
    id: str
    title: str
    description: str
    tags: List[str]
    image_url: str = "https://picsum.photos/seed/{id}/400/300" # Placeholder
    long_description: str = ""
    demo_url: Optional[str] = None
    github_url: Optional[str] = None

def get_projects() -> List[Project]:
    return [
        Project(
            id="sentiment-analysis",
            title="Real-time Sentiment Analysis",
            description="A dashboard tracking live sentiment of Twitter/X streams using BERT.",
            tags=["NLP", "Python", "Transformer", "FastAPI"],
            long_description="""
                This project leverages a fine-tuned BERT model to analyze the sentiment of tweets in real-time.
                It connects to the Twitter API, processes the text stream, and visualizes the sentiment trends
                (Positive, Negative, Neutral) on a live dashboard.
                
                Key Features:
                - Real-time data ingestion
                - Transformer-based classification
                - Interactive visualization with Plotly
            """,
            github_url="https://github.com/example/sentiment",
            demo_url="/demo/sentiment-analysis"
        ),
        Project(
            id="customer-churn",
            title="Customer Churn Prediction",
            description="Predicting customer churn for a telecom company using XGBoost.",
            tags=["ML", "XGBoost", "Scikit-learn", "Pandas"],
            long_description="""
                Built a predictive model to identify customers at risk of churning.
                The model uses historical usage data, billing information, and customer demographics.
                Achieved an AUC-ROC score of 0.85.
                
                Key Features:
                - Data preprocessing and feature engineering
                - Model training and hyperparameter tuning
                - Explainability with SHAP values
            """,
            github_url="https://github.com/example/churn",
            demo_url="/demo/customer-churn"
        ),
        Project(
            id="image-segmentation",
            title="Medical Image Segmentation",
            description="U-Net based model for segmenting tumors in MRI scans.",
            tags=["CV", "PyTorch", "Deep Learning", "U-Net"],
            long_description="""
                Developed a deep learning model to automatically segment brain tumors from MRI scans.
                The architecture is based on U-Net and was trained on the BraTS dataset.
                
                Key Features:
                - Data augmentation pipeline
                - Custom loss function (Dice Loss)
                - High precision segmentation
            """,
            github_url="https://github.com/example/segmentation"
        ),
        Project(
            id="recommendation-engine",
            title="E-commerce Recommender",
            description="Collaborative filtering recommendation system for an online store.",
            tags=["RecSys", "Python", "Spark", "Matrix Factorization"],
            long_description="""
                Implemented a scalable recommendation engine using Matrix Factorization (ALS).
                It provides personalized product recommendations based on user purchase history.
                
                Key Features:
                - Scalable processing with Apache Spark
                - Cold-start problem handling
                - Real-time inference API
            """,
            github_url="https://github.com/example/recsys"
        ),
    ]
