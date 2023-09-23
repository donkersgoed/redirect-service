import aws_cdk as core
import aws_cdk.assertions as assertions

from redirect_service.redirect_service_stack import RedirectServiceStack

# example tests. To run these tests, uncomment this file along with the example
# resource in redirect_service/redirect_service_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = RedirectServiceStack(app, "redirect-service")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
