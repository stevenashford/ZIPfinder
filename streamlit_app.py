import streamlit as st
from pyzipcode import ZipCodeDatabase
import pandas as pd
import folium
from streamlit_folium import st_folium

# Initialize ZipCodeDatabase
zcdb = ZipCodeDatabase()

# Streamlit App
def main():
    st.title("ZIP Code Radius Finder")

    # Initialize session state
    if "results_df" not in st.session_state:
        st.session_state.results_df = None
    if "map_instance" not in st.session_state:
        st.session_state.map_instance = None

    # Input: List of ZIP codes and radius
    zip_codes_input = st.text_area("Enter ZIP codes (one per line):")
    radius = st.number_input("Enter the radius (in miles):", min_value=0.0, value=10.0, step=1.0)

    # Parse input ZIP codes
    if st.button("Find ZIP Codes"):
        if zip_codes_input.strip():
            input_zip_codes = [z.strip() for z in zip_codes_input.splitlines() if z.strip().isdigit()]
            if input_zip_codes:
                results = []
                map_center = None
                map_instance = None

                for zip_code in input_zip_codes:
                    try:
                        origin = zcdb[zip_code]
                        nearby = zcdb.get_zipcodes_around_radius(origin.zip, radius)
                        if map_center is None:
                            map_center = (origin.latitude, origin.longitude)
                            map_instance = folium.Map(location=map_center, zoom_start=10)
                        
                        folium.Marker(
                            [origin.latitude, origin.longitude],
                            popup=f"Origin ZIP: {zip_code}",
                            icon=folium.Icon(color="red")
                        ).add_to(map_instance)

                        for z in nearby:
                            results.append({"Provided ZIP": zip_code, "Matched ZIP": z.zip})
                            folium.Marker(
                                [z.latitude, z.longitude],
                                popup=f"Matched ZIP: {z.zip}",
                                icon=folium.Icon(color="blue")
                            ).add_to(map_instance)
                    except Exception as e:
                        results.append({"Provided ZIP": zip_code, "Matched ZIP": f"Error: {e}"})

                # Convert results to DataFrame
                st.session_state.results_df = pd.DataFrame(results)
                st.session_state.map_instance = map_instance
            else:
                st.error("Please enter valid ZIP codes.")
        else:
            st.error("Please enter at least one ZIP code.")

    # Display results
    if st.session_state.results_df is not None:
        st.write("Results:", st.session_state.results_df)

        # Display map
        if st.session_state.map_instance:
            st.write("Map of Results:")
            st_folium(st.session_state.map_instance, width=700, height=500)

        # Download CSV button
        csv = st.session_state.results_df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="zip_code_results.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
