from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from enum import Enum

from pydantic import BaseModel

from databases.mongo import DatabaseClient
from models.base import MongoBaseModel, PyObjectId


class RequestMethod(str, Enum):
    HTTP = "http"
    SDK = "sdk"


class ModelName(str, Enum):
    LLAMA2_70B_CHAT = "llama2-70b"


class TokenCounts(int, Enum):
    HUNDRED = 100
    THOUSAND = 1000


class Throughputs(BaseModel):
    start_time: datetime
    concurrent_requests: int
    model_name: str
    request_method: RequestMethod
    input_tokens: TokenCounts
    output_tokens: TokenCounts
    tokens_per_second: List[float]


def save_throughputs(throughputs: Throughputs) -> None:
    throughputs_collection = DatabaseClient.get_collection("throughputs")
    throughputs_collection.insert_one(throughputs.model_dump(by_alias=True))


# async def add_transaction(txn: Transaction, org: Optional[Organization] = None) -> None:
#     txns_collection = DatabaseClient.get_collection("transactions_v2")

#     if org is not None:
#         txn.org_local_id = org.local_id

#     await txns_collection.insert_one(txn.model_dump(by_alias=True))


# async def get_past_usage(org: Organization, td: Optional[timedelta] = None) -> int:
#     txns_collection = DatabaseClient.get_collection("transactions_v2")

#     query: Dict[str, Any] = {"org_local_id": org.local_id}

#     if td is not None:
#         start = datetime.now() - td
#         query["start_time"] = {"$gte": start}

#     return await txns_collection.count_documents(query)


# async def get_avg_response_cost(org: Organization) -> float:
#     txns_collection = DatabaseClient.get_collection("transactions_v2")

#     # Filter documents by org_local_id
#     match_stage = {"$match": {"org_local_id": org.local_id}}

#     # Group documents by org_local_id and calculate the sum and count
#     group_stage = {
#         "$group": {
#             "_id": "$org_local_id",
#             "total_cost_sum": {"$sum": "$total_cost"},
#             "count": {"$sum": 1},
#         }
#     }

#     # Calculate the average
#     project_stage = {
#         "$project": {
#             "_id": 0,
#             "avg_response_cost": {
#                 "$cond": {
#                     "if": {"$eq": ["$count", 0]},
#                     "then": 0,
#                     "else": {"$divide": ["$total_cost_sum", "$count"]},
#                 }
#             },
#         }
#     }

#     # Run the aggregation pipeline
#     pipeline = [match_stage, group_stage, project_stage]
#     results = await txns_collection.aggregate(pipeline).to_list(None)

#     # Return the average response cost, or 0 if there are no results
#     return results[0].get("avg_response_cost", 0) if results else 0


# async def get_avg_total_duration(org: Organization) -> float:
#     txns_collection = DatabaseClient.get_collection("transactions_v2")

#     # Filter documents by org_local_id
#     match_stage = {"$match": {"org_local_id": org.local_id}}

#     # Group documents by org_local_id and calculate the sum and count
#     group_stage = {
#         "$group": {
#             "_id": "$org_local_id",
#             "total_duration_sum": {"$sum": "$total_duration_ms"},
#             "count": {"$sum": 1},
#         }
#     }

#     # Calculate the average
#     project_stage = {
#         "$project": {
#             "_id": 0,
#             "avg_total_duration_ms": {
#                 "$cond": {
#                     "if": {"$eq": ["$count", 0]},
#                     "then": 0,
#                     "else": {"$divide": ["$total_duration_sum", "$count"]},
#                 }
#             },
#         }
#     }

#     # Run the aggregation pipeline
#     pipeline = [match_stage, group_stage, project_stage]
#     results = await txns_collection.aggregate(pipeline).to_list(None)

#     # Return the average total duration, or 0 if there are no results
#     return results[0].get("avg_total_duration_ms", 0) if results else 0


# async def get_cost_by_month(org: Organization) -> List[Dict[str, Any]]:
#     txns_collection = DatabaseClient.get_collection("transactions_v2")
#     cursor = txns_collection.find(
#         {"org_local_id": org.local_id}, {"start_time": 1, "total_cost": 1, "_id": 0}
#     )
#     transactions = await cursor.to_list(length=None)

#     monthly_costs: Dict[str, float] = {}  # Dictionary to store costs by "Month Year"
#     for txn in transactions:
#         start_time = txn.get("start_time")
#         if isinstance(start_time, datetime):
#             month_year = f"{start_time.strftime('%b')} {start_time.year}"
#             monthly_costs.setdefault(month_year, 0)
#             monthly_costs[month_year] += txn.get("total_cost", 0)

#     formatted_costs = [
#         {"name": month_year, "Cost": cost} for month_year, cost in monthly_costs.items()
#     ]
#     formatted_costs.sort(key=lambda x: datetime.strptime(str(x["name"]), "%b %Y"))

#     return formatted_costs


# async def get_total_cost(org: Organization) -> float:
#     txns_collection = DatabaseClient.get_collection("transactions_v2")
#     cursor = txns_collection.find(
#         {"org_local_id": org.local_id}, {"start_time": 1, "total_cost": 1, "_id": 0}
#     )
#     transactions = await cursor.to_list(length=None)

#     # Sum up the total cost
#     total_cost = sum(txn.get("total_cost", 0) for txn in transactions)

#     return total_cost
