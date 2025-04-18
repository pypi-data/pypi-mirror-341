from itertools import product
from numpy import arange, array, array_equal, nan, ones
import pytest

from glue.core import Data
from glue.viewers.common.viewer import LayerArtist
from glue_vispy_viewers.volume.volume_viewer import Vispy3DVolumeViewerState

from glue_ar.utils import alpha_composite, binned_opacity, clamp, clamp_with_resolution, clamped_opacity, \
                          clip_linear_transformations, clip_sides, data_count, data_for_layer, \
                          export_label_for_layer, get_resolution, hex_to_components, is_volume_viewer, \
                          iterable_has_nan, iterator_count, layer_color, mask_for_bounds, ndarray_has_nan, \
                          offset_triangles, slope_intercept_between, unique_id, xyz_bounds


def package_installed(package):
    from importlib.util import find_spec
    return find_spec(package) is not None


GLUE_QT_INSTALLED = package_installed("glue_qt")
GLUE_JUPYTER_INSTALLED = package_installed("glue_jupyter")


try:
    from glue_qt.app import GlueApplication
    from glue_vispy_viewers.scatter.qt.scatter_viewer import VispyScatterViewer
    from glue_vispy_viewers.volume.qt.volume_viewer import VispyVolumeViewer
except ImportError:
    pass

try:
    from glue_jupyter.app import JupyterApplication
    from glue_jupyter.ipyvolume import IpyvolumeScatterView, IpyvolumeVolumeView
    from glue_vispy_viewers.scatter.jupyter.scatter_viewer import JupyterVispyScatterViewer
    from glue_vispy_viewers.volume.jupyter.volume_viewer import JupyterVispyVolumeViewer
except ImportError:
    pass


def test_data_count():
    data1 = Data(label="Data 1")
    data2 = Data(label="Data 2")
    viewer_state = Vispy3DVolumeViewerState()

    layer1 = LayerArtist(viewer_state, layer=data1)
    layer1_2 = LayerArtist(viewer_state, layer=data1)
    layer2 = LayerArtist(viewer_state, layer=data2)

    assert data_count((layer1,)) == 1
    assert data_count((layer1, layer1_2)) == 1
    assert data_count((layer1, layer2)) == 2

    subset = data1.new_subset()
    subset_layer = LayerArtist(viewer_state, layer=subset)

    assert data_count((subset_layer,)) == 1
    assert data_count((layer1, subset_layer)) == 1
    assert data_count((layer2, subset_layer)) == 2


def test_export_label_for_layer():
    data = Data(label="Data")
    subset = data.new_subset(label="Subset")
    viewer_state = Vispy3DVolumeViewerState()
    data_layer = LayerArtist(viewer_state, layer=data)
    subset_layer = LayerArtist(viewer_state, layer=subset)

    assert export_label_for_layer(data_layer, add_data_label=True) == "Data"
    assert export_label_for_layer(data_layer, add_data_label=False) == "Data"

    assert export_label_for_layer(subset_layer, add_data_label=True) == "Subset (Data)"
    assert export_label_for_layer(subset_layer, add_data_label=False) == "Subset"


def test_slope_intercept_between():
    assert slope_intercept_between((3, 3), (1, 1)) == (1, 0)
    assert slope_intercept_between((3, 4), (1, 2)) == (1, 1)
    assert slope_intercept_between((-1, 5), (1, 5)) == (0, 5)
    assert slope_intercept_between((-1, 5), (1, 15)) == (5, 10)


def test_clip_linear_transformations():
    bounds = [(0, 2), (0, 8), (2, 6)]

    assert clip_linear_transformations(bounds) == [
        (0.25, -0.25),
        (0.25, -1),
        (0.25, -1)
    ]

    assert clip_linear_transformations(bounds, clip_size=2) == [
        (0.5, -0.5),
        (0.5, -2),
        (0.5, -2)
    ]

    assert clip_linear_transformations(bounds, stretches=(4, 0.5, 0.25)) == [
        (1, -1),
        (0.125, -0.5),
        (0.0625, -0.25)
    ]

    assert clip_linear_transformations(bounds, clip_size=4,
                                       stretches=(4, 0.5, 0.25)) == [
        (4, -4),
        (0.5, -2),
        (0.25, -1)
    ]


