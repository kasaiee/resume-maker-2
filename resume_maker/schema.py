"""
project schema (main schema)
"""
import graphene
from app_accounting.gql import schema as app_accounging_schema


class Query(app_accounging_schema.Query):
    pass


schema = graphene.Schema(query=Query)