from __future__ import annotations

from pathlib import Path
from typing import Any

from hatchling.builders.wheel import WheelBuilder, WheelBuilderConfig

from hatchling.metadata.plugin.interface import MetadataHookInterface

from lazyimports import LazyModules
from lazyimports.__main__ import auto_detect


class LazyimportsHook(MetadataHookInterface):
    PLUGIN_NAME = "lazyimports"

    def update(self, metadata: dict[str, Any]) -> None:
        lazy_modules = LazyModules()

        if not (packages := self.config.get("packages")):
            cfg: WheelBuilderConfig = WheelBuilder(self.root).config
            packages = cfg.packages

        root = Path(self.root)
        for rel_path in packages:
            path = root / rel_path
            lazy_modules.update(auto_detect(path))

        if not any(lazy_modules):
            return

        key = self.config.get("entry_point_name", "lazyimports_auto")
        entry_points = metadata.setdefault("entry-points", {})
        lazyimports_entry_points = entry_points.setdefault("lazyimports", {})
        lazyimports_entry_points[key] = ",".join(lazy_modules)
