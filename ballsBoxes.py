import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

from PIL import Image
from itertools import permutations
import base64
import numpy as np
from functools import lru_cache
import streamlit as st

import streamlit as st
import random
import itertools




from math import comb, factorial



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

numBalls = st.sidebar.number_input('Enter the number of balls', min_value=3, step=1, value=5, max_value=9)
numBoxes = st.sidebar.number_input('Enter the number of boxes', min_value=3, step=1, value=3, max_value=5)


def pie_terms(k, n):
    terms = []
    for i in range(1, k):
        remaining = k - i
        term = rf"\binom{{{k}}}{{{i}}}"
        if remaining > 1:
            term += rf"{remaining}^{{{n}}}"

        if i == 1:
            terms.append(term)
        elif i % 2 == 0:
            terms.append(rf"-{term}")
        else:
            terms.append(rf"+{term}")

    return "".join(terms)


from itertools import combinations
from string import Template

def pie_union_formula(n,numBalls):
    def format_intersection(indices):
        return "|" + "".join(f"B_{i}" for i in indices) + "|"

    def intersection_terms_with_note(r):
        """
        Same as before, BUT without the huge overbrace.
        Simply list the terms normally.
        """
        combos = list(combinations(range(1, n+1), r))
        exprs = [format_intersection(c) for c in combos]

        # No overbrace here now — just return the expression list
        if len(exprs) <= 5:
            return " + ".join(exprs)
        return " + ".join(exprs[:3]) + r" + \cdots + " + " + ".join(exprs[-2:])

    def intersection_terms(r):
        combos = list(combinations(range(1, n+1), r))
        exprs = [format_intersection(c) for c in combos]
        if len(exprs) <= 5:
            return " + ".join(exprs)
        return " + ".join(exprs[:3]) + r" + \cdots + " + " + ".join(exprs[-2:])

    # --- Top line ---
    latex = Template(r"""
{\large
\begin{aligned}
\left|\bigcup_{i=1}^{$n} B_i\right|
=\;&
\textcolor{blue}{\underbrace{$first_row}
_{\substack{1\ \text{at a time,}\\
\text{number of terms } {\scriptstyle = \binom{$n}{1} = $n}}}}\\[22pt]
""").substitute(
        n=n,
        first_row=" + ".join(format_intersection((i,)) for i in range(1, n+1))
    )

    # --- Higher intersections ---
    sign = "-"
    for r in range(2, n+1):
        combos = list(combinations(range(1, n+1), r))
        count = len(combos)

        if r == 2:
            term = intersection_terms_with_note(r)
        else:
            term = intersection_terms(r)

        part = Template(r"""
& $sign\textcolor{blue}{\underbrace{( $term )}
_{\substack{$r\ \text{at a time,}\\
\text{number of terms } {\scriptstyle = \binom{$n}{$r} = $count}}}}\\[22pt]
""").substitute(
            sign=sign, term=term, r=r, n=n, count=count
        )

        latex += part
        sign = "+" if sign == "-" else "-"

    latex += fr"""
\\[10pt]
&\text{{Note:}}\\
&\text{{$B_k$ means Box $k$ is empty.}}\\
&\text{{$B_1B_2$ means Box 1 and Box 2 are known to be empty; no assumption is made about the others.}}\\
&\text{{Contribution is ${numBoxes-2}^{{{numBalls}}}$ where number of boxes = {numBoxes} and number of balls = {numBalls}.}}
"""


    latex += r"\end{aligned}}"

    return latex

def list_set(m):
    if m <= 5:
        return r"\{" + ",".join(str(i) for i in range(1, m+1)) + r"\}"
    return r"\{1,2,\dots," + str(m) + r"\}"



