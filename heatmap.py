import pandas as pd
import numpy as np
import plotly.express as px

def make_heatmap(file):
    filename = file
    TT = "TODO"

    data = pd.read_csv(filename).values
    xcor = data[:, 1]
    ycor = data[:, 2]
    sens = data[:, 6]

    if len(xcor) > 60:
        heatmap_10_2(xcor, ycor, sens, TT)
    elif 7 in xcor:
        heatmap_8_2(xcor, ycor, sens, TT)
    else:
        heatmap_24_2(xcor, ycor, sens, TT)


def heatmap_8_2(xcor, ycor, DB, title):

    M2 = np.full((10, 10), np.nan)
    for i in range(M2.shape[1]):
        for k in range(M2.shape[0]):
            XY0 = DB[(xcor == -(-9 + 2 * (i + 1))) & (ycor == -(-9 + 2 * (k + 1)))]
            if len(XY0) > 0:
                M2[k, 9 - i] = round(XY0 * 100) / 100

    # Create heatmap
    fig = px.imshow(M2, labels=dict(x="Degrees", y="Degrees"),
                    x=['-7', '-5', '-3', '-1', '1', '3', '5', '7'],
                    y=['7', '5', '3', '1', '-1', '-3', '-5', '-7'],
                    color_continuous_scale='turbo',
                    color_continuous_midpoint=25)
    
    fig.update_layout(title=title, xaxis=dict(title='Degrees'), yaxis=dict(title='Degrees'), font=dict(size=16))
    
    # Save figure
    filename = f'C:/VFT/Heatmaps/{title}.png'
    fig.write_image(filename)

def heatmap_10_2(xcor, ycor, DB, title):

    M2 = np.full((10, 10), np.nan)
    for i in range(M2.shape[1]):
        for k in range(M2.shape[0]):
            XY0 = DB[(xcor == -(-9 + 2 * (i + 1))) & (ycor == -(-9 + 2 * (k + 1)))]
            if len(XY0) > 0:
                M2[k, 9 - i] = round(XY0 * 100) / 100

    M2[0, 4] = DB[(xcor == -1) & (ycor == 9)]
    M2[0, 5] = DB[(xcor == 1) & (ycor == 9)]
    M2[4, 9] = DB[(xcor == 9) & (ycor == 1)]
    M2[5, 9] = DB[(xcor == 9) & (ycor == -1)]

    # Create heatmap
    fig = px.imshow(M2, labels=dict(x="Degrees", y="Degrees"),
                    x=['-9', '-7', '-5', '-3', '-1', '1', '3', '5', '7', '9'],
                    y=['9', '7', '5', '3', '1', '-1', '-3', '-5', '-7', '-9'],
                    color_continuous_scale='turbo',
                    color_continuous_midpoint=25)

    fig.update_layout(title=title, xaxis=dict(title='Degrees'), yaxis=dict(title='Degrees'), font=dict(size=16))

    # Save figure
    filename = f'C:/VFT/Heatmaps/{title}.png'
    fig.write_image(filename)


def heatmap_24_2(xcor, ycor, sens, TT):
    # Figure 1: Heatmap of p-values
    M2 = np.full((8, 10), np.nan)
    for i in range(M2.shape[1]):
        for k in range(M2.shape[0]):
            XY0 = sens[(xcor == -33 + 6 * (i + 1)) & (ycor == -(-27 + 6 * (k + 1)))]
            if len(XY0) > 0:
                M2[k, i] = round(XY0 * 100) / 100

    # Create heatmap
    fig = px.imshow(M2, labels=dict(x="Degrees", y="Degrees"),
                    x=['-27', '-21', '-15', '-9', '-3', '3', '9', '15', '21', '27'],
                    y=['21', '15', '9', '3', '-3', '-9', '-15', '-21'],
                    color_continuous_scale='turbo',
                    color_continuous_midpoint=25)

    fig.update_layout(title=TT, xaxis=dict(title='Degrees'), yaxis=dict(title='Degrees'), font=dict(size=16))

    # Save figure
    filename = f'C:/VFT/Heatmaps/{TT}.png'
    fig.write_image(filename)