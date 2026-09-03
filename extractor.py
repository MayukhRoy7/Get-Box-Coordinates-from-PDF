import pdfplumber
import pandas as pd

# 1. SETUP: The Coordinates you provided
# Format: [x0, top, x1, bottom]
COORD_MAP = {
    "Student Name": [412.62, 164.67, 547.29, 184.67],
    "Father's Name": [409.96, 184.67, 569.96, 198.67],
    "Mother's Name": [410.62, 198, 547.96, 212.67],
    "House": [87, 198, 175, 210],
    "Date of Birth": [87.67, 210.67, 176.33, 228],
    "I.D. No": [87, 184.67, 127, 196.67],
    "Section": [411.67, 212.67, 469.67, 229.33],
    "Roll No": [85.67, 170, 100.33, 183.33],
    
    # PA-I
    "English PA-I (10)": [107, 303.33, 163, 326],
    "Bengali PA-I (10)": [107.67, 325.33, 159, 344],
    "Lower Hindi PA-I (10)": [109.67, 348, 163, 366],
    "Mathematics PA-I (10)": [105.67, 363.33, 159.67, 384.67],
    "Science PA-I (10)": [110.33, 383.33, 157, 405.33],
    "Social Science PA-I (10)": [109.67, 400.67, 159.67, 422.67],
    "General Knowledge PA-I (10)": [105, 422.67, 162.33, 441.33],
    "Computer PA-I (10)": [108.33, 444.67, 163, 460.67],

    # CA-I
    "English CA-I (10)": [163, 304.67, 216.33, 326],
    "Bengali CA-I (10)": [163.67, 324.67, 216.33, 344.67],
    "Mathematics CA-I (10)": [161.67, 364, 214.33, 384],
    "Science CA-I (10)": [165.67, 384.67, 217, 404],
    "Social Science CA-I (10)": [164.33, 401.33, 215.67, 419.33],

    # Half Yearly
    "English Half-Yearly (80)": [218.33, 304, 265, 324],
    "Bengali Half-Yearly (80)": [217.67, 327.33, 265.67, 343.33],
    "Lower Hindi Half-Yearly (40)": [215.67, 344, 267, 363.33],
    "Mathematics Half-Yearly (80)": [220.33, 364.67, 266.33, 384.67],
    "Science Half-Yearly (80)": [223.67, 384.67, 266.33, 405.33],
    "Social Science Half-Yearly (80)": [219.67, 401.33, 263, 422],
    "Genral Knowledge Half-Yearly (40)": [220.33, 425.33, 267.67, 442.67],
    "Computer Half-Yearly (40)": [219, 442.67, 265.67, 460],

    # Term 1 Marks
    "English Term 1 Marks (100)": [268.33, 303.33, 310.33, 324],
    "Bengali Term 1 Marks (100)": [267.67, 326, 307.67, 344.67],
    "Lower Hindi Term 1 Marks (50)": [269, 346.67, 309, 364.67],
    "Mathematics Term 1 Marks (100)": [267, 365.33, 308.33, 384],
    "Science Term 1 Marks (100)": [269, 385.33, 309.67, 403.33],
    "Social Science Term 1 Marks (100)": [270.33, 405.33, 310.33, 422.67],
    "General Knowledge Term 1 Marks (50)": [271, 424.67, 310.33, 441.33],
    "Computer Term 1 Marks (50)": [267.67, 442.67, 309, 459.33],

    # Term 1 Co-Scholastic Grades
    "CCA/Skill Term 1 Grade": [163, 507.33, 226.33, 524.67],
    "Art Term 1 Grade": [162.33, 524.67, 223.67, 543.33],
    "Physical Education Term 1 Grade": [159.67, 542.67, 224.33, 566.67],
    "Discipline Term 1 Grade": [163, 564.67, 223, 586],

    # Term 1 Attendance
    "Total Classes (Term 1)": [422.33, 505.33, 503, 526],
    "Days Present (Term 1)": [427, 527.33, 503.67, 543.33],

    # PA-II
    "English PA-II (10)": [310.33, 300.67, 367, 325.33],
    "Bengali PA-II (10)": [311.67, 326, 367.67, 346],
    "Lower Hindi PA-II (10)": [312.33, 345.33, 365, 363.33],
    "Mathematics PA-II (10)": [313, 365.33, 365.67, 382.67],
    "Science PA-II (10)": [312.33, 384, 365.67, 402],
    "Social Science PA-II (10)": [312.33, 404, 366.33, 422],
    "General Knowledge PA-II (10)": [312.33, 423.33, 366.33, 440.67],
    "Computer PA-II (10)": [312.33, 442.67, 368.33, 462],

    # CA-II
    "English CA-II (10)": [371.67, 301.33, 424.33, 325.33],
    "Bengali CA-II (10)": [370.33, 324, 425, 346.67],
    "Mathematics CA-II (10)": [367, 364, 419.67, 382.67],
    "Science CA-II (10)": [369, 384, 421.67, 404],
    "Social Science CA-II (10)": [370.33, 402.67, 425, 424],

    # Annual
    "English Annual (80)": [423, 300, 472.33, 322],
    "Bengali Annual (80)": [426.33, 323.33, 471.67, 345.33],
    "Lower Hindi Annual (40)": [425.67, 344.67, 471.67, 363.33],
    "Mathematics Annual (80)": [425.67, 367.33, 474.33, 384],
    "Science Annual (80)": [424.33, 381.33, 471, 404],
    "Social Science Annual (80)": [425, 400, 469, 421.33],
    "Genral Knowledge Annual (40)": [422.33, 420, 471, 440],
    "Computer Annual (40)": [423, 441.33, 473, 461.33],

    # Term 2 Marks
    "English Term 2 Marks (100)": [474.33, 304, 517.67, 324.67],
    "Bengali Term 2 Marks (100)": [475.67, 326, 516.33, 344.67],
    "Lower Hindi Term 2 Marks (50)": [475, 347.33, 517.67, 364],
    "Mathematics Term 2 Marks (100)": [476.33, 364.67, 518.33, 385.33],
    "Science Term 2 Marks (100)": [475, 383.33, 516.33, 402],
    "Social Science Term 2 Marks (100)": [473.67, 403.33, 516.33, 422],
    "General Knowledge Term 2 Marks (50)": [475.67, 424, 514.33, 440.67],
    "Computer Term 2 Marks (50)": [475, 441.33, 516.33, 460.67],

    # Term 2 Co-Scholastic Grades
    "CCA Term 2 Grade": [228.33, 503.33, 285, 524.67],
    "Art Term 2 Grade": [227.67, 526.67, 286.33, 543.33],
    "Physical Education Term 2 Grade": [227, 544.67, 286.33, 562],
    "Discipline Term 2 Grade": [227, 562.67, 285.67, 585.33],

    # Term 2 Attendance
    "Total Classes (Term 2)": [505, 505.33, 580.33, 526.67],
    "Days Present (Term 2)": [504.33, 526, 580.33, 544.67],
}

