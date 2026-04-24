import streamlit as st
import pandas as pd
import os
import altair as alt

# Set up the page
st.set_page_config(page_title="Fintech Risk Analytics Dashboard", layout="wide")

@st.cache_data
def load_data():
    # Define paths relative to the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)
    data_path = os.path.join(base_dir, 'data', 'cleaned_transactions.csv')
    
    # Read the dataset
    df = pd.read_csv(data_path)
    
    # Generate the 'Risk_Flag' column based on the target 'Class' column
    if 'Class' in df.columns:
        df['Risk_Flag'] = df['Class'].apply(lambda x: 'High Risk' if x == 1 else 'Normal')
    else:
        # Fallback if Class is missing
        df['Risk_Flag'] = 'Normal'
        df.loc[df['Amount'] > 3, 'Risk_Flag'] = 'High Risk'
        
    return df

def main():
    st.title("Fintech Risk Analytics Dashboard")
    st.markdown("Visualize High Velocity spenders and transaction outliers over time.")
    
    with st.spinner("Loading dataset..."):
        df = load_data()

    # Sidebar Filters
    st.sidebar.header("Data Filters")
    risk_filter = st.sidebar.multiselect(
        "Filter by Risk Flag:",
        options=df['Risk_Flag'].unique(),
        default=df['Risk_Flag'].unique()
    )
    
    sample_size = st.sidebar.slider(
        "Sample Size for Normal Transactions",
        min_value=1000, max_value=20000, value=5000, step=1000
    )
    
    # Apply Filter
    filtered_df = df[df['Risk_Flag'].isin(risk_filter)]
    
    # Calculate Metrics
    total_risk_flags = len(filtered_df[filtered_df['Risk_Flag'] == 'High Risk'])
    total_amount_at_risk = filtered_df[filtered_df['Risk_Flag'] == 'High Risk']['Amount'].sum()
    avg_risk_score = (total_risk_flags / len(filtered_df)) * 100 if len(filtered_df) > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Risk Flags", f"{total_risk_flags:,}")
    col2.metric("Total Scaled Amount at Risk", f"{total_amount_at_risk:,.2f}")
    col3.metric("Average Risk Score (%)", f"{avg_risk_score:.2f}%")
    
    st.markdown("---")
    
    # Sample down 'Normal' transactions to prevent browser/rendering freezing, keep all 'High Risk'
    high_risk = filtered_df[filtered_df['Risk_Flag'] == 'High Risk']
    normal = filtered_df[filtered_df['Risk_Flag'] == 'Normal']
    if len(normal) > sample_size:
        normal = normal.sample(n=sample_size, random_state=42)
    plot_df = pd.concat([high_risk, normal])

    st.subheader(f"Amount vs. Time (Sampled to {len(plot_df)} Points)")
    
    # Altair Chart
    scatter_chart = alt.Chart(plot_df).mark_circle(size=40, opacity=0.7).encode(
        x=alt.X('Time', title='Time (Relative Hours)'),
        y=alt.Y('Amount', title='Transaction Amount (Scaled)'),
        color=alt.Color(
            'Risk_Flag',
            scale=alt.Scale(domain=['Normal', 'High Risk'], range=['#1f77b4', 'red']),
            legend=alt.Legend(title="Risk Flag")
        ),
        tooltip=['Time', 'Amount', 'Risk_Flag']
    ).properties(
        height=500
    ).interactive()

    st.altair_chart(scatter_chart, use_container_width=True)

    st.markdown("---")
    st.subheader("Data Explorer: High Risk Transactions")
    high_risk_sorted = high_risk.sort_values(by='Amount', ascending=False)
    st.dataframe(high_risk_sorted, use_container_width=True)

if __name__ == "__main__":
    main()
