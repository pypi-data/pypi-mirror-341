from typing import TYPE_CHECKING, Any

from tasx.mixins._shared import ClientBind

if TYPE_CHECKING:
    from tasx.interface_models import TaskMessageRead


class TaskRunReadMixin(ClientBind):

    id: str
    arguments: dict
    state: dict | None

    def get_argument(
        self, key: str, default: Any = None, ensure_exists: bool = True
    ) -> Any:
        if ensure_exists and key not in self.arguments:
            raise KeyError(f"Key '{key}' not found in task arguments.")
        return self.arguments.get(key, default)

    def get_all_arguments(self) -> dict:
        return self.arguments

    async def return_(
        self, results: dict | None = None, wake_agent: bool = True, **kwargs
    ) -> "TaskRunReadMixin":
        if results is None:
            results = kwargs
        else:
            assert isinstance(results, dict)
            results.update(kwargs)
        task_run_read = await self.tasx_client.runner_client.submit_task_results(
            self.id, results
        )
        if wake_agent:
            await self.tasx_client.runner_client.wake_agent(self.id)
        return task_run_read.bind_client(self.tasx_client)

    async def fail(self, reason: str, wake_agent: bool = True) -> "TaskRunReadMixin":
        """Report this task run as failed.

        Args:
            reason: The reason for the failure
            wake_agent: Whether to wake the agent after reporting failure

        Returns:
            The updated TaskRunRead object
        """
        task_run_read = await self.tasx_client.runner_client.report_task_failure(
            self.id, reason
        )
        if wake_agent:
            await self.tasx_client.runner_client.wake_agent(self.id)
        return task_run_read.bind_client(self.tasx_client)

    async def send_message(
        self, message_content: str, to: str, wake: bool = True
    ) -> "TaskMessageRead":
        """Send a message to either the agent or task.

        Args:

            message_content: The content of the message to send
            to: The recipient - either "agent" or "task"
            wake: Whether to wake the agent after sending the message

        Raises:
            ValueError: If 'to' is not "agent" or "task"
        """
        from tasx.enums import TaskMessageType
        from tasx.interface_models import TaskMessagePayload

        if to == "agent":
            message_type = TaskMessageType.TASK_TO_AGENT
        elif to == "task":
            message_type = TaskMessageType.AGENT_TO_TASK
        else:
            raise ValueError("'to' must be either 'agent' or 'task'")

        message = await self.tasx_client.runner_client.create_task_message(
            task_run_id=self.id,
            message_type=message_type,
            payload=TaskMessagePayload(content=message_content),
        )

        if wake:
            await self.tasx_client.runner_client.wake_agent(self.id)

        return message

    async def send_message_to_agent(
        self, message_content: str, wake: bool = True
    ) -> "TaskMessageRead":
        """Send a message from task to agent."""
        return await self.send_message(message_content, to="agent", wake=wake)

    async def send_message_to_task(self, message_content: str) -> "TaskMessageRead":
        """Send a message from agent to task."""
        return await self.send_message(message_content, to="task")

    async def commit_state(self) -> "TaskRunReadMixin":
        if self.state is None:
            return self
        task_run_read = await self.tasx_client.runner_client.update_task_run_state(
            self.id, self.state
        )
        return task_run_read.bind_client(self.tasx_client)
