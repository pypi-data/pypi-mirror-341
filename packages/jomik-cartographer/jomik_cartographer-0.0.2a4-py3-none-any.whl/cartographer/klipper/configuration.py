from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, TypeVar

from typing_extensions import override

from cartographer.configuration import (
    Configuration as CartographerConfiguration,
)
from cartographer.configuration import (
    ScanModelConfiguration,
    TouchModelConfiguration,
)

if TYPE_CHECKING:
    from configfile import ConfigWrapper


T = TypeVar("T", bound=Enum)


def get_enum_choice(config: ConfigWrapper, option: str, enum_type: type[T], default: T) -> T:
    choice = config.get(option, default.value)
    if choice not in enum_type._value2member_map_:
        msg = f"invalid choice '{choice}' for option '{option}'"
        raise config.error(msg)
    return enum_type(choice)


class KlipperCartographerConfiguration(CartographerConfiguration):
    def __init__(self, config: ConfigWrapper) -> None:
        self.x_offset: float = config.getfloat("x_offset")
        self.y_offset: float = config.getfloat("y_offset")
        self.backlash_compensation: float = config.getfloat("backlash_compensation", 0)
        self.move_speed: float = config.getfloat("move_speed", default=50, above=0)
        self.verbose: bool = config.getboolean("verbose", default=False)

        config_name = config.get_name()

        scan_config = config.getsection(f"{config_name} scan")
        self.scan_samples: int = scan_config.getint("samples", default=50, minval=10)
        self.scan_mesh_runs: int = scan_config.getint("mesh_runs", default=1, minval=1)

        touch_config = config.getsection(f"{config_name} touch")
        self.touch_samples: int = touch_config.getint("samples", default=5, minval=3)
        self.touch_retries: int = touch_config.getint("retries", default=3, minval=0)

        self.scan_models: dict[str, ScanModelConfiguration] = {
            cfg.name: cfg
            for cfg in map(
                KlipperScanModelConfiguration.from_config, config.get_prefix_sections(f"{config_name} scan_model")
            )
        }
        self.touch_models: dict[str, TouchModelConfiguration] = {
            cfg.name: cfg
            for cfg in map(
                KlipperTouchModelConfiguration.from_config, config.get_prefix_sections(f"{config_name} touch_model")
            )
        }


class KlipperScanModelConfiguration(ScanModelConfiguration):
    def __init__(
        self,
        config: ConfigWrapper,
        *,
        name: str,
        coefficients: list[float],
        domain: tuple[float, float],
        z_offset: float,
    ) -> None:
        self._config: ConfigWrapper = config
        self.name: str = name
        self.coefficients: list[float] = coefficients
        self.domain: tuple[float, float] = domain
        self.z_offset: float = z_offset

    @override
    def save_z_offset(self, new_offset: float) -> None:
        self._config.get_printer().lookup_object("configfile").set(
            self._config.get_name(), "z_offset", f"{new_offset:.3f}"
        )

    @staticmethod
    def from_config(config: ConfigWrapper) -> KlipperScanModelConfiguration:
        name = config.get_name().split("scan_model", 1)[1].strip()
        coefficients = config.getfloatlist("coefficients")
        domain_raw = config.getfloatlist("domain", count=2)
        domain = (domain_raw[0], domain_raw[1])
        z_offset = config.getfloat("z_offset")

        return KlipperScanModelConfiguration(
            config,
            name=name,
            coefficients=coefficients,
            domain=domain,
            z_offset=z_offset,
        )


class KlipperTouchModelConfiguration(TouchModelConfiguration):
    def __init__(
        self,
        config: ConfigWrapper,
        *,
        name: str,
        threshold: int,
        speed: float,
        z_offset: float,
        samples: int,
        retries: int,
    ) -> None:
        self._config: ConfigWrapper = config
        self.name: str = name
        self.threshold: int = threshold
        self.speed: float = speed
        self.z_offset: float = z_offset
        self.samples: int = samples
        self.retries: int = retries

    @override
    def save_z_offset(self, new_offset: float) -> None:
        self._config.get_printer().lookup_object("configfile").set(
            self._config.get_name(), "z_offset", f"{new_offset:.3f}"
        )

    @staticmethod
    def from_config(config: ConfigWrapper) -> KlipperTouchModelConfiguration:
        name = config.get_name().split("touch_model", 1)[1].strip()
        threshold = config.getint("threshold", minval=1)
        speed = config.getfloat("speed", above=0)
        z_offset = config.getfloat("z_offset", maxval=0)
        samples = config.getint("samples", default=5, minval=3)
        retries = config.getint("retries", default=3, minval=0)
        return KlipperTouchModelConfiguration(
            config,
            name=name,
            threshold=threshold,
            speed=speed,
            z_offset=z_offset,
            samples=samples,
            retries=retries,
        )
