import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from math import factorial
from PIL import Image
from itertools import permutations
import base64

st.set_page_config(layout="wide")

st.markdown('''
<style>
.katex-html {
    text-align: left;
}
</style>''',
unsafe_allow_html=True
)


def description(x):
    
    theString = ''
    
    def uniquePermutations(x):
        unique_perms = []
        seen = set()

        # Generate permutations and filter out duplicates
        for perm in permutations(sorted(x, reverse=True)):
            if perm not in seen:
                unique_perms.append(perm)
                seen.add(perm)

        return sorted(unique_perms, key=lambda r: r[0], reverse=True)


    def generate_statement(x):
        total_balls = sum(x)
        boxes = len(x)

        statement = f"There are a total of {total_balls} balls. We want to place "
        for i in range(boxes):
            ball_word = 'ball' if x[i] == 1 else 'balls'
            statement += f"{x[i]} {ball_word} in Box {i+1}"
            if i < boxes - 1:
                statement += ", "
            else:
                statement += "."

        statement = f"\\text{{{statement}}}"
        return statement


    def binom_result(x):
        output = []
        total = sum(x)
        csum = total
        for element in x:
            output.append(csum)
            csum -= element
        return output

    def combination_str(x):
        p = sorted(x, reverse=True)
        q = binom_result(p)

        freq = [x.count(f) for f in set(x)]
        print(freq)
        a = str(sum(freq))+'!'
        if all(val==1 for val in freq):
            freqString =  f"{{{a}}}"
        else:
            b = '!'.join(str(l) for l in freq if l > 1)+'!'
            freqString =  f"\\frac{{{a}}}{{{b}}}"

        num_ways = ''
        for k in range(len(p)):
            if p[k]>1:
                if q[k]>p[k]:
                    num_ways += f"\\binom{{{q[k]}}}{{{p[k]}}}"
            else:
                if q[k]>1:
                    num_ways += f"\\cdot{{{q[k]}}}"
        theString = generate_statement(p) + f"\\\\ \\text{{This can be done in}}" + num_ways + f"\\text{{ ways.}}"
        theString += f"\\\\ \\text{{The number of ways to arrange (}}"\
        +', '.join([str(t) for t in p])+f"\\text{{)}}"+f"\\text{{ is }}"\
        +freqString
        
        theString += f"\\\\ \\text{{So balls can be placed in }} {{{len(x)}}} \\text{{ boxes in }}" + num_ways\
        + f"\\cdot{{{freqString}}}" +f"\\text{{ ways.}}"

        return theString.strip()  # Remove trailing space

    latex_string = combination_str(x)
    
    return latex_string

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

# # Streamlit app
st.sidebar.header('Select Number of Balls and Boxes')

numBalls = st.sidebar.number_input('Enter the number of balls', min_value=3, step=1, value=5, max_value=12)
numBoxes = st.sidebar.number_input('Enter the number of boxes', min_value=3, step=1, value=3, max_value=6)

