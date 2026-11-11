"""Central configuration so every run is reproducible."""
from pathlib import Path

SEED = 20260611
N_RECORDS = 20_000
TEST_SIZE = 0.30
N_BOOTSTRAP = 1_000
DECISION_THRESHOLD = 0.30  # documented operating point (see docs/methodology.md)

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
RESULTS_DIR = ROOT / "results"
FIG_DIR = RESULTS_DIR / "figures"
TABLE_DIR = RESULTS_DIR / "tables"

DATA_FILE = DATA_DIR / "synthetic_applicants.csv"

# Protected / sensitive attributes. They are NEVER given to the model as inputs
# ("fairness through unawareness") but are used to audit outcomes.
PROTECTED = ["gender", "region_type"]

MODEL_FEATURES = [
    "txn_velocity_24h",
    "avg_txn_amount_log",
    "night_txn_ratio",
    "new_device_flag",
    "account_age_days",
    "id_match_score",
    "device_tier",
    "geo_mismatch_flag",
]

# Features suspected of acting as proxies for region_type (tested, not assumed).
SUSPECT_PROXIES = ["id_match_score", "device_tier", "geo_mismatch_flag"]
