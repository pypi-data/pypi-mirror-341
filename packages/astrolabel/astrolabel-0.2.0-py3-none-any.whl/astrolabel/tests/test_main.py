import pathlib

from astrolabel import LabelLibrary, AstroLabel, DEFAULT_LIBRARY_PATH
import pytest

import shutil


@pytest.fixture
def set_env(monkeypatch):
    monkeypatch.delenv("ASTROLABEL", raising=False)


@pytest.fixture(scope="module")
def std_ll() -> LabelLibrary:
    return LabelLibrary.read(DEFAULT_LIBRARY_PATH)


@pytest.fixture(scope="module")
def empty_ll() -> LabelLibrary:
    return LabelLibrary(formats={}, scripts={}, labels={})


@pytest.fixture
def tmp_library_path(tmp_path) -> pathlib.Path:
    library_path = tmp_path / "astrolabel.yml"
    shutil.copy(DEFAULT_LIBRARY_PATH, library_path)

    return library_path


def test_library_path(std_ll, empty_ll):
    assert std_ll.library_path == DEFAULT_LIBRARY_PATH
    assert empty_ll.library_path is None


def test_info(capsys):
    ll = LabelLibrary(formats={}, scripts={}, labels={'z': AstroLabel(symbol="z", description="Redshift"),
                                                      'fesc': AstroLabel(symbol="f_{\\text{esc}}", description="Escape fraction")})
    ll.info()

    captured = capsys.readouterr()
    assert captured.out == "   z: Redshift\nfesc: Escape fraction\n"


def test_read_from_file(tmp_library_path):
    ll = LabelLibrary.read(tmp_library_path)

    assert ll.library_path == tmp_library_path


def test_read_from_workdir(set_env, tmp_library_path, monkeypatch):
    monkeypatch.chdir(tmp_library_path.parent)
    ll = LabelLibrary.read()

    assert ll.library_path == tmp_library_path


def test_read_from_env_variable(set_env, tmp_library_path, monkeypatch):
    monkeypatch.setenv("ASTROLABEL", str(tmp_library_path))
    ll = LabelLibrary.read()

    assert ll.library_path == tmp_library_path


def test_read_from_default_location(set_env):
    ll = LabelLibrary.read()

    assert ll.library_path == DEFAULT_LIBRARY_PATH


def test_read_is_directory(tmp_path):
    tmp_dir = tmp_path / "42"
    tmp_dir.mkdir()

    with pytest.raises(IsADirectoryError, match="'.*' is a directory"):
        LabelLibrary.read(tmp_dir)


def test_read_file_not_found(tmp_path):
    with pytest.raises(FileNotFoundError, match="File '.*' does not exist"):
        LabelLibrary.read(tmp_path / "non_existing_file.yml")


def test_get_label_key_not_found(std_ll):
    with pytest.raises(KeyError, match="Label key '42' not found"):
        std_ll.get_label('42')


def test_get_label_fmt_not_found(std_ll):
    with pytest.raises(ValueError, match="Label format 'my_fmt' not found. Available formats: .*"):
        std_ll.get_label('z', "my_fmt")


def test_get_label_without_unit(std_ll):
    assert std_ll.get_label('z') == "$z$"


def test_get_label_with_unit(std_ll):
    assert std_ll.get_label('sfr') == r"$\mathrm{SFR}$ [$\mathrm{M_{\odot}\,yr^{-1}}$]"


def test_get_label_log_without_unit(std_ll):
    assert std_ll.get_label('z', fmt="log") == r"$\log_{10}\,z$"


def test_get_label_log_with_unit(std_ll):
    assert std_ll.get_label('sfr', fmt="log") == (r"$\log_{10}\,\left(\mathrm{SFR} / \mathrm{M_{\odot}\,"
                                                  r"yr^{-1}}\right)$")


def test_get_label_with_scaled_unit(std_ll):
    assert std_ll.get_label('flam', scale=1e-20) == r"$f^\lambda$ [$\mathrm{10^{-20}\,erg\,A^{-1}\,s^{-1}\,cm^{-2}}$]"


def test_format_unit_with_scale(std_ll):
    assert LabelLibrary._format_unit("1e1") in (r"$\mathrm{10\,}$", r"$\mathrm{10}$")
    assert LabelLibrary._format_unit("1e10") in (r"$\mathrm{10^{10}\,}$", r"$\mathrm{10^{10}}$")
    assert LabelLibrary._format_unit("1.1e10") in (r"$\mathrm{1.1 \times 10^{10}\,}$", r"$\mathrm{1.1 \times 10^{10}}$")


def test_get_label_with_subs(std_ll):
    assert std_ll.get_label('m_star') == r"$\mathrm{M}_{\bigstar}$ [$\mathrm{M_{\odot}}$]"
    assert std_ll.get_label('m_star_star') == r"$\mathrm{M}_{\bigstar,\bigstar}$ [$\mathrm{M_{\odot}}$]"

def test_get_label_with_sups(std_ll):
    assert std_ll.get_label('flam_ha') == r"$f^\lambda_{\mathrm{H}\alpha}$ [$\mathrm{erg\,A^{-1}\,s^{-1}\,cm^{-2}}$]"
    assert std_ll.get_label('flam_ha_obs') == r"$f^\lambda_{\mathrm{H}\alpha,\mathrm{obs}}$ [$\mathrm{erg\,A^{-1}\,s^{-1}\,cm^{-2}}$]"

def test_get_label_with_subs_and_sups(std_ll):
    assert std_ll.get_label('m_star^obs_int') == r"$\mathrm{M}_{\bigstar,\mathrm{int}}^{\mathrm{obs}}$ [$\mathrm{M_{\odot}}$]"

def test_get_laebl_with_wrap(std_ll):
    assert std_ll.get_label('bd_obs') == r"$\left(\mathrm{H}\alpha/\mathrm{H}\beta\right)_{\mathrm{obs}}$"

def test_get_label_with_empty_sub_sup(std_ll):
    assert std_ll.get_label("z_None^None") == "$z$"

def test_get_symbol(std_ll):
    assert std_ll.get_symbol("sfr") == r"$\mathrm{SFR}$"

def test_get_symbol_with_unit(std_ll):
    assert std_ll.get_symbol("m_star") == r"$\mathrm{M}_{\bigstar}$"