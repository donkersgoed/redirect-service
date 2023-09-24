"""The proxy module, responsible for the API Gateway proxy."""

from dataclasses import dataclass
from typing import List

from aws_cdk import (
    aws_apigateway as apigateway,
    aws_certificatemanager as acm,
    aws_route53 as route53,
    aws_route53_targets as route53_targets,
)
from constructs import Construct


@dataclass
class ApiMapping:
    """Model for API mappings."""

    domain_names: List[str]
    hosted_zone_name: str
    hosted_zone_id: str


class Proxy(Construct):
    """The proxy class, responsible for the API Gateway proxy."""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        """Construct a new Proxy class."""
        super().__init__(scope, construct_id, **kwargs)

        api_mappings = [
            ApiMapping(
                domain_names=["w.l15d.com"],
                hosted_zone_name="w.l15d.com",
                hosted_zone_id="Z05942751EXJO1M3FVCXE",
            ),
            ApiMapping(
                domain_names=[
                    "www.dev.bitesizedserverless.com",
                    "dev.bitesizedserverless.com",
                ],
                hosted_zone_name="dev.bitesizedserverless.com",
                hosted_zone_id="Z06173232SSK9M0YR7IRP",
            ),
        ]

        self.rest_api = apigateway.RestApi(
            scope=self,
            id="ProxyApi",
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=apigateway.Cors.ALL_ORIGINS,
                allow_methods=apigateway.Cors.ALL_METHODS,
            ),
            deploy_options=apigateway.StageOptions(
                logging_level=apigateway.MethodLoggingLevel.INFO,
                data_trace_enabled=True,
            ),
        )

        for api_mapping in api_mappings:
            ZoneMapping(
                scope=self,
                construct_id=f"ZoneMapping{api_mapping.hosted_zone_name}",
                api_mapping=api_mapping,
                rest_api=self.rest_api,
            )


class ZoneMapping(Construct):
    """Construct for the resources required for a custom domain name."""

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        api_mapping: ApiMapping,
        rest_api: apigateway.RestApi,
        **kwargs,
    ) -> None:
        """Add custom domain names for the given list of custom hostnames."""
        super().__init__(scope, construct_id, **kwargs)

        api_hosted_zone = route53.HostedZone.from_hosted_zone_attributes(
            scope=self,
            id=f"HostedZone{api_mapping.hosted_zone_id}",
            hosted_zone_id=api_mapping.hosted_zone_id,
            zone_name=api_mapping.hosted_zone_name,
        )

        for domain_name in api_mapping.domain_names:
            api_cert = acm.Certificate(
                scope=self,
                id=f"APICertificate{domain_name}",
                domain_name=domain_name,
                validation=acm.CertificateValidation.from_dns(
                    hosted_zone=api_hosted_zone
                ),
            )
            domain = apigateway.DomainName(
                scope=self,
                id=f"CustomDomainName{domain_name}",
                domain_name=domain_name,
                certificate=api_cert,
                endpoint_type=apigateway.EndpointType.REGIONAL,
                security_policy=apigateway.SecurityPolicy.TLS_1_2,
            )

            route53.ARecord(
                scope=self,
                id=f"CustomDomainAliasRecord{domain_name}",
                zone=api_hosted_zone,
                target=route53.RecordTarget.from_alias(
                    route53_targets.ApiGatewayDomain(domain)
                ),
                record_name=domain_name,
            )

            domain.add_base_path_mapping(rest_api)
