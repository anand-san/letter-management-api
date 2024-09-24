import strawberry
from api.resolvers import Query, Mutation

schema = strawberry.Schema(query=Query, mutation=Mutation)