def test_layer_color():
    data = Data(label="Data")
    viewer_state = Vispy3DVolumeViewerState()
    layer = LayerArtist(viewer_state, layer=data)
    layer.state.color = "#abcdef"

    assert layer_color(layer.state) == "#abcdef"

    layer.state.color = "0.35"
    assert layer_color(layer.state) == "#808080"

    layer.state.color = "0.75"
    assert layer_color(layer.state) == "#808080"


def test_clip_sides_non_native():
    viewer_state = Vispy3DVolumeViewerState()
    viewer_state.native_aspect = False

    viewer_state.x_min = 0
    viewer_state.x_max = 8
    viewer_state.y_min = -2
    viewer_state.y_max = 2
    viewer_state.z_min = -1
    viewer_state.z_max = 1

    resolutions = (32, 64, 128, 256, 512)
    clip_sizes = (1, 2, 3, 5, 10)
    for resolution, clip_size in product(resolutions, clip_sizes):
        viewer_state.resolution = resolution
        size = 2 * clip_size / resolution
        assert clip_sides(viewer_state, clip_size=clip_size) == (size, size, size)


def test_clip_sides_native():
    viewer_state = Vispy3DVolumeViewerState()
    viewer_state.native_aspect = True

    viewer_state.x_min = 0
    viewer_state.x_max = 8
    viewer_state.y_min = -2
    viewer_state.y_max = 2
    viewer_state.z_min = -1
    viewer_state.z_max = 1

    resolutions = (32, 64, 128, 256, 512)
    clip_sizes = (1, 2, 3, 5, 10)
    for resolution, clip_size in product(resolutions, clip_sizes):
        viewer_state.resolution = resolution
        max_size = 2 * clip_size / resolution
        assert clip_sides(viewer_state, clip_size=clip_size) == (max_size, max_size / 2, max_size / 4)


@pytest.mark.skipif(not (GLUE_QT_INSTALLED or GLUE_JUPYTER_INSTALLED),
                    reason="Requires either glue-qt or glue-jupyter to create application")
def test_mask_for_bounds():
    x_values = range(10, 25)
    y_values = range(130, 145)
    z_values = range(-50, -35)
    data = Data(x=x_values, y=y_values, z=z_values)
    try:
        app = GlueApplication()
        app.add_data(data)
        viewer = app.new_data_viewer(VispyScatterViewer, data=data)
    except NameError:
        app = JupyterApplication()
        app.add_data(data)
        viewer = app.new_data_viewer(JupyterVispyScatterViewer, data=data)
    viewer.state.x_att = data.id['x']
    viewer.state.y_att = data.id['y']
    viewer.state.z_att = data.id['z']
    viewer.add_data(data)
    layer_state = viewer.layers[0].state

    viewer.state.x_min = 12  # Cuts off the first two points
    viewer.state.x_max = 25
    viewer.state.y_min = 130
    viewer.state.y_max = 141  # Cuts off the last three points
    viewer.state.z_min = -70
    viewer.state.z_max = -30

    bounds = xyz_bounds(viewer.state, with_resolution=False)
    mask = array([i not in (0, 1, 12, 13, 14) for i in range(15)])
    assert array_equal(mask_for_bounds(viewer.state, layer_state, bounds), mask)


def test_hex_to_components():
    assert hex_to_components("#7f11e0") == [127, 17, 224]
    assert hex_to_components("#abcdef47") == [171, 205, 239, 71]
    assert hex_to_components("#000000") == [0, 0, 0]
    assert hex_to_components("#00000000") == [0, 0, 0, 0]
    assert hex_to_components("#26e04a") == [38, 224, 74]
    assert hex_to_components("#ff021706") == [255, 2, 23, 6]


