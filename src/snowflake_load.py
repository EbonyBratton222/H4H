"""Load the synthetic facility and appointment CSVs into Snowflake.

The data is made up (is_synthetic = TRUE). It goes to FIRST_CALL.SYNTHETIC.
Reads SNOWFLAKE_* settings from .env (see sample.env).

Run it with: python src/snowflake_load.py
"""

import os
from pathlib import Path

import snowflake.connector
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
SQL = ROOT / "snowflake" / "setup.sql"
CSV_DIR = ROOT / "data" / "synthetic"
FILES = ["sa_health_facilities_synthetic.csv", "sa_appointment_slots_synthetic.csv"]
EXPECTED_ROWS = {"FACILITIES": 82, "APPOINTMENT_SLOTS": 2915}


def connect():
    """Open a connection using SNOWFLAKE_* from .env."""
    load_dotenv(ROOT / ".env")
    settings = {
        "account": os.environ["SNOWFLAKE_ACCOUNT"],
        "user": os.environ["SNOWFLAKE_USER"],
        "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
        "role": os.getenv("SNOWFLAKE_ROLE") or None,
    }
    if os.getenv("SNOWFLAKE_AUTHENTICATOR"):     # e.g. externalbrowser for SSO / MFA
        settings["authenticator"] = os.environ["SNOWFLAKE_AUTHENTICATOR"]
    else:
        settings["password"] = os.environ["SNOWFLAKE_PASSWORD"]
    return snowflake.connector.connect(**settings)


def statements():
    """Split setup.sql on semicolons, dropping comment-only chunks."""
    for chunk in SQL.read_text().split(";"):
        lines = [l for l in chunk.splitlines() if l.strip() and not l.strip().startswith("--")]
        if lines:
            yield "\n".join(lines)


def load():
    with connect() as conn, conn.cursor() as cur:
        put_done = False
        for sql in statements():
            if sql.startswith("COPY INTO") and not put_done:
                for name in FILES:
                    cur.execute(f"PUT 'file://{(CSV_DIR / name).as_posix()}' @RAW_FILES OVERWRITE = TRUE")
                put_done = True
            cur.execute(sql)
        for table, expected in EXPECTED_ROWS.items():
            count = cur.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            assert count == expected, f"{table}: expected {expected} rows, got {count}"
            print(f"{table}: {count} rows")
        regions = cur.execute("SELECT COUNT(DISTINCT acpr_code) FROM FACILITIES").fetchone()[0]
        assert regions == 11, f"expected facilities in 11 SA regions, got {regions}"
    print("Loaded into FIRST_CALL.SYNTHETIC (tables FACILITIES, APPOINTMENT_SLOTS, view FACILITY_AVAILABILITY)")


if __name__ == "__main__":
    load()
