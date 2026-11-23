
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

possible_paths = [
    project_path / "DATA" / "processed",
    project_path / "processed"
]

data_path = next(
    (
        path for path in possible_paths
        if (path / "business_kpis.csv").exists()
    ),
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
value_segments = load_csv("customer_value_segments.csv", index_col=0)
concentration = load_csv("revenue_concentration.csv")
sales_trends = load_csv("sales_trends.csv")


def require_data(data, filename):
    if data is None:
        st.error(f"Missing file: {filename}")
        st.info(f"Expected folder: {data_path}")
        return False

    if data.empty:
        st.warning(f"No data available in {filename}")
        return False

    return True


def find_column(df, candidates):
    lookup = {
        str(col).strip().lower(): col
        for col in df.columns
    }

    for candidate in candidates:
        result = lookup.get(candidate.lower())
        if result is not None:
            return result

    return None


def show_distribution(df, title):
    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    category_columns = [
        col for col in df.columns
        if col not in numeric_columns
    ]

    if not category_columns or not numeric_columns:
        st.info("No suitable category and numeric columns for a chart.")
        return

    category = category_columns[0]
    value = numeric_columns[0]

    chart_data = (
        df.groupby(category, dropna=False)[value]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        chart_data,
        x=category,
        y=value,
        title=title
    )

    st.plotly_chart(fig, use_container_width=True)


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
        "Customer Loyalty",
        "Sales Trends"
    ]
)

st.sidebar.divider()
st.sidebar.caption("E-Commerce Data Analysis Project")

# ==========================================
# 5. BUSINESS OVERVIEW
# ==========================================

if page == "Business Overview":

    st.header("📊 Business Performance Overview")

    if require_data(kpis, "business_kpis.csv"):

        if {"metric", "value"}.issubset(kpis.columns):
            metrics = dict(
                zip(
                    kpis["metric"].astype(str).str.strip(),
                    pd.to_numeric(kpis["value"], errors="coerce")
                )
            )

            def get_metric(name):
                return metrics.get(name, float("nan"))

            c1, c2, c3, c4 = st.columns(4)

            sales = get_metric("Total Product Sales")
            orders = get_metric("Total Orders")
            customers = get_metric("Total Customers")
            repeat_rate = get_metric("Repeat Purchase Rate")

            c1.metric(
                "Total Sales (BRL)",
                f"R$ {sales:,.2f}" if pd.notna(sales) else "N/A"
            )

            c2.metric(
                "Total Orders",
                f"{orders:,.0f}" if pd.notna(orders) else "N/A"
            )

            c3.metric(
                "Total Customers",
                f"{customers:,.0f}" if pd.notna(customers) else "N/A"
            )

            c4.metric(
                "Repeat Purchase Rate",
                f"{repeat_rate:.2f}%" if pd.notna(repeat_rate) else "N/A"
            )

        else:
            st.warning(
                "KPI file does not contain the expected "
                "'metric' and 'value' columns."
            )

        st.divider()
        st.subheader("Business KPI Details")

        st.dataframe(
            kpis,
            use_container_width=True,
            hide_index=True
        )

# ==========================================
# 6. CUSTOMER SEGMENTATION
# ==========================================

