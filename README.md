# Job Tracker

## Uploading a Spreadsheet

To upload a spreadsheet and populate the database:

1. Place your `.xlsx` file in a known location.
2. Update the `file_path` variable in `app/upload_spreadsheet.py` with the path to your file.
3. Run the script:
   ```bash
   python app/upload_spreadsheet.py
   ```
4. Ensure the spreadsheet columns match the database model fields.

See `functional-requirements.md` for functional and technical requirements.
