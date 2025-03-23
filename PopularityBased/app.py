import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output
import pandas as pd
import numpy as np

# Load Data
popular_df = pd.read_pickle("popular_books.pkl")
pt = pd.read_pickle("pivot_table.pkl")  # Load collaborative filtering pivot table
similarity_score = np.load("similarity_score.npy")  # Load similarity scores

# Function to recommend books
def recommend(book_name):
    try:
        index = np.where(pt.index == book_name)[0][0]
        similar_items = sorted(
            list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True
        )[1:6]
        recommended_books = [pt.index[i[0]] for i in similar_items]
        return recommended_books
    except:
        return []

# Function to create book cards
def create_book_cards(df):
    cards = []
    for _, row in df.iterrows():
        stars = "⭐" * int(row["avg_rating"])  # Generate stars based on rating
        card = dbc.Card(
            [
                dbc.CardImg(src=row["image_url"], top=True, style={"height": "200px", "object-fit": "cover"}),
                dbc.CardBody([
                    html.H5(row["book_title"], className="card-title"),
                    html.P(f"✍️ Author: {row['book_author']}", className="card-text"),
                    html.P(f"📖 Number of Ratings: {row['num_ratings']}", className="card-text"),
                    html.P(f"⭐ Rating: {row['avg_rating']} {stars}", className="card-text"),
                ]),
            ],
            className="mb-3",
            style={"width": "300px", "margin": "10px"},
        )
        cards.append(card)
    return cards

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

# Layout
app.layout = dbc.Container([
    html.H1("📚 Top 50 Popular Books", className="text-center mb-4"),
    dbc.Row(create_book_cards(popular_df), className="d-flex flex-wrap justify-content-center"),
    html.Hr(),
    html.H2("🔍 Find Similar Books", className="text-center mt-4"),
    dcc.Dropdown(
        id="book-dropdown",
        options=[{"label": title, "value": title} for title in pt.index],
        placeholder="Select a book...",
        className="mb-3",
    ),
    dbc.Row(id="recommended-books", className="d-flex flex-wrap justify-content-center"),
], fluid=True)

# Callback to update recommended books
@app.callback(
    Output("recommended-books", "children"),
    Input("book-dropdown", "value")
)
def update_recommendations(book_name):
    if not book_name:
        return []
    recommended_books = recommend(book_name)
    recommended_df = popular_df[popular_df["book_title"].isin(recommended_books)]
    return create_book_cards(recommended_df)

if __name__ == '__main__':
    app.run(debug=True)
