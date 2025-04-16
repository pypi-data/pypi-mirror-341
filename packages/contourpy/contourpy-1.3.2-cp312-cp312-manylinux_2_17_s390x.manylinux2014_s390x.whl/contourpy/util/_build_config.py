# _build_config.py.in is converted into _build_config.py during the meson build process.

from __future__ import annotations


def build_config() -> dict[str, str]:
    """
    Return a dictionary containing build configuration settings.

    All dictionary keys and values are strings, for example ``False`` is
    returned as ``"False"``.

        .. versionadded:: 1.1.0
    """
    return dict(
        # Python settings
        python_version="3.12",
        python_install_dir=r"/usr/local/lib/python3.12/site-packages/",
        python_path=r"/tmp/build-env-kwqhyruk/bin/python",

        # Package versions
        contourpy_version="1.3.2",
        meson_version="1.7.2",
        mesonpy_version="0.17.1",
        pybind11_version="2.13.6",

        # Misc meson settings
        meson_backend="ninja",
        build_dir=r"/project/.mesonpy-ms6x48wm/lib/contourpy/util",
        source_dir=r"/project/lib/contourpy/util",
        cross_build="False",

        # Build options
        build_options=r"-Dbuildtype=release -Db_ndebug=if-release -Db_vscrt=md -Dvsenv=True --native-file=/project/.mesonpy-ms6x48wm/meson-python-native-file.ini",
        buildtype="release",
        cpp_std="c++17",
        debug="False",
        optimization="3",
        vsenv="True",
        b_ndebug="if-release",
        b_vscrt="from_buildtype",

        # C++ compiler
        compiler_name="gcc",
        compiler_version="10.2.1",
        linker_id="ld.bfd",
        compile_command="c++",

        # Host machine
        host_cpu="s390x",
        host_cpu_family="s390x",
        host_cpu_endian="big",
        host_cpu_system="linux",

        # Build machine, same as host machine if not a cross_build
        build_cpu="s390x",
        build_cpu_family="s390x",
        build_cpu_endian="big",
        build_cpu_system="linux",
    )
