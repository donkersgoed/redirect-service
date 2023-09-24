#!/usr/bin/env python3
"""Main entrypoint for the redirect service."""
import aws_cdk as cdk

from redirect_service.redirect_service_stack import RedirectServiceStack


app = cdk.App()
RedirectServiceStack(app, "RedirectServiceStack")

app.synth()
