import plotly.express as px
import pandas as pd
import plotly.express as px

def save_plot_as_image(df, name="insight_plot"):
    import plotly.io as pio
    try:
        fig = px.line(df)  # generic fallback graph
        path = f"temp_charts/{name}.png"
        pio.write_image(fig, path, format="png", width=800, height=400)
        return path
    except Exception as e:
        print(f"Failed to save plot image: {e}")
        return None

def visualize_from_llm_response(df, query, llm_response):
    chart_type = llm_response.get("chart_type", "bar").lower()
    x = llm_response.get("x")
    y = llm_response.get("y")
    group_by = llm_response.get("group_by")

    try:
        if chart_type == "bar":
            fig = px.bar(df, x=x, y=y, color=group_by)
        elif chart_type == "line":
            fig = px.line(df, x=x, y=y, color=group_by)
        elif chart_type == "scatter":
            fig = px.scatter(df, x=x, y=y, color=group_by)
        elif chart_type == "box":
            fig = px.box(df, x=x, y=y, color=group_by)
        elif chart_type == "violin":
            fig = px.violin(df, x=x, y=y, color=group_by)
        elif chart_type == "area":
            fig = px.area(df, x=x, y=y, color=group_by)
        elif chart_type == "pie":
            fig = px.pie(df, names=x, values=y)
        else:
            return None, "Unsupported chart type."
        return fig, f"Generated {chart_type} chart for {x} vs {y}."
    except Exception as e:
        return None, f"Visualization failed: {str(e)}"

def visualize_comparison_overlay(df1, df2, x, y, name1, name2, chart_type):
    df1_copy = df1.copy()
    df2_copy = df2.copy()
    df1_copy["dataset"] = name1
    df2_copy["dataset"] = name2
    combined = pd.concat([df1_copy, df2_copy])

    try:
        if chart_type == "bar":
            fig = px.bar(combined, x=x, y=y, color="dataset", barmode="group")
        elif chart_type == "line":
            fig = px.line(combined, x=x, y=y, color="dataset")
        elif chart_type == "scatter":
            fig = px.scatter(combined, x=x, y=y, color="dataset")
        else:
            return None, "Unsupported chart type."
        return fig, f"{chart_type.title()} chart overlay of {name1} and {name2}."
    except Exception as e:
        return None, str(e)

def visualize_comparison_side_by_side(df1, df2, x, y, chart_type):
    try:
        fig1, fig2 = None, None
        if chart_type == "bar":
            fig1 = px.bar(df1, x=x, y=y, title="Dataset 1")
            fig2 = px.bar(df2, x=x, y=y, title="Dataset 2")
        elif chart_type == "line":
            fig1 = px.line(df1, x=x, y=y, title="Dataset 1")
            fig2 = px.line(df2, x=x, y=y, title="Dataset 2")
        elif chart_type == "scatter":
            fig1 = px.scatter(df1, x=x, y=y, title="Dataset 1")
            fig2 = px.scatter(df2, x=x, y=y, title="Dataset 2")
        return fig1, fig2
    except Exception as e:
        return None, None


import re
import pandas as pd
import plotly.express as px

def guess_and_generate_chart(df: pd.DataFrame, insight_text: str):
    """
    Guess what chart to generate from insight text and plot from dataframe.
    Returns a Plotly figure if a valid chart suggestion is found.
    """
    try:
        chart_type = None
        if "histogram" in insight_text.lower():
            chart_type = "histogram"
        elif "bar chart" in insight_text.lower():
            chart_type = "bar"
        elif "line chart" in insight_text.lower() or "trend" in insight_text.lower():
            chart_type = "line"
        elif "scatter" in insight_text.lower():
            chart_type = "scatter"

        possible_cols = [col for col in df.columns if re.search(rf"\b{col}\b", insight_text, re.IGNORECASE)]
        x_col = possible_cols[0] if possible_cols else df.columns[0]

        if chart_type == "histogram":
            return px.histogram(df, x=x_col, title=f"Histogram of {x_col}")
        elif chart_type == "bar":
            value_counts = df[x_col].value_counts().nlargest(20)
            return px.bar(x=value_counts.index, y=value_counts.values, labels={"x": x_col, "y": "Count"},
                          title=f"Bar Chart of {x_col}")
        elif chart_type == "line":
            if pd.api.types.is_numeric_dtype(df[x_col]):
                return px.line(df, x=df.index, y=x_col, title=f"Line Chart of {x_col}")
        elif chart_type == "scatter":
            if len(possible_cols) >= 2:
                return px.scatter(df, x=possible_cols[0], y=possible_cols[1], title="Scatter Plot")
        return None
    except Exception:
        return None