elif page == "Customer Segmentation":

    st.header("👥 Customer Segmentation")

    if require_data(segments, "customer_segments.csv"):

        st.subheader("Customer Segmentation Data")

        st.dataframe(
            segments,
            use_container_width=True
        )

        segment_col = find_column(
            segments,
            ["Segment", "segment", "Customer_Segment"]
        )

        if segment_col is not None:

            counts = (
                segments[segment_col]
                .value_counts()
                .reset_index()
            )

            counts.columns = ["Segment", "Customers"]

            fig = px.bar(
                counts,
                x="Segment",
                y="Customers",
                color="Segment",
                title="Customers by Segment"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:
            show_distribution(
                segments.reset_index(),
                "Customer Segmentation Distribution"
            )

    if require_data(rfm, "customer_rfm.csv"):

        with st.expander("View RFM Data"):
            st.dataframe(
                rfm,
                use_container_width=True
            )

# ==========================================
# 7. CUSTOMER VALUE
# ==========================================

elif page == "Customer Value":

    st.header("💎 Customer Value Analysis")

    if require_data(
        value_segments,
        "customer_value_segments.csv"
    ):

        st.subheader("Customer Value Data")

        st.dataframe(
            value_segments,
            use_container_width=True
        )

        show_distribution(
            value_segments.reset_index(),
            "Customer Value Distribution"
        )

# ==========================================
# 8. REVENUE CONCENTRATION
# ==========================================

elif page == "Revenue Concentration":

    st.header("📊 Revenue Concentration Analysis")

    if require_data(
        concentration,
        "revenue_concentration.csv"
    ):

        st.subheader("Revenue Concentration Data")

        st.dataframe(
            concentration,
            use_container_width=True,
            hide_index=True
        )

        numeric_columns = concentration.select_dtypes(
            include="number"
        ).columns.tolist()

        if len(numeric_columns) >= 2:

            fig = px.line(
                concentration,
                x=numeric_columns[0],
                y=numeric_columns[1],
                markers=True,
                title="Revenue Concentration"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

# ==========================================
# 9. CUSTOMER LOYALTY
# ==========================================

elif page == "Customer Loyalty":

    st.header("🔁 Customer Loyalty Analysis")

    if require_data(rfm, "customer_rfm.csv"):

        frequency_col = find_column(
            rfm,
            ["Frequency", "frequency", "order_count"]
        )

        if frequency_col is not None:

            frequency = pd.to_numeric(
                rfm[frequency_col],
                errors="coerce"
            ).dropna()

            one_time = int((frequency == 1).sum())
            repeat = int((frequency > 1).sum())

            c1, c2 = st.columns(2)

            c1.metric("One-Time Customers", f"{one_time:,}")
            c2.metric("Repeat Customers", f"{repeat:,}")

            loyalty_data = pd.DataFrame({
                "Customer Type": [
                    "One-Time Customers",
                    "Repeat Customers"
                ],
                "Customers": [
                    one_time,
                    repeat
                ]
            })

            fig = px.pie(
                loyalty_data,
                names="Customer Type",
                values="Customers",
                hole=0.45,
                title="Customer Loyalty Distribution"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:
            st.warning(
                "Frequency column was not found in customer_rfm.csv."
            )


# ==========================================
# 10. SALES TRENDS
# ==========================================

elif page == "Sales Trends":
    # ==========================================

    st.header("📈 Sales Trends Analysis")

    if require_data(sales_trends, "sales_trends.csv"):

        required_columns = {
            "year_month",
            "Orders",
            "Revenue"
        }

        if not required_columns.issubset(sales_trends.columns):

            st.error(
                "sales_trends.csv must contain: "
                "year_month, Orders, Revenue"
            )

        else:

            sales = sales_trends.copy()

            sales["year_month"] = pd.to_datetime(
                sales["year_month"],
                errors="coerce"
            )

            sales["Revenue"] = pd.to_numeric(
                sales["Revenue"],
                errors="coerce"
            )

            sales["Orders"] = pd.to_numeric(
                sales["Orders"],
                errors="coerce"
            )

            sales = (
                sales.dropna(subset=["year_month"])
                .sort_values("year_month")
            )

            # INTERACTIVE YEAR FILTER

            sales["Year"] = sales["year_month"].dt.year

            available_years = sorted(
                sales["Year"].dropna().unique().tolist()
            )

            selected_years = st.multiselect(
                "Select Years",
                options=available_years,
                default=available_years
            )

            sales = sales[
                sales["Year"].isin(selected_years)
            ].copy()

            if sales.empty:
                st.warning("No sales data for the selected years.")
                st.stop()

            # Sales trends KPIs
            total_revenue = sales["Revenue"].sum()
            total_orders = sales["Orders"].sum()
            average_monthly_revenue = sales["Revenue"].mean()

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Revenue in Trend Dataset",
                f"R$ {total_revenue:,.2f}"
            )

            c2.metric(
                "Orders in Trend Dataset",
                f"{total_orders:,.0f}"
            )

            c3.metric(
                "Average Monthly Revenue",
                f"R$ {average_monthly_revenue:,.2f}"
            )

            st.divider()

            # Monthly revenue
            st.subheader("Monthly Revenue Trend")

            fig_revenue = px.line(
                sales,
                x="year_month",
                y="Revenue",
                markers=True,
                title="Monthly Revenue Trend"
            )

            st.plotly_chart(
                fig_revenue,
                use_container_width=True
            )

            # ==========================================
            # YEAR-OVER-YEAR REVENUE COMPARISON
            # ==========================================

            st.subheader("Year-over-Year Revenue Comparison")

            comparison_data = sales.copy()

            comparison_data["Month"] = (
                comparison_data["year_month"].dt.month
            )

            comparison_data["Year"] = (
                comparison_data["year_month"].dt.year.astype(str)
            )

            monthly_comparison = (
                comparison_data
                .groupby(["Year", "Month"], as_index=False)["Revenue"]
                .sum()
            )

            fig_comparison = px.line(
                monthly_comparison,
                x="Month",
                y="Revenue",
                color="Year",
                markers=True,
                title="Monthly Revenue Comparison by Year",
                labels={
                    "Month": "Month of Year",
                    "Revenue": "Revenue (BRL)",
                    "Year": "Year"
                }
            )

            fig_comparison.update_xaxes(
                tickmode="array",
                tickvals=list(range(1, 13)),
                ticktext=[
                    "Jan", "Feb", "Mar", "Apr",
                    "May", "Jun", "Jul", "Aug",
                    "Sep", "Oct", "Nov", "Dec"
                ]
            )

            fig_comparison.update_layout(
                hovermode="x unified",
                legend_title_text="Year"
            )

            st.plotly_chart(
                fig_comparison,
                use_container_width=True
            )

            # Monthly orders
            st.subheader("Monthly Order Volume")

            fig_orders = px.bar(
                sales,
                x="year_month",
                y="Orders",
                title="Monthly Orders"
            )

            st.plotly_chart(
                fig_orders,
                use_container_width=True
            )

            # Month-over-Month growth
            if "MoM_Growth" in sales.columns:

                st.subheader("Month-over-Month Revenue Growth")

                sales["MoM_Growth"] = pd.to_numeric(
                    sales["MoM_Growth"],
                    errors="coerce"
                )

                fig_mom = px.bar(
                    sales,
                    x="year_month",
                    y="MoM_Growth",
                    title="MoM Revenue Growth (%)"
                )

                fig_mom.update_layout(
                    yaxis_title="MoM Growth (%)"
                )

                st.plotly_chart(
                    fig_mom,
                    use_container_width=True
                )

            # Year-over-Year growth
            if "YoY_Growth" in sales.columns:

                st.subheader("Year-over-Year Revenue Growth")

                sales["YoY_Growth"] = pd.to_numeric(
                    sales["YoY_Growth"],
                    errors="coerce"
                )

                if "Comparison_Quality" in sales.columns:

                    yoy_data = sales[
                        sales["Comparison_Quality"]
                        == "Standard Comparison"
                    ].copy()

                else:
                    yoy_data = sales.copy()

                yoy_data = yoy_data.dropna(
                    subset=["YoY_Growth"]
                )

                if not yoy_data.empty:

                    fig_yoy = px.bar(
                        yoy_data,
                        x="year_month",
                        y="YoY_Growth",
                        title="YoY Revenue Growth (%)"
                    )

                    fig_yoy.update_layout(
                        yaxis_title="YoY Growth (%)"
                    )

                    st.plotly_chart(
                        fig_yoy,
                        use_container_width=True
                    )

                else:
                    st.info(
                        "No standard YoY comparisons available."
                    )

            # Data quality
            if "Comparison_Quality" in sales.columns:

                st.subheader("YoY Comparison Quality")

                quality = (
                    sales["Comparison_Quality"]
                    .value_counts()
                    .reset_index()
                )

                quality.columns = [
                    "Comparison Quality",
                    "Months"
                ]

                st.dataframe(
                    quality,
                    use_container_width=True,
                    hide_index=True
                )

            # Full table
            st.subheader("Sales Trends Data")

            st.dataframe(
                sales,
                use_container_width=True,
                hide_index=True
            )

            # ==========================================
            # ADVANCED BUSINESS INSIGHTS
            # ==========================================

            st.divider()
            st.header("💡 Advanced Business Insights")

            # 1. Highest Revenue Month
            peak_month = sales.loc[sales["Revenue"].idxmax()]

            peak_month_name = peak_month["year_month"].strftime(
                "%B %Y"
            )

            st.success(
                f"🏆 Highest Revenue Month: {peak_month_name} "
                f"— R$ {peak_month['Revenue']:,.2f}"
            )

            # 2. Year-over-Year Comparable Revenue
            st.subheader("Year-over-Year Comparable Revenue")

            yearly_monthly = sales.copy()

            yearly_monthly["Year"] = (
                yearly_monthly["year_month"].dt.year
            )

            yearly_monthly["Month"] = (
                yearly_monthly["year_month"].dt.month
            )

            revenue_by_month = (
                yearly_monthly
                .groupby(["Year", "Month"])["Revenue"]
                .sum()
                .unstack("Year")
            )

            years = sorted(revenue_by_month.columns)

            if len(years) >= 2:

                comparison_rows = []

                for previous_year, current_year in zip(
                    years[:-1],
                    years[1:]
                ):

                    if current_year != previous_year + 1:
                        continue

                    comparable = revenue_by_month[
                        [previous_year, current_year]
                    ].dropna()

                    if comparable.empty:
                        continue

                    previous_revenue = comparable[
                        previous_year
                    ].sum()

                    current_revenue = comparable[
                        current_year
                    ].sum()

                    if previous_revenue <= 0:
                        continue

                    growth = (
                        (current_revenue - previous_revenue)
                        / previous_revenue
                    ) * 100

                    comparison_rows.append({
                        "Comparison": (
                            f"{previous_year} vs {current_year}"
                        ),
                        "Comparable Months": len(comparable),
                        "Previous Revenue": previous_revenue,
                        "Current Revenue": current_revenue,
                        "Growth (%)": round(growth, 2)
                    })

                if comparison_rows:

                    comparison_df = pd.DataFrame(
                        comparison_rows
                    )

                    st.dataframe(
                        comparison_df,
                        use_container_width=True,
                        hide_index=True
                    )

                    st.caption(
                        "Growth is calculated using only months "
                        "available in both years. Interpret results "
                        "carefully when comparable months are limited."
                    )

                else:
                    st.info(
                        "No comparable consecutive years available."
                    )

            else:
                st.info(
                    "Select at least two years to compare revenue."
                )

            # 3. Best Year by Average Monthly Revenue
            st.subheader("Average Monthly Revenue by Year")

            yearly_performance = (
                yearly_monthly
                .groupby("Year")
                .agg(
                    Total_Revenue=("Revenue", "sum"),
                    Months=("Month", "nunique")
                )
                .reset_index()
            )

            yearly_performance["Average_Monthly_Revenue"] = (
                yearly_performance["Total_Revenue"]
                / yearly_performance["Months"]
            )

            st.dataframe(
                yearly_performance,
                use_container_width=True,
                hide_index=True
            )

            # 4. Data Quality Warning
            st.subheader("Data Quality Insights")

            if "Comparison_Quality" in sales.columns:

                quality_counts = (
                    sales["Comparison_Quality"]
                    .value_counts()
                )

                low_base_count = quality_counts.get(
                    "Low Base", 0
                )

                no_comparison_count = quality_counts.get(
                    "No Comparison", 0
                )

                if low_base_count > 0:
                    st.warning(
                        f"⚠️ {low_base_count} month(s) have "
                        "a low comparison base."
                    )

                if no_comparison_count > 0:
                    st.info(
                        f"ℹ️ {no_comparison_count} month(s) "
                        "have no valid YoY comparison."
                    )

            st.caption(
                "Business insights are based on the selected "
                "years and the available monthly sales data."
            )
