"""user field matcher models"""
from typing import Type

from django.db import models
from django.forms import ModelForm
from django.utils.translation import gettext as _
from rest_framework.serializers import BaseSerializer

from passbook.core.models import Group
from passbook.policies.models import Policy
from passbook.policies.types import PolicyRequest, PolicyResult


class GroupMembershipPolicy(Policy):
    """Check that the user is member of the selected group."""

    group = models.ForeignKey(Group, null=True, blank=True, on_delete=models.SET_NULL)

    @property
    def serializer(self) -> BaseSerializer:
        from passbook.policies.group_membership.api import (
            GroupMembershipPolicySerializer,
        )

        return GroupMembershipPolicySerializer

    def form(self) -> Type[ModelForm]:
        from passbook.policies.group_membership.forms import GroupMembershipPolicyForm

        return GroupMembershipPolicyForm

    def passes(self, request: PolicyRequest) -> PolicyResult:
        return PolicyResult(self.group.users.filter(pk=request.user.pk).exists())

    class Meta:

        verbose_name = _("Group Membership Policy")
        verbose_name_plural = _("Group Membership Policies")
