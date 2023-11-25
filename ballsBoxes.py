import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from math import factorial
from PIL import Image

st.set_page_config(layout="wide")



# Function to generate and display the table image
def prod(iterable):
    prd = 1
    for num in iterable:
        prd *= num
    return prd

def partitions(n, k):
    def generate_partitions(cur_sum, cur_list):
        if len(cur_list) == k:
            if cur_sum == n:
                partitions.append(cur_list[:])
            return

        start = 1 if not cur_list else cur_list[-1]
        for i in range(start, n - cur_sum + 1):
            if cur_sum + i <= n:  # Avoid unnecessary iterations
                generate_partitions(cur_sum + i, cur_list + [i])

    partitions = []
    generate_partitions(0, [])
    return partitions

def display_table_image(font_family, numBalls, numBoxes):
    

    result = partitions(numBalls, numBoxes)
    
    num_rows = len(result)
    num_cols = 7

    def generate_equation(x,y):
        if y == 1:
            theString = '+'.join(str(val) for val in x)
            return rf"${theString}$"
        
        if y == 2:
            a = str(sum(x))+'!'
            b = '!'.join(str(l) for l in x if l > 1)+'!'
            freq = [x.count(f) for f in set(x)]
            if all(val==1 for val in freq):
                return rf"$\frac{{{a}}}{{{b}}}\cdot{sum(freq)}!$"
            else:
                c = '!'.join(str(l) for l in freq if l > 1)+'!'
                return rf"$\frac{{{a}}}{{{b}}}\cdot\frac{{{sum(freq)}!}}{{{c}}}$"
        
        if y == 3:
            freq = [x.count(f) for f in set(x)]
            a = str(sum(x))+'!'
            b = '!'.join(str(l) for l in x if l > 1)+'!'
            if all(val==1 for val in freq):
                return rf"$\frac{{{a}}}{{{b}}}$"
            else:
                c = b + '!'.join(str(l) for l in freq if l > 1)+'!'
                return rf"$\frac{{{a}}}{{{c}}}$"
            
        if y == 4:
            freq = [x.count(f) for f in set(x)]
            a = str(sum(freq))+'!'
            if all(val==1 for val in freq):
                return rf"${a}$"
            else:
                b = '!'.join(str(l) for l in freq if l > 1)+'!'
            return rf"$\frac{{{a}}}{{{b}}}$"
        
            
    columns = ['Distribution(II)','Calc.(DD)','Count(DD)','Calc.(DI)','Count(DI)','Calc.(ID)','Count(ID)']
    data = {i: [] for i in columns}

    rowCount = 0
    for rowCount in range(0,num_rows):
        
        theRow = result[rowCount]
        
        num_permutations = factorial(sum(theRow)) // prod(factorial(x) for x in theRow)
        freq = [theRow.count(f) for f in set(theRow)]
        num_permutations *= factorial(sum(freq)) // prod(factorial(x) for x in freq if x > 1)
        
        data['Distribution(II)'].append(generate_equation(theRow,1))
        data['Calc.(DD)'].append(generate_equation(theRow,2))
        data['Count(DD)'].append(num_permutations)
        data['Calc.(DI)'].append(generate_equation(theRow,3))
        
        num_permutations = factorial(sum(theRow)) // prod(factorial(x) for x in theRow)
        freq = [theRow.count(f) for f in set(theRow)]
        num_permutations = num_permutations // prod(factorial(x) for x in freq if x > 1)
        
        data['Count(DI)'].append(num_permutations)
        
        data['Calc.(ID)'].append(generate_equation(theRow,4))
        
        freq = [theRow.count(f) for f in set(theRow)]
        num_permutations = factorial(sum(freq)) // prod(factorial(x) for x in freq if x > 1)    
        data['Count(ID)'].append(num_permutations)

    # Create DataFrame with specified number of rows and columns
    df = pd.DataFrame(data)

    # Use the selected font family
    plt.rcParams['mathtext.fontset'] = 'custom'
    plt.rcParams['font.family'] = font_family

    # Adjust font size and cell dimensions based on rows and columns
    font_size   =   72
    if num_rows>6:
        cell_height = 0.15
    else:
        cell_height = 0.5

    # Render LaTeX in DataFrame using matplotlib with increased cell padding
    plt.figure(figsize=(9,12))  # Adjust figure size based on rows and columns
    column_widths = [0.8, 0.65, 0.6, 0.65, 0.6, 0.65, 0.6]

    # Create lighter cell colors to introduce space illusion
    cell_colors = [['white'] * num_cols for _ in range(num_rows)]

    table = plt.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center',
                      cellColours=cell_colors,colWidths=column_widths)

    # Adjust cell dimensions
    cellDict = table.get_celld()
    for key in cellDict:
        cellDict[key].set_height(cell_height)  # Set cell height
        cellDict[key].set_text_props(color='black')# Set text size and color
        if key[1] == 1:
            cellDict[key].set_text_props(color='blue')
        if key[1] == 3:
            cellDict[key].set_text_props(color='red')

    # Adjust table properties
    table.auto_set_font_size(False)
    table.set_fontsize(font_size)  # Set font size
    table.scale(1.5, 1.5)  # Scale the table

    plt.axis('off')  # Hide axes
    plt.tight_layout()

    # Save the table as a high-quality image (PNG or PDF)
    plt.savefig('table_image.png', dpi=200, bbox_inches='tight')  # Adjust DPI as needed

    # Display the high-quality image
    st.image('table_image.png')

# Streamlit app
st.sidebar.header('Select #Balls and #Boxes')

numBalls = st.sidebar.number_input('Enter the number of balls', min_value=5, step=1, value=6, max_value=10)
numBoxes = st.sidebar.number_input('Enter the number of boxes', min_value=2, step=1, value=3, max_value=4)

st.sidebar.header('Select Font Family')

selected_font = st.sidebar.selectbox('Choose a font', ['Arial', 'Helvetica', 'Roboto', 'Open Sans', 'Lato', 'PT Sans', 'Nunito'])

# Button to display the table image when clicked
if st.sidebar.button('Display Table'):
    display_table_image(selected_font, numBalls, numBoxes)
