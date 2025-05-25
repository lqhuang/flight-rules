---
title: 'MinIO: Bootstrap a User and Bucket'
date: 2025-05-25
tags:
  - container
---

I found the default MinIO configuration insufficient for my needs, so I created a custom Dockerfile to bootstrap a user and bucket. This allows me to set up MinIO with a specific user and bucket right from the start.

```bash
#!/bin/sh

# Extended from
# https://github.com/minio/minio/blob/master/dockerscripts/docker-entrypoint.sh

# If command starts with an option, prepend minio.
if [ "${1}" != "minio" ]; then
    if [ -n "${1}" ]; then
        set -- minio "$@"
    fi
fi

docker_switch_user() {
    if [ -n "${MINIO_USERNAME}" ] && [ -n "${MINIO_GROUPNAME}" ]; then
        if [ -n "${MINIO_UID}" ] && [ -n "${MINIO_GID}" ]; then
            chroot --userspec=${MINIO_UID}:${MINIO_GID} / "$@"
        else
            echo "${MINIO_USERNAME}:x:1000:1000:${MINIO_USERNAME}:/:/sbin/nologin" >>/etc/passwd
            echo "${MINIO_GROUPNAME}:x:1000" >>/etc/group
            chroot --userspec=${MINIO_USERNAME}:${MINIO_GROUPNAME} / "$@"
        fi
    else
        exec "$@"
    fi
}


###############################
# Custom entrypoint for MinIO #
###############################

MINIO_ALIAS=minio
MINIO_ENDPOINT=http://localhost:9000

ensure_env_vars() {
    required_env_vars=(
        MINIO_ROOT_USER
        MINIO_ROOT_PASSWORD
        X_USER_NAME
        X_SECRET_KEY
        X_DEFAULT_BUCKET
    )
    for env_var in "${required_env_vars[@]}"; do
        if [[ -z "${env_var:-}" ]]; then
            echo "Required environment variable ${env_var} is not set."
            exit 1
        fi
    done
}

minio_create_default_user_and_bucket() {
    mc admin user add ${MINIO_ALIAS} ${X_USER_NAME} ${X_SECRET_KEY} || true
    mc admin policy attach ${MINIO_ALIAS} readwrite --user=${X_USER_NAME} || true
    mc admin user ls ${MINIO_ALIAS}

    mc mb --ignore-existing ${MINIO_ALIAS}/${X_DEFAULT_BUCKET}
    mc anonymous set download ${MINIO_ALIAS}/${X_DEFAULT_BUCKET}
    mc anonymous get-json ${MINIO_ALIAS}/${X_DEFAULT_BUCKET}

    # mc ls --recursive --versions ${MINIO_ALIAS}/${X_DEFAULT_BUCKET}
    # mc tree --files ${MINIO_ALIAS}/${X_DEFAULT_BUCKET}

    # - `none` - Disable anonymous access to the ALIAS.
    # - `download` - Enable download-only access to the ALIAS.
    # - `upload` - Enable upload-only access to the ALIAS.
    # - `public` - Enable download and upload access to the ALIAS.
}

ensure_minio_alive_and_set_alias() {
    mc alias set ${MINIO_ALIAS} ${MINIO_ENDPOINT} ${MINIO_ROOT_USER} ${MINIO_ROOT_PASSWORD} 2>/dev/null
}

bootstrap_in_background() {
    # After executing the block, the until loop returns to check the condition again.
    while (! ensure_minio_alive_and_set_alias); do
        echo "Waiting for MinIO server to be live..."
        sleep 0.5
    done

    echo "MinIO server is live, proceeding with setup..."
    minio_create_default_user_and_bucket
    echo "MinIO server setup completed successfully. Bootstrap script finished."
}


ensure_env_vars
if ! command -v mc &> /dev/null; then
    echo "mc (MinIO Client) is not installed. Please install it first."
    exit 1
fi
bootstrap_in_background &

# Run the main command
docker_switch_user "$@"
```

Simply replace the original `docker-entrypoint.sh` in your MinIO Docker image with this script.

```yaml
services:
  minio:
    image: minio/minio:RELEASE.2025-04-22T22-12-26Z
    ...
    environment:
      MINIO_ROOT_USER: xxx
      MINIO_ROOT_PASSWORD: xxx
      MINIO_CONSOLE_ADDRESS: ':9001'

      X_USER_NAME: xxx
      X_SECRET_KEY: xxx
      X_DEFAULT_BUCKET: xxx
    volumes:
      - ../somewhere:/data
      # Overwrite entrypoint to use custom script
      - ./minio-entrypoint.sh:/usr/bin/docker-entrypoint.sh
    command: ['server', '/data']
```

Inspired by the following resources:

- [Create default buckets via environment variables in docker - minio/minio/issues #4769](https://github.com/minio/minio/issues/4769)
- [amazon s3 - Minio: Add a public bucket with docker-compose - Stack Overflow](https://stackoverflow.com/questions/66412289/minio-add-a-public-bucket-with-docker-compose)