# 2. DEFINING THE FINAL HEADER ORDER
# Includes extracted columns + empty columns (Grades, Totals, %)
FINAL_COLUMNS = [
    "Student Name", "Father's Name", "Mother's Name", "House", "Date of Birth", "I.D. No", "Section", "Roll No",
    "English PA-I (10)", "Bengali PA-I (10)", "Lower Hindi PA-I (10)", "Mathematics PA-I (10)", "Science PA-I (10)", "Social Science PA-I (10)", "General Knowledge PA-I (10)", "Computer PA-I (10)", "PA-I Total (80)", "PA-I %",
    "English CA-I (10)", "Bengali CA-I (10)", "Mathematics CA-I (10)", "Science CA-I (10)", "Social Science CA-I (10)", "CA-I Total (50)", "CA-I %",
    "English Half-Yearly (80)", "Bengali Half-Yearly (80)", "Lower Hindi Half-Yearly (40)", "Mathematics Half-Yearly (80)", "Science Half-Yearly (80)", "Social Science Half-Yearly (80)", "Genral Knowledge Half-Yearly (40)", "Computer Half-Yearly (40)", "Half-Yearly Total (520)", "Half-Yearly %",
    "English Term 1 Marks (100)", "Bengali Term 1 Marks (100)", "Lower Hindi Term 1 Marks (50)", "Mathematics Term 1 Marks (100)", "Science Term 1 Marks (100)", "Social Science Term 1 Marks (100)", "General Knowledge Term 1 Marks (50)", "Computer Term 1 Marks (50)", "Term 1 Total (650)", "Term 1 %",
    "English Term 1 Grade", "Bengali Term 1 Grade", "Lower Hindi Term 1 Grade", "Mathematics Term 1 Grade", "Science Term 1 Grade", "Social Science Term 1 Grade", "General Knowledege Term 1 Grade", "Computer Term 1 Grade",
    "CCA/Skill Term 1 Grade", "Art Term 1 Grade", "Physical Education Term 1 Grade", "Discipline Term 1 Grade",
    "Total Classes (Term 1)", "Days Present (Term 1)", "Attendance % (Term 1)",
    "English PA-II (10)", "Bengali PA-II (10)", "Lower Hindi PA-II (10)", "Mathematics PA-II (10)", "Science PA-II (10)", "Social Science PA-II (10)", "General Knowledge PA-II (10)", "Computer PA-II (10)", "PA-II Total (80)", "PA-II %",
    "English CA-II (10)", "Bengali CA-II (10)", "Mathematics CA-II (10)", "Science CA-II (10)", "Social Science CA-II (10)", "CA-II Total (50)", "CA-II %",
    "English Annual (80)", "Bengali Annual (80)", "Lower Hindi Annual (40)", "Mathematics Annual (80)", "Science Annual (80)", "Social Science Annual (80)", "Genral Knowledge Annual (40)", "Computer Annual (40)", "Annual Total (520)", "Annual %",
    "English Term 2 Marks (100)", "Bengali Term 2 Marks (100)", "Lower Hindi Term 2 Marks (50)", "Mathematics Term 2 Marks (100)", "Science Term 2 Marks (100)", "Social Science Term 2 Marks (100)", "General Knowledge Term 2 Marks (50)", "Computer Term 2 Marks (50)", "Term 2 Total (650)", "Term 2 %",
    "English Term 2 Grade", "Bengali Term 2 Grade", "Lower Hindi Term 2 Grade", "Mathematics Term 2 Grade", "Science Term 2 Grade", "Social Science Term 2 Grade", "General Knowledege Term 2 Grade", "Computer Term 2 Grade",
    "CCA Term 2 Grade", "Art Term 2 Grade", "Physical Education Term 2 Grade", "Discipline Term 2 Grade",
    "Total Classes (Term 2)", "Days Present (Term 2)", "Attendance % (Term 2)", "TOTAL"
]

