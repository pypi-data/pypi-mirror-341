from requests import Session, RequestException
from typing import Dict, Any, Optional, List, BinaryIO, cast
import os
from .exceptions import (
    HerawError,
    AuthenticationError,
    ValidationError,
    RateLimitError,
    ServerError,
)
from .types import (
    ProjectDict,
    FileDict,
    FolderDict,
    FolderContentDict,
    CastDict,
    CustomFieldDict,
    SubtitleDict,
    SearchResultDict,
    TeamDict,
    EntityDict,
    FileCreateResponseDict,
    PartUploadDict,
    FileUploadDict,
)


class Heraw:
    """
    Client for the heraw API.

    This client handles authentication and provides methods for
    all heraw API endpoints.
    """

    def __init__(self, api_key: str, base_url: str = "https://api.heraw.com/public/v1"):
        """
        Initialize the heraw API client.

        Args:
            api_key: Your heraw API key
            base_url: The base URL for the heraw API
        """
        self.api_key = api_key
        self.base_url = base_url
        self.session = Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
        debug: bool = False,
    ) -> Dict[str, Any]:
        """
        Make a request to the heraw API.

        Args:
            method: HTTP method (get, post, put, delete)
            endpoint: API endpoint to call
            params: Query parameters to include in the request
            data: Form data to include in the request
            json: JSON data to include in the request
            files: Files to upload

        Returns:
            The JSON response from the API

        Raises:
            HerawError: If the API returns an error
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        try:
            response = self.session.request(
                method, url, params=params, data=data, json=json, files=files
            )
            if debug:
                print(response.text)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            status_code = getattr(e.response, "status_code", None)
            error_response = None

            if hasattr(e, "response") and e.response is not None:
                try:
                    error_response = e.response.json()
                    error_message = error_response.get("message", str(e))
                except ValueError:
                    error_message = str(e)
            else:
                error_message = str(e)

            if status_code == 401:
                raise AuthenticationError(
                    message=error_message,
                    status_code=status_code,
                    response=error_response,
                ) from e
            elif status_code == 422:
                raise ValidationError(
                    message=error_message,
                    status_code=status_code,
                    response=error_response,
                ) from e
            elif status_code == 429:
                raise RateLimitError(
                    message=error_message,
                    status_code=status_code,
                    response=error_response,
                ) from e
            elif status_code and status_code >= 500:
                raise ServerError(
                    message=error_message,
                    status_code=status_code,
                    response=error_response,
                ) from e
            else:
                raise HerawError(
                    message=error_message,
                    status_code=status_code,
                    response=error_response,
                ) from e

    # Entity methods

    def list_entities(self, workspace_name: str) -> List[EntityDict]:
        """
        List all entities in a workspace.
        """
        endpoint = f"workspaces/{workspace_name}/entities"
        return cast(List[EntityDict], self._request("get", endpoint))

    def create_entity(self, data: Dict[str, Any], workspace_name: str) -> EntityDict:
        """
        Create an entity.
        """
        endpoint = f"workspaces/{workspace_name}/entities"
        return cast(EntityDict, self._request("post", endpoint, json=data))

    def update_entity(
        self, entity_uuid: str, data: Dict[str, Any], workspace_name: str
    ) -> EntityDict:
        """
        Update an entity.
        """
        endpoint = f"workspaces/{workspace_name}/entities/{entity_uuid}"
        return cast(EntityDict, self._request("patch", endpoint, json=data))

    def delete_entity(self, entity_uuid: str, workspace_name: str) -> Dict[str, Any]:
        """
        Delete an entity.
        """
        endpoint = f"workspaces/{workspace_name}/entities/{entity_uuid}"
        return self._request("delete", endpoint)

    # File methods

    def create_file(self, data: Dict[str, Any], workspace_name: str) -> FileDict:
        """
        Create a new file entry to be uploaded.

        Args:
            data: File data including folderUuid, mimeType, size, name, etc.
            workspace_name: The name of the workspace

        Returns:
            The created file entry
        """
        if workspace_name:
            endpoint = f"workspaces/{workspace_name}/files"
        else:
            endpoint = "file"
        response = self._request("post", endpoint, json=data)
        return cast(FileDict, response)

    def delete_file(self, file_uuid: str, workspace_name: str) -> Dict[str, Any]:
        """
        Delete a file.

        Args:
            file_uuid: The UUID of the file to delete
            workspace_name: The name of the workspace

        Returns:
            The deletion response
        """
        if workspace_name:
            endpoint = f"workspaces/{workspace_name}/files/{file_uuid}"
        else:
            endpoint = f"file/{file_uuid}"
        return self._request("delete", endpoint)

    def delete_file_permanently(
        self, file_uuid: str, workspace_name: str
    ) -> Dict[str, Any]:
        """
        Delete a file permanently and destroy all assets.

        Args:
            file_uuid: The UUID of the file to delete
            workspace_name: The name of the workspace

        Returns:
            The deletion response
        """
        if workspace_name:
            endpoint = f"workspaces/{workspace_name}/files/{file_uuid}/delete"
        else:
            endpoint = f"file/{file_uuid}/delete"
        return self._request("delete", endpoint)

    def update_file_status(
        self, file_uuid: str, status: str, workspace_name: str
    ) -> FileDict:
        """
        Update the status of a file.

        Args:
            file_uuid: The UUID of the file
            status: The new status (default, retake, in_progress, to_validate, final)
            workspace_name: The name of the workspace

        Returns:
            The updated file
        """
        if workspace_name:
            endpoint = f"workspaces/{workspace_name}/file/{file_uuid}/status"
        else:
            endpoint = f"file/{file_uuid}/status"
        response = self._request("put", endpoint, json={"status": status})
        return cast(FileDict, response)

    def get_file_version(
        self,
        file_uuid: str,
        file_version: str,
        workspace_name: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> FileDict:
        """
        Get a file version.

        Args:
            file_uuid: The UUID of the file
            file_version: The version of the file
            workspace_name: The name of the workspace
            params: Optional query parameters

        Returns:
            The file version
        """
        if workspace_name:
            endpoint = (
                f"workspaces/{workspace_name}/files/{file_uuid}/versions/{file_version}"
            )
        else:
            endpoint = f"file/{file_uuid}/v/{file_version}"
        return cast(FileDict, self._request("get", endpoint, params=params))

    def create_file_version(
        self, file_uuid: str, data: Dict[str, Any], workspace_name: str
    ) -> FileDict:
        """
        Create a new version of a file.

        Args:
            file_uuid: The UUID of the file
            data: Version data
            workspace_name: The name of the workspace

        Returns:
            The created file version
        """
        if workspace_name:
            endpoint = f"workspaces/{workspace_name}/files/{file_uuid}/versions"
        else:
            endpoint = f"file-versions/{file_uuid}"
        return cast(FileDict, self._request("post", endpoint, json=data))

    def get_file_subtitles(
        self,
        file_uuid: str,
        file_version: str,
        workspace_name: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> List[SubtitleDict]:
        """
        Get file subtitles.

        Args:
            file_uuid: The UUID of the file
            file_version: The version of the file
            workspace_name: The name of the workspace
            params: Optional query parameters

        Returns:
            The file subtitles
        """
        if workspace_name:
            endpoint = f"workspaces/{workspace_name}/files/{file_uuid}/versions/{file_version}/subtitles"
        else:
            endpoint = f"file/{file_uuid}/v/{file_version}/subtitles"
        response = self._request("get", endpoint, params=params)
        if isinstance(response, list):
            return response
        elif "subtitles" in response:
            return response["subtitles"]
        return []

    def get_file_custom_fields(
        self, file_uuid: str, workspace_name: str
    ) -> Dict[str, Any]:
        """
        List all the custom field values related to a file.

        Args:
            file_uuid: The UUID of the file
            workspace_name: The name of the workspace

        Returns:
            The file custom fields
        """
        endpoint = f"workspaces/{workspace_name}/files/{file_uuid}/custom-fields"
        return self._request("get", endpoint)

    def set_file_custom_fields(
        self, file_uuid: str, data: Dict[str, Any], workspace_name: str
    ) -> Dict[str, Any]:
        """
        Set custom field values to a file.

        Args:
            file_uuid: The UUID of the file
            data: Custom field values
            workspace_name: The name of the workspace

        Returns:
            The updated file
        """
        endpoint = f"workspaces/{workspace_name}/files/{file_uuid}/custom-fields"
        return self._request("put", endpoint, json=data)

    def ingest_file(self, data: Dict[str, Any], workspace_name: str) -> FileDict:
        """
        Upload a file at path while creating any missing folder.

        Args:
            data: Ingest data
            workspace_name: The name of the workspace

        Returns:
            The ingestion result
        """
        if workspace_name:
            endpoint = f"workspaces/{workspace_name}/ingest"
        else:
            endpoint = "ingest"
        return cast(FileDict, self._request("post", endpoint, json=data))

    def ingest_file_from_s3(
        self, data: Dict[str, Any], workspace_name: str
    ) -> Dict[str, Any]:
        """
        Upload a file from an S3 source at path while creating any missing folder.

        Args:
            data: S3 source data
            workspace_name: The name of the workspace

        Returns:
            The ingestion result
        """
        if workspace_name:
            endpoint = f"workspaces/{workspace_name}/ingest/s3"
        else:
            endpoint = "ingest/s3"
        return self._request("post", endpoint, json=data)

    def _complete_multipart_upload(
        self,
        asset_uuid: str,
        upload_id: str,
        parts: List[PartUploadDict],
        workspace_name: str,
    ) -> FileDict:
        """
        Complete a multipart upload.
        """
        if workspace_name:
            endpoint = f"workspaces/{workspace_name}/assets/{asset_uuid}/upload"
        else:
            endpoint = f"assets/{asset_uuid}/upload"

        body = {"uploadId": upload_id, "parts": parts}

        return cast(FileDict, self._request("patch", endpoint, json=body))

    def upload_file(
        self, data: FileUploadDict, workspace_name: str, file_path: str
    ) -> FileDict:
        """
        Upload a file.

        Args:
            data: File metadata including name, mimeType, folderUuid, etc.
            workspace_name: The name of the workspace
            file_path: Path to the file to upload

        Returns:
            The uploaded file information
        """
        import urllib3
        import urllib.parse

        # Create a separate HTTP connection pool with flexible SSL settings
        http = urllib3.PoolManager(
            retries=urllib3.Retry(3, backoff_factor=0.5),
            timeout=urllib3.Timeout(connect=10.0, read=30.0),
        )

        if workspace_name:
            endpoint = f"workspaces/{workspace_name}/files"
        else:
            endpoint = "files"

        # Get file size
        file_size = os.path.getsize(file_path)

        # Prepare upload request body
        body = {
            "name": data.get("name", os.path.basename(file_path)),
            "mimeType": data.get("mimeType", "application/octet-stream"),
            "size": file_size,
            "folderUuid": data.get("folderUuid"),
            "version": data.get("version", 1),
            "uploadGroup": data.get("uploadGroup"),
        }

        if data.get("customFields"):
            body["customFields"] = data.get("customFields")

        # Initiate upload
        file_entry = cast(
            FileCreateResponseDict,
            self._request("post", endpoint, json=body),
        )

        # Extract necessary information
        asset_uuid = file_entry["asset"]["uuid"]
        upload_id = file_entry["uploadId"]
        upload_links = file_entry["links"]
        parts: List[PartUploadDict] = []

        # Upload each chunk to S3
        with open(file_path, "rb") as file:
            for link in upload_links:
                part_number = link["part"]
                chunk_size = link["size"]
                chunk = file.read(chunk_size)

                # Parse the S3 URL to extract host and path+query
                url_parts = urllib.parse.urlparse(link["url"])
                host = url_parts.netloc

                headers = {
                    "Content-Length": str(len(chunk)),
                    "Host": host,
                }

                # Use urllib3 directly for more control over the SSL connection
                try:
                    resp = http.request(
                        "PUT",
                        link["url"],
                        body=chunk,
                        headers=headers,
                        assert_same_host=False,
                        redirect=False,
                    )

                    if resp.status >= 300:
                        raise HerawError(
                            f"Error uploading to S3: HTTP {resp.status}",
                            status_code=resp.status,
                            response={
                                "response": resp.data.decode("utf-8", errors="ignore")
                            },
                        )

                    # Get ETag from response headers
                    etag = resp.headers.get("ETag", "").strip('"')

                except Exception as e:
                    raise HerawError(f"Failed to upload chunk to S3: {str(e)}")

                parts.append({"PartNumber": part_number, "ETag": etag})

        # Complete the multipart upload
        return self._complete_multipart_upload(
            asset_uuid, upload_id, parts, workspace_name
        )

    # Project methods

    def list_projects(self, workspace_name: str) -> List[ProjectDict]:
        """
        List all the projects in a workspace.

        Args:
            workspace_name: The name of the workspace

        Returns:
            A list of projects
        """
        if workspace_name:
            endpoint = f"workspaces/{workspace_name}/projects"
        else:
            endpoint = "projects"
        return cast(List[ProjectDict], self._request("get", endpoint))

    def create_project(self, data: Dict[str, Any], workspace_name: str) -> ProjectDict:
        """
        Create a new project.

        Args:
            data: Project data
            workspace_name: The name of the workspace

        Returns:
            The created project
        """
        if workspace_name:
            endpoint = f"workspaces/{workspace_name}/projects"
        else:
            endpoint = "projects"
        return cast(ProjectDict, self._request("post", endpoint, json=data))

    def get_project(self, project_uuid: str, workspace_name: str) -> ProjectDict:
        """
        Get a project by UUID.

        Args:
            project_uuid: The UUID of the project
            workspace_name: The name of the workspace

        Returns:
            The project
        """
        if workspace_name:
            endpoint = f"workspaces/{workspace_name}/projects/{project_uuid}"
        else:
            endpoint = f"projects/{project_uuid}"
        return cast(ProjectDict, self._request("get", endpoint))

    def update_project(
        self, project_uuid: str, data: Dict[str, Any], workspace_name: str
    ) -> ProjectDict:
        """
        Update a project.

        Args:
            project_uuid: The UUID of the project
            data: Project data to update
            workspace_name: The name of the workspace

        Returns:
            The updated project
        """
        if workspace_name:
            endpoint = f"workspaces/{workspace_name}/projects/{project_uuid}"
        else:
            endpoint = f"projects/{project_uuid}"
        return cast(ProjectDict, self._request("patch", endpoint, json=data))

    def delete_project(self, project_uuid: str, workspace_name: str) -> Dict[str, Any]:
        """
        Delete a project.

        Args:
            project_uuid: The UUID of the project
            workspace_name: The name of the workspace

        Returns:
            The deletion response
        """
        if workspace_name:
            endpoint = f"workspaces/{workspace_name}/projects/{project_uuid}"
        else:
            endpoint = f"projects/{project_uuid}"
        return self._request("delete", endpoint)

    def update_project_status(self, project_uuid: str, status: str) -> ProjectDict:
        """
        Update a project's status.

        Args:
            project_uuid: The UUID of the project
            status: The new status (IN_PROGRESS, ARCHIVED)

        Returns:
            The updated project
        """
        endpoint = f"projects/{project_uuid}/status"
        return cast(
            ProjectDict, self._request("put", endpoint, json={"status": status})
        )

    def search_projects(
        self, criteria: Dict[str, Any], workspace_name: str
    ) -> SearchResultDict:
        """
        Search for projects.

        Args:
            criteria: Search criteria
            workspace_name: The name of the workspace

        Returns:
            Search results
        """
        endpoint = f"workspaces/{workspace_name}/search/projects"
        return cast(SearchResultDict, self._request("post", endpoint, json=criteria))

    def get_project_custom_fields(
        self, project_uuid: str, workspace_name: str
    ) -> List[CustomFieldDict]:
        """
        List all the custom field values in a project.

        Args:
            project_uuid: The UUID of the project
            workspace_name: The name of the workspace

        Returns:
            The project custom fields
        """
        endpoint = f"workspaces/{workspace_name}/projects/{project_uuid}/custom-fields"
        return cast(List[CustomFieldDict], self._request("get", endpoint))

    def set_project_custom_fields(
        self, project_uuid: str, data: Dict[str, Any], workspace_name: str
    ) -> ProjectDict:
        """
        Set custom field values to a project.

        Args:
            project_uuid: The UUID of the project
            data: Custom field values
            workspace_name: The name of the workspace

        Returns:
            The updated project
        """
        endpoint = f"workspaces/{workspace_name}/projects/{project_uuid}/custom-fields"
        return cast(ProjectDict, self._request("put", endpoint, json=data))

    def get_project_teams(
        self, project_uuid: str, workspace_name: str
    ) -> List[TeamDict]:
        """
        Get all teams and members for a given project.

        Args:
            project_uuid: The UUID of the project
            workspace_name: The name of the workspace

        Returns:
            Project teams and members
        """
        if workspace_name:
            endpoint = f"workspaces/{workspace_name}/projects/{project_uuid}/teams"
        else:
            endpoint = f"projects/{project_uuid}/teams"
        return cast(List[TeamDict], self._request("get", endpoint))

    # Folder methods

    def get_folder(self, folder_uuid: str, workspace_name: str) -> FolderDict:
        """
        Get a folder.

        Args:
            folder_uuid: The UUID of the folder
            workspace_name: The name of the workspace

        Returns:
            The folder
        """
        if workspace_name:
            endpoint = f"workspaces/{workspace_name}/folders/{folder_uuid}"
        else:
            endpoint = f"folder/{folder_uuid}"
        return cast(FolderDict, self._request("get", endpoint))

    def delete_folder(self, folder_uuid: str, workspace_name: str) -> Dict[str, Any]:
        """
        Delete a folder.

        Args:
            folder_uuid: The UUID of the folder
            workspace_name: The name of the workspace

        Returns:
            The deletion response
        """
        if workspace_name:
            endpoint = f"workspaces/{workspace_name}/folders/{folder_uuid}"
        else:
            endpoint = f"folder/{folder_uuid}"
        return self._request("delete", endpoint)

    def create_folder(self, data: Dict[str, Any], workspace_name: str) -> FolderDict:
        """
        Create a folder.

        Args:
            data: Folder data
            workspace_name: The name of the workspace

        Returns:
            The created folder
        """
        if workspace_name:
            endpoint = f"workspaces/{workspace_name}/folders"
        else:
            endpoint = "folder"
        return cast(FolderDict, self._request("post", endpoint, json=data))

    def get_folder_content(
        self, folder_uuid: str, workspace_name: str, basic: bool = False
    ) -> FolderContentDict:
        """
        Get folder content.

        Args:
            folder_uuid: The UUID of the folder
            workspace_name: The name of the workspace
            basic: Whether to return basic content

        Returns:
            The folder content
        """
        params = {"basic": "true" if basic else None}
        if workspace_name:
            endpoint = f"workspaces/{workspace_name}/folders/{folder_uuid}/content"
        else:
            endpoint = f"folder-content/{folder_uuid}"
        return cast(FolderContentDict, self._request("get", endpoint, params=params))

    def invite_users_to_folder(
        self, folder_uuid: str, data: Dict[str, Any], workspace_name: str
    ) -> Dict[str, Any]:
        """
        Invite users to a folder.

        Args:
            folder_uuid: The UUID of the folder
            data: Invitation data
            workspace_name: The name of the workspace

        Returns:
            The invitation response
        """
        if workspace_name:
            endpoint = f"workspaces/{workspace_name}/folders/{folder_uuid}/user"
        else:
            endpoint = f"folder/{folder_uuid}/invite"
        return self._request("post", endpoint, json=data)

    def set_folder_teams(
        self, folder_uuid: str, team_uuids: List[str], workspace_name: str
    ) -> Dict[str, Any]:
        """
        Change project teams with access to folder.

        Args:
            folder_uuid: The UUID of the folder
            team_uuids: List of team UUIDs
            workspace_name: The name of the workspace

        Returns:
            The update response
        """
        if workspace_name:
            endpoint = f"workspaces/{workspace_name}/folder/{folder_uuid}/teams"
        else:
            endpoint = f"folder/{folder_uuid}/teams"
        return self._request("put", endpoint, json={"teamUuids": team_uuids})

    # Cast methods

    def list_casts(
        self, workspace_name: str, project_uuid: Optional[str] = None
    ) -> List[CastDict]:
        """
        List casts.

        Args:
            workspace_name: The name of the workspace
            project_uuid: Optional project UUID to filter casts

        Returns:
            A list of casts
        """
        params = {"projectUuid": project_uuid} if project_uuid else None
        if workspace_name:
            endpoint = f"workspaces/{workspace_name}/casts"
        else:
            endpoint = "casts"
        return cast(List[CastDict], self._request("get", endpoint, params=params))

    def create_cast(self, data: Dict[str, Any], workspace_name: str) -> CastDict:
        """
        Create a new cast.

        Args:
            data: Cast data
            workspace_name: The name of the workspace

        Returns:
            The created cast
        """
        if workspace_name:
            endpoint = f"workspaces/{workspace_name}/casts"
        else:
            endpoint = "cast"
        return cast(CastDict, self._request("post", endpoint, json=data))

    def update_cast(
        self, cast_uid: str, data: Dict[str, Any], workspace_name: str
    ) -> CastDict:
        """
        Update a cast.

        Args:
            cast_uid: The UID of the cast
            data: Cast data to update
            workspace_name: The name of the workspace

        Returns:
            The updated cast
        """
        if workspace_name:
            endpoint = f"workspaces/{workspace_name}/casts/{cast_uid}"
        else:
            endpoint = f"cast/{cast_uid}"
        return cast(CastDict, self._request("patch", endpoint, json=data))

    def delete_cast(self, cast_uid: str, workspace_name: str) -> Dict[str, Any]:
        """
        Delete a cast.

        Args:
            cast_uid: The UID of the cast
            workspace_name: The name of the workspace

        Returns:
            The deletion response
        """
        if workspace_name:
            endpoint = f"workspaces/{workspace_name}/casts/{cast_uid}"
        else:
            endpoint = f"cast/{cast_uid}"
        return self._request("delete", endpoint)

    def share_cast(
        self, cast_uid: str, data: Dict[str, Any], workspace_name: str
    ) -> Dict[str, Any]:
        """
        Share a cast.

        Args:
            cast_uid: The UID of the cast
            data: Share data including emails and message
            workspace_name: The name of the workspace

        Returns:
            The share response
        """
        if workspace_name:
            endpoint = f"workspaces/{workspace_name}/casts/{cast_uid}/share"
        else:
            endpoint = "cast/share"
        return self._request("post", endpoint, json=data)

    # Custom Fields methods

    def list_custom_fields(self, workspace_name: str) -> List[CustomFieldDict]:
        """
        List all custom fields for a workspace.

        Args:
            workspace_name: The name of the workspace

        Returns:
            A list of custom fields
        """
        endpoint = f"workspaces/{workspace_name}/custom-fields"
        return cast(List[CustomFieldDict], self._request("get", endpoint))

    def create_custom_field(
        self, data: Dict[str, Any], workspace_name: str
    ) -> CustomFieldDict:
        """
        Create a custom field.

        Args:
            data: Custom field data
            workspace_name: The name of the workspace

        Returns:
            The created custom field
        """
        endpoint = f"workspaces/{workspace_name}/custom-fields"
        return cast(CustomFieldDict, self._request("post", endpoint, json=data))

    def update_custom_field(
        self, custom_field_uuid: str, data: Dict[str, Any], workspace_name: str
    ) -> CustomFieldDict:
        """
        Update a custom field.

        Args:
            custom_field_uuid: The UUID of the custom field
            data: Custom field data to update
            workspace_name: The name of the workspace

        Returns:
            The updated custom field
        """
        endpoint = f"workspaces/{workspace_name}/custom-fields/{custom_field_uuid}"
        return cast(CustomFieldDict, self._request("patch", endpoint, json=data))

    def delete_custom_field(
        self, custom_field_uuid: str, workspace_name: str
    ) -> Dict[str, Any]:
        """
        Delete a custom field.

        Args:
            custom_field_uuid: The UUID of the custom field
            workspace_name: The name of the workspace

        Returns:
            The deletion response
        """
        endpoint = f"workspaces/{workspace_name}/custom-fields/{custom_field_uuid}"
        return self._request("delete", endpoint)

    # Search methods

    def search(
        self,
        query: str,
        workspace_name: str,
        contexts: Optional[List[str]] = None,
        folder_uuid: Optional[str] = None,
    ) -> SearchResultDict:
        """
        Search for files, folders, comments.

        Args:
            query: Search query
            workspace_name: The name of the workspace
            contexts: Optional contexts to search in
            folder_uuid: Optional folder UUID to limit search

        Returns:
            Search results
        """
        params: Dict[str, Any] = {"query": query}
        if contexts:
            params["contexts"] = ",".join(contexts)
        if folder_uuid:
            params["folderUuid"] = folder_uuid

        if workspace_name:
            endpoint = f"workspaces/{workspace_name}/search"
        else:
            endpoint = "search"
        return cast(SearchResultDict, self._request("get", endpoint, params=params))

    # Subtitles methods

    def get_subtitle(
        self,
        subtitle_uuid: str,
        workspace_name: str,
        format: Optional[str] = None,
        timestamp: Optional[str] = None,
    ) -> SubtitleDict:
        """
        Get a subtitle.

        Args:
            subtitle_uuid: The UUID of the subtitle
            workspace_name: The name of the workspace
            format: Optional format parameter
            timestamp: Optional timestamp parameter

        Returns:
            The subtitle
        """
        params: Dict[str, Any] = {}
        if format:
            params["format"] = format
        if timestamp:
            params["timestamp"] = timestamp

        if workspace_name:
            endpoint = f"workspaces/{workspace_name}/subtitles/{subtitle_uuid}"
        else:
            endpoint = f"subtitle/{subtitle_uuid}"
        return cast(SubtitleDict, self._request("get", endpoint, params=params))

    def upload_subtitle(
        self,
        file_data: BinaryIO,
        file_name: str,
        file_uuid: str,
        locale: str,
        workspace_name: str,
    ) -> SubtitleDict:
        """
        Upload a subtitle file.

        Args:
            file_data: The subtitle file data
            file_name: The name of the subtitle file
            file_uuid: The UUID of the file to attach the subtitle to
            locale: The locale of the subtitle (e.g., en_US)
            workspace_name: The name of the workspace

        Returns:
            The uploaded subtitle
        """
        files = {"file": (file_name, file_data)}
        data = {
            "fileUuid": file_uuid,
            "locale": locale,
        }

        if workspace_name:
            endpoint = f"workspaces/{workspace_name}/subtitles"
        else:
            endpoint = "subtitle"
        return cast(
            SubtitleDict, self._request("post", endpoint, data=data, files=files)
        )