def test_unique_id():
    ids = [unique_id() for _ in range(25)]
    assert all(len(id) == 32 for id in ids)
    assert len(set(ids)) == 25


def test_alpha_composite():
    over = [110, 206, 15, 0.3]
    under = [89, 97, 202, 0.4]
    alpha_combined = 0.3 + 0.4 * 0.7
    rgb_new = [(o * 0.3 + u * 0.4 * 0.7) / alpha_combined for o, u in zip(over[:3], under[:3])]
    assert alpha_composite(over, under) == rgb_new + [alpha_combined]

    over = [110, 206, 15, 0.6]
    under = [89, 97, 202, 0.7]
    alpha_combined = 0.6 + 0.7 * 0.4
    rgb_new = [(o * 0.6 + u * 0.7 * 0.4) / alpha_combined for o, u in zip(over[:3], under[:3])]
    assert alpha_composite(over, under) == rgb_new + [alpha_combined]

    # Here over has full opacity, so the composition should just be the over color
    over = [255, 10.5, 176]
    under = [12, 116, 175, 0.5]
    assert alpha_composite(over, under) == over + [1]


def test_data_for_layer():
    data = Data(label="Data")
    subset = data.new_subset(label="Subset")
    viewer_state = Vispy3DVolumeViewerState()
    data_layer = LayerArtist(viewer_state, layer=data)
    subset_layer = LayerArtist(viewer_state, layer=subset)

    assert data_for_layer(data_layer) == data
    assert data_for_layer(subset_layer) == data


def test_ndarray_has_nan():
    assert ndarray_has_nan(array([3.0, nan, -4.7, 2, nan]))
    assert not ndarray_has_nan(array([3.0, 2.6, -4.7, 2, -10.5]))


def test_iterable_has_nan():
    assert iterable_has_nan((nan, 2.7, 3.5))
    assert iterable_has_nan([2.1, nan, 11.0, 2.6])
    assert not iterable_has_nan([2.1, -3.5, 4.6])
    assert not iterable_has_nan((2.2, 4.6, -0.7))


def test_iterator_count():
    assert iterator_count(iter([1, 2, 3, 4, 5])) == 5
    assert iterator_count(iter(range(11))) == 11


@pytest.mark.skipif(not GLUE_QT_INSTALLED,
                    reason="Requires glue-qt to test Qt VisPy volume viewer")
def test_is_volume_viewer_qt():
    qt_app = GlueApplication()
    vispy_scatter = qt_app.new_data_viewer(VispyScatterViewer)
    vispy_volume = qt_app.new_data_viewer(VispyVolumeViewer)
    assert not is_volume_viewer(vispy_scatter)
    assert is_volume_viewer(vispy_volume)


@pytest.mark.skipif(not GLUE_JUPYTER_INSTALLED,
                    reason="Requires glue-jupyter to test Jupyter VisPy and ipyvolume viewers")
def test_is_volume_viewer_jupyter():
    jupyter_app = JupyterApplication()

    vispy_scatter = jupyter_app.new_data_viewer(JupyterVispyScatterViewer)
    vispy_volume = jupyter_app.new_data_viewer(JupyterVispyVolumeViewer)
    assert not is_volume_viewer(vispy_scatter)
    assert is_volume_viewer(vispy_volume)

    ipv_scatter = jupyter_app.new_data_viewer(IpyvolumeScatterView)
    ipv_volume = jupyter_app.new_data_viewer(IpyvolumeVolumeView)
    assert not is_volume_viewer(ipv_scatter)
    assert is_volume_viewer(ipv_volume)


@pytest.mark.skipif(not GLUE_QT_INSTALLED,
                    reason="Requires glue-qt to test Qt VisPy volume viewer")
