# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .attach_boot_strap.attach_boot_strap_builder import AttachBootStrapBuilder
    from .attachcli.attachcli_builder import AttachcliBuilder
    from .attachcloudx.attachcloudx_builder import AttachcloudxBuilder
    from .attached.attached_builder import AttachedBuilder
    from .attachedconfig.attachedconfig_builder import AttachedconfigBuilder
    from .attachfeature.attachfeature_builder import AttachfeatureBuilder
    from .attachment.attachment_builder import AttachmentBuilder
    from .available.available_builder import AvailableBuilder
    from .config.config_builder import ConfigBuilder1
    from .detach.detach_builder import DetachBuilder
    from .detachcloudx.detachcloudx_builder import DetachcloudxBuilder
    from .duplicateip.duplicateip_builder import DuplicateipBuilder
    from .duplicatelocationname.duplicatelocationname_builder import DuplicatelocationnameBuilder
    from .exportcsv.exportcsv_builder import ExportcsvBuilder
    from .input.input_builder import InputBuilder
    from .process.process_builder import ProcessBuilder
    from .quickconnectvariable.quickconnectvariable_builder import QuickconnectvariableBuilder
    from .vbond.vbond_builder import VbondBuilder
    from .verify.verify_builder import VerifyBuilder


class ConfigBuilder:
    """
    Builds and executes requests for operations under /template/device/config
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def attach_boot_strap(self) -> AttachBootStrapBuilder:
        """
        The attachBootStrap property
        """
        from .attach_boot_strap.attach_boot_strap_builder import AttachBootStrapBuilder

        return AttachBootStrapBuilder(self._request_adapter)

    @property
    def attachcli(self) -> AttachcliBuilder:
        """
        The attachcli property
        """
        from .attachcli.attachcli_builder import AttachcliBuilder

        return AttachcliBuilder(self._request_adapter)

    @property
    def attachcloudx(self) -> AttachcloudxBuilder:
        """
        The attachcloudx property
        """
        from .attachcloudx.attachcloudx_builder import AttachcloudxBuilder

        return AttachcloudxBuilder(self._request_adapter)

    @property
    def attached(self) -> AttachedBuilder:
        """
        The attached property
        """
        from .attached.attached_builder import AttachedBuilder

        return AttachedBuilder(self._request_adapter)

    @property
    def attachedconfig(self) -> AttachedconfigBuilder:
        """
        The attachedconfig property
        """
        from .attachedconfig.attachedconfig_builder import AttachedconfigBuilder

        return AttachedconfigBuilder(self._request_adapter)

    @property
    def attachfeature(self) -> AttachfeatureBuilder:
        """
        The attachfeature property
        """
        from .attachfeature.attachfeature_builder import AttachfeatureBuilder

        return AttachfeatureBuilder(self._request_adapter)

    @property
    def attachment(self) -> AttachmentBuilder:
        """
        The attachment property
        """
        from .attachment.attachment_builder import AttachmentBuilder

        return AttachmentBuilder(self._request_adapter)

    @property
    def available(self) -> AvailableBuilder:
        """
        The available property
        """
        from .available.available_builder import AvailableBuilder

        return AvailableBuilder(self._request_adapter)

    @property
    def config(self) -> ConfigBuilder1:
        """
        The config property
        """
        from .config.config_builder import ConfigBuilder1

        return ConfigBuilder1(self._request_adapter)

    @property
    def detach(self) -> DetachBuilder:
        """
        The detach property
        """
        from .detach.detach_builder import DetachBuilder

        return DetachBuilder(self._request_adapter)

    @property
    def detachcloudx(self) -> DetachcloudxBuilder:
        """
        The detachcloudx property
        """
        from .detachcloudx.detachcloudx_builder import DetachcloudxBuilder

        return DetachcloudxBuilder(self._request_adapter)

    @property
    def duplicateip(self) -> DuplicateipBuilder:
        """
        The duplicateip property
        """
        from .duplicateip.duplicateip_builder import DuplicateipBuilder

        return DuplicateipBuilder(self._request_adapter)

    @property
    def duplicatelocationname(self) -> DuplicatelocationnameBuilder:
        """
        The duplicatelocationname property
        """
        from .duplicatelocationname.duplicatelocationname_builder import (
            DuplicatelocationnameBuilder,
        )

        return DuplicatelocationnameBuilder(self._request_adapter)

    @property
    def exportcsv(self) -> ExportcsvBuilder:
        """
        The exportcsv property
        """
        from .exportcsv.exportcsv_builder import ExportcsvBuilder

        return ExportcsvBuilder(self._request_adapter)

    @property
    def input(self) -> InputBuilder:
        """
        The input property
        """
        from .input.input_builder import InputBuilder

        return InputBuilder(self._request_adapter)

    @property
    def process(self) -> ProcessBuilder:
        """
        The process property
        """
        from .process.process_builder import ProcessBuilder

        return ProcessBuilder(self._request_adapter)

    @property
    def quickconnectvariable(self) -> QuickconnectvariableBuilder:
        """
        The quickconnectvariable property
        """
        from .quickconnectvariable.quickconnectvariable_builder import QuickconnectvariableBuilder

        return QuickconnectvariableBuilder(self._request_adapter)

    @property
    def vbond(self) -> VbondBuilder:
        """
        The vbond property
        """
        from .vbond.vbond_builder import VbondBuilder

        return VbondBuilder(self._request_adapter)

    @property
    def verify(self) -> VerifyBuilder:
        """
        The verify property
        """
        from .verify.verify_builder import VerifyBuilder

        return VerifyBuilder(self._request_adapter)
