import boto3
import pathlib

rek = boto3.client("rekognition", region_name="us-east-1")  # غير الريجن إذا تبي
collection = "NAWA_PILGRIMS"

for img in pathlib.Path("faces").glob("*.png"):
    with img.open("rb") as f:
        rek.index_faces(
            CollectionId=collection,
            Image={"Bytes": f.read()},
            ExternalImageId=img.stem,  # بدون الامتداد
            DetectionAttributes=[]
        )
    print("✅ Indexed:", img.stem)

print(f"Indexing {img.name} → Format: {img.suffix}")
