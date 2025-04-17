import pytest
import omniscript


@pytest.fixture(scope="module")
def default_adapter(engine):
    """ Fixture for getting the default adapter from omni engine """
    adapter_list = engine.get_adapter_list()
    adapter = omniscript.find_adapter(adapter_list, 'eth0')

    if adapter is None:
        adapter = omniscript.find_adapter(adapter_list, 'eno1')
    return adapter


@pytest.fixture(scope="module")
def captures(default_adapter):
    """ Capture template fixture """
    template = omniscript.CaptureTemplate()

    if default_adapter:
        template.set_adapter(default_adapter)

    template.general.option_continuous_capture = True
    template.general.option_capture_to_disk = True
    template.general.option_start_capture = False
    template.general.option_timeline_app_stats = True
    template.general.option_timeline_stats = True
    template.general.option_timeline_top_stats = True
    template.general.option_timeline_voip_stats = True
    template.analysis.option_alarms = True
    template.analysis.option_analysis_modules = True
    template.analysis.option_application = True
    template.analysis.option_compass = True
    template.analysis.option_country = True
    template.analysis.option_error = True
    template.analysis.option_expert = True
    template.analysis.option_network = True
    template.analysis.option_passive_name_resolution = True
    template.analysis.node_protocol_detail_limit.enabled = True
    template.analysis.node_limit.enabled = True
    template.analysis.protocol_limit.enabled = True
    template.analysis.option_size = True
    template.analysis.option_summary = True
    template.analysis.option_traffic_history = True
    template.analysis.option_voice_video = True
    template.analysis.option_web = True

    names = [f'Capture {i}' for i in range(1, 4)]

    yield template, names


@pytest.mark.skip('Adapter not not found issue not resolved')
def test_capture_creation(captures, engine):
    """ Test the creation of a capture """
    template, names = captures

    for name in names:
        template.general.name = name
        capture = engine.create_capture(template)
        assert capture is not None, f'Failed to create {name}'