def test_get_resolution_qt():
    qt_app = GlueApplication()

    vispy_volume = qt_app.new_data_viewer(VispyVolumeViewer)
    vispy_volume.state.resolution = 64
    assert get_resolution(vispy_volume.state) == 64

    # Check default behavior
    vispy_scatter = qt_app.new_data_viewer(VispyScatterViewer)
    assert get_resolution(vispy_scatter) == 256


@pytest.mark.skipif(not GLUE_JUPYTER_INSTALLED,
                    reason="Requires glue-jupyter to test Jupyter VisPy and ipyvolume viewers")
def test_get_resolution_jupyter():
    jupyter_app = JupyterApplication()
    volume_data1 = Data(label='Volume Data',
                        x=arange(24).reshape((2, 3, 4)),
                        y=ones((2, 3, 4)),
                        z=arange(100, 124).reshape((2, 3, 4)))
    jupyter_app.add_data(volume_data1)

    vispy_volume = jupyter_app.new_data_viewer(JupyterVispyVolumeViewer)
    vispy_volume.add_data(volume_data1)
    vispy_volume.state.resolution = 32
    assert get_resolution(vispy_volume.state) == 32

    ipv_volume = jupyter_app.new_data_viewer(IpyvolumeVolumeView)
    ipv_volume.add_data(volume_data1)
    ipv_volume.layers[-1].state.max_resolution = 128
    assert get_resolution(ipv_volume.state) == 128

    volume_data2 = Data(label='Volume Data',
                        x=arange(24).reshape((2, 3, 4)),
                        y=ones((2, 3, 4)),
                        z=arange(100, 124).reshape((2, 3, 4)))
    jupyter_app.add_data(volume_data2)
    vispy_volume.add_data(volume_data2)
    ipv_volume.add_data(volume_data2)
    ipv_volume.layers[-1].state.max_resolution = 64
    assert get_resolution(vispy_volume.state) == 32
    assert get_resolution(ipv_volume.state) == 128

    ipv_volume.layers[-1].state.max_resolution = 512
    assert get_resolution(ipv_volume.state) == 512


def test_clamp():
    assert clamp(2, 0, 1) == 1
    assert clamp(-1, 0, 1) == 0
    assert clamp(0.5, 0, 1) == 0.5
    assert clamp(9, 5, 7) == 7
    assert clamp(16.2, 20.5, 31.6) == 20.5
    assert clamp(5.6, 4.8, 7.2) == 5.6


def test_clamped_opacity():
    assert clamped_opacity(0.1) == 0.1
    assert clamped_opacity(0.77) == 0.77
    assert clamped_opacity(-2) == 0
    assert clamped_opacity(1.6) == 1


def test_clamp_with_resolution():
    assert clamp_with_resolution(2, 0, 1, 0.5) == 1
    assert clamp_with_resolution(-1, 0, 1, 0.2) == 0
    assert clamp_with_resolution(0.5, 0, 1, 0.3) == 0.6
    assert clamp_with_resolution(16.2, 10, 20, 0.5) == 16
    assert clamp_with_resolution(5.6, 4.8, 7.2, 1) == 6


def test_binned_opacity():
    assert binned_opacity(0.13, 0.2) == 0.2
    assert binned_opacity(0.3, 0.25) == 0.25
    assert binned_opacity(-1.3, 0.1) == 0
    assert binned_opacity(2.46, 0.01) == 1
    assert binned_opacity(0.775, 0.02) == 0.78


def test_offset_triangles():
    assert offset_triangles([[0, 1, 2], [1, 2, 3], [0, 2, 3]], 6) == [(6, 7, 8), (7, 8, 9), (6, 8, 9)]
    assert offset_triangles([[2, 1, 6], [5, 7, 4]], 5) == [(7, 6, 11), (10, 12, 9)]
    assert offset_triangles([[0, 1, 2], [2, 3, 0], [3, 1, 2]], 0) == [(0, 1, 2), (2, 3, 0), (3, 1, 2)]
