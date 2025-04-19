"""ScenarioList model.

```
from allphins.models import ScenarioList
```
"""
import uuid

from allphins.client import Client
from allphins.client.result import DictResult
from allphins.client.result import Result
from allphins.const import ALLPHINS_API_URL
from allphins.const import GET
from allphins.const import POST
from allphins.models.base import BaseModel
from allphins.utils import validate_uuid4


class ScenarioList(BaseModel):
    """ScenarioList model."""

    path = f'{ALLPHINS_API_URL}/scenario_lists/'
    PAGE_SIZE = 1000

    def __init__(self, scenario_list_id: uuid.UUID | str):
        """Instantiate a Scenario list from a scenario list UUID.

        Args:
            scenario_list_id (uuid.UUID): UUID of the scenario list.

        Raises:
            ValueError: If the scenario list_id is not a valid UUID.
        """
        if not validate_uuid4(scenario_list_id):
            raise ValueError(f'{scenario_list_id} is not a valid UUID.')

        super().__init__(str(scenario_list_id))

    @classmethod
    def all(cls) -> Result:
        """Get all the scenario lists.

        Returns:
            list[dict]: List of the scenario lists dict representation.
        """
        return DictResult(Client().call_api(ScenarioList.path, GET))

    def aggregation(self, policies: list[int], computation_date: str) -> Result:
        """Get the aggregation for the given scenariolist and policies at the given computation date.

        Args:
            policies (list[int]): List of policy ids.
            computation_date (str): Date of the computation.

        Returns:
            DictResult: DictResult containing the aggregation.
        """
        url = f'{self._item_path}compute/'
        json = {'policies': policies, 'computation_date': computation_date, 'filters': {}}
        aggs = Client().call_api_with_pagination(url, POST, json=json, page_size=ScenarioList.PAGE_SIZE)
        return DictResult(aggs)

    @classmethod
    def cedant_top_agg(cls, computation_date: str) -> Result:
        """Get the cedant top aggregation per scenariolist at the given computation date.

        Args:
            computation_date (str): Date of the computation.

        Returns:
            DictResult: DictResult containing the cedant top aggregation.
        """
        url = f'{ScenarioList.path}cedant_top_agg/?computation_date={computation_date}'
        aggs = Client().call_api(url, GET)
        return DictResult(aggs)

    def composition(self, computation_date: str) -> Result:
        """Get layers composition for each scenario of a given scenariolist.

        Args:
            computation_date (str): Date of the computation.

        Returns:
            DictResult: DictResult containing the composition.
        """
        url = f'{self._item_path}layers_composition/?computation_date={computation_date}'
        aggs = Client().call_api(url, GET)
        return DictResult(aggs)
