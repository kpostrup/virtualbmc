FROM ubuntu:20.04 as build
WORKDIR /build/virtualbmc
ENV DEBIAN_FRONTEND=noninteractive
RUN grep -E '^deb ' /etc/apt/sources.list | sed -E 's,^deb (.+),deb-src \1,g' >/etc/apt/sources.list.d/deb-src.list && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends \
        devscripts \
        equivs
COPY debian debian
RUN mk-build-deps \
        --install \
        --tool 'apt-get -o APT::Get::Assume-Yes=1 -o Debug::pkgProblemResolver=yes --no-install-recommends' \
        debian/control
COPY . .
RUN debuild -b -us -uc
RUN mkdir ../packages && \
    cd ../packages && \
    cp ../*.deb . && \
    dpkg-scanpackages . | gzip >Packages.gz

FROM ubuntu:20.04
COPY --from=build /build/packages /packages
RUN echo 'deb [trusted=yes] file:///packages ./' >/etc/apt/sources.list.d/local.list && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends virtualbmc && \
    rm -rf /var/lib/apt/lists/*
ENTRYPOINT ["vbmcd", "--foreground"]
