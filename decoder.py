# Imports
# Be sure to run 'pip install requests beautifulsoup4' to use the neccesary libraries.
import requests
from bs4 import BeautifulSoup

def print_grid_from_url(url):
    try:
        # Retrieve the content of the Google Doc
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
    except requests.exceptions.RequestException as e:
        print(f"Error: Unable to retrieve the document. {e}")
        return
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the table in the document
    table = soup.find('table')
    
    # Initialize an empty dictionary to store the characters and their positions
    char_positions = {}
    
    # Parse the table rows
    if table:
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) == 3:
                char = cells[1].get_text().strip()
                x = cells[0].get_text().strip()
                y = cells[2].get_text().strip()
                if x.isdigit() and y.isdigit():
                    x = int(x)
                    y = int(y)
                    char_positions[(x, y)] = char
    
    # Determine the size of the grid
    if char_positions:
        max_x = max(pos[0] for pos in char_positions.keys())
        max_y = max(pos[1] for pos in char_positions.keys())
        
        # Initialize the grid with spaces
        grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]
        
        # Fill the grid with characters from char_positions
        for (x, y), char in char_positions.items():
            grid[max_y - y][x] = char  # Adjust y-coordinate to print correctly
        
        # Print the grid
        for row in grid:
            print(''.join(row))
    else:
        print("No valid character positions found in the document.")

# Allow user to input a Google Doc link and check if it's valid
url = input("Please enter the Google Doc link: ")
print_grid_from_url(url)
