FROM alpine:3.15.5 as build

ARG CLOUDFLARED_VERSION=2022.7.1

RUN apk add curl
RUN curl -Lo cloudflared https://github.com/cloudflare/cloudflared/releases/download/${CLOUDFLARED_VERSION}/cloudflared-linux-arm64 && \
    chmod +x cloudflared


# FROM gcr.io/distroless/base-debian11:nonroot
FROM alpine

ARG USER=cloudflared

RUN adduser -D $USER

COPY --from=build --chown=cloudflared /cloudflared /usr/local/bin/

USER $USER

ENTRYPOINT ["cloudflared", "--no-autoupdate"]

CMD ["version"]
