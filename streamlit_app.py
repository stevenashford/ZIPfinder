import streamlit as st
from pyzipcode import ZipCodeDatabase

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
                results = {}

                for zip_code in input_zip_codes:
                    try:
                        origin = zcdb[zip_code]
                        nearby = zcdb.get_zipcodes_around_radius(origin.zip, radius)
                        results[zip_code] = [z.zip for z in nearby]
                    except Exception as e:
                        results[zip_code] = f"Error: {e}"

                # Display results
                for zip_code, nearby_zips in results.items():
                    if isinstance(nearby_zips, list):
                        st.write(f"ZIP Codes within {radius} miles of {zip_code}: {', '.join(nearby_zips)}")
                    else:
                        st.write(f"Error with ZIP Code {zip_code}: {nearby_zips}")
            else:
                st.error("Please enter valid ZIP codes.")
        else:
            st.error("Please enter at least one ZIP code.")

if __name__ == "__main__":
    main()
