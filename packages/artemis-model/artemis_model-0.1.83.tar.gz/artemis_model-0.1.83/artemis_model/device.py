import enum
import uuid
from datetime import datetime

from sqlalchemy import JSON, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.associationproxy import association_proxy

from artemis_model.base import CustomSyncBase, CustomBase, TimeStampMixin


class DeviceMixin(TimeStampMixin):
    """
    Represents a Jukebox device associated with zone that can be controlled by multiple users.
    """
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    zone_id: Mapped[int] = mapped_column(ForeignKey("zone.id"), nullable=False, index=True)
    
    device_id: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)  # e.g., "Living Room Jukebox"
    fcm_token: Mapped[str | None] = mapped_column(nullable=True)
    device_specs: Mapped[dict] = mapped_column(JSON, nullable=True)  # control_mode can be stored here

    @declared_attr
    def zone(cls) -> Mapped["Zone"]:
        return relationship(back_populates="devices")

    @declared_attr
    def device_user_assoc(cls) -> Mapped[list["DeviceUserAssoc"]]:
        return relationship(cascade="all, delete-orphan")

    @declared_attr
    def users(cls) -> Mapped[list["User"]]:
        return relationship(
            secondary="device_user_assoc", 
            viewonly=True
        )


class DeviceSync(CustomSyncBase, DeviceMixin):
    pass


class Device(CustomBase, DeviceMixin):
    pass


class DeviceUserAssocMixin(TimeStampMixin):
    """
    Association table for many-to-many relationship between UserAccount and Device.
    """

    device_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("device.id"), primary_key=True, nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user.id"), primary_key=True, nullable=False
    )

    last_seen: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)


class DeviceUserAssocSync(CustomSyncBase, DeviceUserAssocMixin):
    pass


class DeviceUserAssoc(CustomBase, DeviceUserAssocMixin):
    pass