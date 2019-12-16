import random
import string
import time
import sys
import os
from azure.common.client_factory import get_client_from_auth_file
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.containerinstance import ContainerInstanceManagementClient
from azure.mgmt.containerinstance.models import (ContainerGroup,
                                                 Container,
                                                 ContainerGroupNetworkProtocol,
                                                 ContainerGroupRestartPolicy,
                                                 ContainerPort,
                                                 EnvironmentVariable,
                                                 IpAddress,
                                                 Port,
                                                 ResourceRequests,
                                                 ResourceRequirements,
                                                 OperatingSystemTypes)


class WorkersManager(object):

    def __init__(self, resource_group_name='virriusResourceGroup', container_image_name="virriusserver.azurecr.io/worker:v1", auth_file_path="my.azureauth"):
        self.resource_group_name = resource_group_name
        self.container_image_name = container_image_name
        self.auth_file_path = os.path.join(os.path.dirname(__file__), auth_file_path)
        self.aciclient = get_client_from_auth_file(
            ContainerInstanceManagementClient, self.auth_file_path)
        self.resclient = get_client_from_auth_file(
            ResourceManagementClient, self.auth_file_path)
        self.resource_group = self.resclient.resource_groups.get(
            resource_group_name)

    def run_task_based_container(self, aci_client, resource_group, container_group_name,
                                 container_image_name, start_command_line=None):
        """Creates a container group with a single task-based container who's
        restart policy is 'Never'. If specified, the container runs a custom
        command line at startup.

        Arguments:
            aci_client {azure.mgmt.containerinstance.ContainerInstanceManagementClient}
                        -- An authenticated container instance management client.
            resource_group {azure.mgmt.resource.resources.models.ResourceGroup}
                        -- The resource group in which to create the container group.
            container_group_name {str}
                        -- The name of the container group to create.
            container_image_name {str}
                        -- The container image name and tag, for example:
                        microsoft\aci-helloworld:latest
            start_command_line {str}
                        -- The command line that should be executed when the
                        container starts. This value can be None.
        """

        start_command_line = "python worker.py {}".format(container_group_name)

        print("Creating container group '{0}' with start command '{1}'"
              .format(container_group_name, start_command_line))

        # Configure the container
        container_resource_requests = ResourceRequests(memory_in_gb=1, cpu=1.0)
        container_resource_requirements = ResourceRequirements(
            requests=container_resource_requests)
        container = Container(name=container_group_name,
                              image=container_image_name,
                              resources=container_resource_requirements,
                              command=start_command_line.split())

        # Configure the container group
        group = ContainerGroup(location=resource_group.location,
                               containers=[container],
                               os_type=OperatingSystemTypes.linux,
                               restart_policy=ContainerGroupRestartPolicy.never)

        # Create the container group
        result = aci_client.container_groups.create_or_update(resource_group.name,
                                                              container_group_name,
                                                              group)

        # Wait for the container create operation to complete. The operation is
        # "done" when the container group provisioning state is one of:
        # Succeeded, Canceled, Failed
        while result.done() is False:
            sys.stdout.write('.')
            time.sleep(1)

        # Get the provisioning state of the container group.
        container_group = aci_client.container_groups.get(resource_group.name,
                                                          container_group_name)
        if str(container_group.provisioning_state).lower() == 'succeeded':
            print("\nCreation of container group '{}' succeeded."
                  .format(container_group_name))
        else:
            print("\nCreation of container group '{}' failed. Provisioning state"
                  "is: {}".format(container_group_name,
                                  container_group.provisioning_state))

    def delete_container_group(self, task_container_group_name):
        self.aciclient.container_groups.delete(self.resource_group_name,
                                               task_container_group_name)
