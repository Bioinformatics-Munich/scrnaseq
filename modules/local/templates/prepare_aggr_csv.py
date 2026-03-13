#!/usr/bin/env python3
"""
Only finds paths to molecule_info.h5 (count) or sample_molecule_info.h5 (multi),
pairs each with sample_id, and writes CSV (sample_id, molecule_h5). Nothing else.
"""

import csv
import glob
import os
import sys


def main():
    out_csv = sys.argv[1]
    mode = sys.argv[2].lower()

    if mode == "count":
        # Staged dirs: outs_1, outs_2, ...; each has molecule_info.h5. sample_ids in same order.
        n = int(sys.argv[3])
        sample_ids = sys.argv[4 : 4 + n]
        rows = []
        for i in range(n):
            staged = "outs_%d" % (i + 1)
            mol_h5 = os.path.abspath(os.path.join(staged, "molecule_info.h5"))
            rows.append((sample_ids[i], mol_h5))

    elif mode == "count_paths":
        # No staged dirs: build paths from outdir + sample_ids (cellranger layout: outdir/cellranger/<id>/outs/molecule_info.h5).
        outdir = sys.argv[3].rstrip("/")
        sample_ids = sys.argv[4:]
        rows = []
        for sid in sample_ids:
            mol_h5 = os.path.join(outdir, "cellranger", sid, "outs", "molecule_info.h5")
            rows.append((sid, os.path.abspath(mol_h5)))

    elif mode == "multi_paths":
        # No staged dirs: build paths from outdir + sample_ids (cellranger multi layout).
        outdir = sys.argv[3].rstrip("/")
        sample_ids = sys.argv[4:]
        rows = []
        for sid in sample_ids:
            mol_h5 = os.path.join(outdir, "cellranger_multi", sid, "per_sample_outs", sid, "sample_molecule_info.h5")
            rows.append((sid, os.path.abspath(mol_h5)))
            
    elif mode == "multi":
        # Single staged dir outs_1: per_sample_outs/<SampleName>/sample_molecule_info.h5
        pattern = "outs_1/per_sample_outs/*/sample_molecule_info.h5"
        rows = []
        for mol_h5 in sorted(glob.glob(pattern)):
            if not os.path.isfile(mol_h5):
                continue
            sample_id = os.path.basename(os.path.dirname(mol_h5))
            rows.append((sample_id, os.path.abspath(mol_h5)))
    else:
        sys.exit("Unknown mode: use 'count', 'count_paths', 'multi_paths', or 'multi'")

    with open(out_csv, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["sample_id", "molecule_h5"])
        for sid, p in rows:
            w.writerow([sid, p])


if __name__ == "__main__":
    main()
