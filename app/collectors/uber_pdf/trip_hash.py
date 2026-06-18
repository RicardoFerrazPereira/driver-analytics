import hashlib


def generate_trip_hash(record):

    content = "|".join(
        [
            str(record.get("trip_date")),
            str(record.get("processed_time")),
            str(record.get("trip_time")),
            str(record.get("event_type")),
            str(record.get("gross_amount")),
        ]
    )

    return hashlib.sha256(content.encode("utf-8")).hexdigest()
