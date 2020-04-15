import xlrd
import argparse

# arguments
parser = argparse.ArgumentParser(description='CPTAC Datascope Automation')
parser.add_argument('-f', dest='filename', help='filepath for Qualified Sheet')
parser.add_argument('-s', dest='sheet', help='Sheet within file')
args = parser.parse_args()

# get the file
try:
    workbook = xlrd.open_workbook(args.filename, on_demand = True)
except FileNotFoundError as e:
    print(e)
    exit(1)

# get the sheet
try:
    worksheet = workbook.sheet_by_name(args.sheet)
except xlrd.biffh.XLRDError as e:
    print('Tried: ', args.sheet)
    print('Sheet Names ', workbook.sheet_names())
    exit(1)


first_row = [] # The row where we stock the name of the column
for col in range(worksheet.ncols):
    first_row.append( worksheet.cell_value(0,col) )
# tronsform the workbook to a list of dictionnary
data =[]
for row in range(1, worksheet.nrows):
    elm = {}
    for col in range(worksheet.ncols):
        elm[first_row[col]]=worksheet.cell_value(row,col)
    data.append(elm)
print(data)

# path case (default)
# list of sheets
# display each sheet with a number
# let the user select a number
# load that sheet
# list of fields expected
# bug user about missing fields; each let them put in another (use numbers)
# translate to what db expects
# N/A in numeric fields


# radiology case
# is this new or replace all?
# add to mongo

# clinical case
# TODO, display err for now
