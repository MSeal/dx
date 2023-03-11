import pkg_resources


def installed_packages():
    return {pkg.key for pkg in pkg_resources.working_set}


class SoftDependencies:
    """Determines whether or not soft-dependencies are installed.
    Used for flagging whether or not specific formatting rules should be applied.
    """

    CUDF_INSTALLED = "cudf" in installed_packages()
    DASK_INSTALLED = "dask" in installed_packages()
    GEOPANDAS_INSTALLED = "geopandas" in installed_packages()
    MODIN_INSTALLED = "modin" in installed_packages()
    POLARS_INSTALLED = "polars" in installed_packages()
    VAEX_INSTALLED = "vaex" in installed_packages()


soft_deps = SoftDependencies()
