import streamlit as st
from pyzipcode import ZipCodeDatabase
import pandas as pd

# Initialize ZipCodeDatabase
zcdb = ZipCodeDatabase()

# Streamlit App
def main():
    st.title("ZIP Code Radius Finder")

    # Input: List of ZIP codes and radius
    zip_codes_input = st.text_area("Enter ZIP codes (one per line):")
    radius = st.number_input("Enter the radius (in miles):", min_value=0.0, value=10.0, step=1.0)

    # Parse input ZIP codes
    if st.button("Find ZIP Codes"):
        if zip_codes_input.strip():
            input_zip_codes = [z.strip() for z in zip_codes_input.splitlines() if z.strip().isdigit()]
            if input_zip_codes:
                results = []

                for zip_code in input_zip_codes:
                    try:
                        origin = zcdb[zip_code]
                        nearby = zcdb.get_zipcodes_around_radius(origin.zip, radius)
                        for z in nearby:
                            results.append({"Provided ZIP": zip_code, "Matched ZIP": z.zip})
                    except Exception as e:
                        results.append({"Provided ZIP": zip_code, "Matched ZIP": f"Error: {e}"})

                # Convert results to DataFrame
                results_df = pd.DataFrame(results)

                # Display results
                st.write("Results:", results_df)

                # Download CSV button
                csv = results_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="zip_code_results.csv",
                    mime="text/csv"
                )
            else:
                st.error("Please enter valid ZIP codes.")
        else:
            st.error("Please enter at least one ZIP code.")

if __name__ == "__main__":
    main()