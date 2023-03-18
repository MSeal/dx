import uuid

import pandas as pd
import pytest

from dx.formatters.main import handle_format
from dx.settings import get_settings, settings_context
from dx.types.dex_metadata import DEXMetadata, DEXView
from dx.utils.formatting import generate_metadata, is_dex_metadata, is_dex_view_metadata

settings = get_settings()


class TestFormatting:
    @pytest.mark.parametrize("display_mode", ["simple", "enhanced"])
    @pytest.mark.parametrize("datalink_enabled", [True, False])
    def test_df_attrs_with_noteable_key_updates_metadata(
        self,
        sample_random_dataframe: pd.DataFrame,
        display_mode: str,
        datalink_enabled: bool,
        sample_dex_view_metadata: DEXView,
    ):
        """
        Test that DEX metadata is updated when the dataframe attributes are updated
        under the "noteable" key.
        """
        sample_random_dataframe.attrs = {"noteable": sample_dex_view_metadata}
        params = dict(display_mode=display_mode, enable_datalink=datalink_enabled)
        with settings_context(generate_dex_metadata=True, **params):
            _, metadata = handle_format(sample_random_dataframe)
            display_metadata = metadata[settings.MEDIA_TYPE]
        assert "dx" in display_metadata
        assert "views" in display_metadata["dx"]
        assert len(display_metadata["dx"]["views"]) == 1
        assert (
            display_metadata["dx"]["views"][0]["decoration"]["title"]
            == sample_dex_view_metadata.decoration.title
        )

    @pytest.mark.parametrize("display_mode", ["simple", "enhanced"])
    @pytest.mark.parametrize("datalink_enabled", [True, False])
    def test_df_attrs_will_not_update_metadata(
        self,
        sample_random_dataframe: pd.DataFrame,
        display_mode: str,
        datalink_enabled: bool,
        sample_dex_view_metadata: DEXView,
    ):
        """
        Test that DEX metadata is not updated when the dataframe attributes are updated
        without a "noteable" key.
        """
        sample_random_dataframe.attrs = sample_dex_view_metadata

        params = dict(display_mode=display_mode, enable_datalink=datalink_enabled)
        with settings_context(generate_dex_metadata=True, **params):
            _, metadata = handle_format(sample_random_dataframe)
            display_metadata = metadata[settings.MEDIA_TYPE]
        # this should create a default view, but not pass the .attrs
        # because it's missing the 'noteable' key
        assert "dx" in display_metadata
        assert "views" in display_metadata["dx"]
        assert len(display_metadata["dx"]["views"]) == 1
        assert (
            display_metadata["dx"]["views"][0]["decoration"]["title"]
            != sample_dex_view_metadata.decoration.title
        )

    @pytest.mark.parametrize("display_mode", ["simple", "enhanced"])
    @pytest.mark.parametrize("datalink_enabled", [True, False])
    def test_setting_disabled_will_not_update_metadata(
        self,
        sample_random_dataframe: pd.DataFrame,
        display_mode: str,
        datalink_enabled: bool,
        sample_dex_view_metadata: DEXView,
    ):
        """
        Test that the metadata is not updated if GENERATE_DEX_METADATA is False.
        The only override here is with explicit DEX plotting calls, which isn't
        covered in this test.
        """
        sample_random_dataframe.attrs = {"noteable": sample_dex_view_metadata}

        params = dict(display_mode=display_mode, enable_datalink=datalink_enabled)
        with settings_context(
            generate_dex_metadata=False,
            allow_noteable_attrs=False,
            **params,
        ):
            _, metadata = handle_format(sample_random_dataframe)
            display_metadata = metadata[settings.MEDIA_TYPE]
        assert "dx" not in display_metadata


class TestStructure:
    def test_dex_view_metadata_parsing(
        self, sample_random_dataframe: pd.DataFrame, sample_dex_view_metadata: DEXView
    ):
        """
        Test that calling generate_metadata() can properly update
        DEX metadata given a key/value pair belonging to a DEX view.
        """
        dex_view_metadata_dict = sample_dex_view_metadata.dict(by_alias=True)
        for key in dex_view_metadata_dict.keys():
            partial_view_metadata = {key: dex_view_metadata_dict[key]}
            assert is_dex_view_metadata(partial_view_metadata)

            display_id = str(uuid.uuid4())
            with settings_context(generate_dex_metadata=True):
                metadata = generate_metadata(
                    sample_random_dataframe,
                    display_id,
                    extra_metadata=partial_view_metadata,
                )
            assert "dx" in metadata
            assert "views" in metadata["dx"]
            assert len(metadata["dx"]["views"]) == 1
            assert metadata["dx"]["views"][0][key] == dex_view_metadata_dict[key]

    def test_dex_metadata_parsing(
        self, sample_random_dataframe: pd.DataFrame, sample_dex_metadata: DEXMetadata
    ):
        """
        Test that calling generate_metadata() can properly update
        DEX metadata given a key/value pair belonging to upper-level
        DEX metadata.
        """
        dex_metadata_dict = sample_dex_metadata.dict(by_alias=True)
        for key in dex_metadata_dict.keys():
            partial_metadata = {key: dex_metadata_dict[key]}
            assert is_dex_metadata(partial_metadata)

            display_id = str(uuid.uuid4())
            with settings_context(generate_dex_metadata=True):
                metadata = generate_metadata(
                    sample_random_dataframe,
                    display_id,
                    extra_metadata=partial_metadata,
                )
            assert "dx" in metadata
            assert "views" in metadata["dx"]
            assert metadata["dx"][key] == dex_metadata_dict[key]

    @pytest.mark.parametrize("allow_noteable_attrs", [True, False])
    def test_noteable_attrs(
        self,
        sample_random_dataframe: pd.DataFrame,
        allow_noteable_attrs: bool,
        sample_dex_view_metadata: DEXView,
    ):
        """
        Test that calling generate_metadata() can properly update
        DEX metadata given a key/value pair belonging to the
        "noteable" key as long as settings.ALLOW_NOTEABLE_ATTRS is True.
        """
        sample_random_dataframe.attrs = {"noteable": sample_dex_view_metadata}
        display_id = str(uuid.uuid4())
        with settings_context(
            generate_dex_metadata=False,
            allow_noteable_attrs=allow_noteable_attrs,
        ):
            metadata = generate_metadata(
                sample_random_dataframe,
                display_id,
                extra_metadata={"noteable": {"decoration": {"title": "test title"}}},
            )
        if allow_noteable_attrs:
            assert "dx" in metadata
            assert "views" in metadata["dx"]
            assert len(metadata["dx"]["views"]) == 1
            assert (
                metadata["dx"]["views"][0]["decoration"]["title"]
                == sample_dex_view_metadata.decoration.title
            )
        else:
            assert "dx" not in metadata


class TestPlottingMetadata:
    pass
