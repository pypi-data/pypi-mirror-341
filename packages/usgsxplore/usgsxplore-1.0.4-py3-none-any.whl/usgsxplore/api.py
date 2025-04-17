"""
Description: module contain the API class to download and interact with the USGS api
(https://m2m.cr.usgs.gov/api/docs/json/).
This class is highly inspired by https://github.com/yannforget/landsatxplore.

Last modified: 2024
Author: Luc Godin
"""

import datetime
import json
import random
import signal
import string
import sys
import time
from collections.abc import Generator
from urllib.parse import urljoin

import requests
from tqdm import tqdm

from usgsxplore.errors import (
    ScenesNotFound,
    USGSAuthenticationError,
    USGSError,
    USGSInvalidDataset,
    USGSRateLimitError,
)
from usgsxplore.filter import SceneFilter
from usgsxplore.scenes_downloader import ScenesDownloader

API_URL = "https://m2m.cr.usgs.gov/api/api/json/stable/"


class API:
    """EarthExplorer API."""

    def __init__(self, username: str, token: str, debug_mode: bool = False) -> None:
        """EarthExplorer API.

        :param username: EarthExplorer username.
        :param token: EarthExplorer token.
        """
        self.url = API_URL
        self.session = requests.Session()
        self.label = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.debug_mode = debug_mode
        self.login(username, token)

    @staticmethod
    def raise_api_error(response: requests.Response) -> None:
        """Parse API response and return the appropriate exception.

        :param response: Response from USGS API.
        :raise USGSAuthenticationError: If credentials are not valid of if user lacks permission.
        :raise USGSRateLimitError: If there are too many request
        :raise USGSError: If the USGS API returns a non-null error code.
        """
        data = response.json()
        error_code = data.get("errorCode")
        error_msg = data.get("errorMessage")
        if error_code:
            if error_code in ("AUTH_INVALID", "AUTH_UNAUTHROIZED", "AUTH_KEY_INVALID"):
                raise USGSAuthenticationError(f"{error_code}: {error_msg}.")
            if error_code == "RATE_LIMIT":
                raise USGSRateLimitError(f"{error_code}: {error_msg}.")
            if error_code == "DATASET_INVALID":
                raise USGSInvalidDataset(f"{error_code}: {error_msg}.")
            raise USGSError(f"{error_code}: {error_msg}.")

    def request(self, endpoint: str, params: dict = None, retries: int = 1, timeout: int = 40) -> dict:
        """
        Perform a request to the USGS M2M API with a timeout and retry mechanism.

        :param endpoint: API endpoint.
        :param params: API parameters.
        :param retries: Number of retries in case of rate limit error.
        :raise USGSAuthenticationError: If credentials are not valid or if user lacks permission.
        :raise USGSRateLimitError: If there are too many requests.
        :return: JSON data returned by the USGS API.
        """
        url = urljoin(self.url, endpoint)
        data = json.dumps(params)

        for attempt in range(retries + 1):
            try:
                if self.debug_mode:
                    print(f"[DEBUG] Request attempt {attempt + 1}/{retries + 1}")
                    print(f"[DEBUG] URL: {url}")
                    print(f"[DEBUG] Params: {params}")
                    print(f"[DEBUG] Timeout: {timeout}")

                response = self.session.get(url, data=data, timeout=timeout)

                if self.debug_mode:
                    print(f"[DEBUG] Response status code: {response.status_code}")
                    print(f"[DEBUG] Response text: {response.text}")

                self.raise_api_error(response)
                return response.json().get("data")
            except USGSRateLimitError:
                if attempt < retries:
                    if self.debug_mode:
                        print("[DEBUG] Rate limit hit, retrying in 3s...")
                    time.sleep(3)  # Attente avant de réessayer
                else:
                    raise
            except requests.Timeout:
                if attempt < retries:
                    if self.debug_mode:
                        print("[DEBUG] Request timed out, retrying in 2s...")
                    time.sleep(2)  # Attente avant de réessayer en cas de timeout
                else:
                    raise requests.Timeout("Request timed out after multiple attempts")

    def login(self, username: str, token: str) -> None:
        """Get an API key. With the login-token request

        :param username: EarthExplorer username.
        :param token: EarthExplorer token.
        :raise USGSAuthenticationError: If the authentication failed
        """
        login_url = urljoin(self.url, "login-token")
        payload = {"username": username, "token": token}
        r = self.session.post(login_url, json.dumps(payload))
        self.raise_api_error(r)
        self.session.headers["X-Auth-Token"] = r.json().get("data")

    def logout(self) -> None:
        """Logout from USGS M2M API."""
        self.request("logout")
        self.session = requests.Session()

    def get_entity_id(self, display_id: str | list[str], dataset: str) -> str | list[str]:
        """Get scene ID from product ID.

        Note
        ----
        As the lookup endpoint has been removed in API v1.5, the function makes
        successive calls to scene-list-add and scene-list-get in order to retrieve
        the scene IDs. A temporary sceneList is created and removed at the end of the
        process.

        :param display_id: Input display ID. Can also be a list of display IDs.
        :param dataset: Dataset alias.
        :return: Output entity ID. Can also be a list of entity IDs depending on input.
        """
        # scene-list-add support both entityId and entityIds input parameters
        param = "entityId"
        if isinstance(display_id, list):
            param = "entityIds"

        # a random scene list name is created -- better error handling is needed
        # to ensure that the temporary scene list is removed even if scene-list-get
        # fails.
        list_id = _random_string()
        self.request(
            "scene-list-add",
            params={
                "listId": list_id,
                "datasetName": dataset,
                "idField": "displayId",
                param: display_id,
            },
        )
        r = self.request("scene-list-get", params={"listId": list_id})
        entity_id = [scene["entityId"] for scene in r]
        self.request("scene-list-remove", params={"listId": list_id})

        if param == "entityId":
            return entity_id[0]

        return entity_id

    def metadata(self, entity_id: str, dataset: str) -> dict:
        """Get metadata for a given scene.

        :param entity_id: entity id of the scene
        :param dataset: name of the scene dataset
        :return Scene metadata.
        """
        r = self.request(
            "scene-metadata",
            params={
                "datasetName": dataset,
                "entityId": entity_id,
                "metadataType": "full",
            },
        )
        return r

    def get_display_id(self, entity_id: str, dataset: str) -> str:
        """
        Get display ID from entity ID.

        :param entity_id: entity id of the scene
        :param dataset: Dataset alias.
        :return: display id of the scene
        """
        meta = self.metadata(entity_id, dataset)
        return meta["displayId"]

    def dataset_filters(self, dataset: str) -> list[dict]:
        """
        Return the result of a dataset-filters request

        :param dataset: Dataset alias.
        :return: result of the dataset-filters request
        """
        return self.request("dataset-filters", {"datasetName": dataset})

    def dataset_names(self) -> list[str]:
        """
        Return a list of all existing dataset
        """
        list_dataset = self.request("dataset-search")
        return [dataset["datasetAlias"] for dataset in list_dataset]

    def search(
        self,
        dataset: str,
        location: tuple[float, float] | None = None,
        bbox: tuple[float, float, float, float] | None = None,
        max_cloud_cover: int | None = None,
        date_interval: tuple[str, str] | None = None,
        months: list[int] | None = None,
        meta_filter: str | None = None,
        max_results: int | None = None,
    ) -> list[dict]:
        """
        Search for scenes, and return a list of all scenes found.
        Works with multiple adv_scene_search to get all scenes

        :param dataset: Alias dataset
        :param location: (longitude, latitude) of the point of interest.
        :param bbox: (xmin, ymin, xmax, ymax) of the bounding box.
        :param max_cloud_cover: Max. cloud cover in percent (1-100).
        :param date_interval: (start_date, end_date) of scene acquisition
        :param months: Limit results to specific months (1-12).
        :param meta_filter: String representation of metadata filter ex: camera=L
        :param max_results: Max. number of results. Return all if not provided
        :return: list of scene metadata
        """
        args = {
            "bbox": bbox,
            "max_cloud_cover": max_cloud_cover,
            "months": months,
            "meta_filter": meta_filter,
            "location": location,
            "date_interval": date_interval,
        }
        scene_filter = SceneFilter.from_args(**args)
        scenes = []
        for batch_scenes in self.batch_search(dataset, scene_filter, max_results):
            scenes += batch_scenes
        return scenes

    def batch_search(
        self,
        dataset: str,
        scene_filter: SceneFilter | None = None,
        max_results: int | None = None,
        metadata_type: str = "full",
        use_tqdm: bool = True,
        batch_size: int = 10000,
    ) -> Generator[list[dict], None, None]:
        """
        Return a Generator with each element is a list of 10000 (batch_size) scenes information.
        The scenes are filtered with the scene_filter given.

        :param dataset: Alias dataset
        :param scene_filter: Filter for the scene you want
        :param max_results: max scenes wanted, if None return all scenes found
        :param metadata_type: identifies which metadata to return (full|summary)
        :param use_tqdm: if True display a progress bar of the search
        :param batch_size: number of maxResults of each scene-search
        :return: generator of scenes information batch
        """
        starting_number = 1
        if use_tqdm:
            total = max_results if max_results else None
            p_bar = tqdm(desc="Import scenes metadata", total=total, unit="Scenes")

        while True:
            if max_results and starting_number + batch_size > max_results:
                batch_size = max_results - starting_number + 1
            scene_search = self.scene_search(dataset, scene_filter, batch_size, starting_number, metadata_type)
            yield scene_search["results"]
            starting_number = scene_search["nextRecord"]

            if use_tqdm:
                p_bar.n = starting_number - 1
                p_bar.total = (
                    max_results
                    if max_results and max_results <= scene_search["totalHits"]
                    else scene_search["totalHits"]
                )
                p_bar.refresh()

            if (max_results and scene_search["nextRecord"] > max_results) or starting_number == scene_search[
                "totalHits"
            ]:
                break
        if use_tqdm:
            p_bar.n = p_bar.total
            p_bar.close()

    def scene_search(
        self,
        dataset: str,
        scene_filter: SceneFilter | None = None,
        max_results: int = 100,
        starting_number: int = 1,
        metadata_type: str = "full",
    ) -> dict:
        """Search for scenes.

        :param dataset: Case-insensitive dataset alias (e.g. landsat_tm_c1).
        :param scene_filter: Filter for the scene you want
        :param max_results: Max. number of results. Defaults to 100.
        :param starting_number: starting number of the search. Default 1
        :param metadata_type: identifies which metadata to return (full|summary)
        :return: Result of the scene-search request.
        """
        # we compile the metadataFilter if it exist to format it for the API
        if scene_filter and "metadataFilter" in scene_filter:
            scene_filter["metadataFilter"].compile(self.dataset_filters(dataset))

        r = self.request(
            "scene-search",
            params={
                "datasetName": dataset,
                "sceneFilter": scene_filter,
                "maxResults": max_results,
                "metadataType": metadata_type,
                "startingNumber": starting_number,
            },
        )
        return r

    def download(
        self,
        dataset: str,
        entity_ids: list[str],
        output_dir: str = ".",
        max_thread: int = 5,
        overwrite: bool = False,
        pbar_type: int = 2,
    ) -> None:
        """
        Download GTiff images identify from their entity id, use the M2M API. Progress of
        the downloading can be displayed in terms of the p_bar_type given.

        :param dataset: Alias dataset of scenes wanted
        :param entity_ids: list of entity id of scenes wanted
        :param output_dir: output directory to store GTiff images
        :param max_thread: maximum number of thread that would be used for the downloading
        :param p_bar_type: way to display progress bar (0: no pbar, 1: one pbar, 2: pbar for each scenes)
        """
        # first clean the residus of previous download
        self.clean_download()

        scenes_downloader = ScenesDownloader(entity_ids, output_dir, max_thread, pbar_type, overwrite)

        # get download-options and send it to the scenes_downloader
        download_options = self.request("download-options", {"datasetName": dataset, "entityIds": entity_ids})
        if download_options is None:
            raise ScenesNotFound(f"No scenes found in the dataset '{dataset}'.")
        scenes_downloader.set_download_options(download_options)

        # send a download-request with parsed products
        download_list = scenes_downloader.get_downloads()
        request_results = self.request("download-request", {"downloads": download_list, "label": self.label})

        # defined the ctrl-c signal to stop all downloading thread
        # pylint: disable=unused-argument
        def _handle_sigint(sign, frame):
            scenes_downloader.stop_download()
            sys.exit(0)

        signal.signal(signal.SIGINT, _handle_sigint)

        # first download all scenes in availableDownloads from the download-request
        download_ids = []
        for download in request_results["availableDownloads"]:
            download_ids.append(download["downloadId"])
            scenes_downloader.download(download["entityId"], download["url"])

        # then loop with download-retrieve request every 30 sec to get
        # all download link
        while True:
            retrieve_results = self.request("download-retrieve", {"label": self.label})
            # loop in all link "available" and "requested" and download it
            # with the Product.download method
            for download in retrieve_results["available"] + retrieve_results["requested"]:
                if download["downloadId"] not in download_ids:
                    download_ids.append(download["downloadId"])
                    scenes_downloader.download(download["entityId"], download["url"])

            # if all the link are not ready yet, sleep 30 sec and loop, else exit from the loop
            if len(download_ids) < (len(download_list) - len(request_results["failed"])):
                time.sleep(30)
            else:
                break

        # cleanup the download order and wait all thread to finish
        self.clean_download()
        scenes_downloader.wait_all_thread()

    def clean_download(self) -> None:
        """
        This method clean residus of download in the API it first do
        a "download-order-remove", then it do a "download-search" and do a "download-remove" for each download.
        It called by the download method 2 times
        """
        self.request("download-order-remove", {"label": self.label})
        download_search = self.request("download-search", {"label": self.label})
        if download_search:
            for dl in download_search:
                self.request("download-remove", {"downloadId": dl["downloadId"]})


def _random_string(length=10):
    """Generate a random string."""
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


# End-of-file (EOF)
