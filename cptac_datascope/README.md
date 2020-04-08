This tool hopes to greatly streamline the process of processing the CDR qualified data to update CPTAC datascope.

## Steps without this tool

# Get the CRD Qualified sheet.
This should contain either just the new data, or all of the data.

# Rename fields
The fields expected are as follows:
Case_ID	Specimen_ID	Slide_ID	Tumor	Topographic_Site	Specimen_Type	Weight	Tumor_Site	Percent_Tumor_Nuclei	Percent_Total_Cellularity	Percent_Necrosis	Volume	Percent_Blast	Fully_Qualified	HasRadiology	Radiology	Pathology									

Rename the fields to match.
HasRadiology, Radiology, and Pathology should be left empty until...

# Populate HasRadiology, Radiology, and Pathology
Has Radiology should be "yes" or "no". Radiology should be equal Case_ID if radiology is found, otherwise empty. Pathology should equal the Slide_ID. These fields are used for linking.

# Clean Numeric Fields
The following fields are numeric:
 Weight Percent_Tumor_Nuclei	Percent_Total_Cellularity	Percent_Necrosis	Volume	 Percent_Blast
Replace N/A or other non-numeric fields with -1, to denote missing data

# Add to the database.
The data is hosted on mongo via bindaas. Export/convert the data from the previous step into something that mongo can understand (e.g. JSON). If

# Update Clinical Data
The script to add associated clinical data is (here)[https://gist.github.com/birm/1bcfe96a450a1ea3f98af3685328a53d] with sample data. Sometimes, we should check if new clinical data is available, and add that to the database.

# Links
Generate the link mapping file. This is a single json object where the Slide_ID is the key, and the link types available are children. Example (here)[https://gist.github.com/birm/cdd4c513a2ad0bb8340c492fc9d7d038].
