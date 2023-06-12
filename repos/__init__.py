from clients import athena_client
from .discharge_repo import DischargeRepo
from .aurora import AuroraStore
from settings import AURORA_REPO_URI


aurora_store = AuroraStore(AURORA_REPO_URI)
discharge_repo_client = DischargeRepo(athena_client, aurora_store)
