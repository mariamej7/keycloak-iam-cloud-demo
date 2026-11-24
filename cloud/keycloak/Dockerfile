# Image Keycloak autonome, sans lien avec le projet PFA.
FROM quay.io/keycloak/keycloak:26.8.2 AS builder
ENV KC_DB=postgres
RUN /opt/keycloak/bin/kc.sh build

FROM quay.io/keycloak/keycloak:26.8.2
COPY --from=builder /opt/keycloak/ /opt/keycloak/
COPY --chown=1000:0 cloud/keycloak/universite-realm.json /opt/keycloak/data/import/universite-realm.json
COPY --chown=1000:0 cloud/keycloak/start-cloud.sh /opt/keycloak/bin/start-cloud.sh
EXPOSE 10000
ENTRYPOINT ["/bin/sh", "/opt/keycloak/bin/start-cloud.sh"]
