#### Performing different CRUD operations on elastic search with the help of REST api.

<br>

### Development Dependencies :
Set up a basic server using Python (v3.6) and Django (v2.2.5), and
spin up a local Elasticsearch (>=v7.5) database.

<br>
### Endpoints :

- `POST` **/insert**  - To insert document to elastic search. Takes `{"path": "file_or_dir_path"}` in json body.
- `GET` **/show** - To get all the documents from elastic search.
- `PUT` **/update** - To get all the documents from elastic search. Takes `{"document_id": "valid_doc_id", "tag": "new_tag"}` in json body.
- `DELETE` **/delete/\<int:doc_id\>** - To delete document present in elastic search, takes doc_id in url.

<br>

### Development Approach - 
1.  Following the TDD approach, firstly created unittests for the functions which perform crud operations in elastic search.
2.  Created a view **insert_fileinfo()** which takes path of directory or file and sends it to **insert()** function
    which creates an index in elastic search and inserts the document in it.
    
    Input: {“file_path”: <file path of file located in the server>}
    
    Processing: The metadata of the file or directory should be inserted into Elasticsearch under the index
    name fs_metadata_<datetime>. If the file path leads to a file, extract the extension from it, and update
    the metadata with an “extension” field. Additionally, for both files and directories include the field
    “date_ingested” with the datetime that the data was ingested at.
    
    Output: {“data_inserted”: <data that was inserted into Elasticsearch>, “message”: <request
    success/fail message>, “status_code”: <request status code>}

3.  Created a view **view_files()** which takes no parameters, it just calls **get_docs()** function
    which fetch and returns all the documents present in elastic search.
    
    Input: None
    Processing: Return all Elasticsearch documents.
    Output: {“fs_metadata”: [{<document 1>}, {<document 2>}, …, {<document n>}], “message”:
    <request success/fail message”>, “status_code”: <request status code>}

4.  Created a view **update_fileinfo()** which takes doc_id and tag as parameters and calls **update() function**
    which updates the document and adds tag to it.
    
    Input: {“document_id”:<the ID of a specific Elasticsearch document>, “tag”:<user input tag name>}
    Processing: Update the document to include the tag from the user input.
    Output: {“fs_metadata”: {<updated document>}, {“status_code”: <request status code>}}

5.  Created a view **delete_fileinfo()** which takes **doc_id** as parameter and calls **delete() function**
    which deletes the document from elastic search.
    
    Input: {“document_id”: <the ID of a specific Elasticsearch docoment>}
    Processing: Delete the Elasticsearch document with the specified ID.
    Output: {“document_id”: <ID of deleted document>, “message”: <request success or fail>,
    “status_code”: <request status code>}

<br>

### Run Commands - 

- The requirements for this project are in `DJANGO_APP`. 

- Create a `.env` file in your project folder and pass `ELASTICSEARCH_HOST` & `ELASTICSEARCH_PORT` variables there.


```bash

# (recommended) create a conda env
conda create -n env_nvs python=3.6
conda activate env_nvs

# get inside of project dir
cd DJANGO_APP

#install requirements for development
pip install -r requirements.txt

# migrate initial tables
python manage.py migrate

# run django server
python manage.py runserver

# run unit tests
python manage.py test

```
