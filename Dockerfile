FROM public.ecr.aws/docker/library/golang:1.20-alpine AS build

WORKDIR /build

COPY . .

RUN go mod download -x

RUN mkdir -p build_assets && \
  env CGO_ENABLED=0 go build -v -o build_assets/v2ray -ldflags "-s -w" ./main

WORKDIR /build/build_assets

#ENTRYPOINT["tail", "-f", "/dev/null"]
