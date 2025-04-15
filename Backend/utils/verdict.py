def classify_result(ai_score, exif_tags, byte_result):
    ai = ai_score > 0.75
    exif = bool(exif_tags)
    chunk = byte_result.get("chunk_match", False)
    c2pa = byte_result.get("c2pa_found", False)
    manipulated = byte_result.get("manipulated", False)

    # CASE 1: AI-generated
    if ai and exif and (chunk or c2pa):
        return ("image is ai-generated", "High AI score, metadata present, and byte or watermark match detected.")

    # CASE 2: AI-generated, watermark manipulated
    elif ai and not exif and (chunk or c2pa):
        return ("image is ai-generated but the watermark has been manipulated", "High AI score, no metadata, but watermark or chunk signature detected.")

    # CASE 3: Real image, modified by AI
    elif not ai and exif and (chunk or c2pa):
        return ("image is real but has been modified using an ai model", "Low AI score, metadata present, but modification signatures found.")

    # CASE 4: Real, modified and manipulated watermark
    elif not ai and not exif and (chunk or c2pa):
        return ("image is real but has been modified using an ai model & the watermark has been manipulated", "Low AI score, no metadata, but watermark or chunk found.")

    # CASE 5: Fully real
    else:
        return ("image is real", "Low AI score, no metadata, and no byte signature match.")
