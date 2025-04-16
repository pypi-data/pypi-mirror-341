# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from replicate import ReplicateClient, AsyncReplicateClient

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTrainings:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: ReplicateClient) -> None:
        training = client.trainings.retrieve(
            "training_id",
        )
        assert training is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: ReplicateClient) -> None:
        response = client.trainings.with_raw_response.retrieve(
            "training_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        training = response.parse()
        assert training is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: ReplicateClient) -> None:
        with client.trainings.with_streaming_response.retrieve(
            "training_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            training = response.parse()
            assert training is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: ReplicateClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `training_id` but received ''"):
            client.trainings.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: ReplicateClient) -> None:
        training = client.trainings.list()
        assert training is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: ReplicateClient) -> None:
        response = client.trainings.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        training = response.parse()
        assert training is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: ReplicateClient) -> None:
        with client.trainings.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            training = response.parse()
            assert training is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_cancel(self, client: ReplicateClient) -> None:
        training = client.trainings.cancel(
            "training_id",
        )
        assert training is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_cancel(self, client: ReplicateClient) -> None:
        response = client.trainings.with_raw_response.cancel(
            "training_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        training = response.parse()
        assert training is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_cancel(self, client: ReplicateClient) -> None:
        with client.trainings.with_streaming_response.cancel(
            "training_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            training = response.parse()
            assert training is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_cancel(self, client: ReplicateClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `training_id` but received ''"):
            client.trainings.with_raw_response.cancel(
                "",
            )


class TestAsyncTrainings:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncReplicateClient) -> None:
        training = await async_client.trainings.retrieve(
            "training_id",
        )
        assert training is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncReplicateClient) -> None:
        response = await async_client.trainings.with_raw_response.retrieve(
            "training_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        training = await response.parse()
        assert training is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncReplicateClient) -> None:
        async with async_client.trainings.with_streaming_response.retrieve(
            "training_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            training = await response.parse()
            assert training is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncReplicateClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `training_id` but received ''"):
            await async_client.trainings.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncReplicateClient) -> None:
        training = await async_client.trainings.list()
        assert training is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncReplicateClient) -> None:
        response = await async_client.trainings.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        training = await response.parse()
        assert training is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncReplicateClient) -> None:
        async with async_client.trainings.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            training = await response.parse()
            assert training is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_cancel(self, async_client: AsyncReplicateClient) -> None:
        training = await async_client.trainings.cancel(
            "training_id",
        )
        assert training is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_cancel(self, async_client: AsyncReplicateClient) -> None:
        response = await async_client.trainings.with_raw_response.cancel(
            "training_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        training = await response.parse()
        assert training is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_cancel(self, async_client: AsyncReplicateClient) -> None:
        async with async_client.trainings.with_streaming_response.cancel(
            "training_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            training = await response.parse()
            assert training is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_cancel(self, async_client: AsyncReplicateClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `training_id` but received ''"):
            await async_client.trainings.with_raw_response.cancel(
                "",
            )
