import json
from typing import Optional

import requests


class CRFAPIClient:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.token = token

    def _get_headers(self):
        return {"Authorization": f"Token {self.token}", "Content-Type": "application/json"}

    def _get_headers_without_content_type(self):
        return {"Authorization": f"Token {self.token}"}

    def _get_paginated_data(self, url: str, params: dict = {}) -> list[dict]:
        next_url = url
        data = []
        use_https = url.startswith("https://")
        is_first_call = True

        while next_url:
            # Ensure HTTPS consistency if base URL uses HTTPS
            if use_https and next_url.startswith("http://"):
                next_url = next_url.replace("http://", "https://")
            if is_first_call:
                response = requests.get(next_url, headers=self._get_headers(), params=params)
                is_first_call = False
            else:
                response = requests.get(next_url, headers=self._get_headers())
            response.raise_for_status()
            response_data = response.json()
            data.extend(response_data["results"])
            next_url = response_data.get("next")

        return data

    def get_projects(self) -> list[dict]:
        return self._get_paginated_data(f"{self.base_url}/api/v1/projects")

    def create_project(self, name: str, brief: str, default_llm_model: Optional[str]) -> dict:
        create_project_payload = {
            "name": name,
            "business_brief": brief,
            "key": name,
        }
        if default_llm_model:
            create_project_payload["default_llm_model"] = default_llm_model

        return requests.post(
            f"{self.base_url}/api/v1/projects/",
            headers=self._get_headers(),
            json=create_project_payload,
        )

    def delete_project(self, project_id: str) -> dict:
        return requests.delete(
            f"{self.base_url}/api/v1/projects/{project_id}/",
            headers=self._get_headers(),
        )

    def get_documents(self, project_id: str) -> list[dict]:
        return self._get_paginated_data(f"{self.base_url}/api/v1/projects/{project_id}/documents")

    def get_table_data(
        self,
        project_id: str,
        table_id: Optional[str] = None,
        table_name: Optional[str] = None,
        page: int = 1,
        page_size: int = 100,
        remove_embeddings: bool = True,
        chunk_id: Optional[str] = None,
        document_id: Optional[str] = None,
    ) -> list[dict]:
        """
        Get table data with various filtering options.

        Args:
            project_id: The ID of the project
            table_id: Optional ID of the specific table
            table_name: Optional name of the table
            page: Page number for pagination (default: 1)
            page_size: Number of items per page (default: 100)
            remove_embeddings: Whether to remove embeddings from the response (default: True)
            chunk_id: Optional ID of a specific chunk to filter by
            document_id: Optional ID of a specific document to filter by

        Returns:
            List of table data entries

        """
        if not (table_id or table_name):
            raise ValueError("Either table_id or table_name must be provided")

        params = {
            "remove_embeddings": str(remove_embeddings).lower(),
        }

        if table_id:
            params["table_id"] = table_id
        if table_name:
            params["table_name"] = table_name
        if chunk_id:
            params["chunk_id"] = chunk_id
        if document_id:
            params["document_id"] = document_id
        if page:
            params["page"] = page
        if page_size:
            params["page_size"] = page_size

        return self._get_paginated_data(
            f"{self.base_url}/api/v1/projects/{project_id}/get-data/", params=params
        )

    def get_table_data_by_chunk(
        self,
        project_id: str,
        chunk_id: str,
        remove_embeddings: bool = True,
        page: int = 1,
        page_size: int = 100,
    ) -> list[dict]:
        """Convenience method to get table data filtered by chunk ID"""
        return self.get_table_data(
            project_id=project_id,
            chunk_id=chunk_id,
            remove_embeddings=remove_embeddings,
            page=page,
            page_size=page_size,
        )

    def get_table_data_by_document(
        self,
        project_id: str,
        document_id: str,
        remove_embeddings: bool = True,
        page: int = 1,
        page_size: int = 100,
    ) -> list[dict]:
        """Convenience method to get table data filtered by document ID"""
        return self.get_table_data(
            project_id=project_id,
            document_id=document_id,
            remove_embeddings=remove_embeddings,
            page=page,
            page_size=page_size,
        )

    def write_table_data(
        self, project_id: str, table_name: str, data: list[dict], override: bool = False
    ) -> dict:
        if isinstance(data, dict):
            data = [data]
        if isinstance(data, list):
            data = json.dumps(data)
        return requests.post(
            f"{self.base_url}/api/v1/projects/{project_id}/write-data/",
            headers=self._get_headers(),
            json={"table_name": table_name, "data": data, "override": override},
        )

    def get_pipeline_runs(self, project_id: str) -> list[dict]:
        return self._get_paginated_data(
            f"{self.base_url}/api/v1/projects/{project_id}/pipeline-runs"
        )

    def get_pipeline_run(self, project_id: str, pipeline_run_id: str) -> dict:
        return requests.get(
            f"{self.base_url}/api/v1/projects/{project_id}/pipeline-runs/{pipeline_run_id}",
            headers=self._get_headers(),
        )

    def abort_pipeline_run(self, project_id: str, pipeline_run_id: str) -> dict:
        return requests.post(
            f"{self.base_url}/api/v1/projects/{project_id}/pipeline-runs/{pipeline_run_id}/abort",
            headers=self._get_headers(),
        )

    def build_table(
        self,
        project_id: str,
        table_name: str,
        use_sample: bool = True,
        pipeline_name: str = "v0",
        mode: str = "recreate",
        document_ids: list[str] = None,
        llm_model: Optional[str] = None,
    ) -> dict:
        """
        Build a table with the specified parameters.

        Args:
            project_id: The ID of the project
            table_name: Name of the table to build
            use_sample: Whether to use sample data (default: True)
            pipeline_name: Name of the pipeline to use (default: "v0")
            mode: Build mode - "recreate" or other modes (default: "recreate")
            document_ids: Optional list of document IDs to process
            llm_model: Optional LLM model to use

        Returns:
            API response as dictionary

        """
        payload = {
            "table_name": table_name,
            "use_sample": use_sample,
            "pipeline_name": pipeline_name,
            "mode": mode,
        }

        if document_ids:
            payload["document_ids"] = document_ids
        if llm_model:
            payload["llm_model"] = llm_model

        return requests.post(
            f"{self.base_url}/api/v1/projects/{project_id}/build-table/",
            headers=self._get_headers(),
            json=payload,
        ).json()

    def bulk_upload_documents(
        self,
        project_id: str,
        files_paths: list[str],
        skip_parsing: bool = False,
        batch_size: int = 10,
    ) -> list[dict]:
        responses = []
        data = {"skip_parsing": "true"} if skip_parsing else {}

        # Process files in batches
        for i in range(0, len(files_paths), batch_size):
            batch = files_paths[i : i + batch_size]
            files_to_upload = []

            try:
                # Open files for current batch
                for file_path in batch:
                    files_to_upload.append(
                        ("files", (file_path.split("/")[-1], open(file_path, "rb")))
                    )

                # Upload current batch
                response = requests.post(
                    f"{self.base_url}/api/v1/projects/{project_id}/documents/bulk-upload/",
                    headers=self._get_headers_without_content_type(),
                    files=files_to_upload,
                    data=data,
                )
                response.raise_for_status()
                responses.append(response.json())

            finally:
                # Ensure files are closed even if an error occurs
                for _, (_, file_obj) in files_to_upload:
                    file_obj.close()

        return responses

    def list_tables(self, project_id: str) -> list[dict]:
        return self._get_paginated_data(f"{self.base_url}/api/v1/projects/{project_id}/tables/")

    def create_table(self, project_id: str, table_name: str, columns: list[dict]) -> dict:
        return requests.post(
            f"{self.base_url}/api/v1/projects/{project_id}/tables/",
            headers=self._get_headers(),
            json={"name": table_name, "columns": columns},
        )

    def update_table(self, project_id: str, table_id: str, columns: list[dict]) -> dict:
        return requests.patch(
            f"{self.base_url}/api/v1/projects/{project_id}/tables/{table_id}/",
            headers=self._get_headers(),
            json={"columns": columns},
        )

    def create_table_version(self, project_id: str, table_id: str) -> dict:
        return requests.post(
            f"{self.base_url}/api/v1/projects/{project_id}/tables/{table_id}/versions/",
            headers=self._get_headers(),
        )

    def clear_table(self, project_id: str, table_name: str) -> dict:
        return requests.post(
            f"{self.base_url}/api/v1/projects/{project_id}/clear-table/",
            headers=self._get_headers(),
            json={"table_name": table_name},
        )

    def create_object_extractor(
        self,
        project_id: str,
        brief: str,
        chunk_ids: Optional[list[str]] = None,
        document_ids: Optional[list[str]] = None,
        extractable_pydantic_class: str = None,
        extraction_prompt: str = None,
        llm_model: str = None,
        name: str = None,
        filtering_tag_extractor: str = None,
        filtering_key: str = None,
        filtering_value: str = None,
    ) -> dict:
        if chunk_ids is None:
            chunk_ids = []
        if document_ids is None:
            document_ids = []
        return requests.post(
            f"{self.base_url}/api/v1/projects/{project_id}/object-extractors/",
            headers=self._get_headers(),
            json={
                "brief": brief,
                "chunk_ids": chunk_ids,
                "document_ids": document_ids,
                "extractable_pydantic_class": extractable_pydantic_class,
                "extraction_prompt": extraction_prompt,
                "llm_model": llm_model,
                "name": name,
                "prompt_generation_status": "completed",
                "filtering_tag_extractor": filtering_tag_extractor,
                "filtering_key": filtering_key,
                "filtering_value": filtering_value,
            },
        )

    def list_object_extractors(self, project_id: str) -> list[dict]:
        return self._get_paginated_data(
            f"{self.base_url}/api/v1/projects/{project_id}/object-extractors/"
        )

    def update_object_extractor(
        self,
        project_id: str,
        object_extractor_id: str,
        brief: str = None,
        chunk_ids: list[str] = None,
        document_ids: list[str] = None,
        extractable_pydantic_class: str = None,
        extraction_prompt: str = None,
        llm_model: str = None,
        name: str = None,
        filtering_tag_extractor: str = None,
        filtering_key: str = None,
        filtering_value: str = None,
    ) -> dict:
        fields = {
            "brief": brief,
            "chunk_ids": chunk_ids,
            "document_ids": document_ids,
            "extractable_pydantic_class": extractable_pydantic_class,
            "extraction_prompt": extraction_prompt,
            "llm_model": llm_model,
            "name": name,
            "filtering_tag_extractor": filtering_tag_extractor,
            "filtering_key": filtering_key,
            "filtering_value": filtering_value,
        }

        payload = {k: v for k, v in fields.items() if v is not None}

        return requests.patch(
            f"{self.base_url}/api/v1/projects/{project_id}/object-extractors/{object_extractor_id}/",
            headers=self._get_headers(),
            json=payload,
        )

    def delete_object_extractor(self, project_id: str, object_extractor_id: str) -> dict:
        return requests.delete(
            f"{self.base_url}/api/v1/projects/{project_id}/object-extractors/{object_extractor_id}/",
            headers=self._get_headers(),
        )

    def create_object_extractor_tables_and_versions(
        self, project_id: str, object_extractor_id: str
    ) -> dict:
        responses = []
        tables_and_schemas = [
            {
                "name": f"extracted_objects_extractor_{object_extractor_id}",
                "columns": [
                    {"name": "id", "type": "uuid"},
                    {"name": "chunk_id", "type": "uuid"},
                    {"name": "json_object", "type": "json"},
                ],
            },
            {
                "name": f"alerts_extractor_{object_extractor_id}",
                "columns": [
                    {"name": "id", "type": "uuid"},
                    {"name": "chunk_id", "type": "uuid"},
                    {"name": "json_alert", "type": "json"},
                    {"name": "extracted_object_id", "type": "uuid"},
                ],
            },
            {
                "name": f"pushed_objects_extractor_{object_extractor_id}",
                "columns": [
                    {"name": "status", "type": "text"},
                ],
            },
        ]
        responses = []
        for table in tables_and_schemas:
            table_response = self.create_table(project_id, table["name"], table["columns"])
            table_id = table_response.json()["id"]
            response = self.create_table_version(project_id, table_id)
            responses.append(response.json())
        return responses

    def list_tag_extractors(self, project_id: str) -> list[dict]:
        return self._get_paginated_data(
            f"{self.base_url}/api/v1/projects/{project_id}/tag-extractors/"
        )

    def create_tag_extractor(
        self,
        project_id: str,
        brief: str,
        chunk_ids: Optional[list[str]] = None,
        document_ids: Optional[list[str]] = None,
        tagging_tree: Optional[list[dict]] = None,
        extraction_prompt: str = None,
        llm_model: str = None,
        name: str = None,
    ) -> dict:
        if chunk_ids is None:
            chunk_ids = []
        if document_ids is None:
            document_ids = []
        return requests.post(
            f"{self.base_url}/api/v1/projects/{project_id}/tag-extractors/",
            headers=self._get_headers(),
            json={
                "brief": brief,
                "chunk_ids": chunk_ids,
                "document_ids": document_ids,
                "tagging_tree": tagging_tree,
                "extraction_prompt": extraction_prompt,
                "llm_model": llm_model,
                "name": name,
                "prompt_generation_status": "completed",
            },
        )

    def update_tag_extractor(
        self,
        project_id: str,
        tag_extractor_id: str,
        brief: str = None,
        chunk_ids: list[str] = None,
        document_ids: list[str] = None,
        tagging_tree: list[dict] = None,
        extraction_prompt: str = None,
        llm_model: str = None,
        name: str = None,
    ) -> dict:
        payload = {}
        if brief:
            payload["brief"] = brief
        if chunk_ids:
            payload["chunk_ids"] = chunk_ids
        if document_ids:
            payload["document_ids"] = document_ids
        if tagging_tree:
            payload["tagging_tree"] = tagging_tree
        if extraction_prompt:
            payload["extraction_prompt"] = extraction_prompt
        if llm_model:
            payload["llm_model"] = llm_model
        if name:
            payload["name"] = name

        return requests.patch(
            f"{self.base_url}/api/v1/projects/{project_id}/tag-extractors/{tag_extractor_id}/",
            headers=self._get_headers(),
            json=payload,
        )

    def delete_tag_extractor(self, project_id: str, tag_extractor_id: str) -> dict:
        return requests.delete(
            f"{self.base_url}/api/v1/projects/{project_id}/tag-extractors/{tag_extractor_id}/",
            headers=self._get_headers(),
        )

    def create_tag_extractor_tables_and_versions(
        self, project_id: str, tag_extractor_id: str
    ) -> dict:
        responses = []
        tables_and_schemas = [
            {
                "name": f"extracted_tags_extractor_{tag_extractor_id}",
                "columns": [
                    {"name": "chunk_id", "type": "uuid"},
                    {"name": "metadata", "type": "json"},
                    {"name": "id", "type": "text"},
                ],
            },
            {
                "name": f"alerts_tags_extractor_{tag_extractor_id}",
                "columns": [
                    {"name": "id", "type": "uuid"},
                    {"name": "chunk_id", "type": "uuid"},
                    {"name": "json_alert", "type": "json"},
                ],
            },
        ]
        for table in tables_and_schemas:
            table_response = self.create_table(project_id, table["name"], table["columns"])
            table_id = table_response.json()["id"]
            response = self.create_table_version(project_id, table_id)
            responses.append(response.json())
        return responses

    def retrieve_with_semantic_search(
        self, project_id: str, query: str, indexes: list[str], n_objects: int
    ) -> dict:
        response = requests.post(
            f"{self.base_url}/api/v1/projects/{project_id}/retrieve-with-naive/",
            headers=self._get_headers(),
            json={"query": query, "indexes": indexes, "n_objects": n_objects},
        )
        return response.json()["retrieval_results"]

    def retrieve_with_graph_search(
        self, project_id: str, query: str, indexes: list[str], n_objects: int
    ) -> dict:
        response = requests.post(
            f"{self.base_url}/api/v1/projects/{project_id}/retrieve-with-graph/",
            headers=self._get_headers(),
            json={"query": query, "indexes": indexes, "n_objects": n_objects},
        )
        return response.json()["retrieval_results"]

    def run_graph_query(self, project_id: str, query: str) -> dict:
        response = requests.post(
            f"{self.base_url}/api/v1/projects/{project_id}/run-neo4j-query/",
            headers=self._get_headers(),
            json={"query": query},
        )
        return response.json()["retrieval_results"]
