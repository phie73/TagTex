# TagTex
Creating custom nametags, badges. Planning to use Python + LaTeX only.

### Preparation:
1. download two (!) .csv files from your competition registration list.  
  a) select only the registered competitors (accepted / "bestätigt"), save this as `YOURCOMPETITIONID-registration.csv`, example `GermanNationals2023-registration.csv`  
  b) select ALL people who have ever registered for the competition, including waitlist or deleted registrations, save as for example `YOURCOMPETITIONID-registration-all.csv`, example: `GermanNationals2023-registration-all.csv`

2. download and extract the WCA database in tsv format.  
  place `WCA_export.tsv` in a suitable directory and let the script `main.py` know where to find this information on your device, fill out the hardcoded variable `WCA_database_path` for that purpose.

### Example usage:
```shell
python main.py -c ../wca-competition-orga/GermanNationals2023-registration -id GermanNationals2023 > output.txt
```
This output can be placed in the template document and will serve as the content to be formatted into printable nametags.

It is advisable to check with a 100% scaled view of the resulting PDF if the size fits with your physical nametags before printing and cutting. The labels package documentation can assist with choosing other dimensions for whitespace on the sheets or a different setup of the grid, and the current example has been tested with 55 x 90 mm tags.
