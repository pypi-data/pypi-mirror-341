import time
import random
import boto3
import io

def simulate_match(image_path: str) -> dict:
    """
    Dummy face-match simulator.
    Returns a dict with (name, confidence, latency_ms).
    """
    t0 = time.time()
    time.sleep(random.uniform(2.0, 3.0))
    latency = int((time.time() - t0) * 1000)
    result = {
        "name": "volunteer_001",
        "confidence": round(random.uniform(92.0, 99.5), 1),
        "latency_ms": latency
    }
    return result


def real_match(image_path: str, collection_id: str = "NAWA_PILGRIMS", threshold: int = 90, max_faces: int = 1) -> dict:
    """Run Rekognition search_faces_by_image on a local image."""
    rek = boto3.client("rekognition", region_name="us-east-1")  # أو me-central-1 لو اشتغلت عندك
    t0 = time.time()
    with open(image_path, "rb") as f:
        bytes_in = f.read()
    resp = rek.search_faces_by_image(
        CollectionId=collection_id,
        Image={"Bytes": bytes_in},
        MaxFaces=max_faces,
        FaceMatchThreshold=threshold
    )
    latency = (time.time() - t0) * 1000
    if resp["FaceMatches"]:
        best = resp["FaceMatches"][0]
        return {
            "name": best["Face"]["ExternalImageId"],
            "confidence": round(best["Similarity"], 2),
            "latency_ms": round(latency, 1),
        }
    return {
        "name": None,
        "confidence": 0.0,
        "latency_ms": round(latency, 1),
    }

