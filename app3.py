from tabula import read_pdf

df = read_pdf('https://www.colorado.gov/pacific/sites/default/files/0119_MarijuanaSalesReport_PUBLISH.pdf')

int(list(df.columns.values))pr