# 3. PROCESSING
print("Starting extraction... this might take a minute.")
extracted_data = []

# Replace this with your actual PDF filename
pdf_path = "report_cards.pdf"

try:
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        for i, page in enumerate(pdf.pages):
            print(f"Processing page {i+1} of {total_pages}...")
            
            row_data = {}
            
            # Extract data for keys where we have coordinates
            for key, box in COORD_MAP.items():
                try:
                    # Crop the page to the specific box and extract text
                    # box is [x0, top, x1, bottom]
                    crop = page.crop(box)
                    text = crop.extract_text()
                    if text:
                        row_data[key] = text.strip()
                    else:
                        row_data[key] = "" # Handle empty boxes
                except Exception as e:
                    row_data[key] = "" # Handle coordinate errors gracefully
            
            extracted_data.append(row_data)

    # 4. EXPORT TO EXCEL
    print("Creating Excel file...")
    df = pd.DataFrame(extracted_data)

    # Add missing columns (Totals, Grades, %) as empty strings
    for col in FINAL_COLUMNS:
        if col not in df.columns:
            df[col] = ""

    # Reorder columns to match the exact sequence you wanted
    df = df[FINAL_COLUMNS]

    # Save
    output_filename = "final_report_data.xlsx"
    df.to_excel(output_filename, index=False)
    print(f"Success! Download {output_filename}")
    
    # If running in Colab, this triggers a download
    try:
        from google.colab import files
        files.download(output_filename)
    except ImportError:
        pass

except FileNotFoundError:
    print(f"Error: Could not find '{pdf_path}'. Please make sure you uploaded the file and named it correctly.")