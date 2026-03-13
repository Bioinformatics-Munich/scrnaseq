//
// Creates the aggregation CSV only: writes (sample_id, molecule_h5) using params.outdir and
// sample_ids. Paths follow cellranger output layout. No path inputs; subworkflow handles paths later.
//

process PREPARE_AGGR_CSV {
    tag "${aligner}"
    label 'process_single'

    publishDir "${params.outdir}/cellranger_aggr_input", mode: 'copy', pattern: '*.csv', when: params.outdir

    input:
    tuple val(aligner), val(sample_ids)

    output:
    path("aggr_*.csv"), emit: csv

    script:
    if (aligner != "cellranger" && aligner != "cellrangermulti") error "Alignment type ${aligner} not supported for aggregation"
    def outdir_escaped = params.outdir.toString().replace("'", "'\"'\"'")
    def ids_escaped = sample_ids.collect { "'${it.replace("'", "'\"'\"'")}'" }.join(' ')
    """
    python3 $projectDir/modules/local/templates/prepare_aggr_csv.py aggr_${aligner}.csv ${aligner} '${outdir_escaped}' ${ids_escaped}
    """
}