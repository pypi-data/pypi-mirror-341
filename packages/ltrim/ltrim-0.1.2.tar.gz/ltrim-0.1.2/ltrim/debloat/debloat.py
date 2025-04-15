import ast
import logging
import sys
from pprint import pformat as pp

from ltrim.debloat.process import debloat, run_profiler, run_pycg
from ltrim.debloat.utils import (
    blacklist,
    filter_pycg,
    sort_report,
    update_alive_modules,
)
from ltrim.transformers import ImportsFinder
from ltrim.utils import Config, Stats, cmd_message, mkdirp

# Create the log directory if it doesn't exist
mkdirp("log")

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="log/debloat.log",
    filemode="w",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


class Debloater:
    """
    Debloater class that encapsulates the debloating process.

    :param filename: The name of the application to debloat
    :param top_k: The number of modules to debloat
    :param scoring: The scoring method to calculate the top K ranking of the modules
    """

    def __init__(
        self,
        config: Config,
        top_K,
        scoring,
        disable_pycg,
    ):
        self.config = config
        self.appname = config.appname
        self.top_K = top_K
        self.scoring = scoring
        self.stats = Stats(self.appname, self.top_K)
        self.pycg = not disable_pycg

    def run(self):
        with open(self.appname, "r") as f:
            source = f.read()

        ast_source = ast.parse(source)

        # --------------------------------------------------------------------- #
        # ----------------------- Static Analysis Phase ----------------------- #
        # --------------------------------------------------------------------- #

        # Step 1: Find imported modules
        cmd_message("Finding imports...")
        imports_finder = ImportsFinder()
        imports_finder.visit(ast_source)
        cmd_message("Imports found!", "success")
        logger.info(f"Imports found: {imports_finder.imports}")

        # Step 2: Use PyCG to extract the call graph of the application
        if sys.version_info.minor <= 10 and self.pycg:
            cmd_message("Extracting call graph...")
            call_graph = run_pycg(self.appname)
            cmd_message("Call graph extracted!", "success")
            logger.info(f"Call graph extracted: {call_graph}")
        else:
            call_graph = []

        # --------------------------------------------------------------------- #
        # ------------------------ Constructing Phase ------------------------- #
        # --------------------------------------------------------------------- #

        # Step 3: Construct a list of the imported modules
        imported_modules = []

        for module_name in imports_finder.imports:
            if module_name in blacklist:
                continue

            imported_modules.append(module_name)

        logger.info(f"Filtered imports: {imported_modules}")

        # --------------------------------------------------------------------- #
        # ------------------------- Profiling Phase --------------------------- #
        # --------------------------------------------------------------------- #

        # Step 4: Profile the import process of the application
        cmd_message("Profiling the import process...")
        report = run_profiler(imported_modules)

        # Extract the total memory used by the imported modules
        total_memory = report["total_memory"]
        del report["total_memory"]

        # Extract the total time taken to import modules
        total_time = sum(
            [report[module]["time"] for module in imported_modules if module in report]
        )

        cmd_message(f"Total memory used in the import process: {total_memory:.2f}MB")
        cmd_message(f"Total time taken for the import process: {total_time:.2f}ms")

        # Step 5 - Sort the profiler report using the scoring method
        sorted_report = sort_report(report, self.scoring, total_time, total_memory)

        # Filter modules in the blacklist
        sorted_report = [
            module for module in sorted_report if module[0] not in blacklist
        ]
        logger.info(pp(sorted_report[: self.top_K]))
        cmd_message("Profiling completed!", "success")

        # --------------------------------------------------------------------- #
        # ------------------------- Debloating Phase -------------------------- #
        # --------------------------------------------------------------------- #

        # Step 6 - Debloat the top K modules

        modules_to_debloat = []

        # Initialize a ModuleRecord for stats tracking
        for module, entry in sorted_report[: self.top_K]:
            modules_to_debloat.append(module)
            self.stats.add_module(module)
            cmd_message(f"Module {module}: {entry}")
            self.stats.set_profiling_stats(
                module=module, memory=entry["memory"], time=entry["time"], before=False
            )

        alive_modules = set(modules_to_debloat)

        for midx, module in enumerate(modules_to_debloat):
            cmd_message(f"Debloating module {module} ({midx + 1}/{self.top_K})", "info")

            if module not in alive_modules:
                cmd_message(f"Module {module} is not longer needed!")
                continue

            # Step 6.1 - Filter the PyCG attributes
            filtered_attributes = filter_pycg(module, call_graph)
            logger.info(f"Attributes to keep based on PyCG: {filtered_attributes}")

            # Step 6.2 - Debloat the module
            module_path, delta_record = debloat(
                config=self.config,
                module=module,
                marked_attributes=filtered_attributes,
            )
            self.stats.set_path(module, module_path)
            self.stats.set_debloating_stats(module, delta_record)

            # Re-import to update alive_modules
            new_report = run_profiler(imported_modules)
            update_alive_modules(alive_modules, new_report)

        # --------------------------------------------------------------------- #
        # ---------------------- Stats-collecting Phase ----------------------- #
        # --------------------------------------------------------------------- #

        # Step 7 - Collect statistics

        # Step 7.1 - Run profiler
        final_report = run_profiler(imported_modules)
        logger.info("Final report after debloating:")
        logger.info(pp(final_report))

        # Step 7.2 - Get statistics for alive modules
        for module in alive_modules:
            entry = final_report[module]
            self.stats.set_profiling_stats(
                module=module, memory=entry["memory"], time=entry["time"], before=True
            )

        # Step 7.3 - Convert to CSV
        self.stats.convert_to_csv()

        # --------------------------------------------------------------------- #
        # ------------------------------- Done -------------------------------- #
        # --------------------------------------------------------------------- #

        cmd_message("Debloating process completed successfully!", "success")

        cmd_message("For detailed statistics, check log/ directory")
