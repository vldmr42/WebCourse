import graphene

from catalog.schema import Query as CatalogQuery

class Query(CatalogQuery, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)