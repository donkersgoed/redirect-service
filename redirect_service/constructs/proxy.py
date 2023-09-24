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

        # A list of custom domain names and their hosted zone names
        # this API should respond to.
        api_mappings = [
            ApiMapping(
                domain_names=["w.l15d.com"],
                hosted_zone_name="w.l15d.com",
                hosted_zone_id="Z05942751EXJO1M3FVCXE",
            ),
            ApiMapping(
                domain_names=[
                    "www.bitesizedserverless.com",
                    "bitesizedserverless.com",
                ],
                hosted_zone_name="bitesizedserverless.com",
                hosted_zone_id="Z00360591I6ENSTBA2JEX",
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
            self._add_mapping(api_mapping, self.rest_api)

    def _add_mapping(
        self,
        api_mapping: ApiMapping,
        rest_api: apigateway.RestApi,
    ) -> None:
        """Add custom domain names for the given list of custom hostnames."""

        api_hosted_zone = route53.HostedZone.from_hosted_zone_attributes(
            scope=self,
            id=f"HostedZone{api_mapping.hosted_zone_id}",
            hosted_zone_id=api_mapping.hosted_zone_id,
            zone_name=api_mapping.hosted_zone_name,
        )

        for domain_name in api_mapping.domain_names:
            CustomDomain(
                scope=self,
                construct_id=domain_name,
                domain_name=domain_name,
                api_hosted_zone=api_hosted_zone,
                rest_api=rest_api,
            )


class CustomDomain(Construct):
    """A construct to group the resources for a custom domain."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        scope: Construct,
        construct_id: str,
        domain_name: str,
        api_hosted_zone: route53.HostedZone,
        rest_api: apigateway.RestApi,
        **kwargs,
    ) -> None:
        """Construct a new CustomDomain class."""
        super().__init__(
            scope,
            construct_id,
            **kwargs,
        )
        # The TLS certificate for the custom domain.
        api_cert = acm.Certificate(
            scope=self,
            id="APICertificate",
            domain_name=domain_name,
            validation=acm.CertificateValidation.from_dns(hosted_zone=api_hosted_zone),
        )

        # The API Gateway custom domain
        domain = apigateway.DomainName(
            scope=self,
            id="CustomDomainName",
            domain_name=domain_name,
            certificate=api_cert,
            endpoint_type=apigateway.EndpointType.REGIONAL,
            security_policy=apigateway.SecurityPolicy.TLS_1_2,
        )
        domain.add_base_path_mapping(rest_api)

        # The Route 53 alias record pointing to the API Gateway custom domain
        route53.ARecord(
            scope=self,
            id="CustomDomainAliasRecord",
            zone=api_hosted_zone,
            target=route53.RecordTarget.from_alias(
                route53_targets.ApiGatewayDomain(domain)
            ),
            record_name=domain_name,
        )
