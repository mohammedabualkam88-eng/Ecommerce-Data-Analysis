
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="E-Commerce Analytics Dashboard",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 E-Commerce Analytics Dashboard")
st.write("Advanced E-Commerce Customer and Revenue Analysis")

st.divider()

# ==========================================
# 2. PROJECT PATHS
# ==========================================

project_path = Path(__file__).resolve().parent.parent

# Support both possible processed folders
possible_paths = [
    project_path / "DATA" / "processed",
    project_path / "processed"
]

data_path = next(
    (path for path in possible_paths if (path / "business_kpis.csv").exists()),
    possible_paths[0]
)

# ==========================================
# 3. LOAD DATA
# ==========================================

@st.cache_data
def load_csv(filename, index_col=None):
    file_path = data_path / filename

    if not file_path.exists():
        return None

    return pd.read_csv(file_path, index_col=index_col)


kpis = load_csv("business_kpis.csv")
rfm = load_csv("customer_rfm.csv")
segments = load_csv("customer_segments.csv", index_col=0)
value_segments = load_csv(
    "customer_value_segments.csv",
    index_col=0
)
concentration = load_csv("revenue_concentration.csv")

# ==========================================
# 4. SIDEBAR
# ==========================================

st.sidebar.title("📊 Dashboard Navigation")

page = st.sidebar.radio(
    "Select Analysis",
    [
        "Business Overview",
        "Customer Segmentation",
        "Customer Value",
        "Revenue Concentration",
        "Customer Loyalty"
    ]
)

st.sidebar.divider()
st.sidebar.caption("E-Commerce Data Analysis Project")

# ==========================================
# 5. BUSINESS OVERVIEW
# ==========================================

if page == "Business Overview":

    st.header("📊 Business Performance Overview")

    if kpis is not None:

        required = {"metric", "value"}

        if required.issubset(kpis.columns):

            values = dict(zip(kpis["metric"], kpis["value"]))

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "Total Sales (BRL)",
                f"R$ {values.get('Total Product Sales', 0):,.2f}"
            )

            col2.metric(
                "Total Orders",
                f"{values.get('Total Orders', 0):,.0f}"
            )

            col3.metric(
                "Total Customers",
                f"{values.get('Total Customers', 0):,.0f}"
            )

            col4.metric(
                "Repeat Purchase Rate",
                f"{values.get('Repeat Purchase Rate', 0):.2f}%"
            )

            st.divider()

            st.subheader("Business KPI Details")

            st.dataframe(
                kpis,
                use_container_width=True,
                hide_index=True
            )

            st.subheader("Business Metrics")

            chart_data = kpis[
                kpis["metric"].isin([
                    "Total Orders",
                    "Total Customers"
                ])
            ]

            fig = px.bar(
                chart_data,
                x="metric",
                y="value",
                color="metric",
                text="value",
                title="Orders vs Customers"
            )

            fig.update_traces(texttemplate="%{text:,.0f}")

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.error("Invalid business_kpis.csv columns.")

    else:
        st.error("business_kpis.csv not found.")

# ==========================================
# 6. CUSTOMER SEGMENTATION
# ==========================================


