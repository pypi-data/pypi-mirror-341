from typing import Annotated

from fastapi import APIRouter, Depends, Body

from kuhl_haus.bedrock.app.auth2 import api_key_auth
from kuhl_haus.bedrock.app.bedrock import get_embeddings_model
from kuhl_haus.bedrock.app.schema import EmbeddingsRequest, EmbeddingsResponse
from kuhl_haus.bedrock.app.env import DEFAULT_EMBEDDING_MODEL

router = APIRouter(
    prefix="/embeddings",
    dependencies=[Depends(api_key_auth)],
)


@router.post("", response_model=EmbeddingsResponse)
async def embeddings(
        embeddings_request: Annotated[
            EmbeddingsRequest,
            Body(
                examples=[
                    {
                        "model": "cohere.embed-multilingual-v3",
                        "input": [
                            "Your text string goes here"
                        ],
                    }
                ],
            ),
        ]
):
    if embeddings_request.model.lower().startswith("text-embedding-"):
        embeddings_request.model = DEFAULT_EMBEDDING_MODEL
    # Exception will be raised if model not supported.
    model = get_embeddings_model(embeddings_request.model)
    return model.embed(embeddings_request)
