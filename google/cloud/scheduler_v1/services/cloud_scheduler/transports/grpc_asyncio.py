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

from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple

from google.api_core import grpc_helpers_async  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.scheduler_v1.types import cloudscheduler
from google.cloud.scheduler_v1.types import job
from google.cloud.scheduler_v1.types import job as gcs_job
from google.protobuf import empty_pb2 as empty  # type: ignore

from .base import CloudSchedulerTransport
from .grpc import CloudSchedulerGrpcTransport


class CloudSchedulerGrpcAsyncIOTransport(CloudSchedulerTransport):
    """gRPC AsyncIO backend transport for CloudScheduler.

    The Cloud Scheduler API allows external entities to reliably
    schedule asynchronous jobs.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _grpc_channel: aio.Channel
    _stubs: Dict[str, Callable] = {}

    @classmethod
    def create_channel(
        cls,
        host: str = "cloudscheduler.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> aio.Channel:
        """Create and return a gRPC AsyncIO channel object.
        Args:
            address (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            aio.Channel: A gRPC AsyncIO channel object.
        """
        scopes = scopes or cls.AUTH_SCOPES
        return grpc_helpers_async.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            **kwargs,
        )

    def __init__(
        self,
        *,
        host: str = "cloudscheduler.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: aio.Channel = None,
        api_mtls_endpoint: str = None,
        client_cert_source: Callable[[], Tuple[bytes, bytes]] = None,
        quota_project_id=None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            channel (Optional[aio.Channel]): A ``Channel`` instance through
                which to make calls.
            api_mtls_endpoint (Optional[str]): The mutual TLS endpoint. If
                provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or applicatin default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]): A
                callback to provide client SSL certificate bytes and private key
                bytes, both in PEM format. It is ignored if ``api_mtls_endpoint``
                is None.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        if channel:
            # Sanity check: Ensure that channel and credentials are not both
            # provided.
            credentials = False

            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
        elif api_mtls_endpoint:
            host = (
                api_mtls_endpoint
                if ":" in api_mtls_endpoint
                else api_mtls_endpoint + ":443"
            )

            # Create SSL credentials with client_cert_source or application
            # default SSL credentials.
            if client_cert_source:
                cert, key = client_cert_source()
                ssl_credentials = grpc.ssl_channel_credentials(
                    certificate_chain=cert, private_key=key
                )
            else:
                ssl_credentials = SslCredentials().ssl_credentials

            # create a new channel. The provided one is ignored.
            self._grpc_channel = type(self).create_channel(
                host,
                credentials=credentials,
                credentials_file=credentials_file,
                ssl_credentials=ssl_credentials,
                scopes=scopes or self.AUTH_SCOPES,
                quota_project_id=quota_project_id,
            )

        # Run the base constructor.
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes or self.AUTH_SCOPES,
            quota_project_id=quota_project_id,
        )

        self._stubs = {}

    @property
    def grpc_channel(self) -> aio.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Sanity check: Only create a new channel if we do not already
        # have one.
        if not hasattr(self, "_grpc_channel"):
            self._grpc_channel = self.create_channel(
                self._host, credentials=self._credentials,
            )

        # Return the channel from cache.
        return self._grpc_channel

    @property
    def list_jobs(
        self,
    ) -> Callable[
        [cloudscheduler.ListJobsRequest], Awaitable[cloudscheduler.ListJobsResponse]
    ]:
        r"""Return a callable for the list jobs method over gRPC.

        Lists jobs.

        Returns:
            Callable[[~.ListJobsRequest],
                    Awaitable[~.ListJobsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_jobs" not in self._stubs:
            self._stubs["list_jobs"] = self.grpc_channel.unary_unary(
                "/google.cloud.scheduler.v1.CloudScheduler/ListJobs",
                request_serializer=cloudscheduler.ListJobsRequest.serialize,
                response_deserializer=cloudscheduler.ListJobsResponse.deserialize,
            )
        return self._stubs["list_jobs"]

    @property
    def get_job(self) -> Callable[[cloudscheduler.GetJobRequest], Awaitable[job.Job]]:
        r"""Return a callable for the get job method over gRPC.

        Gets a job.

        Returns:
            Callable[[~.GetJobRequest],
                    Awaitable[~.Job]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_job" not in self._stubs:
            self._stubs["get_job"] = self.grpc_channel.unary_unary(
                "/google.cloud.scheduler.v1.CloudScheduler/GetJob",
                request_serializer=cloudscheduler.GetJobRequest.serialize,
                response_deserializer=job.Job.deserialize,
            )
        return self._stubs["get_job"]

    @property
    def create_job(
        self,
    ) -> Callable[[cloudscheduler.CreateJobRequest], Awaitable[gcs_job.Job]]:
        r"""Return a callable for the create job method over gRPC.

        Creates a job.

        Returns:
            Callable[[~.CreateJobRequest],
                    Awaitable[~.Job]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_job" not in self._stubs:
            self._stubs["create_job"] = self.grpc_channel.unary_unary(
                "/google.cloud.scheduler.v1.CloudScheduler/CreateJob",
                request_serializer=cloudscheduler.CreateJobRequest.serialize,
                response_deserializer=gcs_job.Job.deserialize,
            )
        return self._stubs["create_job"]

    @property
    def update_job(
        self,
    ) -> Callable[[cloudscheduler.UpdateJobRequest], Awaitable[gcs_job.Job]]:
        r"""Return a callable for the update job method over gRPC.

        Updates a job.

        If successful, the updated [Job][google.cloud.scheduler.v1.Job]
        is returned. If the job does not exist, ``NOT_FOUND`` is
        returned.

        If UpdateJob does not successfully return, it is possible for
        the job to be in an
        [Job.State.UPDATE_FAILED][google.cloud.scheduler.v1.Job.State.UPDATE_FAILED]
        state. A job in this state may not be executed. If this happens,
        retry the UpdateJob request until a successful response is
        received.

        Returns:
            Callable[[~.UpdateJobRequest],
                    Awaitable[~.Job]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_job" not in self._stubs:
            self._stubs["update_job"] = self.grpc_channel.unary_unary(
                "/google.cloud.scheduler.v1.CloudScheduler/UpdateJob",
                request_serializer=cloudscheduler.UpdateJobRequest.serialize,
                response_deserializer=gcs_job.Job.deserialize,
            )
        return self._stubs["update_job"]

    @property
    def delete_job(
        self,
    ) -> Callable[[cloudscheduler.DeleteJobRequest], Awaitable[empty.Empty]]:
        r"""Return a callable for the delete job method over gRPC.

        Deletes a job.

        Returns:
            Callable[[~.DeleteJobRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_job" not in self._stubs:
            self._stubs["delete_job"] = self.grpc_channel.unary_unary(
                "/google.cloud.scheduler.v1.CloudScheduler/DeleteJob",
                request_serializer=cloudscheduler.DeleteJobRequest.serialize,
                response_deserializer=empty.Empty.FromString,
            )
        return self._stubs["delete_job"]

    @property
    def pause_job(
        self,
    ) -> Callable[[cloudscheduler.PauseJobRequest], Awaitable[job.Job]]:
        r"""Return a callable for the pause job method over gRPC.

        Pauses a job.

        If a job is paused then the system will stop executing the job
        until it is re-enabled via
        [ResumeJob][google.cloud.scheduler.v1.CloudScheduler.ResumeJob].
        The state of the job is stored in
        [state][google.cloud.scheduler.v1.Job.state]; if paused it will
        be set to
        [Job.State.PAUSED][google.cloud.scheduler.v1.Job.State.PAUSED].
        A job must be in
        [Job.State.ENABLED][google.cloud.scheduler.v1.Job.State.ENABLED]
        to be paused.

        Returns:
            Callable[[~.PauseJobRequest],
                    Awaitable[~.Job]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "pause_job" not in self._stubs:
            self._stubs["pause_job"] = self.grpc_channel.unary_unary(
                "/google.cloud.scheduler.v1.CloudScheduler/PauseJob",
                request_serializer=cloudscheduler.PauseJobRequest.serialize,
                response_deserializer=job.Job.deserialize,
            )
        return self._stubs["pause_job"]

    @property
    def resume_job(
        self,
    ) -> Callable[[cloudscheduler.ResumeJobRequest], Awaitable[job.Job]]:
        r"""Return a callable for the resume job method over gRPC.

        Resume a job.

        This method reenables a job after it has been
        [Job.State.PAUSED][google.cloud.scheduler.v1.Job.State.PAUSED].
        The state of a job is stored in
        [Job.state][google.cloud.scheduler.v1.Job.state]; after calling
        this method it will be set to
        [Job.State.ENABLED][google.cloud.scheduler.v1.Job.State.ENABLED].
        A job must be in
        [Job.State.PAUSED][google.cloud.scheduler.v1.Job.State.PAUSED]
        to be resumed.

        Returns:
            Callable[[~.ResumeJobRequest],
                    Awaitable[~.Job]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "resume_job" not in self._stubs:
            self._stubs["resume_job"] = self.grpc_channel.unary_unary(
                "/google.cloud.scheduler.v1.CloudScheduler/ResumeJob",
                request_serializer=cloudscheduler.ResumeJobRequest.serialize,
                response_deserializer=job.Job.deserialize,
            )
        return self._stubs["resume_job"]

    @property
    def run_job(self) -> Callable[[cloudscheduler.RunJobRequest], Awaitable[job.Job]]:
        r"""Return a callable for the run job method over gRPC.

        Forces a job to run now.
        When this method is called, Cloud Scheduler will
        dispatch the job, even if the job is already running.

        Returns:
            Callable[[~.RunJobRequest],
                    Awaitable[~.Job]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "run_job" not in self._stubs:
            self._stubs["run_job"] = self.grpc_channel.unary_unary(
                "/google.cloud.scheduler.v1.CloudScheduler/RunJob",
                request_serializer=cloudscheduler.RunJobRequest.serialize,
                response_deserializer=job.Job.deserialize,
            )
        return self._stubs["run_job"]


__all__ = ("CloudSchedulerGrpcAsyncIOTransport",)
