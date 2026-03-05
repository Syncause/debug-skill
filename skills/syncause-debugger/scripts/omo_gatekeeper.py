#!/usr/bin/env python3
import sys
import argparse

def check_omo2_to_omo3(trace_id):
    if not trace_id or len(trace_id) < 8:
        print("[REJECTED] OMO-2 -> OMO-3 Gate Failed: Invalid or missing traceId. You MUST capture a valid trace first.", file=sys.stderr)
        sys.exit(1)
    print(f"[PASSED] OMO-2 Gate cleared for trace: {trace_id}. Proceed to OMO-3.")
    sys.exit(0)

def check_omo3_to_omo4(root_cause_file):
    if not root_cause_file:
        print("[REJECTED] OMO-3 -> OMO-4 Gate Failed: You MUST provide the specific file path of the root cause.", file=sys.stderr)
        sys.exit(1)
    print(f"[PASSED] OMO-3 Gate cleared for file: {root_cause_file}. Proceed to OMO-4 code edits.")
    sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Soft Gating for Syncause Debugger OMO Workflow")
    parser.add_argument("--gate", choices=["omo2", "omo3"], required=True, help="Which gate to check")
    parser.add_argument("--trace-id", default="", help="The found traceId (required for omo2)")
    parser.add_argument("--cause-file", default="", help="The file path of the root cause (required for omo3)")
    args = parser.parse_args()

    if args.gate == "omo2":
        if not args.trace_id:
            print("[REJECTED] Missing --trace-id argument.", file=sys.stderr)
            sys.exit(1)
        check_omo2_to_omo3(args.trace_id)
    elif args.gate == "omo3":
        if not args.cause_file:
            print("[REJECTED] Missing --cause-file argument.", file=sys.stderr)
            sys.exit(1)
        check_omo3_to_omo4(args.cause_file)
