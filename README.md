# Customer .csv Parsing & Importing
### By mave-odoo

## Context
To be able to go into production, The customer first needed to import a large amount of data, the majority of which included photos.

These data present in .csv format had as image source a url http.drive.google.com.

Google Drive API quotas are very limited. Too many requests to the API cause blocking and lead to timeout in odoo.

## Solution
A script that will browse all the .csv files, create new .csv files and replace the drive.google url with the base64 encoded image. It will then use an other [script](https://github.com/tfrancoi/odoo_csv_import) to import the data directly into the database.

### Prerequisite
- Have the .csv files locally on your machine.
- Have the corresponding images locally on your machine.
- The images must have been named correctly so that the script can link the correct image with the correct line in the .csv files (more infos below)
- Having the third party script installed and the right corresponding configuration file. More infos about the installation of it [here](https://github.com/tfrancoi/odoo_csv_import), and about the configuration file [here](https://github.com/tfrancoi/odoo_csv_import)

### Run the script
Navigate to the root of the script file and run:
`bash run.sh <images_directory_path> <csv_directory_path>`

## Steps

#####   1) Images Directory parsing
The script will first map every image name with its path into a JSON file.

#####   2) .csv file parsing
It will then browse every .csv files contained in the csv directory.
It will try to match every data line with an image based on the previously created JSON files containing all images names & path.
If a match is found, it will fill/replace the value in the image column with the corresponding image path.
If no match is found it will leave the value in the column image as an empty string.
A new .csv files is then created with the new values.

The new .csv files and some logs infos can be found in ./result/ at that point

#####    3) Images encoding
It will then take the newly created .csv files and encode the images in base64.
The image columns are now base64 encoded.

#####    3) Data importation
It will then use the [script](https://github.com/tfrancoi/odoo_csv_import) the import the data on to the database.
This step requires to have a properly configured `./configuration.conf`

# More infos coming soon..






