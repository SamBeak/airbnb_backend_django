import strawberry
from rooms import schema as rooms_schema

@strawberry.type
class Query(rooms_schema.Query): # Query class를 rooms_schema.Query로 상속
    pass

@strawberry.type
class Mutation:
    pass

schema = strawberry.Schema(query=Query, mutation=Mutation)