//
// Cell aggregation CSV: run only when (aligner is cellranger or cellrangermulti) AND aggregation = true.
//

include { PREPARE_AGGR_CSV } from "../../modules/local/prepare_aggr_csv.nf"

workflow CELL_AGGREGATION {
    take:
        aligner
        ch_outs
        do_aggregation

    main:
        ch_aggr_csv = Channel.empty()

        if (do_aggregation && (aligner == "cellranger" || aligner == "cellrangermulti")) {
            ch_prep = ch_outs
                .map { meta, files -> meta.id }
                .collect()
                .map { ids -> tuple(aligner, ids) }
            PREPARE_AGGR_CSV(ch_prep)
            ch_aggr_csv = PREPARE_AGGR_CSV.out.csv
        }

    emit:
        aggr_csv = ch_aggr_csv
}
