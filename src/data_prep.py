"""Build data/sa_regions.csv from the AIHW My Aged Care region tables (2024-25).

Source: Australian Institute of Health and Welfare, GEN Aged Care Data,
My aged care region supplementary tables 2024-25 (CC BY 4.0).

Run it with: python src/data_prep.py
"""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
XLSX = ROOT / "data" / "a3_acpr_2024_25.xlsx"
OUT = ROOT / "data" / "sa_regions.csv"

# Table 1 percentage columns (stored as fractions, e.g. 0.257) -> our column names
PCT_COLUMNS = {
    "Lives alone (%)": "pct_lives_alone",            # people 65+
    "Other language (%)": "pct_other_language",      # people 65+
    "Requires assistance (%)": "pct_requires_assistance",  # people 55+, core activities
    "First Nations (%)": "pct_first_nations",        # people 50+
}

CARE_TYPES = {
    "Home support": "services_home_support",
    "Home care": "services_home_care",
    "Residential": "services_residential",
}


def sa_only(df):
    df = df[df["State/Territory"].astype(str).str.strip() == "SA"].copy()
    df["code"] = df["ACPR code"].astype(int)
    df["name"] = df["ACPR name"].astype(str).str.strip()
    return df


def build():
    t1 = sa_only(pd.read_excel(XLSX, sheet_name="Table 1", header=4))
    t1 = t1[["code", "name", *PCT_COLUMNS]].rename(columns=PCT_COLUMNS)
    for col in PCT_COLUMNS.values():
        t1[col] = (t1[col] * 100).round(1)

    t2 = sa_only(pd.read_excel(XLSX, sheet_name="Table 2.1", header=3))
    t2["Care type"] = t2["Care type"].astype(str).str.strip()
    services = (
        t2.pivot_table(index="code", columns="Care type", values="Number of services", aggfunc="sum")
        .rename(columns=CARE_TYPES)[list(CARE_TYPES.values())]
        .fillna(0)
        .astype(int)
        .reset_index()
    )

    regions = t1.merge(services, on="code", how="left")
    regions = regions[["code", "name", *CARE_TYPES.values(), *PCT_COLUMNS.values()]]
    return regions.sort_values("code").reset_index(drop=True)


def check(regions):
    assert len(regions) == 11, f"expected 11 SA regions, got {len(regions)}"
    assert list(regions["code"]) == list(range(401, 412)), "expected codes 401-411"
    eyre = regions[regions["name"] == "Eyre Peninsula"].iloc[0]
    assert eyre["services_home_support"] == 17
    assert eyre["services_home_care"] == 6
    assert eyre["services_residential"] == 4
    assert abs(eyre["pct_lives_alone"] - 25.7) < 0.1


if __name__ == "__main__":
    regions = build()
    check(regions)
    regions.to_csv(OUT, index=False)
    print(regions.to_string(index=False))
    print(f"\nEyre Peninsula check passed. Wrote {len(regions)} rows to {OUT}")