# Button to display the table image when clicked
def show(numBalls,numBoxes):
    
    if numBalls < numBoxes:
        st.write(f"One will not be able to distribute {numBalls} balls into {numBoxes} boxes, with the condition that no box is empty.")
    else:
        
        
        
        st.write(f"# Distribution of {numBalls} balls into {numBoxes} boxes")
        st.write(f"# No Box is empty")
        image_filename = f"balls_boxes/balls_{numBalls:02d}_boxes_{numBoxes:02d}.png"
        
        def get_base64_of_bin_file(bin_file):
            with open(bin_file, 'rb') as f:
                data = f.read()
            return base64.b64encode(data).decode()

        # Encode the image file into base64
        image_base64 = get_base64_of_bin_file(image_filename)

        # Display the image using st.markdown
        st.markdown(f'<img src="data:image/png;base64,{image_base64}" alt="Image" style="width: 1200px;">', unsafe_allow_html=True)

        
        
        st.write(f"# There are four cases")

        st.write(f"# {str(1).zfill(2)}. Distribution of {numBalls} distinct balls into {numBoxes} distinct boxes")

        st.write(f"## Solution 01 - Answer using PIE")
        myString = f"\\text{{T}}\\left({{{numBalls}}},{{{numBoxes}}}\\right)={{{numBoxes}}}^{{{numBalls}}}"
        curlyString = ''

        for count_case in range(0,numBoxes-1):
            print(count_case)
            if numBoxes- count_case - 1 > 1:
                if count_case == 0:
                    curlyString += f"\\binom{{{numBoxes}}}{{{count_case+1}}}{{{numBoxes-count_case-1}}}^{{{numBalls}}}"
                elif count_case % 2 == 0:
                    curlyString += f"+\\binom{{{numBoxes}}}{{{count_case+1}}}{{{numBoxes-count_case-1}}}^{{{numBalls}}}"
                else:
                    curlyString += f"-\\binom{{{numBoxes}}}{{{count_case+1}}}{{{numBoxes-count_case-1}}}^{{{numBalls}}}"
            else:
                if count_case == 0:
                    curlyString += f"\\binom{{{numBoxes}}}{{{count_case+1}}}"
                elif count_case % 2 == 0:
                    curlyString += f"+\\binom{{{numBoxes}}}{{{count_case+1}}}"
                else:
                    curlyString += f"-\\binom{{{numBoxes}}}{{{count_case+1}}}"


        st.latex(myString+r"-\left\{"+curlyString+r"\right\}")
        st.write(f"## Solution 02 - Using Recursion")
        myString = f"\\text{{T}}\\left({{n}},{{k}}\\right)={{k}}\\left(\\text{{T}}\\left({{n-1}},{{k-1}}\\right)"+\
        f"+\\text{{T}}\\left({{n-1}},{{k}}\\right)\\right)"

        st.latex(myString)
        st.image('grid_figure_high_res.png')
        myString = f"\\text{{T}}\\left({{5}},{{3}}\\right)={{3}}\\left(\\text{{T}}\\left({{4}},{{2}}\\right)"+\
        f"+\\text{{T}}\\left({{4}},{{3}}\\right)\\right)=3\\left(14+36\\right)=150"
        st.latex(myString)

        myString = r"\text{T}\left(5, 3\right):\
        \\\text{Think of it as the number of 5-letter words from } \{A, B, C\} \text{ with no missing letters.}\
        \text{There are three choices for the first letter.}\
        \\\text{After this, the remaining four letters must be filled in, and the first letter does not have to be used again. There are two cases:}\
        \\\left(a\right)\text{If the letter used at the first position does not occur again, then the word can be completed in T}\left(4,2\right).\
        \\\left(b\right)\text{If the letter used at the first position does occur again, then the number of ways to complete the word is T}\left(4,3\right)."
        st.latex(myString)

        myString = r"A|B|C|A|A\text{ This represents ball 1, 4 and 5 goes to Box 1, ball 2 goes to Box 2 and ball 3 goes to Box 3.}"
        st.latex(myString)

        st.image('grid_figure_high_res_small.png')

        st.write(f"## Solution 03 - Case Work")
        for count_case, case in enumerate(partitions(numBalls,numBoxes)):
            print(case)
            case_number = f"Case - {count_case + 1:02}"
            st.write(f"### {case_number}")
            st.latex(description(case))
            st.image(f'all_images/all_permutations/image_{numBalls:02d}_{numBoxes:02d}_{count_case:02d}_001.png',width=450)

        st.write(f"# {str(2).zfill(2)}. Distribution of {numBalls} identical balls into {numBoxes} distinct boxes")
        myString = ''
        for count_case in range(1,numBoxes+1):
            myString += f"x_{count_case}+"
        myString = myString[:-1] + f"={{{numBalls}}} \\text{{ with }} x\\geq{{{1}}}" + \
        f"\\\\ \\text{{The answer is }}\\binom{{{numBalls-1}}}{{{numBoxes-1}}}" 
        st.latex(myString) 

# Display some initial content




if st.sidebar.button('Display Table'):
    
    show(numBalls,numBoxes)
else:
    st.write(f"# Distribution of balls and boxes")

    st.write(f"## 1 - Choose the number of balls and number of boxes")

    st.write(f"## 2 - Click on Display Table")

    st.markdown(
        "<p style='font-family: \"Verdana\", sans-serif; font-size:18px;'>Initiative taken by ABM</p>",
        unsafe_allow_html=True,
    )
    
    
