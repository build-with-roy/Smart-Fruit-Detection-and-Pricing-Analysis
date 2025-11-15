import requests

def predict_image(
    image_file=None,
    image_bytes=None,
    server_url="http://127.0.0.1:5000/predict",
    district=None,
    market=None,
    latest_only=True,
):
    files = None
    if image_bytes is not None:
        files = {"image": ("upload.jpg", image_bytes, "image/jpeg")}
    elif image_file is not None:
        try:
            image_file.seek(0)
        except Exception:
            pass
        mime = getattr(image_file, "type", None) or "image/jpeg"
        name = getattr(image_file, "name", None) or "upload.jpg"
        files = {"image": (name, image_file, mime)}
    else:
        return {"error": "Invalid input", "message": "Provide image_file or image_bytes"}

    data = {}
    if district:
        data["district"] = district
    if market:
        data["market"] = market
    data["latest_only"] = "true" if latest_only else "false"

    try:
        response = requests.post(server_url, files=files, data=data, timeout=60)
        if response.status_code == 200:
            return response.json()
        else:
            # Try to return JSON error first
            try:
                return response.json()
            except Exception:
                return {"error": f"Status code: {response.status_code}", "message": response.text}
    except Exception as e:
        return {"error": "Connection Error", "message": str(e)}
