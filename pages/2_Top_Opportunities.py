import streamlit as st

from scanner.opportunity_scanner import (
    OpportunityScanner
)

st.title(
    "🔥 Top Opportunities"
)

if st.button(
    "Scan Market"
):

    with st.spinner(
        "Scanning Stocks..."
    ):

        scanner = (
            OpportunityScanner()
        )

        result = (
            scanner.scan()
        )

        if result.empty:

            st.error(
                "No Results"
            )

        else:

            st.success(
                f"{len(result)} Stocks Scanned"
            )

            st.dataframe(
                result,
                use_container_width=True
            )

            csv = (
                result.to_csv(
                    index=False
                )
            )

            st.download_button(

                "Download CSV",

                csv,

                file_name=
                "opportunities.csv",

                mime=
                "text/csv"
            )