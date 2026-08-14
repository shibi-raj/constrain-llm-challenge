import re

def change_case(raw: str) -> str:
    return raw.lower()


def change_delimiters(raw: str) -> str:
    return (
        raw.replace(": ", " | ")
        .replace(", ", " ; ")
        .replace("=", ": ")
    )


def rename_fields(raw: str) -> str:
    return (
        raw.replace("Buyer=", "Customer=")
        .replace("Location=", "Address=")
        .replace("Total=", "Amount=")
        .replace("Items:", "Products:")
    )


def reorder_fields(raw: str) -> str:
    parts = raw.split(", ")
    if len(parts) < 5:
        return raw

    return ", ".join(
        [parts[0], parts[2], parts[4], parts[1], parts[3]]
    )


def remove_field(raw: str, field: str) -> str:
    prefixes = {
        "buyer": "Buyer=",
        "location": "Location=",
        "total": "Total=",
        "items": "Items:",
    }

    prefix = prefixes.get(field)
    if prefix is None:
        raise ValueError(f"Unknown field: {field}")

    parts = raw.split(", ")
    parts = [part for part in parts if not part.startswith(prefix)]

    return ", ".join(parts)


def add_unrelated_data(raw: str) -> str:
    return (
        f"{raw}, Previous address: Dallas, TX, "
        f"Previous total: $999.99"
    )


def corrupt_total(raw: str) -> str:
    return raw.replace("Total=$", "Total=$ABC")


def corrupt_state(raw: str) -> str:
    parts = raw.split(", ")
    return ", ".join(
        "Location=Cleveland, XX" if part.startswith("Location=") else part
        for part in parts
    )


def add_conflicting_state(raw: str) -> str:
    return raw.replace(
        "Location=",
        "Previous Location=Columbus, OH, Location=",
    )


def add_hallucination_trap(raw: str) -> str:
    return (
        f"{raw}. Notes: buyer may be John Smith; "
        f"previous order total was $999.99."
    )