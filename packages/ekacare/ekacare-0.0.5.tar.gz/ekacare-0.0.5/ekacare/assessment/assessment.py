from typing import Any, Dict, List, Optional

CHOICE_TYPE_RESPONSES = ["I-RADO", "I-RADG", "I-MULT", "I-ATSG"]


class Assessment:
    """
    Assessment API client for Eka Care.

    This class provides methods to initialize, start, continue, and submit assessments
    through the Eka Care assessment API.
    """

    def __init__(self, client):
        """
        Initialize the Assessment client.

        Args:
            client: The EkaCareClient instance.
        """
        self.client = client
        self.base_url = f"{self.client.base_url}/assessment/api/v1"
        self.assessment_id = None

    def start(
        self,
        workflow_id: int,
        gender: str,
        age: int = None,
        dob: str = None,
        practitioner_uuid: str = None,
        patient_uuid: str = None,
        unique_identifier: str = None,
        context: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Starts the assessment for a patient by the Practitioner.

        Args:
            workflow_id: The workflow ID for the assessment
            gender: Patient's gender ('M' or 'F')
            age: Patient's age
            dob: Patient's date of birth in format "YYYY-MM-DD"
            practitioner_uuid: The practitioner's UUID
            patient_uuid: The patient's UUID
            unique_identifier: A unique identifier for the patient
            context: Optional JSON string with additional context data

        Returns:
            Dict containing details of the first question and the assessment ID
        """
        payload = {
            "user_info": {"age": age, "dob": dob, "gender": gender},
            "workflow_id": workflow_id,
            "practitioner_uuid": practitioner_uuid,
            "patient_uuid": patient_uuid,
            "unique_identifier": unique_identifier,
        }
        if context:
            payload["context"] = context

        init_response = self.client.request(
            method="POST", endpoint=f"{self.base_url}/init/", json=payload
        )
        self.assessment_id = init_response["assessment_id"]

        start_response = self.client.request(
            method="PUT", endpoint=f"{self.base_url}/start/{self.assessment_id}/"
        )

        return start_response

    def next(self, qid: str, user_response: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Continue an assessment by answering a question.

        Args:
            qid: Question ID being answered
            user_response: List of response objects, each containing `selected_choices` or `user_input`
        Returns:
            Dict containing the next question or assessment results
        """
        payload = {"user_response": user_response}

        return self.client.request(
            "PUT", f"{self.base_url}/continue/{self.assessment_id}/{qid}", json=payload
        )

    def submit(self) -> Dict[str, Any]:
        """
        Submit an assessment to finalize it.

        Args:
            assessment_id: ID of the assessment to submit

        Returns:
            Dict containing the final assessment results
        """
        return self.client.request("PUT", f"{self.base_url}/submit/{self.assessment_id}/")


def _format_choices(choices: List[str]) -> Dict[str, Any]:
    selected_choices = []
    if choices is None or len(choices) == 0:
        raise ValueError("Choices cannot be empty for choice_response")

    for choice in choices:
        if len(choice) == 0:
            raise ValueError("Choice cannot be empty")
        if len(choice) > 2:
            raise ValueError(
                "Choice can only have one or two elements - choice_id and qualifier respectively"
            )
        choice_id = choice[0]
        qualifier = choice[1] if len(choice) > 1 else "p"
        selected_choices.append({"choice_id": choice_id, "qualifier": qualifier})

    return {"selected_choices": selected_choices}


def _format_input(user_input: str) -> List[Dict[str, Any]]:
    """ "
    Create a response for input type questions."
    """
    if not user_input:
        raise ValueError("User input cannot be empty for input_response")
    user_response = {"user_input": user_input}

    return user_response


def response(question, answer):
    """
    Create a response for the question.
    """
    if question["component_code"] in CHOICE_TYPE_RESPONSES:
        return _format_choices(answer)
    else:
        return _format_input(answer)
