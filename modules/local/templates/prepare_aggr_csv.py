#!/usr/bin/env python3
"""
Build aggregation CSV: (sample_id, molecule_h5) for cellranger aggr.
- cellranger (count): paths to molecule_info.h5 under count/<sample_id>/outs/
- cellrangermulti: paths to sample_molecule_info.h5 under .../per_sample_outs/<demux_id/
Paths are relative to the CSV output dir so aggr can find the files when run from outdir.
"""

import csv
import os
import sys


def main():
    if len(sys.argv) < 5:
        sys.exit("Usage: prepare_aggr_csv.py <out_csv> <aligner> <outdir> <id1> [id2 ...]")
    out_csv = sys.argv[1]
    aligner = sys.argv[2].lower()
    outdir = sys.argv[3].rstrip("/")
    ids = sys.argv[4:]
    csv_dir = os.path.join(outdir, "cellranger_aggr_input")
    rows = []

    if aligner == "cellranger":
        # count: cellranger/count/<sample_id>/outs/molecule_info.h5
        for sample_id in ids:
            mol_h5_full = os.path.join(outdir, "cellranger", "count", sample_id, "outs", "molecule_info.h5")
            mol_h5 = os.path.relpath(mol_h5_full, csv_dir)
            rows.append((sample_id, mol_h5))
    elif aligner == "cellrangermulti":
        # multi: cellrangermulti/count/<run_id>/outs/per_sample_outs/<demux_id>/sample_molecule_info.h5
        # ids are "run_id:demux_id"; sample_id in CSV = demux_id
        for pair in ids:
            run_id, demux_id = pair.split(":", 1)
            mol_h5_full = os.path.join(
                outdir, "cellrangermulti", "count", run_id,
                "outs", "per_sample_outs", demux_id, "sample_molecule_info.h5"
            )
            mol_h5 = os.path.relpath(mol_h5_full, csv_dir)
            rows.append((demux_id, mol_h5))
    else:
        sys.exit(f"Unknown aligner: {aligner}. Use 'cellranger' or 'cellrangermulti'.")

    with open(out_csv, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["sample_id", "molecule_h5"])
        for sid, p in rows:
            w.writerow([sid, p])


if __name__ == "__main__":
    main()
