from __future__ import annotations

import sys

from app.core.auth_codes import days_from_now, generate_access_code, stable_hash
from app.db.session import SessionLocal
from app.models.access_code import AccessCode


def main() -> None:
    customer_name = sys.argv[1] if len(sys.argv) > 1 else None
    days = int(sys.argv[2]) if len(sys.argv) > 2 else 30

    raw_code = generate_access_code()

    db = SessionLocal()
    try:
        row = AccessCode(
            code_hash=stable_hash(raw_code),
            customer_name=customer_name,
            expires_at=days_from_now(days),
            max_devices=2,
            status="active",
        )
        db.add(row)
        db.commit()
    finally:
        db.close()

    print(f"Customer: {customer_name or '-'}")
    print(f"Expires in: {days} days")
    print(f"Access code: {raw_code}")


if __name__ == "__main__":
    main()