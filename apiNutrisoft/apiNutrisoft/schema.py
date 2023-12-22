import graphene
import nutrisoft.schema

class Query(nutrisoft.schema.Query, graphene.ObjectType):
    pass

class Mutation(nutrisoft.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query , mutation=Mutation)