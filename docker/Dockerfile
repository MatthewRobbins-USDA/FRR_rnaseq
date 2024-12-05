FROM --platform=linux/amd64 debian:latest

ENV DEBIAN_FRONTEND=noninteractive

# Update and install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        wget \
        unzip \
        gnupg \
		git \
        default-jre \
        python3-pip \
	build-essential \
	r-base \
        libncurses5-dev \
	libbz2-dev \
	liblzma-dev \
	zlib1g-dev \
	libxml2-dev

# Create a symbolic link for Python
RUN ln -s /usr/bin/python3 /usr/bin/python && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mv /usr/lib/python3.11/EXTERNALLY-MANAGED /usr/lib/python3.11/EXTERNALLY-MANAGED.old

RUN pip3 install cutadapt HTSeq

RUN wget https://github.com/samtools/samtools/releases/download/1.18/samtools-1.18.tar.bz2 && \
    bzip2 -d samtools-1.18.tar.bz2 && \
    tar -xf samtools-1.18.tar && \
    cd samtools-1.18 && \
    ./configure --prefix=/usr/ && \
    make && \
    make install

RUN wget https://github.com/usadellab/Trimmomatic/files/5854859/Trimmomatic-0.39.zip && \
    unzip Trimmomatic-0.39.zip && \
    mv Trimmomatic-0.39 /usr/local/Trimmomatic-0.39

RUN R -e "install.packages('ggplot2', repos='https://ftp.osuosl.org/pub/cran/')" && \
    R -e "install.packages('BiocManager', repos='https://ftp.osuosl.org/pub/cran/')"

RUN apt-get update && apt-get install -y libcurl4-openssl-dev libpng-dev libssl-dev \
    g++ gfortran liblapack-dev libopenblas-dev
RUN R -e "BiocManager::install('DESeq2')" && \
	R -e "if ( ! library('DESeq2', character.only=TRUE, logical.return=TRUE) ) {quit(status=1, save='no')}"
RUN R -e "BiocManager::install('edgeR')"
RUN R -e "BiocManager::install('clusterProfiler')" && \
    R -e "BiocManager::install('enrichplot')"

#RUN R -e "if ( ! library('DESeq2', character.only=TRUE, logical.return=TRUE) ) {quit(status=1, save='no')}"

RUN wget https://cloud.biohpc.swmed.edu/index.php/s/oTtGWbWjaxsQ2Ho/download  && \
    unzip download && \
    mv hisat2-2.2.1 /usr/local/ && \
    ln -s /usr/local/hisat2-2.2.1/hisat2 /usr/local/bin/hisat2

RUN wget https://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v0.12.1.zip && \
    unzip fastqc_v0.12.1.zip -d /usr/local && \
    rm fastqc_v0.12.1.zip

RUN pip3 install goatools
RUN mkdir /global
WORKDIR /global
RUN cd /global && wget http://current.geneontology.org/ontology/go-basic.obo && git clone https://github.com/tanghaibao/goatools/

COPY GSEA_4.3.3.zip /global/GSEA_4.3.3.zip
RUN cd /global && unzip GSEA_4.3.3.zip && rm GSEA_4.3.3.zip

RUN apt-get update && apt-get install -y gfortran libcurl4-openssl-dev libssl-dev libpng-dev liblapack-dev libopenblas-dev libfontconfig1-dev

RUN R -e "install.packages(c('fields', 'impute', 'dynamicTreeCut', 'qvalue', 'flashClust', 'Hmisc') )" 
RUN R -e "BiocManager::install('WGCNA')"


RUN R -e "install.packages('remotes')"
RUN R -e "remotes::install_version('ggplot2',version='3.4.0')"
RUN R -e "BiocManager::install('ggtree')"
RUN R -e "BiocManager::install('clusterProfiler')"

RUN pip3 install pandas
COPY go_parse.py /global/go_parse.py
COPY interpro_add_annotations.py /global/interpro_add_annotations.py
COPY mapman_add_annotations.py /global/mapman_add_annotations.py
COPY gff_parse.py /global/gff_parse.py

RUN cd /global && chmod ug+x *.py

ENV PATH="${PATH}:/global"

CMD ["bash"]
