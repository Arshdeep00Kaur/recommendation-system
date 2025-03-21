import dash
import dash_bootstrap_components as dbc
from dash import html
import pandas as pd

# Load DataFrame
popular_df = pd.read_pickle(r"D:\projects\book recommendation\popularity based\popular_books.pkl")

# Fix column name issues
print("Columns in DataFrame:", popular_df.columns)  # Debugging step
popular_df.columns = popular_df.columns.str.strip()  # Remove extra spaces

# Rename columns to a consistent format
popular_df.rename(columns={"Book-Title": "book_title", "Book-Author": "book_author", "Image-URL-M": "image_url"}, inplace=True)

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
], fluid=True)

if __name__ == '__main__':
    app.run(debug=True)
