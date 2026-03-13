//
// Cell aggregation CSV: run only when (aligner is cellranger or cellrangermulti) AND aggregation = true.
//

include { PREPARE_AGGR_CSV } from "../../modules/local/prepare_aggr_csv.nf"

workflow CELLRANGER_AGGR {
    take:
        aligner
        ch_outs
        do_aggregation

    main:
        ch_aggr_csv = Channel.empty()

        if (do_aggregation && (aligner == "cellranger" || aligner == "cellrangermulti")) {
            if (aligner == "cellranger") {
                ch_prep = ch_outs
                    .map { meta, _files -> meta.id }
                    .collect()
                    .map { ids -> tuple(aligner, ids) }
            } else {
                // cellrangermulti: path is count/<run_id>/outs/per_sample_outs/<demux_id>/...; pass "run_id:demux_id" per row.
                ch_prep = ch_outs
                    .map { meta, files ->
                        files.findAll { f -> f.toString().contains("/per_sample_outs/") }
                            .collect { f -> "${meta.id}:${f.toString().split("/per_sample_outs/")[1].split("/")[0]}" }
                            .unique()
                    }
                    .collect()
                    .map { list_of_lists -> tuple(aligner, list_of_lists.flatten()) }
            }
            PREPARE_AGGR_CSV(ch_prep)
            ch_aggr_csv = PREPARE_AGGR_CSV.out.csv
        }

    emit:
        aggr_csv = ch_aggr_csv
}
