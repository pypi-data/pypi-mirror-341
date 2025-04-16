# Py4HEAppE API Client Generation
The content contains how to re-generate the HEAppE API wrapper with the new version of the HEAppE API

## Steps
1. Obtain HEAppE API Swagger definition **(eg.http://localhost:5000/swagger/py4heappe/swagger.json)**
2. Upload the downloaded Swagger definition and replace it in repository folder **'Tools\APIWrapperGen\swagger.json'** 
3. Commit into random branch (not into develop or main)
4. Manually triggered pipeline for the API wrapper generation
5. Download pipeline artefact and replace files in **'src/py4heappe/core' (except base directory)**
6. Modify Py4HEAppE CLI affected commands