ARG SOURCE_IMAGE="python:3.6-alpine3.8"
FROM ${SOURCE_IMAGE} as builder

COPY ./src /opt/build
WORKDIR /opt/build

RUN mkdir -p /build/packages/
RUN python setup.py bdist_wheel --dist-dir=/build/packages/

FROM ${SOURCE_IMAGE}
MAINTAINER "Nickolas Fox <tarvitz@blacklibrary.ru>"
LABEL net.w40k.app="face-check" \
      net.w40k.description="well played tv face check resource"
RUN apk add --no-cache ca-certificates

COPY --from=builder /build/packages/ /build/

RUN pip install /build/*.whl gunicorn
CMD gunicorn face_check.wsgi:application \
        --log-level=info \
        --bind 0.0.0.0:8000 \
        --name grart \
        --pid /gunicorn.pid \
