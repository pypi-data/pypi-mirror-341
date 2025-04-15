"""GO Binary Comparator."""

import logging
import statistics
from collections.abc import Iterable
from pathlib import Path
from typing import Final

from gographer import CompareReport, Disassembly, Grapher
from pygobuildinfo import get_go_build_info  # type: ignore[import-untyped]

from volexity.gostrap.sample_generator import ArchTypes, PlatformTypes, SampleGenerator

from .models.go_version import GOVersion

logger: Final[logging.Logger] = logging.getLogger(__name__)


class GoCompare:
    """GO Binary Comparator."""

    def __init__(
        self,
        sample_generator: SampleGenerator,
        sample_path: Path,
        *,
        reference_path: Path | None = None,
        display_progress: bool = False,
        threshold: float = 0.0,
    ) -> None:
        """Initialize a new instance of GoCompare.

        Args:
            sample_generator: Instance of sample generator to build reference sample with.
            sample_path: Path of the sample to compare.
            reference_path: Optional path to a reference sample to compare with.
            display_progress: Weather to output progress updates to the console.
            threshold: Similarity threshold.
        """
        self.__gographer: Final[Grapher] = Grapher(threshold=threshold, display_progress=display_progress)
        self.__sample_generator: Final[SampleGenerator] = sample_generator
        self.__reference_path: Final[Path | None] = reference_path
        self.__sample_path: Final[Path] = sample_path
        self.__sample_disassembly: Disassembly | None = None

        self._display_progress: Final[bool] = display_progress
        self._legacy_cutoff: Final[GOVersion] = GOVersion("go1.16")  # 1.13 linux, 1.16 MacOS

    def compare(self, go_versions: list[str] | None = None, go_libs: list[str] | None = None) -> CompareReport:
        """Compare against reference GO binaries of the specified GO versions and libraries.

        Args:
            go_versions: List of GO versions to compare against.
            go_libs: List of GO libraries to include in each reference sample.

        Returns:
            The resulting GoGrapher comparaison report.
        """
        libs: Final[list[str]] = go_libs if go_libs else []
        go_vers: Final[list[str]] = go_versions if go_versions else [self.__assert_go_version()]
        logger.info(f"Testing {self.__sample_path.name} against GO version {go_vers} ...")

        # Generate reference samples.
        reference_samples: Final[list[tuple[str, Path]]] = (
            [("local", self.__reference_path)]
            if self.__reference_path
            else self.__sample_generator.generate(go_vers, libs, ArchTypes.AMD64, PlatformTypes.WINDOWS)
        )

        # Disassemble each sample.
        reference_graphs: Final[list[Disassembly]] = self.__generate_graphs(reference_samples)
        if not self.__sample_disassembly:
            msg: Final[str] = "Sample Disassembly Failed."
            raise ValueError(msg)

        # Compute and return the similarity report.
        return self.__gographer.compare(self.__sample_disassembly, reference_graphs)

    @staticmethod
    def __avg(data: Iterable[float]) -> float:
        """Returns the average value of a set of float values.

        Args:
            data: The iterable set of float values.

        Returns:
            The average value.
        """
        try:
            return statistics.mean(data)
        except statistics.StatisticsError:
            return 0.0

    def __generate_graphs(self, reference_samples: list[tuple[str, Path]]) -> list[Disassembly]:
        """."""
        if not self.__sample_disassembly:
            reference_samples.append((self.__sample_path.name, self.__sample_path))

        reference_graphs: Final[list[Disassembly]] = self.__gographer.generate_graphs(reference_samples)

        if not self.__sample_disassembly:
            for index, disassembly in enumerate(reference_graphs):
                if Path(disassembly.path) == self.__sample_path:
                    self.__sample_disassembly = disassembly
                    reference_graphs.pop(index)
                    break

        return reference_graphs

    def get_latest_versions(self) -> list[str]:
        """Returns the list of the latest point realease for each major Go version.

        Returns:
            The list of the latest point realease for each major Go version.
        """
        latest: dict[tuple[int | None, int | None], GOVersion] = {}
        versions: Final[list[GOVersion]] = [
            v
            for v in (GOVersion.from_str(ver) for ver in self.__sample_generator.get_available_go_versions())
            if v and v.is_release() and v >= self._legacy_cutoff
        ]
        for ver in versions:
            index: tuple[int | None, int | None] = (ver.major, ver.minor)
            maximum: GOVersion | None = latest.get(index)
            if not maximum or maximum < ver:
                latest[index] = ver

        return [str(ver) for ver in latest.values()]

    def __assert_go_version(self) -> str:
        """Attemps to figure out the GO version of the sample.

        Returns:
            The GO version used by the sample.
        """
        try:  # Try to extract the GO version from the build info.
            build_info: Final[dict] = get_go_build_info(self.__sample_path.as_posix())
            if build_info["GoVersion"] == "unknown":
                raise KeyError  # noqa: TRY301
            return build_info["GoVersion"]
        except KeyError:  # If obfuscated then tries to assert the GO version using a similarity based approach.
            candidates: Final[list[str]] = sorted(
                {*self.__sample_generator.get_installed_go_versions(), *self.get_latest_versions()}
            )
            logger.info(f"Obfuscated GO version ! Testing candidates : {candidates}")
            return self.__compare_go_runtimes(candidates)

    def __compare_go_runtimes(self, go_versions: list[str]) -> str:
        """Compare the runtimes of the specified GO versions with the sample and return the best match.

        Args:
            go_versions: List of GO versions to test the runtime of.

        Returns:
            The GO version that matched the sample the best.
        """
        reference_samples: Final[list[tuple[str, Path]]] = self.__sample_generator.generate(
            go_versions, [], ArchTypes.AMD64, PlatformTypes.WINDOWS, force=False
        )

        reference_graphs: Final[list[Disassembly]] = self.__generate_graphs(reference_samples)
        if not self.__sample_disassembly:
            msg: Final[str] = "Sample Disassembly Failed."
            raise ValueError(msg)

        # Filter each disassembly to only keep runtime related graphs.
        runtime_graphs: Final[list[Disassembly]] = [
            disasm.filter_symbol(r"^runtime\..+").get_subset(0.02) for disasm in reference_graphs
        ]

        # Test graphs against the malware.
        gographer: Final[Grapher] = Grapher(threshold=0.0, display_progress=self._display_progress)
        compare_results: Final[CompareReport] = gographer.compare(self.__sample_disassembly, runtime_graphs)

        # Compute the average similarity of each runtime
        average_syms: Final[dict[str, float]] = {
            result.dest: GoCompare.__avg(item.similarity for item in result.matches)
            for result in compare_results.matches
        }

        for k, v in average_syms.items():
            logger.debug(f"{k} -> {v}")

        # Select and return the GO version with the highest similarity.
        return max(average_syms, key=average_syms.__getitem__)
