from typing import Any, Callable, Optional

import requests
from pydantic import BaseModel, Field

from src._utils import ProbeResult, SuccessCode, TrialInterface, TrialReport
from src.registry import TrialRegistry


class StereotypeTrial_InputFormat(BaseModel):
    prompt: str = Field(
        ...,
        title="Prompt",
        description="The prompt provided by the server that requires the agent's response.",
    )


class StereotypeTrial_OutputFormat(BaseModel):
    client_response: str = Field(
        ..., title="Client Response", description="The response provided by the agent."
    )


class StereotypeTrialReport(TrialReport):
    def __init__(self, results: Any):
        # Make a deepcopy of the results
        super().__init__(results)
        # If results is a list, group the entries by their "stereotype_type".
        if isinstance(self.results, list):
            grouped_results: dict[str, list[Any]] = {}
            for res in self.results:
                stereotype = res.get("stereotype_type", "unknown")
                if stereotype not in grouped_results:
                    grouped_results[stereotype] = []
                grouped_results[stereotype].append(res)
            self.results = grouped_results

        # Now self.results is expected to be a dict mapping stereotype types to a list of probe results.
        for stereotype_type in self.results:
            self.results[stereotype_type] = [
                ProbeResult(
                    SuccessCode(item["success_code"]),
                    item["description"],
                    item["extra"],
                )
                for item in self.results[stereotype_type]
            ]

    def get_results(self) -> dict:
        """Returns the results in a dictionary format."""
        return {
            stereotype_type: [result.to_dict() for result in results_list]
            for stereotype_type, results_list in self.results.items()
        }


@TrialRegistry.register("StereotypeTrial")
class StereotypeTrial(TrialInterface):
    """
    A client-side trial that interacts with the server's /stereotype_trial endpoint.
    The trial provides an agent description and a list of stereotype types, and then
    continuously polls the server for the next prompt. Incoming prompts are passed
    to a user-supplied interact function, and the agent's reply is sent back until
    the trial concludes with results.
    """

    def __init__(
        self,
        email: str,
        api_key: str,
        interact_function: Callable,
        agent_description: str,
        stereotype_types: list[str],
        trial_id: Optional[str] = None,
        user_notes: Optional[str] = None,
    ):
        # Pass our defined input/output formats to the base class.
        super().__init__(
            email,
            api_key,
            StereotypeTrial_InputFormat,
            StereotypeTrial_OutputFormat,
            interact_function,
        )
        if not agent_description:
            raise ValueError("agent_description cannot be empty")
        if not stereotype_types:
            raise ValueError("stereotype_types cannot be empty")
        self.agent_description = agent_description
        self.stereotype_types = stereotype_types
        self.trial_id = trial_id
        self.user_notes = user_notes

    def run(self) -> TrialReport:
        # Build the initial payload; note that we do not include an input_format key here.
        initial_payload = {
            "email": self.email,
            "agent_description": self.agent_description,
            "stereotype_types": self.stereotype_types,
        }

        # Add optional trial_id and user_notes if provided
        if self.trial_id:
            initial_payload["trial_id"] = self.trial_id
        if self.user_notes:
            initial_payload["user_notes"] = self.user_notes

        response = requests.post(
            "http://gauntlet-load-balancer-203818527.us-east-1.elb.amazonaws.com/stereotype_trial",
            headers={"Authorization": self.api_key},
            json=initial_payload,
        )

        if response.status_code != 200:
            error_detail = response.json().get("detail", "Unknown error")
            if response.status_code == 400:
                raise ValueError(f"Bad request: {error_detail}")
            elif response.status_code == 401:
                raise ValueError(f"Authentication error: {error_detail}")
            elif response.status_code == 404:
                raise ValueError(f"Not found: {error_detail}")
            else:
                raise ValueError(
                    f"Server error ({response.status_code}): {error_detail}"
                )

        response_data = response.json()
        request_id = response_data["request_id"]

        # Continue conversation until the server returns final results.
        while True:
            if "results" in response_data:
                # Trial is complete; wrap the raw results in a StereotypeTrialReport.
                print(
                    f"\nYou can view the report at: https://actualization.ai/request/{request_id}\n"
                )
                return StereotypeTrialReport(response_data["results"])

            next_message = response_data.get("next_message")
            if not next_message:
                raise ValueError("Server response missing next_message")

            # Use the interact function to get the client response.
            # We parse the raw string next_message into our input_format.
            client_response = self.interact_function(
                self.input_format.model_validate({"prompt": next_message})
            ).client_response

            continue_payload = {
                "email": self.email,
                "request_id": request_id,
                "client_response": client_response,
            }

            response = requests.post(
                "http://gauntlet-load-balancer-203818527.us-east-1.elb.amazonaws.com/stereotype_trial",
                headers={"Authorization": self.api_key},
                json=continue_payload,
            )

            if response.status_code != 200:
                error_detail = response.json().get("detail", "Unknown error")
                if response.status_code == 400:
                    raise ValueError(f"Bad request: {error_detail}")
                elif response.status_code == 401:
                    raise ValueError(f"Authentication error: {error_detail}")
                elif response.status_code == 404:
                    raise ValueError(f"Not found: {error_detail}")
                else:
                    raise ValueError(
                        f"Server error ({response.status_code}): {error_detail}"
                    )

            response_data = response.json()

            response_data = response.json()
