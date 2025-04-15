
import json
import os
from typing import Any, List


@staticmethod
def buildODataViewName(baseView: str | None) -> str:
    return f"{baseView}_CDS";

@staticmethod
def __getFilePath(filename: str) -> str:
    return os.path.join(os.path.dirname(__file__), 'views_metadata', filename);

@staticmethod 
def __getFolderPath(*trailing: str):
    return os.path.join(os.path.dirname(__file__), 'views_metadata', *trailing);

@staticmethod
def __sortPaths(p: dict[str, Any]) -> int:
    return p.get('path', '').count('/');

@staticmethod
def __formatPaths(paths: dict[str, Any]) -> List[dict[str, Any]]:
    pathKeys: List[str] = list(paths.keys());
    return list(map(lambda k: {
        'path': k,
        'description': f'{paths.get(k, {}).get("get", {}).get("summary", "")} {paths.get(k, {}).get("get", {}).get("description", "")}',
        # 'parameters': paths.get(k, {}).get("get", {}).get("parameters", []),
    }, pathKeys));

@staticmethod
def __getApprovedPaths(ps: dict[str, Any]) -> List[dict[str, Any]]:
    paths = {};
    for pathName in ps.keys():
        if('get' in ps[pathName]): 
            paths[pathName] = ps[pathName];
    formatted: List[dict[str, Any]] = __formatPaths(paths);
    formatted.sort(key=__sortPaths);

    return [p for p in formatted if (p.get('path', '').count('/') <= 1 and p.get('path', '').count('{') == 0)];

@staticmethod
def getAvailableODataServices() -> List[dict[str, Any]]:
    services: List[dict[str, Any]] = [];
    metadata_folder_path = __getFolderPath();
    for filename in os.listdir(metadata_folder_path):
        if filename.endswith(".json"):  # Ensure only JSON files are processed
            file_path = __getFilePath(filename)
            try:
                # Read and process the file
                with open(file_path, 'r') as file:
                    metadata = json.load(file);
                approved_paths = __getApprovedPaths(metadata.get('paths', {}));
                if(approved_paths):
                    services.append({
                        'name': metadata.get('info', {}).get('name', ''),
                        'classification_label':  metadata.get('info', {}).get('classification_label', ''),
                        'endpoint': f"/sap/opu/odata/sap/{metadata.get('info', {}).get('name', '')}",
                        'description': metadata.get('info', {}).get('description', ''),
                        'paths': approved_paths,
                    });
            except Exception as e:
                 continue;
    return services;   

@staticmethod
def getColumnsInfoRepo() -> str:
    return __getFolderPath('entity_columns');

@staticmethod
def getColumnsInfoFilePath(endpoint_path: str) -> str:
    try:
        endpoint = endpoint_path.replace('/', '').replace('\\', '');
        return __getFolderPath('entity_columns', f'{endpoint}.json');
    except Exception as e:
        return '';

@staticmethod
def getColumnsInfoFileContent(path_to_file: str) -> dict:
    try:
        with open(path_to_file, 'r') as file:
            info = json.load(file);
        return info;
    except Exception as e:
        return {};