def explain_brackets_distribution(n, k, num_examples=4, seed=42):
    
    random.seed(seed)

    st.latex(rf"""
\text{{Distribute }} {n} \text{{ identical balls among }} {k} \text{{ pairwise distinct boxes, each of which must receive at least one ball.}}
""")

    lhs = " + ".join([rf"x_{i}" for i in range(1, k+1)])

    st.latex(rf"""
\text{{We require }} {lhs} = {n}, \qquad x_r \ge 1\ (1 \le r \le {k}).
""")

    st.latex(rf"""
    \text{{Place one ball into each box.}}
    \quad\Rightarrow\quad
    x_r = 1 + y_r,\quad y_r \ge 0.
    """)

    # Explicit lists for (1 + y_i) terms and for y_i terms
    lhs1 = " + ".join([rf"(1+y_{i})" for i in range(1, k+1)])
    lhs2 = " + ".join([rf"y_{i}" for i in range(1, k+1)])
    
    st.latex(rf"""
    {lhs1} = {n}
    \quad\Rightarrow\quad
    {lhs2} = {n-k},\qquad y_r \ge 0.
    """)


    remaining = n - k
    bars = k - 1

    value = comb(n - 1, k - 1)

    st.markdown("---")
    

    o_string = "o" * (n - k)

    first_color = "blue"
    last_color = "red"
    mid_colors = ["green", "purple", "orange", "brown"]
    

    def colored_dividers(k):
        
        blocks = []
    
        for i in range(k):
            if i == 0:
                color = first_color
                shape = r")"
            elif i == k - 1:
                color = last_color
                shape = r"("
            else:
                color = mid_colors[(i - 1) % len(mid_colors)]
                shape = r"(, \, )"
    
            blocks.append(rf"\textcolor{{{color}}}{{\texttt{{{shape}}}}}")
    
        return "".join(blocks)

    divider_string = colored_dividers(k)



    st.latex(rf"""
\text{{Since one ball has already been placed in each of the }} {k} \text{{ boxes,}}
\text{{ we are left with }} {n-k} \text{{ balls to be placed.}}
\\[12pt]
\text{{Start with a string }}
\textcolor{{{first_color}}}{{\texttt{{(}}}}\, {o_string}\,\textcolor{{{last_color}}}{{\texttt{{)}}}}.
\\[12pt]
\text{{To visualise, we use }} {k-1} \text{{ dividers, written as:}}
{divider_string}
\text{{ which close one box and open the next.}}
\\[12pt]
\text{{Arrange the }} {n-k}
\text{{ balls together with the }} {k-1}
\text{{ dividers between }}
\textcolor{{{first_color}}}{{\texttt{{(}}}}\,\text{{and}}\,\textcolor{{{last_color}}}{{\texttt{{)}}}}.
""")

    st.markdown('---')

    def positive_partition(total, k):
        """Return a random positive partition of total into k parts if possible."""
        if total < k:
            return None  # impossible
    
        # Give 1 to each part
        rem = total - k
    
        # Case 1: only one possible partition
        if rem == 0:
            return [1] * k
    
        # If rem is too small for random.sample, use incremental distribution
        if rem < (k - 1):
            parts = [1] * k
            for _ in range(rem):
                parts[random.randrange(k)] += 1
            return parts
    
        # Normal sampling case
        cuts = sorted([0] + random.sample(range(rem + 1), k - 1) + [rem])
        parts = [cuts[i+1] - cuts[i] + 1 for i in range(k)]
        return parts
    
    
    def nonnegative_partition(total, k):
        """Always safe non-negative partition."""
        if total == 0:
            return [0] * k
    
        if total < (k - 1):
            parts = [0] * k
            for _ in range(total):
                parts[random.randrange(k)] += 1
            return parts
    
        cuts = sorted([0] + random.sample(range(total+1), k-1) + [total])
        return [cuts[i+1] - cuts[i] for i in range(k)]
    
    
    def distinct_partition_pair_prefer_positive(total, k):
        """
        Generate two distinct partitions.
        Try positive first; if same or invalid, use non-negative for both.
        """
        p1 = positive_partition(total, k)
        p2 = positive_partition(total, k)
    
        # If positive partitions are invalid or identical → fallback
        if (p1 is None) or (p2 is None) or (p1 == p2):
            p1 = nonnegative_partition(total, k)
            # ensure p2 is distinct
            for _ in range(50):  # plenty of retries
                p2 = nonnegative_partition(total, k)
                if p2 != p1:
                    break
            # If all retries failed (extremely unlikely), enforce difference manually
            if p1 == p2:
                if k > 1:
                    p2 = p2.copy()
                    p2[0], p2[1] = p2[1], p2[0]
    
        return p1, p2

    
    # ---------------------------------------------------
    # COLOR SETUP
    # ---------------------------------------------------
    first_color = "blue"
    last_color = "red"
    mid_colors = ["green", "purple", "orange", "brown"]
    
    def colored_parentheses(index, k):
        """Return \textcolor{color}{( ... )} wrapper for box index (0-based)."""
        if index == 0:
            color = first_color
        elif index == k-1:
            color = last_color
        else:
            color = mid_colors[(index-1) % len(mid_colors)]
        return color
    
    remaining = n - k   # number of o's to place
    
    def make_example(y):
        parts = []
        for i, v in enumerate(y):
            color = colored_parentheses(i, k)
            parts.append(rf"\textcolor{{{color}}}{{(}}" + "\, " + ("o"*v) + " \," +
                         rf"\textcolor{{{color}}}{{)}}")
        return " ".join(parts)
    
    remaining = n - k

    
    num_examples = min(5, 5)  
    examples_y = set()
    examples_list = []
    
    attempts = 0
    max_attempts = 200   
    
    while len(examples_list) < num_examples and attempts < max_attempts:
        attempts += 1
        y1, y2 = distinct_partition_pair_prefer_positive(remaining, k)
    
        # Add both partitions to pool if distinct
        for y in (y1, y2):
            y_tuple = tuple(y)
            if y_tuple not in examples_y:
                examples_y.add(y_tuple)
                examples_list.append(y)
                if len(examples_list) == num_examples:
                    break

    for idx, y in enumerate(examples_list, start=1):
        x = [v + 1 for v in y]
        latex_str = make_example(y)
    
        st.latex(rf"""
        \text{{Example {idx}: }} {latex_str}
        \quad\Longrightarrow\quad
        y={tuple(y)}\ \Rightarrow\ x={tuple(x)}.
        """)
    
    
    st.latex(rf"""
    \text{{Number of ways to arrange the }} n-k \text{{ balls and }} k-1 \text{{ dividers is }} 
    \binom{{(n-k)+(k-1)}}{{k-1}}
    =\binom{{n-1}}{{k-1}}
    =\binom{{{n-1}}}{{{k-1}}}.
    """)


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

        general_pie = rf"""
\text{{In general, the number of onto functions }} 
f:{list_set(numBalls)} \to {list_set(numBoxes)}
\text{{ is }}\\[8pt]
T(n,k)
\;=\;
k^n \;-\;
\left|\bigcup_{{i=1}}^{{k}} B_i\right|
"""

        st.latex(general_pie)

        st.latex(pie_union_formula(numBoxes,numBalls))
        
        myString = rf"""
\text{{T}}\left({numBalls},{numBoxes}\right) = {numBoxes}^{numBalls}
"""
        curlyString = pie_terms(numBoxes, numBalls)
        st.latex(myString+r"-\left\{"+curlyString+r"\right\}")



        st.title("Solution 02 – Using Recursion")
        

        myString = r"""
\text{Let us begin with a numerical example to understand recursion.}\\[6pt]
\text{We will then derive the general formula.}\\[6pt]
\text{Finally, we will compute the value for the number of balls and boxes chosen by you.}\\[14pt]

\text{T}(5,3):\\[6pt]
\text{Think of it as the number of 5-letter words from } \{A,B,C\} \text{ with no missing letters.}\\[10pt]

A \mid B \mid C \mid A \mid A
\qquad
\text{represents: balls 1, 4, and 5 go to Box 1; ball 2 goes to Box 2; ball 3 goes to Box 3.}\\[6pt]

B \mid A \mid C \mid B \mid A
\qquad
\text{represents: balls 2 and 5 go to Box 1; balls 1 and 4 go to Box 2; ball 3 goes to Box 3.}\\[10pt]

\text{So, one can see the similarity between the problems: placing objects into boxes so that no box is empty,}\\
\text{counting the number of onto functions, or forming a 5-letter word in which each letter appears at least once.}\\[14pt]
\text{To count all such words, we begin by choosing the first letter.}\\[6pt]
\text{There are three choices for the first letter.}\\[6pt]
\text{After this, the remaining four letters must be filled, and the first letter need not be reused.}\\[6pt]

\text{There are two cases:}\\[10pt]

\begin{aligned}
(a)\;&\text{If the first letter does not occur again, the word can be completed in } T(4,2).\\[6pt]
(b)\;&\text{If the first letter does occur again, the number of ways to complete the word is } T(4,3).
\end{aligned}
"""
        st.latex(myString)

        myString = rf"\text{{T}}(5,3)=3\big(\text{{T}}(4,2)+\text{{T}}(4,3)\big)=3(14+36)=150"
        st.latex(myString)
        st.image('grid_figure_high_res_small.png')

        
        myString = rf"""
\text{{Using the same reasoning as in }} T(5,3)\text{{, we generalize the idea to }}T(n,k).\\[6pt]
\text{{There are }}k\text{{ choices for the first position.}}\\[6pt]
\text{{After this, the remaining }}n-1\text{{ positions must be filled. So all the }}k\text{{ letters appear at least once.}}\\[6pt]
\text{{This leads to two possibilities:}}\\[10pt]
\text{{(a) The first letter does not appear again, giving }}T(n-1,k-1).\\[4pt]
\text{{(b) The first letter appears again, giving }}T(n-1,k).\\[12pt]

\text{{Hence,}}
\quad
\text{{T}}(n,k)
= k\,\big(\text{{T}}(n-1,k-1)+\text{{T}}(n-1,k)\big)
"""
        st.latex(myString)
        st.latex(r"\text{For example, using the recurrence relation, we can compute } T(7,4)\text{ as follows:}")
        myString = rf"\text{{T}}(7,4)=4\big(\text{{T}}(6,3)+\text{{T}}(6,4)\big)=4(1560+540)=8400"
        st.latex(myString)

        st.image('grid_figure_high_res.png')
                
        st.write(f"## Solution 03 - Case Work")
        for count_case, case in enumerate(partitions(numBalls,numBoxes)):
            print(case)

            case_number = f"Case - {count_case + 1:02}"
            st.write(f"### {case_number}")
            st.latex(description(case))
            st.image(f'all_images/all_permutations/image_{numBalls:02d}_{numBoxes:02d}_{count_case:02d}_001.png',width=450)

        

        st.write(f"# {str(2).zfill(2)}. Distribution of {numBalls} identical balls into {numBoxes} distinct boxes")
        # explain_stars_and_bars(numBalls, numBoxes)
        # explain_gaps_method(8, 3)
        explain_brackets_distribution(numBalls, numBoxes, num_examples=5)

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
    st.markdown(
        "<p style='font-family: \"Verdana\", sans-serif; font-size:12px;'>Click on the arrow(top-left) to open the sidebar(applicable if on phone)</p>",
        unsafe_allow_html=True,
    )