elif page == "Customer Segmentation":

    st.header("👥 Customer Segmentation Analysis")

    if segments is not None:

        segment_df = segments.reset_index()

        if "segment" not in segment_df.columns:
            segment_df = segment_df.rename(
                columns={segment_df.columns[0]: "segment"}
            )

        # ==========================================
        # INTERACTIVE CUSTOMER SEGMENT FILTER
        # ==========================================

        segment_options = sorted(
            segment_df["segment"].dropna().unique().tolist()
        )

        selected_segments = st.multiselect(
            "Select Customer Segments",
            options=segment_options,
            default=segment_options
        )

        filtered_segments = segment_df[
            segment_df["segment"].isin(selected_segments)
        ].copy()

        # ==========================================
        # FILTERED KPIs
        # ==========================================

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Selected Customers",
                f"{filtered_segments['customers'].sum():,.0f}"
            )

        with col2:
            if "total_sales" in filtered_segments.columns:
                st.metric(
                    "Selected Revenue (BRL)",
                    f"R$ {filtered_segments['total_sales'].sum():,.2f}"
                )

        # ==========================================
        # FILTERED CUSTOMER TABLE
        # ==========================================

        st.subheader("Filtered Customer Segments")

        st.dataframe(
            filtered_segments,
            use_container_width=True,
            hide_index=True
        )

        # ==========================================
        # INTERACTIVE CHARTS
        # ==========================================

        if not filtered_segments.empty:

            fig = px.bar(
                filtered_segments,
                x="segment",
                y="customers",
                color="segment",
                text="customers",
                title="Customer Distribution by Segment"
            )

            fig.update_traces(
                texttemplate="%{text:,.0f}",
                textposition="outside"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            if "sales_percentage" in filtered_segments.columns:

                fig2 = px.pie(
                    filtered_segments,
                    names="segment",
                    values="sales_percentage",
                    title="Sales Contribution by Selected Segments"
                )

                st.plotly_chart(
                    fig2,
                    use_container_width=True
                )

        else:
            st.info("Select at least one customer segment.")

    else:
        st.warning("customer_segments.csv not found.")


    st.header("👥 Customer Segmentation Analysis")

    if segments is not None:

        segment_df = segments.reset_index()

        if "segment" not in segment_df.columns:
            segment_df = segment_df.rename(
                columns={segment_df.columns[0]: "segment"}
            )

        st.subheader("Customer Segments")

        st.dataframe(
            segment_df,
            use_container_width=True,
            hide_index=True
        )

        if {"segment", "customers"}.issubset(segment_df.columns):

            fig = px.bar(
                segment_df,
                x="segment",
                y="customers",
                color="segment",
                text="customers",
                title="Customer Distribution by Segment"
            )

            st.plotly_chart(fig, use_container_width=True)

        if {"segment", "sales_percentage"}.issubset(segment_df.columns):

            fig2 = px.pie(
                segment_df,
                names="segment",
                values="sales_percentage",
                title="Sales Contribution by Customer Segment"
            )

            st.plotly_chart(fig2, use_container_width=True)

    else:
        st.warning("customer_segments.csv not found.")

# ==========================================
# 7. CUSTOMER VALUE ANALYSIS
# ==========================================

elif page == "Customer Value":

    st.header("💰 Customer Value Analysis")

    if value_segments is not None:

        value_df = value_segments.reset_index()

        if "value_segment" not in value_df.columns:
            value_df = value_df.rename(
                columns={value_df.columns[0]: "value_segment"}
            )

        st.subheader("Customer Value Segments")

        st.dataframe(
            value_df,
            use_container_width=True,
            hide_index=True
        )

        if {"value_segment", "revenue_share"}.issubset(value_df.columns):

            fig = px.bar(
                value_df,
                x="value_segment",
                y="revenue_share",
                color="value_segment",
                text="revenue_share",
                title="Revenue Contribution by Customer Value Segment",
                labels={
                    "value_segment": "Customer Segment",
                    "revenue_share": "Revenue Share (%)"
                }
            )

            fig.update_traces(texttemplate="%{text:.2f}%")

            st.plotly_chart(fig, use_container_width=True)

        if {"value_segment", "customers"}.issubset(value_df.columns):

            fig2 = px.pie(
                value_df,
                names="value_segment",
                values="customers",
                title="Customer Distribution by Value"
            )

            st.plotly_chart(fig2, use_container_width=True)

    else:
        st.warning("customer_value_segments.csv not found.")

# ==========================================
# 8. REVENUE CONCENTRATION
# ==========================================

elif page == "Revenue Concentration":

    st.header("📈 Customer Revenue Concentration")

    if concentration is not None:

        st.subheader("Revenue Concentration Table")

        st.dataframe(
            concentration,
            use_container_width=True,
            hide_index=True
        )

        required = {
            "Top Customers (%)",
            "Revenue Share (%)"
        }

        if required.issubset(concentration.columns):

            fig = px.bar(
                concentration,
                x="Top Customers (%)",
                y="Revenue Share (%)",
                text="Revenue Share (%)",
                title="Customer Revenue Concentration"
            )

            fig.update_traces(
                texttemplate="%{text:.2f}%",
                textposition="outside"
            )

            fig.update_layout(
                yaxis_range=[0, 100]
            )

            st.plotly_chart(fig, use_container_width=True)

            fig2 = px.line(
                concentration.sort_values("Top Customers (%)"),
                x="Top Customers (%)",
                y="Revenue Share (%)",
                markers=True,
                title="Cumulative Revenue Share"
            )

            fig2.update_layout(
                xaxis_range=[0, 100],
                yaxis_range=[0, 100]
            )

            st.plotly_chart(fig2, use_container_width=True)

    else:
        st.warning("revenue_concentration.csv not found.")

# ==========================================
# 9. CUSTOMER LOYALTY
# ==========================================

elif page == "Customer Loyalty":

    st.header("❤️ Customer Loyalty Analysis")

    if kpis is not None and {"metric", "value"}.issubset(kpis.columns):

        values = dict(zip(kpis["metric"], kpis["value"]))

        repeat_rate = values.get("Repeat Purchase Rate", 0)

        col1, col2 = st.columns(2)

        col1.metric(
            "Repeat Purchase Rate",
            f"{repeat_rate:.2f}%"
        )

        col2.metric(
            "One-Time Customer Rate",
            f"{100 - repeat_rate:.2f}%"
        )

        loyalty_df = pd.DataFrame({
            "Customer Type": [
                "One-Time Customers",
                "Repeat Customers"
            ],
            "Percentage": [
                100 - repeat_rate,
                repeat_rate
            ]
        })

        fig = px.pie(
            loyalty_df,
            names="Customer Type",
            values="Percentage",
            hole=0.5,
            title="Customer Purchase Behavior"
        )

        st.plotly_chart(fig, use_container_width=True)

    if rfm is not None:

        st.subheader("RFM Customer Data")

        st.dataframe(
            rfm.head(100),
            use_container_width=True,
            hide_index=True
        )

        st.caption("Showing the first 100 RFM records.")

# ==========================================
# 10. FOOTER
# ==========================================

st.divider()

st.caption(
    "E-Commerce Analytics Dashboard | "
    "Python • Pandas • Plotly • Streamlit"
)
