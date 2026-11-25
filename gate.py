import json
import sys
from pathlib import Path

REPORT_PATH = Path("eval_report.json")
MIN_PASS_RATE = 0.85
MAX_AVG_LATENCY_MS = 300


def main() -> int:
    if not REPORT_PATH.exists():
        print("GATE FAILED: eval_report.json not found. Run pytest first.")
        return 1

    report = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    print("Release Gate Report:", json.dumps(report))

    if report["security_failures"] > 0:
        print(f"GATE FAILED: {report['security_failures']} security failure(s) detected.")
        return 1

    if report["pass_rate"] < MIN_PASS_RATE:
        print(f"GATE FAILED: pass_rate {report['pass_rate']} < {MIN_PASS_RATE}")
        return 1

    if report["avg_latency_ms"] > MAX_AVG_LATENCY_MS:
        print(f"GATE FAILED: avg_latency_ms {report['avg_latency_ms']} > {MAX_AVG_LATENCY_MS}")
        return 1

    print("GATE PASSED: Ready for deployment.")
    return 0


if __name__ == "__main__":
    sys.exit(main())