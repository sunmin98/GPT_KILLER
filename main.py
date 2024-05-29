import os
from pinecone import Pinecone, ServerlessSpec

# API 키와 호스트 설정
api_key = "e1547614-ee24-460f-b4c1-a3c1611f2bda"
host = "https://db-test-x3xmefr.svc.aped-4627-b74a.pinecone.io"

# Pinecone 클라이언트 초기화
pc = Pinecone(
    api_key=api_key,
    host=host
)

lists = []
# 인덱스 이름 설정
index_name = "db-test"

# 인덱스 존재 여부 확인 및 생성
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=512,  # 해당 인덱스의 차원 수를 512로 설정
        metric='cosine',  # 사용할 거리 측정 방법
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )

# 인덱스 연결
index = pc.Index(index_name)

# 벡터 삽입
vectors_to_insert = [
    {"id": "vec1", "values": [0.1] * 512, "metadata": {"genre": "comedy"}},  # 메타데이터 추가
    {"id": "vec2", "values": [0.2] * 512, "metadata": {"genre": "drama"}},  # 메타데이터 추가
    {"id": "vec3", "values": [0.3] * 512, "metadata": {"genre": "action"}},  # 메타데이터 추가
]

index.upsert(vectors=vectors_to_insert)

# 벡터 검색
query_vector = [0.3] * 512  # 실제 쿼리 벡터 값으로 대체
response = index.query(
    namespace="db-test",  # 네임스페이스가 설정되지 않았으면 빈 문자열
    vector=query_vector,
    top_k=2,
    include_values=True,
    include_metadata=True,
    filter={"genre": {"$eq": "action"}}
)

print("Query result:", response)