ARG SOURCE_IMAGE="python:3.6-alpine3.8"
FROM ${SOURCE_IMAGE} as builder

RUN apk add --no-cache gcc musl-dev postgresql-dev \
    && mkdir -p /build/package/dependencies

RUN cd /build/ \
    && pip download psycopg2 \
    && tar xvzf psycopg2-*.tar.gz -C . \
    && rm -f *.tar.gz \
    && cd psycopg2*/ \
    && python setup.py bdist_wheel --dist-dir=/build/package/dependencies/
WORKDIR /opt/build

#: this step won't be cached, so please keep it as lower as possible
COPY ./src /opt/build
RUN python setup.py bdist_wheel --dist-dir=/build/package/

FROM ${SOURCE_IMAGE}
MAINTAINER "Nickolas Fox <tarvitz@blacklibrary.ru>"
LABEL net.w40k.app="face-check" \
      net.w40k.description="well played tv face check resource"
RUN apk add --no-cache ca-certificates libpq

COPY --from=builder /build/package/ /build/

#: install binary dependencies and global runtime
RUN pip install /build/dependencies/* gunicorn

ARG PIP_EXTRA_DEPENDENCIES
ENV PIP_EXTRA_DEPENDENCIES=${PIP_EXTRA_DEPENDENCIES:-""}
RUN set -x \
    && if [ -z ${PIP_EXTRA_DEPENDENCIES} ]; then \
         pip install /build/*.whl; \
       else \
         package=$(ls /build/*.whl) \
         && pip install ${package}[${PIP_EXTRA_DEPENDENCIES}] ;\
       fi

CMD gunicorn face_check.wsgi:application \
        --log-level=info \
        --bind 0.0.0.0:8000 \
        --name grart \
        --pid /gunicorn.pid \
