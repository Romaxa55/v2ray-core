FROM public.ecr.aws/docker/library/golang:1.20-alpine AS build

WORKDIR /build

COPY . .

RUN go mod download -x

RUN env CGO_ENABLED=0 go build -v -o build_assets/v2ray -ldflags "-s -w" ./main

FROM alpine:3.20.0

RUN apk add --no-cache python3

COPY --from=build /build/build_assets/v2ray /bin/
COPY --from=build /build/build_assets/geoip-only-cn-private.dat /etc/v2ray/
COPY --from=build /build/build_assets/geoip.dat /etc/v2ray/
COPY --from=build /build/build_assets/geosite.dat /etc/v2ray/
COPY --from=build /build/build_assets/add_clients.py /etc/v2ray/add_clients.py
COPY --from=build /build/build_assets/template.json /etc/v2ray/template.json
COPY --from=build /build/build_assets/entrypoint.sh /entrypoint.sh

ENV V2RAY_LOCATION_ASSET /etc/v2ray/

# Устанавливаем права на выполнение скрипта
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
