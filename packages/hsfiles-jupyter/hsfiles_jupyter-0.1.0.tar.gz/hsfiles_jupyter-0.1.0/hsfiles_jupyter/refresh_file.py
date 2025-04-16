import os

from .utils import (
    ResourceFileCacheManager,
    logger,
    HydroShareAuthError,
    get_local_absolute_file_path,
)


async def refresh_file_from_hydroshare(file_path: str):
    """Download the file 'file_path' from HydroShare and replace the local file"""

    rfc_manager = ResourceFileCacheManager()
    try:
        res_info = rfc_manager.get_hydroshare_resource_info(file_path)
    except HydroShareAuthError as e:
        return {"error": str(e)}

    if res_info.hs_file_relative_path not in res_info.files:
        file_not_found = True
        if not res_info.refresh:
            files, _ = rfc_manager.get_files(res_info.resource, refresh=True)
            file_not_found = res_info.hs_file_relative_path not in files
        if file_not_found:
            err_msg = f'File {res_info.hs_file_path} is not found in HydroShare resource: {res_info.resource_id}'
            return {"error": err_msg}

    file_dir = os.path.dirname(file_path)
    downloaded_file_path = get_local_absolute_file_path(file_dir)

    try:
        res_info.resource.file_download(path=res_info.hs_file_relative_path, save_path=downloaded_file_path)
        success_msg = (f'File {res_info.hs_file_path} replaced successfully from'
                       f' HydroShare resource: {res_info.resource_id}')
        return {"success": success_msg}
    except Exception as e:
        hs_error = str(e)
        err_msg = (f'Failed to replace file: {res_info.hs_file_path} from HydroShare'
                   f' resource: {res_info.resource_id}. Error: {hs_error}')
        logger.error(err_msg)
        return {"error": err_msg}
