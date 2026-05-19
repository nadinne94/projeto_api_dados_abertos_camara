"""
Cliente HTTP da API Câmara.

Responsável por:

- requests
- retry / backoff
- paginação
- nested collection
"""

import logging
import time

from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from src.config.api_config import API_CONFIG

logger = logging.getLogger(__name__)

# ==========================================================
# SESSION GLOBAL
# ==========================================================

session = requests.Session()

session.headers.update({

    "Accept": "application/json",

    "User-Agent": "camara-pipeline/1.0"

})

adapter = HTTPAdapter(

    pool_connections=20,

    pool_maxsize=20,

    max_retries=Retry(
        total=0
    )
)

session.mount("https://", adapter)

# ==========================================================
# URL HELPERS
# ==========================================================


def build_endpoint_url(
    endpoint: str
) -> str:
    """
    Monta URL completa.
    """

    if endpoint.startswith("http"):

        return endpoint

    return f"{API_CONFIG['base_url']}{endpoint}"


# ==========================================================
# REQUEST
# ==========================================================


def request_api(
    url: str,
    params: Optional[Dict] = None,
    api_config: Optional[dict] = None
) -> Dict:

    api_config = api_config or API_CONFIG

    params = params or {}

    params.setdefault(
        "itens",
        api_config["page_size"]
    )

    timeout = api_config["timeout"]

    max_retries = api_config["max_retries"]

    retry_delay = api_config["retry_delay"]

    last_exception = None

    for attempt in range(1, max_retries + 1):

        try:

            logger.info(
                "[API] tentativa=%s/%s url=%s",
                attempt,
                max_retries,
                url
            )

            response = session.get(
                url=url,
                params=params,
                timeout=timeout
            )

            status = response.status_code

            if status == 200:

                logger.info(
                    "[API] success status=200"
                )

                return response.json()

            if status == 404:

                logger.warning(
                    "[API] 404 url=%s",
                    url
                )

                return {"dados": []}
            if status == 400:
                logger.warning(
                    "[NESTED_SKIP] endpoint sem recurso id=%s",
                    parent_id
                )

            if status in {

                429,
                500,
                502,
                503,
                504

            }:

                wait = min(
                    retry_delay * (2 ** (attempt - 1)),
                    60
                )

                logger.warning(
                    "[API] retry status=%s wait=%ss",
                    status,
                    wait
                )

                time.sleep(wait)

                continue

            raise RuntimeError(
                f"HTTP {status}: {url}"
            )

        except (
            requests.RequestException,
            ValueError
        ) as exc:

            last_exception = exc

            wait = min(
                retry_delay * (2 ** (attempt - 1)),
                60
            )

            logger.warning(
                "[API] exception=%s retry=%ss",
                exc,
                wait
            )

            time.sleep(wait)

    raise RuntimeError(
        f"Falha API após retries: {url}"
    ) from last_exception


# ==========================================================
# PAGINATION
# ==========================================================


def get_next_page_link(
    response_json: Dict
) -> Optional[str]:
    """
    Extrai link next.
    """

    for link in response_json.get(
        "links",
        []
    ):

        if link.get("rel") == "next":

            return link.get("href")

    return None


def get_all_pages(
    endpoint: str,
    api_config: Optional[dict] = None,
    params: Optional[Dict] = None
) -> List[Dict]:

    api_config = api_config or API_CONFIG

    url = build_endpoint_url(endpoint)

    max_pages = api_config[
        "max_pages_per_execution"
    ]

    request_sleep = api_config[
        "request_sleep"
    ]

    results = []

    page = 1

    first_request = True

    while url and page <= max_pages:

        logger.info(
            "[PAGINATION] page=%s url=%s",
            page,
            url
        )

        response_json = request_api(

            url=url,

            params=(
                params
                if first_request
                else None
            ),

            api_config=api_config
        )

        first_request = False

        dados = response_json.get(
            "dados",
            []
        )

        logger.info(
            "[PAGINATION] registros=%s",
            len(dados)
        )

        results.extend(dados)

        url = get_next_page_link(
            response_json
        )

        page += 1

        time.sleep(request_sleep)

    logger.info(
        "[PAGINATION] total=%s",
        len(results)
    )

    return results


# ==========================================================
# NESTED
# ==========================================================


def format_endpoint(
    endpoint_template: str,
    resource_id: Any
) -> str:

    return endpoint_template.format(
        id=resource_id
    )


def fetch_nested_data(
    endpoint_template: str,
    parent_ids: List[Any],
    api_config: Optional[dict] = None
) -> List[Dict]:

    api_config = api_config or API_CONFIG

    max_workers = api_config[
        "max_workers"
    ]

    nested_sleep = api_config[
        "nested_request_sleep"
    ]

    logger.info(
        "[NESTED] ids=%s workers=%s",
        len(parent_ids),
        max_workers
    )

    def fetch_single(
        resource_id: Any
    ) -> List[Dict]:

        try:

            logger.info(
                "[NESTED] start=%s",
                resource_id
            )

            endpoint = format_endpoint(
                endpoint_template,
                resource_id
            )

            data = get_all_pages(
                endpoint=endpoint,
                api_config=api_config
            )

            for row in data:

                if isinstance(row, dict):

                    row["parent_id"] = resource_id

            logger.info(
                "[NESTED] done=%s rows=%s",
                resource_id,
                len(data)
            )

            time.sleep(nested_sleep)

            return data

        except Exception as exc:

            logger.warning(
                "[NESTED] failed=%s err=%s",
                resource_id,
                exc
            )

            return []

    results = []

    with ThreadPoolExecutor(
        max_workers=max_workers
    ) as executor:

        for idx, partial in enumerate(
            executor.map(
                fetch_single,
                parent_ids
            ),
            start=1
        ):

            results.extend(partial)

            logger.info(
                "[NESTED] progresso=%s/%s",
                idx,
                len(parent_ids)
            )

    logger.info(
        "[NESTED] total=%s",
        len(results)
    )

    return results