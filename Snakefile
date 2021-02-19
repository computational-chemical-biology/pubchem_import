import os

samples = os.listdir('download_test')
samples = [x.replace('.json', '') for x in samples] 

rule all:
    input:
        "summary.txt"

rule classify:
    input:
        "download_test/{sample}.json"
    output:
        "result_test/{sample}_res.json"
    shell:
        "python npclassify.py {input} {output}" 

rule summary:
    input:
        expand("result_test/{sample}_res.json", sample=samples)
    output:
        "summary.txt"
    shell:
        "echo {input} > {output}" 
