365 MACHINE LEARNING PROJECT PACK — IMPORTANT

FILES
- YourName_365_Real_Estate.ipynb: executed notebook with visible outputs
- YourName_365_Coffee_Cafe.ipynb: executed notebook with visible outputs
- *_Notebook_Export.pdf: PDF exports of the notebooks
- *_Report.pdf: concise project report drafts
- real_estate_app.py / coffee_app.py: Streamlit app sources
- *_model.joblib: trained preprocessing/model pipelines
- *_model_dataset.csv / coffee_visit_level_dataset.csv: modelling datasets
- requirements.txt: Python packages for app deployment

BEFORE SUBMISSION
1. Replace YourName in filenames with your own name.
2. Check your institute's exact naming format and upload each notebook and its matching PDF separately if required.
3. Keep the original input files beside the notebooks:
   - dld_transactions.csv
   - 365 Coffee Cafe Dataset.xlsx
4. Read the markdown interpretations and confirm you can explain every filter, feature, metric, and recommendation.
5. Coffee Café note: full-dataset EDA is shown, but the visit-level modelling table uses the first 25,000 transaction lines as a development slice to keep execution manageable. This is a limitation, not the ideal final analysis. If time/memory permits, remove the slice in cell 7 and rerun all cells.
6. Real Estate report is a draft; confirm metrics/interpretations from the notebook outputs before submission.

STREAMLIT DEPLOYMENT (requires your own account)
For each app, create a separate GitHub repository containing:
- the corresponding app .py file renamed to app.py
- its corresponding .joblib model file
- for Real Estate only: real_estate_model_dataset.csv
- requirements.txt
Then create a Streamlit Community Cloud app from that repository, set the main file to app.py, and copy the resulting live URL into your notebook/report. No live URL is included because deployment requires your account authorization.

Use these projects as working drafts and verify all outputs. Do not claim a live deployment until you have deployed and tested it.
