from viewflow import flow
from viewflow.base import this, Flow
from viewflow.flow.views import CreateProcessView, UpdateProcessView
from .views import PersonToClubMembershipViewSet

from .models import PersonToClubMembershipProcess


class PersonToClubMembershipWorkflow(Flow):
    process_class = PersonToClubMembershipProcess
    start_view = PersonToClubMembershipViewSet.as_view({'post': 'create'})
    start = (
        flow.Start(
            start_view,
            fields=['person', 'club', 'valid_from', 'valid_until', 'role', 'reporter', 'approved_by',]
        ).Permission(
            auto_create=True
        ).Next(this.approve)
    )

    approve = (
        flow.View(
            UpdateProcessView,
            fields=["approved"]
        ).Permission(
            auto_create=True
        ).Next(this.check_approve)
    )

    check_approve = (
        flow.If(lambda activation: activation.process.approved)
        .Then(this.send)
        .Else(this.end)
    )

    send = (
        flow.Handler(
            this.send_hello_world_request
        ).Next(this.end)
    )

    end = flow.End()

    def send_hello_world_request(self, activation):
        print(activation.process.text)
