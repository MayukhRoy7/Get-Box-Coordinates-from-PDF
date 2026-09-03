import os
import requests
import time  # Import the time module

def download_report_cards(start_id, end_id, download_folder):
    """
    Downloads a range of PDF report cards to a specified folder with a delay.

    Args:
        start_id (int): The starting number of the report card PDF.
        end_id (int): The ending number of the report card PDF.
        download_folder (str): The absolute path to the folder where files will be saved.
    """
    base_url = "https://s3.ap-southeast-1.amazonaws.com/dpsreportcards/290176/report-cards-641b3cb6f0dda/"

    # Create the download folder if it doesn't exist
    if not os.path.exists(download_folder):
        try:
            os.makedirs(download_folder)
            print(f"Successfully created directory: {download_folder}")
        except OSError as e:
            print(f"Error creating directory {download_folder}: {e}")
            return # Exit if the directory cannot be created

    print(f"Starting download of report cards from {start_id} to {end_id}...")
    print(f"Files will be saved in: {download_folder}")

    for report_id in range(start_id, end_id + 1):
        file_name = f"{report_id}.pdf"
        file_url = f"{base_url}{file_name}"
        save_path = os.path.join(download_folder, file_name)

        try:
            # Send a GET request to the URL
            response = requests.get(file_url, stream=True)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

            # Save the content to a local file
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"Successfully downloaded: {file_name}")

        except requests.exceptions.RequestException as e:
            print(f"Failed to download {file_name}. Reason: {e}")

        finally:
            # --- ADDED DELAY ---
            # Wait for 1 second before the next request, regardless of success or failure.
            print("Waiting for 1 second...")
            time.sleep(1)

if __name__ == "__main__":
    # Define the range of report card numbers to download
    start_report_number = 132339464
    end_report_number = 132340273

    # --- SET YOUR CUSTOM DOWNLOAD FOLDER HERE ---
    # The 'r' before the string is important; it tells Python to treat backslashes as literal characters.
    custom_download_path = r"D:\OneDrive - South Point Education Society\Report Cards\generator\dw"

    download_report_cards(start_report_number, end_report_number, download_folder=custom_download_path)