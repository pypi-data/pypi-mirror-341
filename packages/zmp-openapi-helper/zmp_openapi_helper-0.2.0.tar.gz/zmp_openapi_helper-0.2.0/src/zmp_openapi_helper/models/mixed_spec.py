"""This module provides a model for the mixed API specification."""

from __future__ import annotations

from pathlib import Path
from typing import List, Union

from pydantic import BaseModel


class MethodSpec(BaseModel):
    """A model for the method specification."""

    method: str
    tool_name: str | None = None
    description: str | None = None


class APISimpleSpec(BaseModel):
    """A model for the API simple specification."""

    path: str
    methods: List[str | MethodSpec]


class APIConfig(BaseModel):
    """A model for the API configuration."""

    file_path: Union[str, Path]
    prefix: str | None = None
    apis: List[APISimpleSpec]


class BackendAPIConfig(BaseModel):
    """A model for the backend API configuration."""

    backend: str
    config: APIConfig


class MixedAPISpecConfig(BaseModel):
    """MixedAPISpecConfig is a model that contains the configuration for the mixed backendAPI spec.

    ```json
    [
        {
            "backend": "zcp-alert-backend",
            "config": {
                "file_path": "openapi_spec/zcp_spec/alert_openapi_spec.json",
                "prefix": "/api/alert/v1",
                "apis": [
                    {
                        "path":"/alerts",
                        "methods": ["get", "post"]
                    },
                    {
                        "path":"/api/alert/v1/alerts/webhook",
                        "methods": ["post"]
                    },
                    {
                        "path":"/api/alert/v1/alert/priorities",
                        "methods": ["get"]
                    }
                ]
            }
        },
        {
            "backend": "example-backend",
            "config": {
                "file_path": "openapi_spec/zcp_spec/test_spec.json",
                "prefix": "/api/example/v1",
                "apis": [
                    {
                        "path":"/test",
                        "methods": [
                            {
                                "method": "post",
                                "tool_name": "create_test",
                                "description": "Create test"
                            }
                        ]
                    }
                ]
            }
        }
    ]
    ```
    """

    backends: List[BackendAPIConfig]

    @classmethod
    def from_mixed_spec_file(cls, file_path: Union[str, Path]) -> MixedAPISpecConfig:
        """Load the mixed API specification from a file."""
        with open(file_path, "r") as f:
            return cls.model_validate_json(f.read())
