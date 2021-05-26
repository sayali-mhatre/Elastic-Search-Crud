import os
import json
from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response

from esapp.els import (insert, get_docs, update, delete)


def get_properties(path):
    """
    Derives metadata of given directory path or file path
    If it is file then also adds extension of it
    :params path: string
    :return properties: dict
    """
    properties = {
        "size": os.path.getsize(path),
        "created_at": str(datetime.fromtimestamp(os.path.getctime(path))),
        "modified_at": str(datetime.fromtimestamp(os.path.getmtime(path)))
    }
    if os.path.isfile(path):
        properties['ext'] = path.split('.')[-1]
    return properties


@api_view(['POST'])
def insert_fileinfo(request):
    """
    Inserts document to elasticsearch by calling insert() function
    :request data: path
    :return : data_inserted, message, status_code
    """
    body = json.loads(request.body.decode("utf-8"))
    path = body.get("path")
    if not path:
        return Response({"message": "Invalid body.", "status_code": 400})
    properties = get_properties(path)
    id, message, status = insert(properties)
    properties["_id"] = id
    return Response({
        "data_inserted": properties,
        "message": message,
        "status_code": status
    }, status=status)


@api_view(['GET'])
def view_files(request):
    """
    Gets all the documents from elastic search by calling get_doc() function
    :param : None
    :returns : fs_metadata (all docs), message, status_code
    """
    docs, message, status = get_docs()
    return Response({
        "fs_metadata": docs,
        "message": message,
        "status_code": status
    }, status=status)


@api_view(['PUT'])
def update_fileinfo(request):
    """
    Updates document matadata by calling update() function
    Adds tag to document with id=doc_id
    :returns: fs_metadata, message, status_code
    """
    body = json.loads(request.body.decode("utf-8"))
    document_id = body.get("document_id")
    tag = body.get("tag")
    if not document_id or not tag :
        return Response({"message": "Invalid body.", "status_code": 400})
    _source, message, status = update(document_id, tag)
    return Response({
        "fs_metadata": _source,
        "message": message,
        "status_code": status
    }, status=status)


@api_view(['DELETE'])
def delete_fileinfo(request, doc_id):
    """
    Deletes document having id= doc_id from elastic search
    Calls delete() function
    :param doc_id: string
    """
    _id, message, status = delete(doc_id)
    return Response({
        "document_id": doc_id,
        "message": message if _id else "Document not found!",
        "status": status if _id else 404
    })
