# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import abc
import typing
import pkg_resources

from google import auth
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore

from google.cloud.scheduler_v1beta1.types import cloudscheduler
from google.cloud.scheduler_v1beta1.types import job
from google.cloud.scheduler_v1beta1.types import job as gcs_job
from google.protobuf import empty_pb2 as empty  # type: ignore


try:
    _client_info = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-scheduler",).version,
    )
except pkg_resources.DistributionNotFound:
    _client_info = gapic_v1.client_info.ClientInfo()


class CloudSchedulerTransport(abc.ABC):
    """Abstract transport class for CloudScheduler."""

    AUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    def __init__(
        self,
        *,
        host: str = "cloudscheduler.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: typing.Optional[str] = None,
        scopes: typing.Optional[typing.Sequence[str]] = AUTH_SCOPES,
        quota_project_id: typing.Optional[str] = None,
        **kwargs,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scope (Optional[Sequence[str]]): A list of scopes.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
        """
        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ":" not in host:
            host += ":443"
        self._host = host

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials and credentials_file:
            raise exceptions.DuplicateCredentialArgs(
                "'credentials_file' and 'credentials' are mutually exclusive"
            )

        if credentials_file is not None:
            credentials, _ = auth.load_credentials_from_file(
                credentials_file, scopes=scopes, quota_project_id=quota_project_id
            )

        elif credentials is None:
            credentials, _ = auth.default(
                scopes=scopes, quota_project_id=quota_project_id
            )

        # Save the credentials.
        self._credentials = credentials

        # Lifted into its own function so it can be stubbed out during tests.
        self._prep_wrapped_messages()

    def _prep_wrapped_messages(self):
        # Precompute the wrapped methods.
        self._wrapped_methods = {
            self.list_jobs: gapic_v1.method.wrap_method(
                self.list_jobs,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.ServiceUnavailable, exceptions.DeadlineExceeded,
                    ),
                ),
                default_timeout=600.0,
                client_info=_client_info,
            ),
            self.get_job: gapic_v1.method.wrap_method(
                self.get_job,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.ServiceUnavailable, exceptions.DeadlineExceeded,
                    ),
                ),
                default_timeout=600.0,
                client_info=_client_info,
            ),
            self.create_job: gapic_v1.method.wrap_method(
                self.create_job, default_timeout=600.0, client_info=_client_info,
            ),
            self.update_job: gapic_v1.method.wrap_method(
                self.update_job, default_timeout=600.0, client_info=_client_info,
            ),
            self.delete_job: gapic_v1.method.wrap_method(
                self.delete_job,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.ServiceUnavailable, exceptions.DeadlineExceeded,
                    ),
                ),
                default_timeout=600.0,
                client_info=_client_info,
            ),
            self.pause_job: gapic_v1.method.wrap_method(
                self.pause_job,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.ServiceUnavailable, exceptions.DeadlineExceeded,
                    ),
                ),
                default_timeout=600.0,
                client_info=_client_info,
            ),
            self.resume_job: gapic_v1.method.wrap_method(
                self.resume_job,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.ServiceUnavailable, exceptions.DeadlineExceeded,
                    ),
                ),
                default_timeout=600.0,
                client_info=_client_info,
            ),
            self.run_job: gapic_v1.method.wrap_method(
                self.run_job, default_timeout=600.0, client_info=_client_info,
            ),
        }

    @property
    def list_jobs(
        self,
    ) -> typing.Callable[
        [cloudscheduler.ListJobsRequest],
        typing.Union[
            cloudscheduler.ListJobsResponse,
            typing.Awaitable[cloudscheduler.ListJobsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_job(
        self,
    ) -> typing.Callable[
        [cloudscheduler.GetJobRequest], typing.Union[job.Job, typing.Awaitable[job.Job]]
    ]:
        raise NotImplementedError()

    @property
    def create_job(
        self,
    ) -> typing.Callable[
        [cloudscheduler.CreateJobRequest],
        typing.Union[gcs_job.Job, typing.Awaitable[gcs_job.Job]],
    ]:
        raise NotImplementedError()

    @property
    def update_job(
        self,
    ) -> typing.Callable[
        [cloudscheduler.UpdateJobRequest],
        typing.Union[gcs_job.Job, typing.Awaitable[gcs_job.Job]],
    ]:
        raise NotImplementedError()

    @property
    def delete_job(
        self,
    ) -> typing.Callable[
        [cloudscheduler.DeleteJobRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def pause_job(
        self,
    ) -> typing.Callable[
        [cloudscheduler.PauseJobRequest],
        typing.Union[job.Job, typing.Awaitable[job.Job]],
    ]:
        raise NotImplementedError()

    @property
    def resume_job(
        self,
    ) -> typing.Callable[
        [cloudscheduler.ResumeJobRequest],
        typing.Union[job.Job, typing.Awaitable[job.Job]],
    ]:
        raise NotImplementedError()

    @property
    def run_job(
        self,
    ) -> typing.Callable[
        [cloudscheduler.RunJobRequest], typing.Union[job.Job, typing.Awaitable[job.Job]]
    ]:
        raise NotImplementedError()


__all__ = ("CloudSchedulerTransport",)
