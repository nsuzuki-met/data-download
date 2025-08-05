# Bulk download CLMS data
Individual tiles or datasets can be easily downloaded using the [CLMS portal](https://land.copernicus.eu/).
However, this can become time-consuming when a large amount of data needs to be downloaded. 
Several methods are available to automate this process and download data programmatically.

## Wget
### Manifest file
A manifest file gives a list of all files related to a specific collection. 
This file can be useful to loop through and download all available data.
Manifest files are available [here](https://globalland.vito.be/download/manifest/).
The identifier of each manifest file can be found in the metadata of the related dataset in the [CLMS portfolio](https://land.copernicus.eu/en/products)

#### On Windows
This tutorial uses the WinWget tool, which can be downloaded [here](https://winwget.sourceforge.net/index.html).
The tool requires a working installation of [GnuWin32 wget](https://gnuwin32.sourceforge.net/packages/wget.htm), for which you can follow [this tutorial](https://www.tomshardware.com/how-to/use-wget-download-files-command-line).

1. Download the manifest file
2. Open WinWget
3. Click “Add job” button
4. Give the job a name
5. Add the manifest file under `[-i] input file`. Important: the tool does not support spaces in the path of the manifest file.
6. Set the output directory under `[-P] Prefix (Local Downloads Folder)`
7. On tab “download” add `1` in the text box for `[-w] --wait`
8. (optional) specify retries with `[-t] --tries`
9. Run the job and monitor execution in the `info` and `log` tabs

#### On Linux
This tutorial uses the wget command line utility. 
The following snippet provides an example workflow which can be modified to your needs.


```shell
# Download the manifest file, rename [-O] the file to be a bit shorter
wget -O clms_global_manifest.txt "https://globalland.vito.be/download/manifest/ba_300m_v3_monthly_netcdf/manifest_clms_global_ba_300m_v3_monthly_netcdf_latest.txt"

# Optionally test if the urls in the manifest file are accessible
# Suppress verbose output [-nv], only check file existence without downloading [--spider] and wait for one second [-w] between each request
# Provide the list of urls to check via the manifest file [-i]
wget -nv --spider -w 1 -i clms_global_manifest.txt

# Download all files in the manifest to a subfolder 'clms_global' of your current directory [-P]
# Force the server to check for new versions of the file [--no-cache], disable cookies [--no-cookies] and retry [-t] up to two times on failure
wget --no-cache --no-cookies -w 1 -t 2 -P clms_global -i clms_global_manifest.txt
```

### Recursive download
Wget also supports recursively downloading a directory structure.
If you've found the data you want to download on [the download page](https://globalland.vito.be/download) it is possible to formulate a wget command and download all data in one go.
Some examples are given below, note the use of `-A` (accept, so include) and `-R` (reject, so exclude) to better specify the files to download.
Please note that the recursive download will process several index.html files. This is normal as wget needs to check these files for additional links.

```shell
# Recursively [-r] get all tiff files [-A] on the provided page, wait 1 second [-w] between downloads and retry two times [-t] on failure
# Force the server to check for new versions of the file [--no-cache], disable cookies [--no-cookies] and prevent wget from following urls upwards in the directory hierarchy [--no-parent]
# Ignore the robots.txt file [-e robots=off] to make sure all files are traversed
wget --no-cache --no-cookies --no-parent -e robots=off -w 1 -t 2 -r -A '.tiff' "https://globalland.vito.be/download/geotiff/land_surface_phenology/lsp_300m_v1_yearly/2023/20230101/"

# Download only the first NDVI tiff file for each month of 1998 using a combination of [-A] and [-R]
# Write all files to a single directory using [-nH] and [-nd]
wget --no-cache --no-cookies --no-parent -e robots=off -nH -nd -w 1 -t 2 -r -A '*1998[0-1][0-9]01*tiff' -R '*TIMEGRID*' "https://globalland.vito.be/download/geotiff/ndvi/ndvi_1km_v2_10daily/1998/"
```

## Python - TerraCatalogueClient
This method uses the [terracatalogueclient](https://github.com/VITObelgium/terracatalogueclient) developed by VITO. 
See the [documentation](https://vitobelgium.github.io/terracatalogueclient/index.html) for installation and usage instructions.

A python code snippet is provided to get started more easily.
````python
import datetime as dt
from terracatalogueclient import Catalogue
from terracatalogueclient.config import CatalogueConfig, CatalogueEnvironment

# Create a link to the CLMS catalogue
config = CatalogueConfig.from_environment(CatalogueEnvironment.CGLS)
catalogue = Catalogue(config)

# Optionally list all collections (title and identifier) available in the catalogue
for c in  list(catalogue.get_collections()) :  
    print(f"{c.properties.get("title")} | {c.id}")  

# Select the products you want to download, e.g. the Normalized Difference Vegetation Index: global 10-daily (raster 1km)
products = list(catalogue.get_products(  
   "clms_global_ndvi_1km_v2_10daily_geotiff",  # this value can be found in the metadata of the collection
    start=dt.date(2020, 4, 1),  
    end=dt.date(2020, 4, 15),  
))

# Download the selected products to a specific local folder
catalogue.download_products(products, "/path/to/local/folder")
````
For more information on specifying products and filtering file types see [the package docs](https://vitobelgium.github.io/terracatalogueclient/usage.html#download-products).

## Python - OpenEO
[OpenEO](https://openeo.org/) can be used to download data in batch if some preprocessing steps are needed, such as spatial or temporal filters.
If you need the source data 'as is' it is better to choose one of the other options listed in this document.
Because OpenEO data processing happens remotely you will need an [EGI](https://www.egi.eu/) account which is linked to a [Terrascope EOplaza user](https://portal.terrascope.be/catalogue) with access to sufficient credits.

The following python snippet gives an example to demonstrate a possible workflow.
See the [EO docs](https://openeo.org/documentation/1.0/python/#installation) for more information.

```python
import openeo
from pprint import pprint

# Connect to the vito openeo service, see https://hub.openeo.org/ for all possible providers
connection = openeo.connect("https://openeo.vito.be/openeo/1.2")

# Authenticate interactively using the browser
connection.authenticate_oidc_device()

# Optionally display all available collections
collections = connection.list_collections()
for c in collections:
    print(f"{c.get("title")} | {c.get("id")}")
    
# Examine the collection to verify spatial and temporal availability
pprint(connection.describe_collection("CGLS_NDVI300_V2_GLOBAL").get('cube:dimensions'))
    
# Specify the subset of the datacube you are interested in
ndvicube = connection.load_collection(
  "CGLS_NDVI300_V2_GLOBAL",
  spatial_extent={"west": 5.056629, "south": 51.209138, "east": 5.107784, "north": 51.234182},
  temporal_extent=["2024-03-01", "2024-04-01"],
  bands=["NDVI"]
)

# Set up the processing pipeline
result = ndvicube.save_result("GTiff")
job = result.create_job()

# Start processing (this example consumes 2 credits)
job.start_and_wait()

# Download the processed files to a local folder
job.get_results().download_files("/path/to/local/folder")
```
