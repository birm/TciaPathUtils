import xlrd
import argparse

# arguments
parser = argparse.ArgumentParser(description='CPTAC Datascope Automation')
parser.add_argument('-f', dest='filename', help='filepath for Qualified Sheet')
parser.add_argument('-s', dest='sheet', help='Sheet within file')
parser.add_argument('-t', dest='type', default='p', choices=['path', 'rad', 'clinical', 'links', 'p', 'r', 'c', 'l'], help='What operation to perform')
parser.add_argument('-d', dest='dest', help='Where to put the output. If empty, STDOUT, else the mongo uri given.')
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
postfcn = lambda x: x

# field translation

if (args.type == "p" or args.type == "path"):
    def p_postfcn (x):
        # rename variables
        x['Tumor'] = x['Tumor_Type']
        del x['Tumor_Type']
        x['Volume'] = x['Volume_(ml)']
        del x['Volume_(ml)']
        x['Weight'] = x['Weight_(mg)']
        del x['Weight_(mg)']
        # require variables
        try:
            assert(x['Case_ID'])
            assert(x['Tumor_Site'])
            assert(x['Specimen_ID'])
            assert(x['Slide_ID'])
            assert(x["Topographic_Site"])
            assert(x["Specimen_Type"])
        except KeyError as e:
            print("Expected but did not find " + str(e))
            exit(1)
        # special variables
        x['Pathology'] = x["Slide_ID"]
        x['Genomics'] = x["Case_ID"]
        x['Proteomics'] = x["Case_ID"]
        #TODO actually do radiology search
        x['Radiology'] = x.get("Slide_ID", "")
        if x['Radiology']:
            x["HasRadiology"] = "true"
        else:
            x["HasRadiology"] = "false"
        # transformations
        if x['Genomics'] == 'Available':
            x['Genomics'] = x["Case_ID"]
        else:
            x['Genomics'] = ""
        if x['Proteomics'] == 'Available':
            x['Proteomics'] = x["Case_ID"]
        else:
            x['Proteomics'] = ""
        # numerics N/A or missing to -1
        numerics = ["Weight", "Percent_Tumor_Nuclei", "Percent_Total_Cellularity", "Percent_Necrosis", "Volume", "Percent_Blast" ]
        for n in numerics:
            if not n in x:
                x[n] = "-1"
            elif type(x[n]) is str and not x[n].isnumeric():
                x[n] = "-1"
        return x
    postfcn = p_postfcn
    pass

if (args.type == "r" or args.type == "rad"):
    pass


if (args.type == "c" or args.type == "clinical"):
    # TODO
    pass

if (args.type == "l" or args.type == "links"):
    # TODO
    # fields: Genomics, Proteomics, GDC Link, PDC Link
    pass

# data processing with translation and postfcn
first_row = [] # The row where we stock the name of the column
for col in range(worksheet.ncols):
    first_row.append( worksheet.cell_value(0,col) )
# tronsform the workbook to a list of dictionnary
data =[]
for row in range(1, worksheet.nrows):
    elm = {}
    for col in range(worksheet.ncols):
        x = first_row[col].strip().replace(" ", "_")
        elm[x]=worksheet.cell_value(row,col)
    data.append(postfcn(elm))

# TODO
# post processing
print(data)
