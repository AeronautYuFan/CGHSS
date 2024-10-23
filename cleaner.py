import pandas as pd
import file_utils

fullDataSet = pd.read_csv(file_utils.get_airtable())

cleaned_dataSet = fullDataSet[['Citation', 'Entity Empowered', 'Triggering Event','Location']]

cleaned_dataSet.to_csv('flowChartData.csv', index=False)