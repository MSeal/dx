from dx.filtering import store_sample_to_history
from dx.utils.tracking import DXDF_CACHE, DXDataFrame


def test_store_sample_to_history(
    sample_dxdataframe: DXDataFrame,
    sample_dex_filters: list,
):
    """
    Test that filters applied during sampling are added to
    the DXDataFrame object's metadata.
    """
    display_id = sample_dxdataframe.display_id
    DXDF_CACHE[display_id] = sample_dxdataframe

    store_sample_to_history(
        sample_dxdataframe.df,
        display_id,
        sample_dex_filters,
    )

    assert sample_dxdataframe.metadata["datalink"]["applied_filters"] == sample_dex_filters
    assert sample_dxdataframe.metadata["datalink"]["sampling_time"] is not None
