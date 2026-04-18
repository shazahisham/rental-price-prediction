import requests
import pandas as pd
import io
import re

def scrape_german_data():
    print(">>> Starting Web Scraping: German City GDP Stats...")
    url = "https://en.wikipedia.org/wiki/List_of_German_cities_by_GDP"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers)
        html_data = io.StringIO(response.text)
        
        # This 'match' is what forces it to find 81 cities instead of 11
        tables = pd.read_html(html_data, match="Metropolitan", flavor='lxml')
        df_wiki = tables[0]
        
        # Get City and GDP columns
        df_wiki = df_wiki.iloc[:, [1, 4]] 
        df_wiki.columns = ['City', 'GDP_Per_Capita']
        
        # CLEANING: Remove [1] and standardize names (e.g., 'München' to match your data)
        df_wiki['City'] = df_wiki['City'].apply(lambda x: re.sub(r'\[.*\]', '', str(x)).strip())
        
        # NUMBERS: Remove symbols so math works
        df_wiki['GDP_Per_Capita'] = pd.to_numeric(
            df_wiki['GDP_Per_Capita'].astype(str).str.replace(r'[^\d]', '', regex=True), 
            errors='coerce'
        )
        
        print(f"DONE: Scraped {len(df_wiki)} cities successfully.")
        return df_wiki
    except Exception as e:
        print(f"Scraping Error: {e}")
        return pd.DataFrame(columns=['City', 'GDP_Per_Capita'])